import os
import matplotlib.pyplot as plt


def load_graph(file_path):
    graph = {}
    nodes = set()

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue

            u, v = parts

            if u not in graph:
                graph[u] = []

            graph[u].append(v)

            nodes.add(u)
            nodes.add(v)

    for node in nodes:
        if node not in graph:
            graph[node] = []

    return graph, nodes


def initialize_pagerank(nodes):
    N = len(nodes)
    return {node: 1.0 / N for node in nodes}


def compute_pagerank(graph, nodes, iterations=10, d=0.85):
    pr = initialize_pagerank(nodes)

    print("\nRunning Basic PageRank...\n")

    for i in range(iterations):
        new_pr = {}

        for node in nodes:
            new_pr[node] = (1 - d)

        for node in nodes:
            if len(graph[node]) == 0:
                continue

            share = pr[node] / len(graph[node])

            for neighbor in graph[node]:
                new_pr[neighbor] += d * share

        pr = new_pr
        print(f"Iteration {i+1} completed")

    return pr


def display(pr):
    ranked = sorted(pr.items(), key=lambda x: x[1], reverse=True)

    print("\nFinal PageRank:\n")
    for node, score in ranked[:10]:
        print(f"{node} -> {score:.6f}")

    return dict(ranked)


def plot(pr, k=10):
    ranked = list(pr.items())[:k]

    nodes = [str(x[0]) for x in ranked]
    scores = [x[1] for x in ranked]

    plt.figure()
    plt.bar(nodes, scores)
    plt.title("Basic PageRank (Top Nodes)")
    plt.xlabel("Node")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.show()


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, "data", "Q3", "whole.txt")

    print("Loading graph...")
    graph, nodes = load_graph(file_path)

    print("Total nodes:", len(nodes))

    pr = compute_pagerank(graph, nodes)
    ranked = display(pr)
    plot(ranked)


if __name__ == "__main__":
    main()