import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 1

if __name__ == '__main__':
    animationFrame = 0
    animationFrames = 100
    pixelPattern = [
            (20, 0, 20)
            ]
    pixelPattern = pixelPattern * 300
    #lights.send(['i'])
    while True:
        sinOsc = math.sin(math.pi * 2 * (animationFrame/animationFrames))
        commandList = []
        commandList.append(lights.setBackground((30,0,30)))
        commandList += lights.pixelListToRange(pixelPattern, 0)
        commandList += lights.pixelListToRange(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        animationFrame = (animationFrame +1) % animationFrames
        time.sleep(0.015)
        #input("NEXT")
