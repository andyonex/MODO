# python
# Export deformation animation as obj sequence. 
# specially for bobby
# Author: Andy Budanov
# ```python

import lx
import os
import modo

scene = modo.Scene()

# init File Dialog
try:
	lx.eval("dialog.setup fileSave")
	lx.eval("dialog.title \"Map Save Location...\"")
	lx.eval("dialog.fileTypeCustom obj \"Obj\" \"*.obj\" obj")
	lx.eval('dialog.open')
	fullPath = lx.eval('dialog.result ?')
	(dirPath, filename) = os.path.split(fullPath)
	(shortFileName, extension) = os.path.splitext(filename) 
except RuntimeError:
	lx.eval('sys.exit()')

# store current obj export settings
objExportState = lx.eval("user.value sceneio.obj.export.atCurrentTime ?")

# set obj export settings to freeze deforms
lx.eval("user.value sceneio.obj.export.atCurrentTime 1")

# manage time frame
frate = lx.eval("time.fpsCustom ?")
timeStart = lx.eval("time.range current ?")
timeEnd = lx.eval("time.range current out:?")
frameStart = int(round(timeStart * frate, 0))
frameEnd = int(round(timeEnd * frate, 0))
lx.eval("select.time %s" % timeStart)
frame = frameStart

while frame <= frameEnd:

	# save result mesh to a file
	objPath = dirPath + "\\" + shortFileName + "_" + str(frame) + ".obj"
	lx.eval('!scene.saveAs "%s" wf_OBJ false' % (objPath))
	#lx.eval('!scene.saveSelected "%s"' % (objPath))
	
	# go to a next frame 
	timePos = lx.eval("select.time ?")
	lx.eval("select.time %s" % timePos)
	lx.eval('time.step frame next')
	
	frame += 1

# restire settings
lx.eval("user.value sceneio.obj.export.atCurrentTime %s" % (objExportState))
