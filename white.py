import math
import time
from client import lightStripClient as lights
from widgets import volume

volume.scale = 0.5

if __name__ == '__main__':
    lights.initialize('/dev/ttyACM0')
    print ("CLIENT CONNECTED")

    #lights.send(['i'])
    color = (255, 200, 100)
    while True:
        commandList = []
        commandList.append(lights.setBackground(color))
        commandList.append(lights.render())
        lights.compressCommandList(commandList)
        print(commandList)
        lights.send(commandList)
        input("NEXT")

        color = ((color[0] + 10)%256, (color[1] + 10)%256, (color[2] + 10)%256)
