# python
# Desc: Create animated Skinmesh out of animated objects (transformations only)
# HowTo: Select objects with (without) animation you want to bake to a skinmesh, Run script (original objects will be left intact)
# Issues: Not working with hierarchies
# Author: Andrey Budanov
# ```python
import lx
import os
import modo

# Copy and paste transformation channels
def copyChannel(copyFromName, pasteToName):
	for chName in ["Pos","Rot", "Scl"]:
		ChName_low = chName.lower()
		for ax in ["X","Y","Z"]:
			copyFromXfrmID = lx.eval("query sceneservice item.xfrm%s ? {%s}" % (chName, copyFromName))
			if copyFromXfrmID:
				lx.eval("select.channel {%s:%s.%s} set" % (copyFromXfrmID, ChName_low, ax))
				lx.eval("channel.copy")

				pasteToXfrmID = lx.eval("query sceneservice item.xfrm%s ? {%s}" % (chName, pasteToName))
				lx.eval("select.channel {%s:%s.%s} set" % (pasteToXfrmID, ChName_low, ax) )
				lx.eval("channel.paste")
				lx.eval("channel.toSetup")
        
				# duct tape
				lx.eval("channel.paste")
	return

scene = modo.Scene()
selectedMeshes = scene.selected

# Make a copy
scene.select( selectedMeshes )

# Duplicate and convert instances to mesh
lx.eval("item.duplicate false all:false")
lx.eval("item.setType mesh locator")

# Reassign selection
selectedMeshes = scene.selected

# Create Root Joint
rootJoint = scene.addJointLocator(name = "Joint_Root")
jointList = []
tailJointList = []

# Create joints for all selected objects and transfer animated channels to that joints
for item in selectedMeshes:	

	# Create polygon "Selection Set" for further bind process
	lx.eval("item.componentMode item true")
	scene.select(item)	
	selectionSetName = "Joint_" + item.name.replace(" ", "_")
	lx.eval("item.componentMode polygon true")
	lx.eval('select.editSet "%s" set' % (selectionSetName))

	# Create joint
	newJoint = scene.addJointLocator(name = "Joint_"+item.name)
	newJoint.channel('isRadius').set(0.1)
	newJoint.setParent(rootJoint)
	scene.select(newJoint)
	jointName = lx.eval("item.name ?")
	lx.eval("transform.add type:pos")
	lx.eval("transform.add scl %s" % (newJoint.id))

	# Append joint to the list	
	jointList.append(newJoint)

	# Create temp "tail" joint for Binding process only
	tailJoint = scene.addJointLocator(name = "Joint_"+item.name+"_tail")
	tailJoint.channel('isRadius').set(0.01)
	tailJoint.setParent( newJoint )
	tailJoint.position.z.set(.01)

	# Append temp joint to the list	
	tailJointList.append(tailJoint)

	# Transfer animation
	scene.select(tailJoint)
	copyChannel(item.name, jointName)

# Create empty object to use as pivot
tempItem = scene.addMesh("_tempMesh")
lx.eval('item.parent "%s" {} 0 inPlace:0 duplicate:0' % (tempItem.name))

# Merge into a single mesh
selectedMeshes.insert(0,tempItem)
scene.select( selectedMeshes )
lx.eval('layer.mergeMeshes true')
lx.eval('item.name skinMesh mesh')

# Bind Mesh
lx.eval('select.subItem %s add' % rootJoint.name)
lx.eval('anim.setup on')
lx.eval('!!deform.bind type:rigid falloff:medium segs:true limitWeights:false numWeights:4 minWeight:0.01')

# Apply bind weights to the mesh based on the selection sets
for joint in jointList:
	lx.eval('select.drop polygon')
	scene.select(joint)
	selectionSetName = joint.name.replace(" ", "_")	
	lx.eval('select.useSet %s replace' %selectionSetName)
	lx.eval('tool.set vertMap.setWeight on')
	lx.eval('tool.attr vertMap.setWeight additive false')
	lx.eval('tool.setAttr vertMap.setWeight weight 1')
	lx.eval('tool.doApply')
	lx.eval("deformer.isolateWeights")
	lx.eval('tool.set vertMap.setWeight off 0')	
lx.eval('anim.setup off')

# Scene Cleanup
lx.eval('select.drop item')
scene.select(tailJointList)	
lx.eval('!!item.delete')
