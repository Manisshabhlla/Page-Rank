import numpy as np


def readVectorsSeq(filename):
    """
    Reads full dataset (NO SAMPLING)
    """
    points = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                values = list(map(float, line.split(',')))
                points.append(np.array(values))

    return points


def squared_distance(a, b):
    return np.sum((a - b) ** 2)