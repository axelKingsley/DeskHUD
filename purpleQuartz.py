import random
import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 0.5

if __name__ == '__main__':
    lights.initialize('/dev/ttyACM0')
    print ("CLIENT CONNECTED")

    palette = [(50, 0, 50),
                (20,0,50),
                (50,0,20),
                (0,0,0),
                (0,0,0),
                (100,100,100),
                (50,20,50)]

    halfdrop = [ (0, 0, 0), ] * 132

    backdrop = [ (0, 0, 0), ] * 263

    currentColor = palette[0]

    def randomAppend():
        global halfdrop
        global currentColor
        if random.randint(0,25) == 0:
            currentColor = random.choice(palette)

        halfdrop = halfdrop[1:] + [currentColor]

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

    def quantize(size=5):
        global backdrop
        newBackdrop = []
        for i, pixel in enumerate(backdrop):
            newBackdrop.append((
                    int(pixel[0]/5)*5,
                    int(pixel[1]/5)*5,
                    int(pixel[2]/5)*5
                    ))
        return newBackdrop

    while True:
        randomAppend()

        flippedHalf = halfdrop.copy()
        flippedHalf.reverse()
        backdrop = halfdrop + flippedHalf
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)
        backdrop = smooth(backdrop)

        commandList = []
        commandList += lights.pixelListToCommandList(quantize(backdrop), 0)
        commandList += lights.pixelListToCommandList(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        time.sleep(0.015)
        #input("NEXT")
