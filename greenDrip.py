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

    redHaze = [(0,0,0)]*50 + [(100,255,100)]*213

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

    def pixelAverage(pixel1, pixel2, amnt1=0.5, amnt2=0.5):
        return (
                pixel1[0]*amnt1 + pixel2[0]*amnt2,
                pixel1[1]*amnt1 + pixel2[1]*amnt2,
                pixel1[2]*amnt1 + pixel2[2]*amnt2,
                )

    while True:
        randomInsert()
        pushInsert()
        backdropPostProcess = backdrop.copy()
        for i, pixel in enumerate(backdrop):
            backdropPostProcess[i] = pixelAverage(pixel, pixel, amnt1 = 1, amnt2 = 0.3)
            backdropPostProcess[i] = pixelAverage(backdropPostProcess[i], redHaze[i], amnt1 = 0.95, amnt2 = 0.015)

        backdropPostProcess = smooth(backdropPostProcess)

        commandList = []
        commandList += lights.pixelListToCommandList(backdropPostProcess, 0)
        commandList += lights.pixelListToCommandList(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        time.sleep(0.015)
        #input("NEXT")
