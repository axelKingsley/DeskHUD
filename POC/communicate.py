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

# A simple compression that removes redundant colors from serial command lists
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

# Turns a list of pixels into an optimized command set
def pixelListToRange(pixelList, offset):
    colorMap = {}
    # Reorganize the pixel list, grouping by color
    for index, color in enumerate(pixelList):
        if color in colorMap.keys():
            colorMap[color][0].append(index + offset)
        else:
            colorMap[color] = ([],[])
    # Next search for sequential indexes to turn into a fill
    for color in colorMap.keys():
        colorMap[color][0].sort()
        # Not yet, my brain's not working. please do this later, Axel.

    # Finally render them to a list of commands
    commandList = []
    for color in colorMap.keys():
        commandList.append(setColor(color))
        commandList += [draw(i) for i in colorMap[color][0]]
    return commandList

Serial = serial.Serial('/dev/ttyACM1', baudrate=115200)  # open serial port
time.sleep(3)
print('{} Connection Established'.format(Serial.name))
if __name__ == '__main__':
    animationFrame = 0
    animationFrames = 100
    focusDrawingBlue = [
        (0, 200, 0),
        (0, 200, 0),
        (0, 200, 0),
        (0, 200, 0),
        (0, 200, 0),
        (0, 200, 0),
        (0, 200, 0)
        ]
    focusDrawingRed = [
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (200, 200, 200),
        (200, 200, 200),
        (200, 200, 200),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        ]
    focusDrawingOrangeTunnel = [
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        (200, 100, 0),
        ]
    while True:
        sinOsc = math.sin(math.pi * 2 * (animationFrame/animationFrames))
        commandList = []
        commandList.append(setBackground((30,0,30)))
        commandList += pixelListToRange(focusDrawingRed, 150+sinOsc*32)
        commandList += pixelListToRange(focusDrawingBlue, 200+sinOsc*62)
        commandList += pixelListToRange(focusDrawingOrangeTunnel, 150)
        commandList += pixelListToRange(focusDrawingOrangeTunnel, 250)
        commandList += pixelListToRange(focusDrawingOrangeTunnel, 80)
        commandList.append(render())
        compressCommandList(commandList)
        print(commandList)
        send(commandList)

        animationFrame = (animationFrame +1) % animationFrames
        time.sleep(0.015)
        #input("NEXT")

    input('Waiting')
    Serial.close()             # close port
