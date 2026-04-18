from engine import SearchEngine
import os


def process_actions(engine, actions_file):
    print("\nProcessing actions.txt...\n")

    if not os.path.exists(actions_file):
        print("actions.txt not found!")
        return

    with open(actions_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # skip empty lines
        if not line:
            continue

        print(f">>> {line}")

        parts = line.strip().split()

        command = parts[0]

        try:
            # ---------------- ADD PAGE ----------------
            if command == "addPage":
                if len(parts) < 2:
                    print("Invalid addPage command")
                    continue

                page_name = parts[1].strip()
                page_file = page_name + ".txt"

                full_path = os.path.join(os.path.dirname(actions_file), page_file)

                if not os.path.exists(full_path):
                    print(f"File not found: {full_path}")
                    continue

                engine.addPage(full_path)

            # ---------------- BASIC QUERY ----------------
            elif command == "queryFindPagesWhichContainWord":
                if len(parts) < 2:
                    print("Invalid query")
                    continue

                engine.queryFindPagesWhichContainWord(parts[1].strip())

            # ---------------- POSITION QUERY ----------------
            elif command == "queryFindPositionsOfWordInAPage":
                if len(parts) < 3:
                    print("Invalid position query")
                    continue

                word = parts[1].strip()
                page = parts[2].strip()

                engine.queryFindPositionsOfWordInAPage(word, page)

            # ---------------- TF-IDF RANKING ----------------
            elif command == "queryFindPagesWhichContainWordRanked":
                if len(parts) < 2:
                    print("Invalid ranking query")
                    continue

                engine.queryFindPagesWhichContainWordRanked(parts[1].strip())

            else:
                print(f"Unknown command: {command}")

        except Exception as e:
            print(f"Error processing command: {line}")
            print("Reason:", e)

        print()


def main():
    engine = SearchEngine()

    # robust path handling
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    folder = os.path.join(base_dir, "data", "Q2", "webpages")

    print("Resolved folder path:", folder)

    if not os.path.exists(folder):
        print("ERROR: Folder does not exist!")
        return

    files = os.listdir(folder)
    print("Files found:", files)

    print("\nLoading pages...\n")

    loaded_count = 0

    for file in files:
        # skip unwanted files
        if not file.endswith(".txt"):
            continue

        if file in ["actions.txt", "answers.txt"]:
            continue

        path = os.path.join(folder, file)

        try:
            engine.addPage(path)
            print("Added:", file)
            loaded_count += 1
        except Exception as e:
            print(f"Failed to load {file}: {e}")

    print(f"\nTotal pages loaded: {loaded_count}")

    # ---------------- BASIC TEST QUERIES ----------------
    print("\nQuery Results:\n")

    engine.queryFindPagesWhichContainWord("data")
    engine.queryFindPagesWhichContainWord("structure")
    engine.queryFindPagesWhichContainWord("engineer")

    # ---------------- ACTIONS FILE ----------------
    actions_path = os.path.join(folder, "actions.txt")
    process_actions(engine, actions_path)


if __name__ == "__main__":
    main()