# python
# Rename one by one
# Author: Andy Budanov
# Use to rename multiple objects. 
# It will turn off visibility for not selected and set the viewport on currently renaming object
# Usage: select multiple objects and run @renameOneByOne.py 
# ```python

import lx
import modo
scene = modo.Scene()

# store init state
isIsolated = lx.eval("view3d.inactiveInvisible ?")

lx.eval("view3d.inactiveInvisible true")

# get selected items
selectedMeshes = scene.selected

for meshItem in selectedMeshes:
	scene.select(meshItem)
	lx.eval("viewport.fitSelected")
	try:
		lx.eval("layer.renameSelected")
	except:
		break

lx.eval("view3d.inactiveInvisible %s" %isIsolated)
