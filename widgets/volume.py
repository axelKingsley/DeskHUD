import subprocess

scale = 1

volumesRemembered = 20

previousVolumes = []

def toPixels():
    global previousVolumes
    global volumesRemembered
    global scale
    volumeInfoText = subprocess.run(['amixer', 'get', 'Master'], stdout=subprocess.PIPE).stdout
    # Hacky method to pull the text based on the output observed
    volumeLevel = int(volumeInfoText.split(b'%')[0].split(b'[')[1])

    # Calculating and opacity based on how often we've seen this volume level recently
    if len(previousVolumes) > volumesRemembered:
        previousVolumes = previousVolumes[1:] + [volumeLevel]
    else:
        previousVolumes.append(volumeLevel)

    opacity = (volumesRemembered - previousVolumes.count(volumeLevel))/(volumesRemembered + 0.0)
    if opacity < 0.1: return []

    widgetSize = int(100 * scale)
    widgetLevel = int(volumeLevel * scale)
    onValue = int(200*opacity)
    pixelList = []
    pixelList += [ (onValue, onValue, onValue) ] * min(widgetLevel, widgetSize - 1)
    pixelList += [ (onValue, 0, 0) ]
    pixelList += [ (0, 0, 0) ] * (max((widgetSize -  widgetLevel), 1) - 1)
    return pixelList
