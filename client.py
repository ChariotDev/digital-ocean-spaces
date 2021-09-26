from pyaml import yaml
import os
import fernet
import boto3
import time
from pathlib import Path
import sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from utils import shell

regions = ['ams3', 'fra1', 'nyc3', 'sgp1', 'sfo2', 'sfo3']

# EXCEPTIONS
no_keys = (
    """
    No space_name or API keys have been provided.
    A) Use client(space_name, public_key, secret_key) or,
    B) Supply env.yaml properly, template provided in base directory.
    """
)
invalid_region = (
    f"""
    Recieved invalid region_name, available options:
    regions = {regions}
    """
)
invalid_space_name = (
    """
    Space with that name doesn't exist.
    """
)
no_space_name = (
    """
    No space name provided. Set a space or provide space_name parameter.
    Example 1: Client.set_space('sfo3')
    Example 2: Client.list_files(space_name='sfo3')
    """
)

cant_replace_file_ext = (
    """
    You can not replace the file extention in the 'rename' kwarg.
    Safe: rename = 'old_name' -> 'foo/bar/old_name.txt' -> 'foo/bar/new_name.txt'
    Unsafe: rename = 'new_name.mp4' -> 'foo/bar/old_name.txt' -> 'foo/bar/new_name.mp4'
    """        
)

cant_place_path_in_file_name = (
    """
    You can not place the path in the 'rename' kwarg, use the 'destination' kwarg instead.
    Example: destination = 'new/path/' -> 'old/path/old_name.txt' -> 'new/path/old_name.txt'
    """
)

cant_place_file_name_in_destination = (
    """
    You can not place the file name in the destination path.
    """
)

# HELPERS

def file_to_string(file, type):
    return (
        f"""
    Name: {file.get('Key')} [{type}]
        LastModified: {file.get('LastModified')}
        ETag: {file.get('ETag')}
        Owner: {file.get('Owner').get('DisplayName')}
    ----------"""
    )

def file_or_dir(file):
    if file.get('Key')[-1] and file.get('Key')[-1] == '/':
        return 'directory'
    else:
        return 'file'

def sort_files(all_files, dir, type=None):
    files = ()
    for file in all_files:
        if file.get('Key').startswith(dir):
            if type:
                if type == file_or_dir(file):
                    files += (file, )
            else:
                files += (file, )
    return files

class Client:
    def __init__(self, region_name=None, space_name=None, public_key=None, secret_key=None):
        # Check if key provided, else fetch from env.yaml

        if not region_name or not public_key or not secret_key:
            try:
                with open("./env.yaml", 'r') as stream:
                    env = yaml.safe_load(stream)
                region_name = env['region_name']
                public_key = env['public_key']
                secret_key = env['secret_key']
                space_name = env.get('default_space_name')
            except FileNotFoundError:
                print('Exception: [FileNotFoundError]' + no_keys)
            except KeyError:
                print('Exception: [KeyError]' + no_keys)
            finally:
                pass

        # Quit if no keys
        if not region_name or not public_key or not secret_key:
            raise Exception('[Raised]' + no_keys)

        self.public_key = public_key
        self.secret_key = secret_key

        if region_name.lower() in regions:
            self.region = region_name.lower()
        else:
            raise Exception('[Raised]' + invalid_region)

        self.session = boto3.session.Session().client(
            's3',
            region_name=self.region,
            endpoint_url='https://' + self.region + '.digitaloceanspaces.com',
            aws_access_key_id=self.public_key,
            aws_secret_access_key=self.secret_key,
        )

        self.refresh_spaces()
        self.space = None
        self.space_files = None

        if space_name:
            self.set_space(space_name)
            self.refresh_files()

    def __str__(self):
        return f"Digital Ocean Spaces <Client: {self.region}/{self.space}>"

    def refresh_spaces(self):
        self.spaces = self.session.list_buckets()['Buckets']
        self.space_names = []
        for space in self.spaces:
            self.space_names += [space.get('Name')]

    def list_spaces(self, string=False):

        # return raw json response
        if not string:
            return self.spaces

        # or return fancy string
        response = """ABVAILABLE SPACES\n=========="""
        for space in self.spaces:
            response += (
                f"""
    Name: {space.get('Name')}
        CreationDate: {space.get('CreationDate')}
    ----------"""
            )
        response += "\n=========="
        return response

    def set_space(self, space_name):
        # If space is set and no space_name param, skip
        if not space_name:
            if self.space:
                return
            else:
                raise Exception('[Raised]' + no_space_name +
                                f'Available options:\nspaces = {self.space_names}')
        elif space_name in self.space_names:
            self.space = space_name
        else:
            raise Exception('[Raised]' + invalid_space_name +
                            f'Available options:\nspaces = {self.space_names}')
        return True

    def refresh_files(self, space_name=None):
        self.set_space(space_name)
        self.space_files = self.session.list_objects(Bucket=self.space).get('Contents')
        return True

    def list_dirs(self, path='', space_name=None, string=False, ):
        """
        Lists only directories.
        """
        self.set_space(space_name)
        if not self.space_files or space_name:
            self.refresh_files(space_name)

        files = sort_files(self.space_files, dir, 'directory')

        if not string:
            return files

        response = f"""== [{self.region}/{self.space}] DIRECTORY LIST ==\n=========="""

        for file in files:
            type = file_or_dir(file)
            response += file_to_string(file, type)
    
        response += "\n=========="
        return response

    def list_files(self, path='', space_name=None, string=False, ):
        """
        Lists only files.
        """
        self.set_space(space_name)
        if not self.space_files or space_name:
            self.refresh_files(space_name)

        files = sort_files(self.space_files, path, 'file')
        
        if not string:
            return files

        response = f"""== [{self.region}/{self.space}] FILE LIST ==\n=========="""

        for file in files:
            type = file_or_dir(file)
            response += file_to_string(file, type)

        response += "\n=========="
        return response

    def list_all(self, path='', space_name=None, string=False ):
        """
        Lists files and directories
        """
        self.set_space(space_name)
        if not self.space_files or space_name:
            self.refresh_files(space_name)

        files = sort_files(self.space_files, path)

        if not string:
            return files

        response = f"""== [{self.region}/{self.space}] ALL LIST ==\n=========="""

        for file in files:
            type = file_or_dir(file)
            response += file_to_string(file, type)

        response += "\n=========="
        return response
        
    def download_file(self, file_name, destination="downloads/", space_name=None):
        """
        Downloads a single file.
        """
        self.set_space(space_name)

        directory = destination + os.path.dirname(file_name)

        if not os.path.exists(directory):
            os.makedirs(directory)
        destination += file_name

        try:
            tic = time.perf_counter()
            self.session.download_file(self.space, file_name, destination)
            toc = time.perf_counter()
            print(
                f'Downloaded from {self.region}/{self.space} in {toc - tic:0.4f} seconds \n- Destination -> {destination}')
            return True
        finally:
            pass
        
    def upload_file(self, file, destination="", rename=None, space_name=None, extra_args={}):
        """
        Uploads a single file.
        """
        self.set_space(space_name)

        # Check if destination contains file name
        if os.path.basename(destination):
            raise Exception('[Raised]' + cant_place_file_name_in_destination)

        # Get file name and extentions
        basename = os.path.basename(file)
        file_ext = ''.join(Path(basename).suffixes)
        name = file_ext[-(len(file_ext))]

        # Check for rename and make sure it's safe
        if rename:
            if Path(rename).suffixes:
                raise Exception('[Raised]' + cant_replace_file_ext)
            elif os.path.dirname(rename):
                raise Exception('[Raised]' + cant_place_path_in_file_name)
            else:
                name = rename

        # Make sure destination is marked as a directory
        if destination[-1] != '/':
            destination += '/'
        destination += name + file_ext

        try:
            tic = time.perf_counter()
            self.session.upload_file(file, self.space, destination, ExtraArgs=extra_args)
            toc = time.perf_counter()
            print(
                f'Uploaded to {self.region}/{self.space} in {toc - tic:0.4f} seconds \n- Destination -> {destination}')
            self.refresh_files()
            return True
        finally:
            pass

    def delete_file(self, file_path, yes=False, space_name=None):
        """
        Deletes file that matches file_path exactly.
        """
        self.set_space(space_name)

        if not yes:
            ans = input(f"Confirm you want to delete '{file_path}'? y/N: ")
            if ans.lower not in ['y', 'yes']:
                return False

        res = self.session.delete_object(Bucket=self.space_name, Key=file_path)

        if res.get('ResponseMetadata').get('RetryAttempts') == 0:
            return True
        else:
            return res
