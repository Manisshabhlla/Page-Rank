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


def compute_pagerank(graph, nodes, d=0.85, max_iter=100, tol=1e-6):
    pr = initialize_pagerank(nodes)
    N = len(nodes)

    print("\nStarting PageRank with convergence...\n")

    for i in range(max_iter):
        new_pr = {node: (1 - d) / N for node in nodes}

        dangling_sum = sum(pr[node] for node in nodes if len(graph[node]) == 0)

        for node in nodes:
            if len(graph[node]) == 0:
                continue

            share = pr[node] / len(graph[node])

            for neighbor in graph[node]:
                new_pr[neighbor] += d * share

        for node in nodes:
            new_pr[node] += d * dangling_sum / N

        diff = sum(abs(new_pr[node] - pr[node]) for node in nodes)
        print(f"Iteration {i+1} | Δ = {diff:.8f}")

        pr = new_pr

        if diff < tol:
            print("\nConverged!")
            break

    return pr


def display(pr):
    ranked = sorted(pr.items(), key=lambda x: x[1], reverse=True)

    print("\nTop Ranked Pages:\n")
    for node, score in ranked[:10]:
        print(f"{node} -> {score:.6f}")

    return dict(ranked)


def plot(pr, k=10):
    ranked = list(pr.items())[:k]

    nodes = [str(x[0]) for x in ranked]
    scores = [x[1] for x in ranked]

    plt.figure()
    plt.bar(nodes, scores)
    plt.title("Advanced PageRank (Converged)")
    plt.xlabel("Node")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig("images/PageRank_Converged.png")
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