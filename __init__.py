import bpy

from .GroupByMaterials import SortByMatOperator
from .AddNewUVMap import AddNewUVOperator

bl_info = {
    # required
    'name': 'Hippo Assistant',
    'blender': (2, 93, 0),
    'category': 'Object',
    # optional
    'version': (1, 0, 0),
    'author': 'HaiKouBigHippo',
    'description': 'A set of scripts used while batch baking.批量烘焙时使用的一些脚本集。',
}

PROPS = [
    ('NewUVMap', bpy.props.StringProperty(name='Prefix', default='Bake')),
    ('suffix', bpy.props.StringProperty(name='Suffix', default='Suff')),
    ('add_version', bpy.props.BoolProperty(name='Add Version', default=False)),
    ('version', bpy.props.IntProperty(name='Version', default=1)),
]


class HippoToolPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_HippoTool'
    bl_label = 'Hippo Tool Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        self.layout.label(text='按材质分类')
        col = self.layout.column()
        col.operator(SortByMatOperator.bl_idname, text='一键分类')

        self.layout.label(text='新增UV')
        col = self.layout.column()
        row = col.row()
        row.prop(context.scene, 'NewUVMap')
        row = col.row()
        row.operator(AddNewUVOperator.bl_idname, text='一键新增UV')


CLASSES = [
    HippoToolPanel,
    SortByMatOperator,
    AddNewUVOperator
]


def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    print('registered')  # just for debug
    for cl in CLASSES:
        bpy.utils.register_class(cl)


def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    print('unregistered')  # just for debug
    for cl in CLASSES:
        bpy.utils.unregister_class(cl)


if __name__ == "__main__":
    register()
