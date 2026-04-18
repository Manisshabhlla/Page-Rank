from pyspark import SparkContext
import numpy as np
import random


def squared_distance(a, b):
    return np.sum((a - b) ** 2)


def kcenter_spark(P_rdd, k):
    print("[Spark] Running k-center")

    centers = [P_rdd.takeSample(False, 1)[0]]

    for step in range(1, k):
        print(f"[Spark] Selecting center {step + 1}/{k}")

        distances = P_rdd.map(
            lambda p: min(squared_distance(p, c) for c in centers)
        )

        max_point = P_rdd.zip(distances).max(key=lambda x: x[1])[0]
        centers.append(max_point)

    return centers