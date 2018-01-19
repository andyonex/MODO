# python
# Create a group with a name of the first selected object
# Author: Andy Budanov
# ```python
import lx
import modo
scene = modo.Scene()


orgName = "Group_GRP"

for item in scene.selected:
    if (item.type in ["mesh", "meshInst"]): 
        firstItem = item
        orgName = firstItem.name + "_GRP"
        break

lx.eval('layer.groupSelected')

lx.eval('item.name "%s" groupLocator' %(orgName))