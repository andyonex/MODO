# python
# FREEZE AND EXPORT SELECTED OBJECTS
# BY: Andy Budanov
#
# Freeze selected objects and export with FBX preset settings or OBJ
# In case vertex normals get weird after freeze, 
# try different script arguments:    
# "@freezeAndExport.py"        -freeze and export as FBX
# "@freezeAndExport.py -u"     -update nromals and export as FBX
# "@freezeAndExport.py -t"     -apply 'vertMap.toggleNormalMaps auto'
# "@freezeAndExport.py -s"     -apply 'vertMap.softenNormals connected:true'
# "@freezeAndExport.py -s -o"  -smooth normals and export as OBJ
# "@freezeAndExport.py -c"	   -convert all instances to a regular objects
# ```python

import lx
import modo

scene = modo.Scene()
arg = lx.arg()

lx.eval('select.type item')
selectedMeshes = scene.selected

oldscene = lx.eval('query sceneservice scene.index ? current')

# sotore fbx game export settings
oldexportpreset = lx.eval('game.sceneSettings projectPreset:?')
oldexportpath = lx.eval('game.sceneSettings exportPath:?')
oldexportfbxsettings = lx.eval('game.sceneSettings fbxPreset:?')

# create new scene
lx.eval('scene.new')
newscene = lx.eval('query sceneservice scene.index ? current')

# go back to old scene and throw item over to a new scene
lx.eval('scene.set %s' %oldscene)

# select prev selected meshes
scene.select(selectedMeshes)

# export selected to a new scene
lx.eval('layer.import %s {} move:false position:0' %newscene) 

#
# export
#

# restore export settings
lx.eval('game.sceneSettings projectPreset:%s' %oldexportpreset)

if oldexportpath:
	lx.eval('game.sceneSettings exportPath:%s' %oldexportpath)

lx.eval('game.sceneSettings fbxPreset:%s' %oldexportfbxsettings)


# clean empty meshes
lx.eval("!!select.drop item")
lx.eval("!!select.itemType mesh")
selectedMeshes = scene.selected
itemslist = []
for meshItem in selectedMeshes:
	if meshItem.geometry.internalMesh.PointCount() == 0:
		itemslist.append(meshItem) 
scene.removeItems(itemslist) 

# freeze geometry
lx.eval("!!select.itemType mesh")
lx.eval('poly.freeze twoPoints')


# messing with normals
lx.eval("!!select.drop item")
lx.eval("!!select.itemType mesh")
if len(arg)>0:
	if "-u" in arg:
		lx.eval('vertMap.updateNormals')
	elif "-t" in arg:
		lx.eval('vertMap.toggleNormalMaps auto')

	elif "-s" in arg:
		lx.eval('vertMap.softenNormals connected:true')
else:
	print "no arguments"
	

# Convert all instances to a regular meshes
lx.eval('select.all') 

selectedMeshes = scene.selected

# convert instances to regular meshes
if len(arg)>0:
	if "-c" in arg:
		lx.eval('select.all') 
		selectedMeshes = scene.selected
		for meshItem in selectedMeshes:
			if meshItem.isAnInstance == True:
				scene.select(meshItem)
		lx.eval('item.setType mesh')


# chose export file format
lx.eval('select.all') 
try:
	if "-o" in arg:
		lx.eval('export.selected 16 false false false')
	else: 
		lx.eval('game.export fileDialog:true')
except:
    print "Cancel"

lx.eval('!scene.close')

lx.eval('scene.set %s' %oldscene)
