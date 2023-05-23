#!/bin/bash
cd ../Odoo/odoo &&
x-terminal-emulator -e python3 odoo-bin -d main_db &&
cd ../../Code/Python &&
python3 GUI.py


