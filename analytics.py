def parse_csv_line(line, delimiter=','):
    parts = line.strip().split(delimiter)
    return [p.strip().strip('"') for p in parts]


def compute_moving_average(values, window):
    if window <= 0 or window > len(values):
        raise ValueError("window must be between 1 and len(values)")
    result = []
    for i in range(len(values) - window + 1):
        result.append(sum(values[i:i + window]) / window)
    return result


def group_by(items, key_fn):
    groups = {}
    for item in items:
        k = key_fn(item)
        groups.setdefault(k, []).append(item)
    return groups


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))
