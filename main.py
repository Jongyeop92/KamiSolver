# -*- coding: utf8 -*-


class Kami:

    def __init__(self, width, height):
        self.width  = width
        self.height = height

        self.kamiData  = []
        self.groupList = []

    def setKamiData(self, kamiData):
        for row in kamiData:
            kamiRow = []
            for c in row:
                kamiRow.append(c)

            self.kamiData.append(kamiRow)

        self.setGroupList()

    def getKamiData(self):
        return self.kamiData

    def setGroupList(self):
        self.groupList      = []
        visitedPositionList = []

        for y in range(self.height):
            for x in range(self.width):
                nowColor = self.kamiData[y][x]
                checkPositionList = [(y, x)]
                sameAreaPositionList = []

                while checkPositionList:
                    nowY, nowX = checkPositionList.pop()

                    if (nowY, nowX) in visitedPositionList:
                        continue
                    else:
                        visitedPositionList.append((nowY, nowX))

                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                newY, newX = nowY + dy, nowX + dx

                                if self.isInKami(newY, newX) and self.kamiData[newY][newX] == nowColor and (newY, newX) not in sameAreaPositionList:
                                    sameAreaPositionList.append((newY, newX))
                                    checkPositionList.append((newY, newX))

                if sameAreaPositionList != []:
                    self.groupList.append((nowColor, sameAreaPositionList))

    def getGroupList(self):
        return self.groupList

    def isInKami(self, y, x):
        return 0 <= y and y < self.height and 0 <= x and x < self.width

    def isEnd(self):
        color = self.kamiData[0][0]

        for y in range(self.height):
            for x in range(self.width):
                if self.kamiData[y][x] != color:
                    return False
                
        return True

    def changeColor(self, groupIdx, newColor):
        changeGroup = self.groupList[groupIdx]

        for y, x in changeGroup[1]:
            self.kamiData[y][x] = newColor

        self.setGroupList()


def test():

    kami = Kami(2, 2)
    kami.setKamiData(["00",
                      "11"])

    assert kami.getKamiData() == [['0', '0'],
                                  ['1', '1']]
    assert kami.getGroupList() == [('0', [(0, 0), (0, 1)]),
                                   ('1', [(1, 0), (1, 1)])]
    assert kami.isEnd() == False
    
    kami.changeColor(0, '1')

    assert kami.getKamiData() == [['1', '1'],
                                  ['1', '1']]
    assert kami.getGroupList() == [('1', [(0, 0), (0, 1), (1, 0), (1, 1)])]
    assert kami.isEnd() == True


    kami2 = Kami(2, 2)
    kami2.setKamiData(["00",
                       "12"])

    assert kami2.getKamiData() == [['0', '0'],
                                   ['1', '2']]
    assert kami2.getGroupList() == [('0', [(0, 0), (0, 1)]),
                                    ('1', [(1, 0)]),
                                    ('2', [(1, 1)])]
    assert kami2.isEnd() == False

    kami2.changeColor(1, '0')
    kami2.changeColor(1, '0')

    assert kami2.isEnd() == True


    kami3 = Kami(2, 2)
    kami3.setKamiData(["00",
                       "00"])

    assert kami3.getKamiData() == [['0', '0'],
                                   ['0', '0']]
    assert kami3.getGroupList() == [('0', [(0, 0), (0, 1), (1, 0), (1, 1)])]
    assert kami3.isEnd() == True


    print "Success"


def main():

    pass


if __name__ == "__main__":
    test()
    #main()
