import random
import numpy as np
from clustering.utils import squared_distance


def kcenter(P, k):
    centers = [random.choice(P)]

    for step in range(1, k):
        print(f"[k-center] Selecting center {step + 1}/{k}")

        max_dist = -1
        next_center = None

        for p in P:
            min_dist = min(squared_distance(p, c) for c in centers)

            if min_dist > max_dist:
                max_dist = min_dist
                next_center = p

        centers.append(next_center)

    return centers


def kmeansPP(P, k):
    centers = [random.choice(P)]

    for step in range(1, k):
        print(f"[kmeans++] Selecting center {step + 1}/{k}")

        distances = np.array([
            min(squared_distance(p, c) for c in centers) for p in P
        ])

        probs = distances / distances.sum()
        cumulative = np.cumsum(probs)

        r = random.random()

        for i, val in enumerate(cumulative):
            if r <= val:
                centers.append(P[i])
                break

    return centers


def kmeansObj(P, C):
    print("[Objective] Computing k-means objective...")

    total = 0.0

    for i, p in enumerate(P):
        if i % 500 == 0:
            print(f"Processed {i}/{len(P)} points")

        min_dist = min(squared_distance(p, c) for c in C)
        total += min_dist

    return total / len(P)


def assign_weights(P, centers):
    """
    Assign number of original points closest to each center
    """
    weights = [0] * len(centers)

    for p in P:
        min_idx = 0
        min_dist = float('inf')

        for i, c in enumerate(centers):
            dist = squared_distance(p, c)
            if dist < min_dist:
                min_dist = dist
                min_idx = i

        weights[min_idx] += 1

    return weights

def expand_weighted_points(centers, weights):
    """
    Expand centers based on weights (simple approximation)
    """
    expanded = []

    for c, w in zip(centers, weights):
        repeat = max(1, w // 50)   # scaling factor
        expanded.extend([c] * repeat)

    return expanded

