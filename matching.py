import Route_searching_2D.explore as RS2_E
from multiprocessing import Pool
import sys
import os
import glob
import numpy as np

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(DIR_BASE, "data/")
HEAD_NAME = "city"
HEADER_NUM = 3

def readFile(path):
    header = []
    bigMap = []
    with open(path, "r") as f:
        for i, line in enumerate(f):
            if i < HEADER_NUM:
                header.append(line.strip())
                continue
            bigMap.append(np.array([float(x) for x in line.strip().split(" ")]))
    return header, bigMap

def getData():
    data = {}
    files = glob.glob(os.path.join(DIR_DATA , "*"))
    files = sorted(files)
    dirnames = [os.path.basename(file).replace(HEAD_NAME, "") for file in files]
    dirnames = sorted(dirnames)
    
    oldName = "-"
    # human, count
    for f, dirname in zip(files, dirnames):
        if oldName != dirname[:-1]:
            data[dirname[:-1]] = {dirname[-1]:{}}
        else:
            data[dirname[:-1]][dirname[-1]] = {}
        
        wordFiles = glob.glob(os.path.join(f, "*")) 
        # word
        for wfile in wordFiles:
            header, valueMap = readFile(wfile)
            data[dirname[:-1]][dirname[-1]][header[1]] = valueMap
        
        oldName = dirname[:-1]
    
    return data

def calcE_Distance(array1, array2):
    edMap = []
    for i, line1 in enumerate(array1):
        edMap.append([])
        for line2 in array2:
            edLine = np.linalg.norm(line1 - line2)
            edMap[i].append(edLine)
    return edMap

def wrapper(args):
    return calcExpected(*args)

def calcExpected(map1, map2, targetKey):
    edMap = calcE_Distance(map1, map2[targetKey])
    y = len(edMap) -1
    x = len(edMap[0]) -1
    routeValue = RS2_E.calcrouteValue(edMap)
    _, minNumber = RS2_E.checkParentRoute(routeValue, y, x)
    return [targetKey, minNumber]

def multiProcess(args):
    p = Pool(8)
    output = p.map(wrapper, args)
    p.close()
    return output


def calcSameTarget(data):
    humans = list(data.keys())
    
    print("Choose a human.")
    for i, human in enumerate(humans):
        print("[{0}] {1}".format(i, human))
    
    try:
        num = int(input(">> ").strip())
    except:
        print("Invalid input!")
        return ""
    
    numbers = list(data[humans[num]].keys())
    print("Choose a number in [].")
    for i, number in enumerate(numbers):
        print("[{0}] {1}".format(i, number))
    try:
        num1 = int(input("base>> ").strip())
        num2 = int(input("target>> ").strip())
    except:
        print("Invalid input!")
        return ""
    
    for baseKey in data[humans[num]][numbers[num1]].keys():
        values = []
        args = [[data[humans[num]][numbers[num1]][baseKey],
                data[humans[num]][numbers[num2]],
                key
                ]
                for key in data[humans[num]][numbers[num2]].keys()
                ]
        output = multiProcess(args)
        expected = sorted(output, key=lambda x:x[1])[0][0]
        print("Expected: {0}, Answer: {1}, {2}".format(expected, baseKey, expected==baseKey))
         
def calcDifferentTarget(data):
    return


def main():
    data = getData()
    calcSameTarget(data) 

if __name__=="__main__":
    main()
