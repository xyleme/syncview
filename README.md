# syncview
## Overview
It's a work in progress: the rough basis of a blender AddOn, intended to provide an easy way to navigate a side-by-side stereoscopic setup.
The user can pan and zoom synchronously between two 3dViews.
I basically use it as an alternative to [blender's internal stereoscopic mode](https://docs.blender.org/manual/en/latest/render/output/properties/stereoscopy), essentially because I use a side-by-side custom device and the blender's side-by-side mode results in an uncomfortable tapered display...
This plugin turns blender into a basic photogrammetric workstation if one can provide:
- a couple of oriented and georeferenced cameras e.g. issued from a [MicMac](https://github.com/micmacIGN/micmac) reconstruction,
- and a set of georeferenced data handled with [Blender GIS](https://github.com/domlysz/BlenderGIS).

![](https://github.com/xyleme/syncview/blob/master/capture_v2.jpg)

My own hardware setup involves a Wild ST4 stereoscope mounted ahead of a monitor. This is a dual purpose montage initially used to make photo-interpretation.
![](https://github.com/xyleme/syncview/blob/master/syncview_st4_l.jpg)


## Usage
Basically install the AddOn the usual way, then split the Default 3dView, assign a local camera to each 3dView (the user is supposed to be aware of stereoscopic requirements for the camera pair setup). The 'Syncview settings' menu displays as a sidebar panel within 3dView region (Ctrl+N), allowing to set up left and right cameras. Via a modified keymap within both 3dViews:
- the synchronous panning is accessed by **Shift+Alt+MMB**;
- the synchronous zooming is accessed by **Ctrl+Alt+MMB**;
The latter is x-y responsive:
- y-direction stands for zooming factor;
- x-direction stands for the gap distance between views, providing an intuitive way to manage this tricky aspect of stereoscopic effect *e.g.* on deep scenes.

<p align="center">
  <img width="260" height="246" src="https://github.com/xyleme/syncview/blob/master/capture_panel.jpg">
</p>

- The *Pan ratio* slider allows to adjust the panning factor, especially when the camera view is highly magnified.
- The *Lock View Rotation* toggle prevents the user from bailing out of Camera view.
- In addition the *Auto align view* button performs a (rough) relative automated alignment when you're lost...


Enjoy ;-)
