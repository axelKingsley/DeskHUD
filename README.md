# DeskHUD

# Purpose

I have a NeoPixel light strip attached to my desk. In theory, it would be cool to have the lighting at my desk serve notifications and information, on top of being visually appealing. To do that, I need a code pipeline that goes from my PC to the NeoPixel, by way of Arduino. Once that's well in place, I can write widgets that hook into the client on the PC, controlling the lights in some sophisticated way.

# Physical Layout

I have a semicircular desk with a backing wall resembling a cubicle. I have added a strip of NeoPixel lights to the top edge of the wall. In the future, I plan on adding a second strip (inward facing for illumination), as well as a strip behind me for ambient room lighting.

# Software Architecture

Like all personal projects, it's a mess. But the basic premise is:

* modules in the widget directory generate arrays of pixels to be displayed. Widgets don't need any knowledge of the hardware, and only need to be able to generate (r, g, b) tuples

* the client module is responsible for managing the serial device (though maybe it shouldn't), converting pixels to serial commands, sending serial commands. In addition, it has two optimization workflows (one during pixel->command conversion, and one on a commandList itself) to minimize the amount of serial data being sent. Color changes are minimized, adjacent draw commands are converted to fill commands, and more.

* run.py is responsible for importing the widgets, positioning them, and using the client to send that data to the device

* LightStripSerialServer is an Arduino project that receives serial commands and does the actual NeoPixel hardware interfacing.

# The Results So Far

Depending on the image being drawn, running the strip at 60fps is not unreasonable. Not all drawings are optimization friendly, but there's more work to be done with that later. The device can run animations well, and I have a volume indicator widget which auto-hides when the volume isn't being changed.

You can also reverse the indexing mode if you want to treat the end of the strip as i=0 like I do.
