# python
import lx
import modo

scene = modo.Scene()

#init select path dialog
try:
	lx.command('dialog.setup', style='dir')
	# lx.eval("dialog.result \"c:\"" );
	lx.command('dialog.title', title='Select the Preset Folder')
	lx.eval('dialog.open')
	dirPath = lx.eval('dialog.result ?')
except RuntimeError:
	lx.eval('sys.exit()')

#Save selected objects as presets one by one
if dirPath:
	dirPath = dirPath + "\\"
	selectedMeshes = scene.selected
	for item in selectedMeshes:
		scene.select(item)
		fname = dirPath + item.name + ".lxl"
		lx.command("mesh.presetSave", filename=fname, reuseThumb=0)
