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

masterObject = None

# look if there is a proper object to instantiate 
if len( selectedMeshes ) >= 2:
	for item in reversed(selectedMeshes):
		if (item.type in ["mesh", "meshInst", "locator"]):
			masterObject = item
			break

# place and adjust instances of a last selected object 
if (masterObject != None):
	for item in selectedMeshes:
		if (item.type in ["mesh", "meshInst", "locator"]): 
			if item.id != masterObject.id:
				
				instance = modo.Scene().duplicateItem(masterObject, instance=True)
					
				transf = modo.LocatorSuperType(item).position.get()
				rot =  modo.LocatorSuperType(item).rotation.get()
				scl =  modo.LocatorSuperType(item).scale.get()
					
				# Place instance according to a hierarchy
				if item.parent != None:
					instance.setParent(item.parent)
						
				modo.LocatorSuperType(instance).position.set(transf)
				modo.LocatorSuperType(instance).rotation.set(rot)
				modo.LocatorSuperType(instance).scale.set(scl)
	
	# remove last element from selection
	selectedMeshes.remove(masterObject)
	scene.select(selectedMeshes)
