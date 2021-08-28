import math
import serial
import time

def buildCommand(command, ints):
    resp = command + ' '.join([str(int(i)) for i in ints])
    print(resp)
    return resp

def putPixel(pixel, index):
    return buildCommand('d', [
        i + index,
        pixelList[i][0],
        pixelList[i][1],
        pixelList[i][2]
        ])


def putRange(pixelList, index):
    instructionString = ''
    for i in range(len(pixelList)):
        instructionString += buildCommand('d', [
            i + index,
            pixelList[i][0],
            pixelList[i][1],
            pixelList[i][2]
            ])
    return instructionString

def fill(color, index, length):
    return buildCommand('f', [
        index,
        length,
        color[0],
        color[1],
        color[2]
        ])

def render():
    return buildCommand('s', [])

def send(data):
    Serial.write(bytearray(data, encoding="utf8"))

if __name__ == '__main__':
    Serial = serial.Serial('/dev/ttyACM1')  # open serial port
    time.sleep(3)
    print('{} Connection Established'.format(Serial.name))

    animationFrame = 0
    animationFrames = 50
    focusDrawingBlue = [
        (200, 200, 200),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 200),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (200, 200, 200)
        ]
    focusDrawingRed = [
        (200, 200, 200),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (200, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (200, 200, 200)
        ]
    while True:
        sinOsc = math.sin(math.pi * 2 * (animationFrame/animationFrames))
        frame = ''
        frame += fill((0, 0, 0), 0, 300)
        frame += putRange(focusDrawingRed, 150+sinOsc*32)
        #frame += putRange(focusDrawingBlue, 200+sinOsc*10)
        frame += render()
        send(frame)

        animationFrame = (animationFrame +1) % animationFrames
        time.sleep(0.075)

    input('Waiting')
    Serial.close()             # close port
