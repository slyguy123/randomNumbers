#!/usr/bin/env python3

#######################################################################
## Reads CSV lottery results and generates weighted random numbers   ##
## Now supports filtering out rollover draws (Column D in CSV)       ##
#######################################################################

import os
import dependencies.validateDependencies as dep

depPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pip", "buildDependencies.py")


try:
    import ui.lotteryPickerGUI as lotPick
    lotPick()
except:
    print(f"Running dependencies validation:\npython3 {depPath}")
    dep.missing_dependency()