import bpy

root = bpy.data.collections.get('Female')
collections = root.children_recursive

for col in collections:
    col.hide_render = False
    bpy.data.scenes["Scene"].render.filepath = '//render\{}'.format(col.name)
    bpy.ops.render.render(animation=True)
    col.hide_render = True
