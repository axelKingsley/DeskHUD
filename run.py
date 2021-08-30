import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 3

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
        commandList.append(lights.setBackground((30,0,30)))
        commandList += lights.pixelListToRange(focusDrawingRed, 150+sinOsc*32)
        commandList += lights.pixelListToRange(focusDrawingBlue, 200+sinOsc*62)
        commandList += lights.pixelListToRange(focusDrawingOrangeTunnel, 150)
        commandList += lights.pixelListToRange(focusDrawingOrangeTunnel, 250)
        commandList += lights.pixelListToRange(focusDrawingOrangeTunnel, 80)
        commandList += lights.pixelListToRange(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        animationFrame = (animationFrame +1) % animationFrames
        time.sleep(0.015)
        #input("NEXT")
