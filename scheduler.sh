#!/bin/bash

generate_tasks() {
    num_tasks=$1
    echo "PID,BurstTime,ArrivalTime" > tasks.csv
    
    for ((i=1; i<=num_tasks; i++)); do
        burst_time=$((RANDOM % 10 + 1)) #1-10 sec
        arrival_time=$((RANDOM % 5)) #0-4 sec
        echo "$i,$burst_time,$arrival_time" >> tasks.csv
    done
}

if [ "$#" -ne 2 ]; then
    echo "Usage: bash scheduler.sh <num_tasks> <quantum>"
    exit 1
fi

generate_tasks $1
python3 scheduler.py tasks.csv $2 # execute python scheduler