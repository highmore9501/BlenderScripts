import bpy

from .GroupByMaterials import SortByMatOperator  # 按材质分类
from .RemoveMat import RemoveMatOperator  # 删除所有材质
from .AddNewUVMap import AddNewUVOperator  # 一键新增UV
from .RemoveBakeUV import RemoveUVOperator  # 一键删除UV
from .RemoveUnBakeUV import RemoveOtherUVOperator  # 一键删除其它UV
from .RemoveConstraints import RemoveConstraintsOperator  # 一键清除所有约束
from .RemoveZero import RemoveZeroGroupOperator
from .ParticleToAnimationRebuild import ParticleToAnimationOperator

bl_info = {
    # required
    'name': 'Hippo Tools',
    'blender': (2, 93, 0),
    'category': 'Object',
    'location': 'View 3D > Tool Shelf > HippoTools',
    # optional
    'version': (1, 0, 0),
    'author': 'HaiKouBigHippo',
    'description': ' 个人常用的一些脚本集。',
}

PROPS = [
    ('NewUVMap', bpy.props.StringProperty(name='新UV命名', default='Bake')),
    ('RemoveUVMap', bpy.props.StringProperty(name='删除UV', default='Bake')),
    ('RestUVMap', bpy.props.StringProperty(name='保留UV', default='Bake')),
    ('ps_obj', bpy.props.StringProperty(name='粒子生成体')),
    ('Obj', bpy.props.StringProperty(name='啥啥体')),
    ('add_version', bpy.props.BoolProperty(name='Add Version', default=False)),
    ('version', bpy.props.IntProperty(name='Version', default=1)),
]


class HippoToolPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_HippoTool'
    bl_label = 'Hippo Tool Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HippoTools'

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False

    def draw(self, context):

        layout = self.layout

        layout.label(text='清空数据')
        row = layout.row()
        col = row.column()
        col.operator(RemoveConstraintsOperator.bl_idname, text='约束器', icon='CONSTRAINT')

        col = row.column()
        col.operator(RemoveZeroGroupOperator.bl_idname, text='空顶点组', icon='GROUP_VERTEX')

        col = row.column()
        col.operator(RemoveMatOperator.bl_idname, text='材质', icon='SHADING_SOLID')

        layout.label(text='按材质分类')
        col = layout.column()
        col.operator(SortByMatOperator.bl_idname, text='一键分类', icon='NODE_MATERIAL')

        layout.label(text='新增UV')
        col = layout.column()
        row = col.row()
        row.prop(context.scene, 'NewUVMap')
        row = col.row()
        row.operator(AddNewUVOperator.bl_idname, text='一键新增UV', icon='FILE_NEW')

        layout.label(text='删除UV')
        col = layout.column()
        row = col.row()
        row.prop(context.scene, 'RemoveUVMap')
        row = col.row()
        row.operator(RemoveUVOperator.bl_idname, text='一键删除UV', icon='REMOVE')

        layout.label(text='删除其它UV')
        col = layout.column()
        row = col.row()
        row.prop(context.scene, 'RestUVMap')
        row = col.row()
        row.operator(RemoveOtherUVOperator.bl_idname, text='一键删除其它UV', icon='PINNED')

        layout.label(text='粒子动画')
        col = layout.column()
        row = col.row()
        row.prop_search(context.scene, "ps_obj", bpy.data, "objects", icon='OBJECT_DATA')
        row = col.row()
        row.prop_search(context.scene, "Obj", bpy.data, "objects",  icon='OBJECT_DATA')
        row = col.row()
        row.operator(ParticleToAnimationOperator.bl_idname, text='生成粒子动画', icon='RENDER_ANIMATION')


CLASSES = [
    HippoToolPanel,
    SortByMatOperator,
    AddNewUVOperator,
    RemoveUVOperator,
    RemoveOtherUVOperator,
    RemoveMatOperator,
    RemoveConstraintsOperator,
    RemoveZeroGroupOperator,
    ParticleToAnimationOperator
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
