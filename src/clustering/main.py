import time
from clustering.utils import readVectorsSeq
from clustering.clustering import kcenter, kmeansPP, kmeansObj, assign_weights, expand_weighted_points
from clustering.visualization import visualize_clusters


def main():
    print("Program started...")

    filename = "data/Q1/spambase.data"

    print("STEP 1: Loading dataset...")
    P = readVectorsSeq(filename)

    print("STEP 2: Dataset validation")
    print("Total points:", len(P))
    print("Dimensions:", len(P[0]))

    k = 10
    k1 = 100

    # STEP 3
    print("\nSTEP 3: Running k-center")
    C_kcenter = kcenter(P, k)

    # STEP 4
    print("\nSTEP 4: Running kmeans++")
    C_kmeans = kmeansPP(P, k)
    obj = kmeansObj(P, C_kmeans)

    # STEP 5 (Hybrid)
    print("\nSTEP 5: Hybrid approach (Improved)")
    X = kcenter(P, k1)

    print("Assigning weights...")
    weights = assign_weights(P, X)

    print("Expanding weighted coreset...")
    X_weighted = expand_weighted_points(X, weights)

    best_obj = float('inf')
    C_final = None

    for i in range(5):
        print(f"Trial {i+1}/5")
        C_temp = kmeansPP(X_weighted, k)
        obj_temp = kmeansObj(P, C_temp)

        if obj_temp < best_obj:
            best_obj = obj_temp
            C_final = C_temp

    obj_final = best_obj

    # STEP 6
    print("\nSTEP 6: Visualization")
    visualize_clusters(P, C_kmeans, "KMeans++ Clusters")

    # FINAL
    print("\nFINAL COMPARISON")
    print("KMeans++:", obj)
    print("Hybrid:", obj_final)


if __name__ == "__main__":
    main()