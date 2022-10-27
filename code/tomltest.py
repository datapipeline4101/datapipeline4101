import pathlib
import bpy
import tomli
#import os

#path = pathlib.Path(file).parent / "tomconfig.toml"
#print(path)
path1 = pathlib.Path("toml_t.toml")
with path1.open(mode="rb") as fp:
    tomconfig = tomli.load(fp)

#tomconfig = tomli.load("/Users/nathanpichette/Documents/Senior-Design/blender-testing/basic-bpy/tomconfig.toml")
print(path1)