def calculate_scan(requests, head, total_cylinders, direction):
    if not requests:
        return [], 0

    reqs = requests.copy()
    left = sorted([r for r in reqs if r < head])
    right = sorted([r for r in reqs if r >= head])

    seek_sequence = [head]
    total_movement = 0

    if direction == "Left":
        for r in reversed(left): seek_sequence.append(r)
        if right and (not seek_sequence or seek_sequence[-1] != 0):
            seek_sequence.append(0)
        for r in right: seek_sequence.append(r)
    else:  # Right
        for r in right: seek_sequence.append(r)
        if left and (not seek_sequence or seek_sequence[-1] != total_cylinders - 1):
            seek_sequence.append(total_cylinders - 1)
        for r in reversed(left): seek_sequence.append(r)

    for i in range(len(seek_sequence) - 1):
        total_movement += abs(seek_sequence[i] - seek_sequence[i + 1])

    return seek_sequence, total_movement