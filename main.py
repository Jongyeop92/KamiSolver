# -*- coding: utf8 -*-


import copy
import time


COLOR_LIST = ['0', '1', '2']


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
                                if dy * dx != 0:
                                    continue
                                
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

    def showKami(self):
        print '\n'.join(''.join(row) for row in self.kamiData)


def solveKami(kami, depth, changeInfoList=[]):

    if kami.isEnd():
        return [changeInfoList]
    elif depth == 0:
        return None

    resultList = []
    groupList = kami.getGroupList()

    if depth == 1:
        colorCount = 0
        colorList  = []

        for i in range(len(groupList)):
            if groupList[i][0] not in colorList:
                colorList.append(groupList[i][0])
                colorCount += 1

        if colorCount > 2:
            return None
        
    for idx in range(len(groupList)):
        for color in COLOR_LIST:
            if color == groupList[idx][0]:
                continue
            
            copyKami = copy.deepcopy(kami)
            copyKami.changeColor(idx, color)

            result = solveKami(copyKami, depth - 1, changeInfoList + [(idx, color)])

            if result != None:
                resultList += result

    return resultList


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


    kami4 = Kami(2, 2)
    kami4.setKamiData(["00",
                       "11"])

    assert [(0, '1')] in solveKami(kami4, 1)


    kami5 = Kami(2, 2)
    kami5.setKamiData(["00",
                       "12"])

    assert [(0, '1'), (0, '2')] in solveKami(kami5, 2)


    print "Success"


def main():

    kami = Kami(10, 16)

##    depth = 3
##    kami.setKamiData(["1122200022",
##                      "1122200022",
##                      "1122200022",
##                      "1122200000",
##                      "1222201100",
##                      "1001101100",
##                      "1001101100",
##                      "1001100000",
##                      "1221100000",
##                      "0021101122",
##                      "0021101122",
##                      "0021101122",
##                      "0112202211",
##                      "0112202211",
##                      "0112202211",
##                      "0000002211"])

    depth = 4
    kami.setKamiData(["0000000000",
                      "0220222220",
                      "0220200020",
                      "0000201020",
                      "0000200020",
                      "0000222220",
                      "0000000000",
                      "0000000000",
                      "0111111110",
                      "0100000010",
                      "0101111010",
                      "0101221010",
                      "0101111010",
                      "0100000010",
                      "0111111110",
                      "0000000000"])

    startTime = time.time()

    resultList = solveKami(kami, depth)

    timeGap = time.time() - startTime

    for result in resultList:
        print result

    print timeGap
                     


if __name__ == "__main__":
    #test()
    main()
