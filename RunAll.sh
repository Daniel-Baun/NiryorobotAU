#!/bin/bash
cd ../Odoo/odoo &&
nohup python3 odoo-bin -d main_db  > odoo_log.txt 2>&1 &
sleep 3

current_dir=$(pwd)
echo "Current dir: $current_dir"
cd Python &&
nohup python3 GUI.py
nohup python3 robots.py


cd ../FMU/Maestro &&
nohup java -jar maestro-2.3.0-jar-with-dependencies.jar interpret import/spec.mabl -output output

cd ../../Python &&
nohup python3 publish_to_fmu.py

