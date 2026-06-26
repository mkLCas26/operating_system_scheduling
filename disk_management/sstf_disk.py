def calculate_sstf(requests, head):
    if not requests:
        return [], 0

    reqs = requests.copy()
    seek_sequence = [head]
    total_movement = 0
    current_head = head

    while reqs:
        closest = min(reqs, key=lambda x: abs(x - current_head))
        total_movement += abs(closest - current_head)
        current_head = closest
        seek_sequence.append(current_head)
        reqs.remove(closest)

    return seek_sequence, total_movement