import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files": [".env"]}
base = None

setup(  name = "Akinify",
        version = "0.1",
        description = "Spotify stuff",
        options = {"build_exe": build_exe_options},
        executables = [Executable("akinify.py", base=base)])