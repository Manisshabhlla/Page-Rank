from index import PageEntry
import math


class MyHashTable:
    def __init__(self):
        self.table = {}

    def addPositionsForWord(self, word, positions):
        if word not in self.table:
            self.table[word] = set()
        self.table[word].update(positions)

    def get(self, word):
        return self.table.get(word, set())


class InvertedPageIndex:
    def __init__(self):
        self.hashTable = MyHashTable()

    def addPage(self, page):
        word_entries = page.getPageIndex().getWordEntries()

        for word, entry in word_entries.items():
            self.hashTable.addPositionsForWord(
                word, entry.getAllPositionsForThisWord()
            )

    def getPagesWhichContainWord(self, word):
        positions = self.hashTable.get(word)
        return set(pos.getPageEntry().pageName for pos in positions)


class SearchEngine:
    def __init__(self):
        self.index = InvertedPageIndex()

    def addPage(self, pageName):
        page = PageEntry(pageName)
        self.index.addPage(page)

    def normalize(self, word):
        word = word.lower()
        if len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        return word

    def queryFindPagesWhichContainWord(self, word):
        word = self.normalize(word)
        pages = self.index.getPagesWhichContainWord(word)

        if not pages:
            print(f"No webpage contains word {word}")
        else:
            print(", ".join(sorted(pages)))

    def queryFindPositionsOfWordInAPage(self, word, pageName):
        word = self.normalize(word)
        positions = self.index.hashTable.get(word)

        result = []
        for pos in positions:
            if pos.getPageEntry().pageName.endswith(pageName):
                result.append(pos.getWordIndex())

        if not result:
            print(f"Webpage {pageName} does not contain word {word}")
        else:
            result.sort()
            print(f"{pageName}:", ", ".join(map(str, result)))

    # TF-IDF
    def compute_tf(self, word, page):
        word_entries = page.getPageIndex().getWordEntries()
        if word not in word_entries:
            return 0
        return len(word_entries[word].getAllPositionsForThisWord())

    def compute_idf(self, word):
        total_docs = len(self.index.hashTable.table)
        docs_with_word = len(self.index.getPagesWhichContainWord(word))

        if docs_with_word == 0:
            return 0

        return math.log(total_docs / docs_with_word)

    def queryFindPagesWhichContainWordRanked(self, word):
        word = self.normalize(word)

        positions = self.index.hashTable.get(word)
        if not positions:
            print(f"No webpage contains word {word}")
            return

        page_scores = {}

        for pos in positions:
            page = pos.getPageEntry()
            tf = self.compute_tf(word, page)
            idf = self.compute_idf(word)

            score = tf * idf

            if page.pageName not in page_scores:
                page_scores[page.pageName] = 0

            page_scores[page.pageName] += score

        ranked = sorted(page_scores.items(), key=lambda x: x[1], reverse=True)

        print("Ranked Results:")
        for page, score in ranked:
            print(f"{page} -> {score:.4f}")