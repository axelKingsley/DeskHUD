import itertools
import math
import serial
import time

def buildCommand(chars, ints):
    return ''.join(chars) + ' '.join([str(int(i)) for i in ints])

serializePixel = lambda i: '{0:0{1}x}'.format(i, 2)
def setColor(pixel):
    return buildCommand([
        'c',
        serializePixel(pixel[0]),
        serializePixel(pixel[1]),
        serializePixel(pixel[2])],
        [])

def setBackground(color):
    return buildCommand([
        'b',
        serializePixel(color[0]),
        serializePixel(color[1]),
        serializePixel(color[2])],
        [])

def draw(index):
    return buildCommand('d', [
        index,
        ])

def fill(index, length):
    return buildCommand('f', [
        index,
        length
        ])

def render():
    return buildCommand('s', [])

def send(commandList):
    Serial.write(bytearray("".join(commandList), encoding="utf8"))

def compressCommandList(commandList):
    # Compress Draw Commands by deleting draws which will be overwritten
    commandList = [command for index, command
            in enumerate(commandList[:-1])
            if command[0] == 'd'
            and command in commandList[index+1:]]
    # Compress Draw Commands by deleting color settings which will be overwritten
    commandList = [command for index, command
            in enumerate(commandList[:-1])
            if command[0] == 'c'
            and commandList[index + 1][0] == 'c']
    # Here be dragons, and a really good moment to reflect on the opportunity cost
    # of not refactoring recently. Identify all color commands, check if the next
    # color matches the previous, and delete the "next" of the two if so.
    # leave the command in place to not disturb the indexes as we iterate, I was
    # burned by poor understanding of that recently
    colorCommandIndexes = [index for index, command in enumerate(commandList)]
    for index, colorCommandIndex in enumerate(colorCommandIndexes[1:]):
        if commandList[colorCommandIndexes[index - 1]] == commandList[colorCommandIndex[index]]:
            commandList[index] = 'REMOVE'
    commandList = [command for command in commandList if not command == 'REMOVE']



# Turns a list of pixels into an optimized command set
def pixelListToCommandList(pixelList, offset):
    colorMap = {}
    # Reorganize the pixel list, grouping by color
    # each Color Keys to a List of Lists so you can group sequential sets
    # for optimizations
    lastUsedColor = (-1, -1, -1)
    for index, color in enumerate(pixelList):
        absIndex = index + offset
        if color in colorMap.keys():
            if lastUsedColor == color:
                colorMap[color][-1].append(absIndex)
            else:
                colorMap[color].append([absIndex])
        else:
            colorMap[color] = [[absIndex]]
        lastUsedColor = color

    # Finally render them to a list of commands
    commandList = []
    for color in colorMap.keys():
        commandList.append(setColor(color))
        commandList += [fill(i[0], len(i)) for i in colorMap[color] if len(i) > 1]
        commandList += [draw(i[0]) for i in colorMap[color] if len(i) == 1]
    return commandList

def initialize(devicePath='/dev/ttyACM0'):
    global Serial
    Serial = serial.Serial(devicePath, baudrate=230400)  # open serial port
    time.sleep(3)

if __name__ == '__main__':
    pass
