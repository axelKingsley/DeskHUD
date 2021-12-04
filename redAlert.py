import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 0.5

if __name__ == '__main__':
    lights.initialize('/dev/ttyACM0')
    print ("CLIENT CONNECTED")

    animationFrame = 0
    animationFrames = 100

    spotlight = [
        (200, 200, 200),
        (200, 200, 200),
        (200, 200, 200),
        (200, 200, 200),
        (200, 200, 200),
        (200, 200, 200),
        ]

    #lights.send(['i'])
    while True:
        sinOsc = math.sin(math.pi * 2 * (animationFrame/animationFrames))
        commandList = []
        commandList.append(lights.setBackground((255, 0, 0)))
        commandList += lights.pixelListToCommandList(spotlight, 156 + sinOsc*106)
        commandList += lights.pixelListToCommandList(spotlight, 156 - sinOsc*106)
        commandList += lights.pixelListToCommandList(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        animationFrame = (animationFrame +1) % animationFrames
        time.sleep(0.015)
        #input("NEXT")
