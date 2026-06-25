def calculate_fcfs(process_list):
    """
    Takes a list of dictionaries: [{'pid': 'P1', 'at': 0, 'bt': 5}, ...]
    Returns a tuple: (calculated_processes, average_tat, average_wt, gantt_timeline)
    """
    if not process_list:
        return [], 0, 0, []

    # 1. Sort the processes based on Arrival Time (AT)
    # If ATs are equal, it falls back to the order they were added.
    sorted_processes = sorted(process_list, key=lambda x: x['at'])

    current_time = 0
    calculated_processes = []
    gantt_timeline = []
    
    total_tat = 0
    total_wt = 0

    # 2. Calculate CT, TAT, and WT sequentially
    for p in sorted_processes:
        pid = p['pid']
        at = int(p['at'])
        bt = int(p['bt'])

        # If the CPU is idle (process hasn't arrived yet)
        if current_time < at:
            # Record the idle time for the Gantt chart
            gantt_timeline.append(('IDLE', current_time, at))
            current_time = at 

        # Process execution
        start_time = current_time
        completion_time = current_time + bt
        current_time = completion_time

        # Formulas
        turnaround_time = completion_time - at
        waiting_time = turnaround_time - bt

        # Track totals for averages
        total_tat += turnaround_time
        total_wt += waiting_time

        # Save calculations
        calculated_processes.append({
            'pid': pid,
            'at': at,
            'bt': bt,
            'ct': completion_time,
            'tat': turnaround_time,
            'wt': waiting_time
        })

        # Save timeline for Gantt chart
        gantt_timeline.append((pid, start_time, completion_time))

    # 3. Calculate Averages
    n = len(calculated_processes)
    avg_tat = round(total_tat / n, 2)
    avg_wt = round(total_wt / n, 2)

    return calculated_processes, avg_tat, avg_wt, gantt_timeline