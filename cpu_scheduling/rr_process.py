def calculate_rr(process_list, time_quantum):
    """
    Takes a list of dicts and a time quantum.
    Returns: (calculated_processes, average_tat, average_wt, cpu_utilization, gantt_timeline)
    """
    if not process_list or time_quantum <= 0:
        return [], 0, 0, 0, []

    # 1. Create a deep copy so we can modify 'remaining burst time' without destroying the original input
    processes = []
    for p in process_list:
        processes.append({
            'pid': p['pid'],
            'at': int(p['at']),
            'bt': int(p['bt']),
            'rem_bt': int(p['bt']) # <-- NEW: Tracks time left!
        })
        
    # Sort processes by Arrival Time initially
    processes.sort(key=lambda x: x['at'])
    
    current_time = 0
    calculated_processes = []
    raw_timeline = []
    ready_queue = []
    
    total_idle_time = 0
    completed = 0
    n = len(processes)
    
    # Tracks which processes have already entered the ready queue
    added_to_queue = [False] * n 

    # --- THE SIMULATION LOOP ---
    while completed < n:
        # A. Add any processes that have "arrived" by the current_time to the queue
        for i, p in enumerate(processes):
            if p['at'] <= current_time and not added_to_queue[i]:
                ready_queue.append(p)
                added_to_queue[i] = True
                
        # B. If the queue is empty, the CPU sits IDLE until the next process arrives
        if not ready_queue:
            next_arrival = min([p['at'] for i, p in enumerate(processes) if not added_to_queue[i]])
            raw_timeline.append(('IDLE', current_time, next_arrival))
            total_idle_time += (next_arrival - current_time)
            current_time = next_arrival
            continue
            
        # C. Pop the first process off the front of the queue
        current_process = ready_queue.pop(0)
        start_time = current_time
        
        # D. Execute for either the Time Quantum OR whatever is left (whichever is smaller)
        time_to_run = min(time_quantum, current_process['rem_bt'])
        current_time += time_to_run
        current_process['rem_bt'] -= time_to_run
        
        raw_timeline.append((current_process['pid'], start_time, current_time))
        
        # E. VERY IMPORTANT: Check for NEW arrivals while the process was running 
        # BEFORE we put the current process back in line
        for i, p in enumerate(processes):
            if p['at'] <= current_time and not added_to_queue[i]:
                ready_queue.append(p)
                added_to_queue[i] = True
                
        # F. If the process is finished, calculate its final stats
        if current_process['rem_bt'] == 0:
            completed += 1
            ct = current_time
            tat = ct - current_process['at']
            wt = tat - current_process['bt']
            
            calculated_processes.append({
                'pid': current_process['pid'],
                'at': current_process['at'],
                'bt': current_process['bt'],
                'ct': ct,
                'tat': tat,
                'wt': wt
            })
        else:
            # If it's NOT finished, send it to the back of the line!
            ready_queue.append(current_process)

    # --- POST-PROCESSING ---

    # Calculate Averages and Utilization
    total_tat = sum(p['tat'] for p in calculated_processes)
    total_wt = sum(p['wt'] for p in calculated_processes)
    
    avg_tat = round(total_tat / n, 2) if n > 0 else 0
    avg_wt = round(total_wt / n, 2) if n > 0 else 0
    
    total_time = current_time
    busy_time = total_time - total_idle_time
    cpu_util = round((busy_time / total_time) * 100, 2) if total_time > 0 else 0
    
    # Sort the final table so P1, P2, P3 show up in order
    calculated_processes.sort(key=lambda x: int(x['pid'].replace('P', '')))

    # Optional Polish: If a process runs twice in a row (because it's the only one in the queue),
    # this merges those blocks so the Gantt chart looks cleaner.
    optimized_timeline = []
    for entry in raw_timeline:
        if optimized_timeline and optimized_timeline[-1][0] == entry[0]:
            last = optimized_timeline.pop()
            optimized_timeline.append((last[0], last[1], entry[2]))
        else:
            optimized_timeline.append(entry)

    return calculated_processes, avg_tat, avg_wt, cpu_util, optimized_timeline