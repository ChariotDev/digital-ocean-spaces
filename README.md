# digital_ocean_spaces
An MIT licensed python client for Digital Ocean Spaces with a built in shell

## TLDR
The client connects to a Digital Ocean region and can list files/directors and download/upload files.
It has a built in terminal shell for verbose commands and navigation, <- Not yet finished.

## ABOUT
Inspired by [Python3-DigitalOcean-Spaces-Manager-v2-Advanced](https://github.com/Mashoud123/Python3-DigitalOcean-Spaces-Manager-v2-Advanced). An API client was needed for a commercial project and that package was the best contender. Abandoned, riddled with issues and lacking any license for distro and modificaiton, digital_ocean_spaces was built from scratch with an MIT license. Use it, share it and most of all, feel free to modify it, and contribute back.

The digital_ocean_spaces package provides a nearly stress free 'Client' class to help you connect to Digital Ocean spaces. All it needs is your keys and the name of the server to connect to. Once authorized, the client will hopefuly help you figure out what you're doing wrong.

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
from digital_ocean_spaces import Client

client = Client(
  region_name = 'sfo3', # Required
  space_name = 'my_media', # Optional, can be updated with <client>.set_space(space_name)
  public_key = 'foo', # Optional, can set key in digital_ocean_spaces/env.yaml                                                                         
  secret_key = 'bar', # Optional, can set key in digital_ocean_spaces/env.yaml
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
  client.list_spaces(
    space_name=None # Optional if a space is already set
    string=True # Returns a fancy string
  )
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
Client.list_dirs(self, space_name=None, string=False, dir='')
```
```py
# Lists only the available files
Client.list_files(self, space_name=None, string=False, dir='')
```
```py
# Lists all files and directories
Client.list_all(self, space_name=None, string=False, dir='')
```
```py
# Downloads specified file
Client.download_file(self, file_name, destination="downloads/", space_name=None)
```
```py
# Uploads specified file
Client.upload_file(self, file, destination="", rename=None, space_name=None )
```
```py
# Starts verbose shell
Client.shell(self)
```

## CHANGELOG

### 0.1.1
- Documentation

### 0.1.0
- Initial release

