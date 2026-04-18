class Position:
    def __init__(self, page, index):
        self.page = page
        self.index = index

    def getPageEntry(self):
        return self.page

    def getWordIndex(self):
        return self.index


class WordEntry:
    def __init__(self, word):
        self.word = word
        self.positions = []

    def addPosition(self, position):
        self.positions.append(position)

    def getAllPositionsForThisWord(self):
        return self.positions


class MySet:
    def __init__(self):
        self.data = set()

    def addElement(self, element):
        self.data.add(element)

    def union(self, other):
        return self.data.union(other.data)

    def intersection(self, other):
        return self.data.intersection(other.data)