'''
    Name: Algorithms Project 2
    Description: Compression
'''

import queue
import os
import time
import codecs
import math
from collections import defaultdict


class HuffNode:
    def __init__(self, weight, value, left = None, right = None):
        self.value = value
        self.weight = weight
        self.left = left
        self.right = right
    def __lt__(self, other):
         return self.weight < other.weight
    def getLeftChild(self):
        return self.left
    def getRightChild(self):
        return self.right


def main():
    # Choosing File
    print("What file would you like to encode?")
    for f in os.listdir("testfiles/text"):
        print(f)
    while True:
        choice = input()
        try:
            file = codecs.open("testfiles/text/" + choice, 'r', 'utf-8')
            break
        except FileNotFoundError:
            print("Invalid filename, please try again: ")

    # Specify Encoding Filename
    encodeFile = input("\nPlease specify a filename for the encoded file: ")
    if not encodeFile.endswith(".txt"):
        encodeFile = encodeFile + ".txt"

    # Encode file
    encodeStart = time.time()
    huffTree, fileLength, compressLength = HuffmanEncode(file, encodeFile)
    encodeEnd = time.time()
    print("\nHuffman Compression algorithm took", encodeEnd - encodeStart, "milliseconds.")

    answer = input("Decode file? (Y/N): ")
    if answer == 'y' or answer == 'Y':
        decodedFile = input("What should the decoded file be called?: ")
        if not decodedFile.endswith(".txt"):
            decodedFile = decodedFile + ".txt"
        encodeStart = time.time()
        decompress(encodeFile, huffTree, decodedFile)
        encodeEnd = time.time()
        print("\nFile reconstruction took", encodeEnd - encodeStart, "milliseconds.")

    file.seek(0)
    freq = generateFrequencyTable(file)
    total = 0
    numchars = 0
    for char, value in freq.items():
        total += value
        numchars += 1
    fixedLengthAvg = math.ceil(total/numchars)

    print(fixedLengthAvg, fileLength, compressLength)

    print("Number of bits used:", compressLength)
    print("Number of bits required by Fixed Length encoding:", fixedLengthAvg*fileLength)
    print("Compression Ratio: " + str((((fixedLengthAvg*fileLength)-compressLength)/(fixedLengthAvg*fileLength))*100) + "%")



def HuffmanEncode(readFile, writeName):
    print("Generating Frequency Table...")
    freq = generateFrequencyTable(readFile)
    print("Creating Tree Structure...")
    tree = createTree(freq)
    print("Generating Huffman Codes...")
    codes = generateCodes(tree)

    #Write to file
    readFile.seek(0)
    print("\nWriting to file...")

    writeFile = codecs.open("testfiles/encoded/" + writeName, 'w', 'utf-8')
    filelength = 0
    compresslength  = 0
    for line in readFile:
        for char in line:
            writeFile.write(codes[char])
            filelength += 1
            compresslength += len(codes[char])
        writeFile.write('\n')
    writeFile.close()

    return tree, filelength, compresslength


def decompress(read, tree, write):
    writeFile = codecs.open("testfiles/decoded/" + write, 'w', 'utf-8')
    readFile = codecs.open("testfiles/encoded/" + read, 'r', 'utf-8')
    for line in readFile:
        decode(line, writeFile, tree, tree)
    writeFile.close()


def decode(line, writeFile, tree, nodePosition):
    while len(line) > 0:
        if nodePosition[1].value != None:
            writeFile.write(nodePosition[1].value)
            nodePosition = tree
        else:
            if line[0] == '0':
                nodePosition =  nodePosition[1].getLeftChild()
            else:
                nodePosition =  nodePosition[1].getRightChild()
            line = line[1:]


def createTree(frequencies):
    q = queue.PriorityQueue()
    for char, freq in frequencies.items():
        q.put((freq, HuffNode(freq, char)))
    while q.qsize() > 1:
        l, r = q.get(), q.get()
        node = HuffNode(l[0] + r[0], None, l, r)
        q.put((l[0] + r[0], node))
    return q.get()


def generateFrequencyTable(file):
    frequencies = defaultdict(int)
    for line in file:
        for char in line:
            frequencies[char] += 1
    return frequencies


def generateCodes(tree):
    codes = dict()
    walkTree(tree, codes)
    print(codes)
    return codes


def walkTree(node, dictionary, code=""):
    if node[1].value != None:
        dictionary[node[1].value] = code
    else:
        walkTree(node[1].getLeftChild(), dictionary, code + "0")
        walkTree(node[1].getRightChild(), dictionary, code + "1")


if __name__ == "__main__":
    main()