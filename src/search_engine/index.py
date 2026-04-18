from preprocessing import preprocess_text
from structures import Position, WordEntry


class PageIndex:
    def __init__(self):
        self.word_entries = {}

    def addPositionForWord(self, word, position):
        if word not in self.word_entries:
            self.word_entries[word] = WordEntry(word)

        self.word_entries[word].addPosition(position)

    def getWordEntries(self):
        return self.word_entries


class PageEntry:
    def __init__(self, pageName):
        self.pageName = pageName
        self.pageIndex = PageIndex()

        with open(pageName, 'r', encoding="utf-8") as f:
            text = f.read()

        words = preprocess_text(text)

        for word, idx in words:
            pos = Position(self, idx)
            self.pageIndex.addPositionForWord(word, pos)

    def getPageIndex(self):
        return self.pageIndex