# digital-ocean-spaces
An MIT licensed python client for Digital Ocean Spaces with a built in shell

## TLDR
The client connects to a Digital Ocean region and can list files/directors and download/upload files.
It has a built in terminal shell for verbose commands and navigation, <- Not yet finished.

## ABOUT
Inspired by [Python3-DigitalOcean-Spaces-Manager-v2-Advanced](https://github.com/Mashoud123/Python3-DigitalOcean-Spaces-Manager-v2-Advanced). An API client was needed for a commercial project and that package was the best contender. Abandoned, riddled with issues and lacking any license for distro and modificaiton, digital_ocean_spaces was built from scratch with an MIT license. Use it, share it and most of all, feel free to modify it, and contribute back.

The digital-ocean-spaces package provides a nearly stress free 'Client' class that wraps boto3 to help you connect to Digital Ocean spaces. All it needs is your keys and the name of the server to connect to. Once authorized, the client will hopefuly help you figure out what you're doing wrong.

Once you have an authorized client ( server name, public key, secret key,) you should be able to implement it into your existing application like normal.

Alternatively, if you want to stay in the console and use verbose commands, you can run <Client>.shell() <- Not yet finished.
                                                                                                            
## QUICKSTART

### INSTALL
```console
Console
$ pip install digital-ocean-spaces
or...
$ pip install git+git@github.com:ChariotDev/digital-ocean-spaces.git
```

### USE EXAMPLE
```py
# main.py
from spaces import Client

client = Client(
  region_name = 'sfo3', # Required
  space_name = 'my_media', # Optional, can be set in spaces/env.yaml and/or be updated with <client>.set_space(space_name)
  public_key = 'foo', # Required, but can set key in spaces/env.yaml                                                                         
  secret_key = 'bar', # Required, but can set key in spaces/env.yaml

  # If any of region_name, public_key or secret_key are not provided, Client will override all values with env.yaml values.

)
```

### LIST AVAILABLE SPACES
```py
# main.py
## Returns raw response content json
client.list_spaces()

## Readable version
print(
  client.list_spaces(
    string=True # Returns a fancy string
  )
)
```

### LIST ALL AVAILABLE FILES
```py
# main.py
## Returns raw response content json
client.list_files(
  space_name=None # Optional if a space is already set
)

## Readable version
print(
  client.list_spaces
    space_name=None # Optional if a space is already set
    string=True # Returns a fancy string
  )
)

## Search/list by path begins with 'foo', 'foo/', 'foo/bar.txt'
client.list_files(
    path="foo/"
    space_name=None # Optional if a space is already set
)

```

### DOWNLOAD FILE
```py
# main.py

client.download_file(
  file_name='foo/bar.txt'
  destination='downloads/' # Optional, should use a useful directory
  space_name=None # Optional if a space is already set
)

# Download to -> downloads/foo/bar.txt

```

### UPLOAD FILE
```py
# main.py

client.upload_file(
  file='my/pc/foo/bar.txt'
  destination='foo/' # Optional, should use a useful directory
  rename=None # Optional, file name only, no paths or extentions
  space_name=None # Optional if a space is already set
)

# Upload to -> foo/bar.txt
```

### VERBOSE SHELL

```console
console

$ client.shell()
```

## TECHNICAL

### CLIENT FUNCTIONS

```py
# Creates a Client object
Client<.__init__>(self, region_name=None, space_name=None, public_key=None, secret_key=None)
```

```py
# Updates and stores available spaces
Client.refresh_spaces()
```
```py
# Lists available spaces
Client.list_spaces(self, string=False)
```
```py
# Sets active space
Client.set_space(self, space_name)
```
```py
# Updates and stores available files
Client.refresh_files(self, space_name=None)
```
```py
# Lists only the available directories
Client.list_dirs(self, path='', space_name=None, string=False)
```
```py
# Lists only the available files
Client.list_files(self, path='', space_name=None, string=False)
```
```py
# Lists all files and directories
Client.list_all(self, path='', space_name=None, string=False)
```
```py
# Downloads specified file
Client.download_file(self, file_name, destination="downloads/", space_name=None)
```
```py
# Uploads specified file
Client.upload_file(self, file, destination="", rename=None, space_name=None)
```
```py
# Deletes specified file
Client.delete_file(self, file_path, yes=False, space_name=None)
```
```py
# Starts verbose shell
Client.shell(self)
```

## CHANGELOG

### 0.2.2
- added error to upload_file to prevent file name in destination path

### 0.2.1
- remove pkg-resources==0.0.0 dependency
- rebuild requirement.txt

### 0.2.0
- dir kwarg renamed to path, moved to the first positional arg in: list_files, list_dirs, list_all
- space_files will populate upon client instance if space_name is supplied.
- added delete_file function

### 0.1.5
- Fixed manifest

### 0.1.2
- Add region name field to env.yaml
- Add default space field to env.yaml
- Renamed import module to spaces for simplicity

### 0.1.1
- Documentation

### 0.1.0
- Initial release

