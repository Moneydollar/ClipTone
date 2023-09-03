import sys
from cx_Freeze import setup, Executable

# Define platform-specific settings
base = None
icon = None

if sys.platform == "win32":
    base = "Win32GUI"  # For Windows, use Win32GUI to hide the console
    icon = "assets/icon64.ico"  # Replace with the path to your Windows icon
elif sys.platform == "linux" or sys.platform == "linux2":
    icon = "/home/cashc/Documents/Projects/ClipTone-1.3.4/assets/icon64.png"  # Replace with the path to your Linux icon

# Define includes, exclude, and packages
includes = []
include_files = ["/home/cashc/Documents/Projects/ClipTone-1.3.4/assets"]
excludes = ["pydoc_data", "setuptools", "distutils"]
packages = ["os"]

setup(
    name="ClipTone",
    version="1.3.3",
    description="ClipTone",
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
            shortcut_name="ClipTone",
            shortcut_dir="DesktopFolder",
            icon=icon,  # Set the icon based on the platform
        )
    ],
)
