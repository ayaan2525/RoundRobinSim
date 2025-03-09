import pandas as pd
import sys

def round_robin(tasks, quantum):
    queue = tasks.to_dict(orient="records") #convert df to list of dict
    schedule = []
    time = 0
    waiting_time = {task["PID"]: 0 for task in queue}
    turnaround_time = {}
    remaining_burst_time = {task["PID"]: task["BurstTime"] for task in queue}

    while queue:
        task = queue.pop(0) #fetch 1st task
        pid, arrival_time = task['PID'], task['ArrivalTime']

        # execute for quantum time
        if remaining_burst_time[pid] > quantum:
            time += quantum
            remaining_burst_time[pid] -= quantum
            queue.append(task)
        else:
            time += remaining_burst_time[pid]
            turnaround_time[pid] = time - arrival_time
            waiting_time[pid] = turnaround_time[pid] - task['BurstTime']
            remaining_burst_time[pid] = 0

        schedule.append((pid, time))
    return schedule, waiting_time, turnaround_time

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 scheduler.py tasks.csv time_quantum")
        sys.exit(1)
    
    tasks_file = sys.argv[1]
    time_quantum = int(sys.argv[2])

    tasks = pd.read_csv(tasks_file)

    schedule, waiting_time, turnaround_time = round_robin(tasks, time_quantum)
    tasks["WaitingTime"] = tasks["PID"].map(waiting_time)
    tasks["TurnAroundTime"] = tasks["PID"].map(turnaround_time)

    tasks.to_csv("tasks.csv", index=False)
    print("\nUpdated tasks.csv with waiting and turnaround time")
    print(tasks)