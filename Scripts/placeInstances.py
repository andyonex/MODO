# python
# Place instances to other objects position
# Author: Andy Budanov
# Place an instance of the last selected object to match to transformation of every other selected object
# Usage: 
# 1. Select multiple objects you want to replace.
# 2. Select object that you want to instantiate 
# 3. run the script with @placeInstances.py
# you'll be left with replaced objects selection (without the last one) so you can delete or group them
# ```python

import lx
import modo
scene = modo.Scene()

selectedMeshes = scene.selected

if len( selectedMeshes ) > 2:
	org = selectedMeshes[len(selectedMeshes)-1]
	for item in scene.selected:
		if item.id != org.id:

			instance = modo.Scene().duplicateItem(org, instance=True)
			
			transf = modo.LocatorSuperType(item).position.get()
			rot =  modo.LocatorSuperType(item).rotation.get()
			scl =  modo.LocatorSuperType(item).scale.get()
			
			if item.parent != None:
				instance.setParent(item.parent)
				
			modo.LocatorSuperType(instance).position.set(transf)
			modo.LocatorSuperType(instance).rotation.set(rot)
			modo.LocatorSuperType(instance).scale.set(scl)

# remove last element from selection
selectedMeshes.pop()
scene.select(selectedMeshes)
