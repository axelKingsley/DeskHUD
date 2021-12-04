import random
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

    palette = [
            (200, 200, 0),
            (0, 0, 0),
            (255, 255, 0),
            (220, 200, 10),
            (210, 100, 0),
            (160, 100, 0),
            (160, 100, 0),
            (20, 17, 0),
            (20, 5, 0),
            (20, 17, 5),
            (20, 17, 5),
            (20, 17, 5),
            ]

    def sconce():
        sconceSize = 7
        flameSize = random.randint(1, 3)
        leftSide = random.randint(0, sconceSize - flameSize)
        rightSide = sconceSize - leftSide
        return [(0,0,0)] * leftSide + [random.choice(palette)] * flameSize + [(0,0,0)] * rightSide

    #lights.send(['i'])

    redHaze = [(0,0,0)]*50 + [(255,0,0)]*213

    backdrop = [(0,0,0)]*263

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

    def pixelAverage(pixel1, pixel2, amnt1=0.5, amnt2=0.5):
        return (
                pixel1[0]*amnt1 + pixel2[0]*amnt2,
                pixel1[1]*amnt1 + pixel2[1]*amnt2,
                pixel1[2]*amnt1 + pixel2[2]*amnt2,
                )

    def applySconces(numberOfSconces, sconceStart = 50, sconceEnd = 263 - len(sconce())):
        global backdrop
        for i in range(numberOfSconces):
            offset = int((((sconceEnd - sconceStart)/(numberOfSconces-1)) * i) + sconceStart)
            for j, pixel in enumerate(sconce()):
                if offset + j < len(backdrop) and random.randint(0,3) == 0:
                    backdrop[offset + j] = pixelAverage(backdrop[offset + j], pixel, amnt1 = 0.75, amnt2 = 0.35)

    while True:
        sconceStart = 50
        # A sconce size is subtracted because we are spacing out their start indicies.
        sconceEnd = 263 - len(sconce())
        numberOfSconces = 7
        applySconces(7)


        backdropPostProcess = backdrop.copy()
        for i, pixel in enumerate(backdrop):
            backdropPostProcess[i] = pixelAverage(pixel, pixel, amnt1 = 1, amnt2 = 0.3)
            backdropPostProcess[i] = pixelAverage(backdropPostProcess[i], redHaze[i], amnt1 = 0.95, amnt2 = 0.015)

        backdropPostProcess = smooth(backdropPostProcess)


        commandList = []
        commandList.append(lights.setBackground((0, 0, 0)))
        commandList += lights.pixelListToCommandList(backdropPostProcess, 0)
        commandList += lights.pixelListToCommandList(volume.toPixels(), 0)

        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)

        animationFrame = (animationFrame +1) % animationFrames
        time.sleep(0.01)
        #input("NEXT")
