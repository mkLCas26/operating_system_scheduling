def calculate_sjf(process_list, is_preemptive):
    """
    Returns: (calculated_processes, average_tat, average_wt, cpu_utilization, gantt_timeline)
    """
    if not process_list:
        return [], 0, 0, 0, []

    # 1. Setup deep copy and include 'rem_bt' (remaining burst time)
    processes = []
    for p in process_list:
        processes.append({
            'pid': p['pid'],
            'at': int(p['at']),
            'bt': int(p['bt']),
            'rem_bt': int(p['bt']),
            'ct': 0, 'tat': 0, 'wt': 0
        })

    current_time = 0
    completed = 0
    n = len(processes)
    raw_timeline = []
    total_idle_time = 0

    # --- THE SIMULATION ---
    if not is_preemptive:
        # NON-PREEMPTIVE LOGIC (Standard SJF)
        while completed < n:
            available = [p for p in processes if p['at'] <= current_time and p['rem_bt'] > 0]

            if not available:
                next_arrival = min(p['at'] for p in processes if p['rem_bt'] > 0)
                raw_timeline.append(('IDLE', current_time, next_arrival))
                total_idle_time += (next_arrival - current_time)
                current_time = next_arrival
                continue

            # Sort by Burst Time (Shortest first), then Arrival Time
            available.sort(key=lambda x: (x['rem_bt'], x['at']))
            current_process = available[0]

            start_time = current_time
            time_to_run = current_process['rem_bt']
            current_time += time_to_run
            current_process['rem_bt'] = 0

            raw_timeline.append((current_process['pid'], start_time, current_time))

            current_process['ct'] = current_time
            current_process['tat'] = current_process['ct'] - current_process['at']
            current_process['wt'] = current_process['tat'] - current_process['bt']
            completed += 1

    else:
        # PREEMPTIVE LOGIC (SRTF - Shortest Remaining Time First)
        while completed < n:
            available = [p for p in processes if p['at'] <= current_time and p['rem_bt'] > 0]

            if not available:
                next_arrival = min(p['at'] for p in processes if p['rem_bt'] > 0)
                raw_timeline.append(('IDLE', current_time, next_arrival))
                total_idle_time += (next_arrival - current_time)
                current_time = next_arrival
                continue

            # Sort by Remaining Burst Time, then Arrival Time
            available.sort(key=lambda x: (x['rem_bt'], x['at']))
            current_process = available[0]

            start_time = current_time
            
            # Execute for exactly 1 unit of time
            current_process['rem_bt'] -= 1
            current_time += 1

            raw_timeline.append((current_process['pid'], start_time, current_time))

            if current_process['rem_bt'] == 0:
                current_process['ct'] = current_time
                current_process['tat'] = current_process['ct'] - current_process['at']
                current_process['wt'] = current_process['tat'] - current_process['bt']
                completed += 1

    # --- POST-PROCESSING ---
    # Merge contiguous blocks in the timeline
    optimized_timeline = []
    for entry in raw_timeline:
        if optimized_timeline and optimized_timeline[-1][0] == entry[0]:
            last = optimized_timeline.pop()
            optimized_timeline.append((last[0], last[1], entry[2]))
        else:
            optimized_timeline.append(entry)

    # Calculate Stats
    total_tat = sum(p['tat'] for p in processes)
    total_wt = sum(p['wt'] for p in processes)
    
    avg_tat = round(total_tat / n, 2) if n > 0 else 0
    avg_wt = round(total_wt / n, 2) if n > 0 else 0
    
    total_time = current_time
    busy_time = total_time - total_idle_time
    cpu_util = round((busy_time / total_time) * 100, 2) if total_time > 0 else 0
    
    processes.sort(key=lambda x: int(x['pid'].replace('P', '')))

    return processes, avg_tat, avg_wt, cpu_util, optimized_timeline