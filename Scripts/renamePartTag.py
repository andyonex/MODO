#python
# Use to replace polygon tag 'part' with the name of an object
# Author: Andy Budanov
# ```python
import modo
import lx

scene = modo.Scene()

selectedMeshes = scene.selected

for meshItem in selectedMeshes:
	scene.select(meshItem)
	lx.eval("select.polygon add 0 face")
	lx.eval('poly.setPart "%s"' %meshItem.name)	

