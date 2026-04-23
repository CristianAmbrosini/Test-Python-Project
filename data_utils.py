def normalize(values):
    mn = min(values)
    mx = max(values)
    return [(v - mn) / (mx - mn) for v in values]


def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def merge_dicts(a, b):
    out = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = merge_dicts(out[k], v)
        else:
            out[k] = v
    return out
