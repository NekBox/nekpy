import numpy as np

def grep_log(lines, key, pos=None):
    offset = len(key.split())
    res = []
    for line in lines:
        if key in line:
            if pos is None:
                res.append([float(x) for x in line.split()[offset:]])
            else:
                res.append(float(line.split()[pos]))

    return np.array(res)

