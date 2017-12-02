#python
# zero out position depending on selection type
# VERTEX: set to 0 for each vertex
# EDGE | POLYGON: set 0 for a selection bounding box center
# ITEM: set position to 0
# Arguments: x,y,z 
# USAGE: "@resetPosition.py xz" will zero out position on x and z axis
# https://i.imgur.com/DG7ENJa.gifv
# Author: Andy Budanov
# ```python

import modo
import lx

scene = modo.Scene()

def resetPosition( axis ):
	if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
		lx.eval("vert.set %s 0.0 false true" %axis)
	elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
		lx.eval("vert.center %s" %axis) 
	elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
		lx.eval("vert.center %s" %axis)
	elif lx.eval1( "select.typeFrom typelist:item;edge;vertex;polygon ?" ):
		for item in scene.selected:
			lx.eval("transform.channel pos.%s 0.0" %axis)
	return 

arg = lx.arg()
if len(arg)>0:
	for char in arg.upper():
		resetPosition( char )
else: 
	arg = "XYZ"
	for char in arg.upper():
		resetPosition( char )
