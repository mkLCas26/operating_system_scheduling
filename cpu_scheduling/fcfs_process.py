def calculate_fcfs(process_list):
    """
    Returns: (calculated_processes, average_tat, average_wt, cpu_utilization, gantt_timeline)
    """
    # Added an extra 0 in the return statement for CPU Util
    if not process_list:
        return [], 0, 0, 0, [] 

    sorted_processes = sorted(process_list, key=lambda x: x['at'])

    current_time = 0
    calculated_processes = []
    gantt_timeline = []
    
    total_tat = 0
    total_wt = 0
    total_idle_time = 0  # Variable to track total idle time

    for p in sorted_processes:
        pid = p['pid']
        at = int(p['at'])
        bt = int(p['bt'])

        if current_time < at:
            gantt_timeline.append(('IDLE', current_time, at))
            total_idle_time += (at - current_time)  # Add to idle time
            current_time = at 

        start_time = current_time
        completion_time = current_time + bt
        current_time = completion_time

        turnaround_time = completion_time - at
        waiting_time = turnaround_time - bt

        total_tat += turnaround_time
        total_wt += waiting_time

        calculated_processes.append({
            'pid': pid,
            'at': at,
            'bt': bt,
            'ct': completion_time,
            'tat': turnaround_time,
            'wt': waiting_time
        })

        gantt_timeline.append((pid, start_time, completion_time))

    n = len(calculated_processes)
    avg_tat = round(total_tat / n, 2)
    avg_wt = round(total_wt / n, 2)
    
    # CPU Utilization Calculation
    total_time = current_time 
    busy_time = total_time - total_idle_time
    # Formula: (Busy Time / Total Time) * 100
    cpu_util = round((busy_time / total_time) * 100, 2) if total_time > 0 else 0

    return calculated_processes, avg_tat, avg_wt, cpu_util, gantt_timeline