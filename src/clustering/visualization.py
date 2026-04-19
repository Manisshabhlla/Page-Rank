import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np


def visualize_clusters(P, centers, title):
    print("[Visualization] Reducing dimensions using PCA...")

    data = np.array(P)
    centers = np.array(centers)

    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)
    reduced_centers = pca.transform(centers)

    print("[Visualization] Plotting clusters...")

    plt.figure(figsize=(8, 6))
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], s=10, alpha=0.4)
    plt.scatter(reduced_centers[:, 0], reduced_centers[:, 1], s=100, marker='x')

    plt.title(title)
    plt.savefig(f"images/{title}.png")
    plt.show()