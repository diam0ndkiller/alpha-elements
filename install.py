#!/bin/python3

import platform
import getpass
import os

SYSTEM = platform.system()[0]

LINUX = SYSTEM == 'L'
WINDOWS = SYSTEM == 'W'

if LINUX:
    MC_DIR = "/home/" + getpass.getuser() + "/.minecraft"
elif WINDOWS:
    MC_DIR = "C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft"

CONFIG_DIR = MC_DIR + "/alpha_elements"

if LINUX:
    os.system('mkdir -p "' + CONFIG_DIR + '">/dev/null')
elif WINDOWS:
    os.system('mkdir "' + CONFIG_DIR.replace('/', '\\') + '">nul')

if LINUX:
    os.system(f"cp -r ./__RESOURCES__/ {CONFIG_DIR}/")
    os.system(f"cp ./alpha_elements.py {CONFIG_DIR}/")
    os.system(f"cp ./LICENSE.md {CONFIG_DIR}/")
    os.system(f"cp ./README.md {CONFIG_DIR}/")
    os.system('xdg-open "https://github.com/diam0ndkiller/dcgf"')
elif WINDOWS:
    CONFIG_DIR = CONFIG_DIR.replace("/", "\\")
    os.system(f"copy .\\__RESOURCES__ {CONFIG_DIR}\\ /E")
    os.system(f"copy .\\alpha_elements.py {CONFIG_DIR\\")
    os.system(f"copy .\\LICENSE.md {CONFIG_DIR\\")
    os.system(f"copy .\\README.md {CONFIG_DIR\\")
    os.system('start "https://github.com/diam0ndkiller/dcgf"')
