def calculate_fcfs(requests, head):
    if not requests:
        return [], 0

    seek_sequence = [head] + requests.copy()
    total_movement = 0

    for i in range(len(seek_sequence) - 1):
        total_movement += abs(seek_sequence[i] - seek_sequence[i+1])

    return seek_sequence, total_movement