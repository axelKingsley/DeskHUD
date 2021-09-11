import random
import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 0.5

if __name__ == '__main__':
    lights.initialize('/dev/ttyACM0')
    print ("CLIENT CONNECTED")

    palette = [(0, 50, 0),
                (20,50,0),
                (0,0,0),
                (0,0,0),
                (0,0,0),
                (0,0,0),
                (0,0,0),
                (0,0,0),
                (0,0,0),
                (0,0,0),
                (0,0,0),
                (0,50,20)]

    backdrop = [ (0, 0, 0), ] * 263


    def randomInsert():
        global backdrop
        sliceIndex = random.randint(0,263)
        backdrop = backdrop[:sliceIndex] + [random.choice(palette)] + backdrop[sliceIndex:]
        backdrop = backdrop[-263:]

    def smooth(backdrop):
        newBackdrop = []
        for i, pixel in enumerate(backdrop):
            before = backdrop[i-1]
            after  = backdrop[(i+1)%263]
            newBackdrop.append((
                    int((before[0] + pixel[0] + after[0])/3),
                    int((before[1] + pixel[1] + after[1])/3),
                    int((before[2] + pixel[2] + after[2])/3),
                    ))
        return newBackdrop

    def pushInsert():
        global backdrop
        backdrop = backdrop[1:] + [random.choice(palette)]

    while True:
        randomInsert()
        pushInsert()

        commandList = []
        commandList += lights.pixelListToCommandList(smooth(backdrop), 0)
        commandList += lights.pixelListToCommandList(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        time.sleep(0.015)
        #input("NEXT")
