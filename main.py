#!/usr/bin/env python3

#######################################################################
## Reads CSV lottery results and generates weighted random numbers   ##
## Now supports filtering out rollover draws (Column D in CSV)       ##
#######################################################################

import os
import subprocess
import sys


modules = ["tkinter","numpy", "pandas", "matplotlib", "requests", "bs4"]  # Add your modules here
sucess = {}
for module in modules:
    try:
        test = subprocess.run([sys.executable, "-c", f"import {module}"], check=True)
        if test.returncode == 0:
            #print(f"{module} is installed.")
            sucess[module] = True
    except subprocess.CalledProcessError:
        #print(f"Please install | {module:^20}|")
        sucess[module] = False
valid = all(sucess.values())
for key, value in sucess.items():
    if not value:
        print(f"Please install the missing module: {key}")
        sys.exit(1)
        print(f"{key} is installed.")

if(valid):
    print(f"All required modules are installed. Proceeding with the program...")
    import ui.lotteryPickerGUI as lotpic
    #lotpic.run_gui()