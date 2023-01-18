import bpy

from .panels.clearDataPanel import ClearDataPanel
from .panels.clearMatPanel import ClearMatPanel
from .panels.UVDataPanle import UVDataPanel
from .panels.changeMatPanel import ChangeMatPanel
from .panels.particleAnimatePanel import ParticleAnimatePanel
from .panels.othersFunctionPanel import OthersFunctionPanel

bl_info = {
    # required
    'name': 'Hippo Tools',
    'blender': (2, 93, 0),
    'category': 'Object',
    'location': 'View 3D > Tool Shelf > HippoTools',
    # optional
    'version': (1, 0, 0),
    'author': '海口大河马 HaiKouBigHippo',
    'description': ' 个人常用的一些脚本集。',
}

PROPS = [
    ('NewUVMap', bpy.props.StringProperty(name='新UV命名', default='Bake')),
    ('RemoveUVMap', bpy.props.StringProperty(name='删除UV', default='Bake')),
    ('RestUVMap', bpy.props.StringProperty(name='保留UV', default='Bake')),
    ('ps_obj', bpy.props.StringProperty(name='粒子生成体')),
    ('Obj', bpy.props.StringProperty(name='派生源')),
    ('add_version', bpy.props.BoolProperty(name='Add Version', default=False)),
    ('version', bpy.props.IntProperty(name='Version', default=1)),
    ('ChangeColor', bpy.props.BoolProperty(name='颜色', default=False)),
    ('BaseColor', bpy.props.FloatVectorProperty(
        name = "",
        subtype = "COLOR",
        default = (1.0,1.0,1.0,1.0),
        size = 4
        )),
    ('ChangeRoughness', bpy.props.BoolProperty(name='糙度', default=False)),
    ('Roughness', bpy.props.FloatProperty(name='', default=0.0)),
    ('ChangeMetalness', bpy.props.BoolProperty(name='金属度', default=False)),
    ('Metalness', bpy.props.FloatProperty(name='', default=0.0)),
    ('ChangeEmitColor', bpy.props.BoolProperty(name='自发光色', default=False)),
    ('EmitColor', bpy.props.FloatVectorProperty(
        name = "",
        subtype = "COLOR",
        default = (1.0,1.0,1.0,1.0),
        size = 4
        )),
    ('ChangeEmitStrength', bpy.props.BoolProperty(name='自发光强度', default=False)),
    ('EmitStrength', bpy.props.FloatProperty(name='', default=0.0)),
]

CLASSES = [
    ClearDataPanel,
    ClearMatPanel,
    UVDataPanel,    
    ParticleAnimatePanel,
    ChangeMatPanel,
    OthersFunctionPanel
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
