# python
# Replace instances of an instances with the regular instances
# https://i.imgur.com/hvJv2S0.gifv
# Usage: Select the original objects, instances of which you want to fix
# Author: Andy Budanov
# ```python
import lx
import modo

#
# Transform instances of a source object to a position of the provided 
# object and delete that objects afterwards
#
def placeInstances( source, objectsList ):
	instancesList = []
	# Place and adjust instances of a source object
	for item in objectsList:
		instance = modo.Scene().duplicateItem( source, instance=True )
		instance.name = item.name		
		pos = modo.LocatorSuperType( item ).position.get()
		rot = modo.LocatorSuperType( item ).rotation.get()
		scl = modo.LocatorSuperType( item ).scale.get()
		# Place instance according to an a hierarchy
		if item.parent != None:
			instance.setParent( item.parent )		
		# restore transformations
		modo.LocatorSuperType( instance ).position.set( pos )
		modo.LocatorSuperType( instance ).rotation.set( rot )
		modo.LocatorSuperType( instance ).scale.set( scl)
		instancesList.append( instance )

	scene.select( objectsList )
	lx.eval( "delete" )
	return instancesList

#
# Return all instances of and object 
#
def findinstances(scene, item, list = None):
	if list is None:
		list = []
	list.append( item )
	scene.select( item )		
	try:
		lx.eval( "select.itemInstances" )		
		selectedInstances = scene.selected
		for inst in selectedInstances:
				findinstances(scene, inst, list)
 	except: pass
	return list

#
# Main
#
scene = modo.Scene()
selectedMeshes = scene.selected

meshlist = []
for item in selectedMeshes:
	if item.type == "mesh":
		meshlist.append( item )

fixedList = []
for item in meshlist:
	scene.select( item )
	try:
		lx.eval( "select.itemInstances" )
		selectedInstances = scene.selected
		for inst in selectedInstances:
			instlist = findinstances( scene, inst )
			if ( len(instlist) > 1 ):
				fixedList += placeInstances( item, instlist )
	except: pass
	scene.select( item )

scene.select( fixedList )
