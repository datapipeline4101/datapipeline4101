import pip
pip.main(['install', 'tomli', '--user'])

import sys

# 2. watch blender's python path in console output at this moment
# 3. insert the path to packages_path below and uncomment

packages_path = r"c:\users\stern\appdata\roaming\python\python310\site-packages" # the path you see in console

# 4. uncomment the next code and launch script in blender interpreter again

sys.path.insert(0, packages_path )
import tomli

import pathlib
import bpy
import tomli
#import os

#path = pathlib.Path(file).parent / "tomconfig.toml"
#print(path)
path1 = pathlib.Path(r"C:\Users\stern\Documents\college\senior_proj\datapipeline4101\code\toml_t.toml")
with path1.open(mode="rb") as fp:
    tomconfig = tomli.load(fp)

#tomconfig = tomli.load("/Users/nathanpichette/Documents/Senior-Design/blender-testing/basic-bpy/tomconfig.toml")
print(path1)