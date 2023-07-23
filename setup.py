import sys
from cx_Freeze import setup, Executable
import os.path

includes = []
include_files = ["assets/"]

# Exclude unnecessary packages
excludes = ["pydoc_data", "setuptools", "distutils"]

# Dependencies are automatically detected, but some modules need help.
packages = ["os"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Video to Audio Downloader",
    version="1.0.0",
    description="Simple Python Video Audio Downloader and Converter",
    author="Cash E. Coffman",
    author_email="",
    options={
        "build_exe": {
            "includes": includes,
            "excludes": excludes,
            "packages": packages,
            "include_files": include_files,
        }
    },
    executables=[
        Executable(
            "main.py",
            base=base,
            copyright="Cash E. Coffman",
            icon="assets/icon.ico",
        )
    ],
)
