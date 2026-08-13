#!/usr/bin/env python3

##########################################################################
##########################################################################
## This file will download and install dependencies for these scripts ####
##########################################################################
##########################################################################
import importlib.util
import subprocess
import sys

def missing_dependency():
    modules = ["numpy", "pandas", "matplotlib", "requests", "bs4"]  # Add your modules here
    for module in modules:
        try:
            test = subprocess.run([sys.executable, "-c", f"import {module}"], check=False)
            print(test)
        except subprocess.CalledProcessError:
            pass
            #print(f"{module} is not installed.")

            
def apt_installer(package):
    try:
        subprocess.run([package, "--version"])
        return 1
    except FileNotFoundError:
        print(f"{package}is not installed. Installing now...")
        input(f"Press Enter to continue with installing {package} and dependencies via apt...")
        subprocess.run(["sudo", "apt", "update"])
        subprocess.run(["sudo", "apt", "install", package])
        return 1
    except:
        print(f"{package} is already installed.")
        return 0

def pip_installer(package_name):
    # Check if the package is already installed
    if importlib.util.find_spec(package_name) is None:
        print(f"{package_name} is not installed. Installing now...")
        subprocess.run(["sudo", "pipx", "install", package_name])
    else:
        print(f"{package_name} is already installed.")

def install_modules():
    modules= ["python3-tk"]  # Add your modules here

    for module in modules:
        if apt_installer(module) == 1:
            pip_installer(module)

#subprocess.run([sys.executable, "-c", "import pandas"], check=False)