#!/usr/bin/env python3

##########################################################################
##########################################################################
## This file will download and install dependencies for these scripts ####
##########################################################################
##########################################################################
import importlib.util
import subprocess
import sys

def check_and_install_pip():
    try:
        # Upgrade pip if it's already installed
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip is installed and upgraded.")
        return 1
    except subprocess.CalledProcessError:
        print("pip is not installed. Please install pip manually or use a package manager. Run the following cmd: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py : followed by : python3 get-pip.py")
        return 0

def check_and_install_dependencies(package_name):
    # Check if the package is already installed
    if importlib.util.find_spec(package_name) is None:
        print(f"{package_name} is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    else:
        print(f"{package_name} is already installed.")


# Call the function to check and install/upgrade pip
#check_and_install_pip()

# Example usage with a list of modules to check
modules = ["numpy", "pandas", "matplotlib", "requests", "bs4"]  # Add your modules here

if check_and_install_pip() == 1:
    for module in modules:
        check_and_install_dependencies(module)
