from pyspark import SparkContext
import os
import matplotlib.pyplot as plt


def parse_line(line):
    parts = line.strip().split()
    if len(parts) != 2:
        return None
    return parts[0], parts[1]


def plot(pr_dict, k=10):
    ranked = sorted(pr_dict.items(), key=lambda x: x[1], reverse=True)[:k]

    nodes = [str(x[0]) for x in ranked]
    scores = [x[1] for x in ranked]

    plt.figure()
    plt.bar(nodes, scores)
    plt.title("Spark PageRank")
    plt.xlabel("Node")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.show()


def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, "data", "Q3", "whole.txt")

    print("Loading graph from:", file_path)

    sc = SparkContext("local", "PageRank")

    lines = sc.textFile(file_path)
    parsed = lines.map(parse_line).filter(lambda x: x is not None)

    links = parsed.groupByKey().mapValues(list).cache()
    ranks = links.mapValues(lambda _: 1.0)

    print("\nRunning Spark PageRank...\n")

    for i in range(10):
        contribs = links.join(ranks).flatMap(
            lambda x: [(dest, x[1][1] / len(x[1][0])) for dest in x[1][0]]
        )

        ranks = contribs.reduceByKey(lambda x, y: x + y) \
                        .mapValues(lambda r: 0.15 + 0.85 * r)

        print(f"Iteration {i+1} done")

    result = ranks.collect()
    result_sorted = sorted(result, key=lambda x: x[1], reverse=True)

    print("\nTop Ranked Pages (Spark):\n")
    for node, score in result_sorted[:10]:
        print(f"{node} -> {score:.6f}")

    plot(dict(result_sorted))

    sc.stop()


if __name__ == "__main__":
    main()