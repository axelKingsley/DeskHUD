import random
import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 0.5

if __name__ == '__main__':
    lights.initialize('/dev/ttyACM0')
    print ("CLIENT CONNECTED")

    palette = [
            (20, 50, 50),
            (0, 0, 50),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 50, 50),
            ]

    backdrop = [ (0, 0, 0), ] * 263


    def randomInsert():
        global backdrop
        sliceIndex = random.randint(0,253)
        sliceSize  = random.randint(0,10)
        backdrop = backdrop[:sliceIndex+1] + [random.choice(palette)]*sliceSize + backdrop[sliceIndex+sliceSize:]

    def randomDelete():
        global backdrop
        sliceIndex = random.randint(0,253)
        backdrop = backdrop[:sliceIndex] + [(0,0,0)]*sliceSize + backdrop[sliceIndex+sliceSize:]

    def smooth():
        global backdrop
        newBackdrop = []
        for i, pixel in enumerate(backdrop):
            before = backdrop[i-1]
            after  = backdrop[(i+1)%263]
            newBackdrop.append((
                    int((before[0] + pixel[0] + after[0])/3),
                    int((before[1] + pixel[1] + after[1])/3),
                    int((before[2] + pixel[2] + after[2])/3),
                    ))
        backdrop = newBackdrop

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
        randomInsert()

        smooth()

        backdrop = backdrop[:263]

        commandList = []
        commandList += lights.pixelListToCommandList(quantize(backdrop), 0)
        commandList += lights.pixelListToCommandList(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        time.sleep(0.15)
        #input("NEXT")
