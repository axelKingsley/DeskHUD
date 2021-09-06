import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 1

if __name__ == '__main__':
    lights.initialize('/dev/ttyACM0')
    print ("CLIENT CONNECTED")

    animationFrame = 0
    animationFrames = 100
    pixelPattern = [
            (44,44,44),
            (0,0,0)
            ]
    pixelPattern = pixelPattern * 140

    spotlight = [
            (100,0,0),
            (100,100,0),
            (0,100,0),
            (0,100,100),
            (0,0,100),
            (100,0,100),
            ]
    #lights.send(['i'])
    while True:
        sinOsc = math.sin(math.pi * 2 * (animationFrame/animationFrames))
        commandList = []
       # commandList.append(lights.setBackground((100, 100, 100)))
        commandList += lights.pixelListToCommandList(pixelPattern, 0)
        commandList += lights.pixelListToCommandList(spotlight, 150 + sinOsc*100)
        commandList += lights.pixelListToCommandList(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        animationFrame = (animationFrame +1) % animationFrames
        time.sleep(0.015)
        #input("NEXT")
