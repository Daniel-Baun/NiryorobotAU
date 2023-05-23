#!/bin/bash

# Function to kill a process by its name
kill_process() {
    process_name="$1"
    pids=$(pgrep -f "$process_name")
    if [ -n "$pids" ]; then
        echo "Killing $process_name..."
        kill $pids
    fi
}

# Trap the script exit to ensure processes are killed
cleanup() {
    kill_process "odoo-bin"
    kill_process "python3 GUI.py"
    kill_process "python3 robots.py"
    kill_process "java -jar maestro-2.3.0-jar-with-dependencies.jar"
    kill_process "python3 publish_to_fmu.py"
}

# Set up trap to call cleanup function on script exit
trap cleanup EXIT

cd ../Odoo/odoo &&
nohup python3 odoo-bin -d main_db > odoo_log.txt 2>&1 &
sleep 3

current_dir=$(pwd)
echo "Current dir: $current_dir"

cd ../../Code/Python &&
nohup python3 GUI.py > gui_log.txt 2>&1 &

nohup python3 robots.py > robots_log.txt 2>&1 &

cd ../FMU/Maestro &&
nohup java -jar maestro-2.3.0-jar-with-dependencies.jar interpret import/spec.mabl -output output > maestro_log.txt 2>&1 &

cd ../../Python &&
nohup python3 publish_to_fmu.py > publish_log.txt 2>&1 &

# Wait for user input to exit the script
read -p "Press Enter to exit..."
