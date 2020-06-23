# syncview
## Overview
It's a work in progress: the rough basis of a blender AddOn, intended to provide an easy way to navigate a side-by-side stereoscopic setup.
The user can pan and zoom synchronously between two 3dViews. It turns blender into a basic photogrammetric workstation if one can provide:
- a couple of oriented and georeferenced cameras e.g. issued from a [MicMac](https://github.com/micmacIGN/micmac) reconstruction,
- and a set of georeferenced data handled with [Blender GIS](https://github.com/domlysz/BlenderGIS).

![](https://github.com/xyleme/syncview/blob/master/capture.jpg)

My own hardware setup involves a Wild ST4 stereoscope mounted ahead of a monitor. This is a dual purpose montage initially used to make photo-interpretation.

## Usage
Basically install the AddOn the usual way, then split the Default 3dView, assign a local camera to each 3dView. The 'Syncview settings' menu displays in the Tool shelf (Ctrl+T), allowing to set up left and right cameras. Via a modified keymap within both 3dViews:
- the synchronous panning is accessed by Shift+Alt+MMB;
- the synchronous zooming is accessed by Ctrl+Alt+MMB;
The 'Lock View Rotation' toggle prevents the user to bail out of Camera view.
In addition the 'Auto align view' button performs a (rough) relative automated alignment when you're lost...
