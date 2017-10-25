# python
# Export animated objects as obj sequence
# Usage: Select items you want to export, start the script with @exportAsObjSeq.py
# specially for Bobby
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

# store current scene
oldscene = lx.eval('query sceneservice scene.index ? current')

# manage time frame
frate = lx.eval("time.fpsCustom ?")
timeStart = lx.eval("time.range current ?")
timeEnd = lx.eval("time.range current out:?")
frameStart = int(round(timeStart * frate, 0))
frameEnd = int(round(timeEnd * frate, 0))
lx.eval("select.time %s" % timeStart)
frame = frameStart

# get selected items
selectedMeshes = scene.selected

while frame <= frameEnd:

	tempMesh = scene.addItem(modo.c.MESH_TYPE)

	for meshItem in selectedMeshes:
		scene.select(meshItem)
		lx.eval("select.polygon add 0 face")
		lx.eval("select.copy")
		scene.select(tempMesh)
		lx.eval("select.paste")
	
	# create new scene
	lx.eval('scene.new')
	newscene = lx.eval('query sceneservice scene.index ? current')

	# go back to old scene and throw item over to a new scene
	lx.eval('scene.set %s' %oldscene)

	# select prev selected meshes
	scene.select(tempMesh)

	lx.eval("poly.freeze twoPoints false 2 true true true true 5.0 false Morph")

	# export selected to a new scene
	lx.eval('layer.import %s {} move:false position:0' %newscene)
	
	# save result mesh to a file
	objPath = dirPath + "\\" + shortFileName + "_" + str(frame) + ".obj"
	lx.eval('!scene.saveAs "%s" wf_OBJ false' % (objPath))
	
	lx.eval('!scene.close')
	lx.eval('scene.set %s' %oldscene)
	
	# go to a next frame 
	timePos = lx.eval("select.time ?")
	lx.eval("select.time %s" % timePos)
	lx.eval('time.step frame next')
	
	scene.removeItems(tempMesh)
	
	frame += 1
