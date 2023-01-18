import bpy

from ..operators.AddReferencePlane import AddReferencePlaneOperator
from ..operators.DistributeObToTargets import DistributeObToTargetsOperator

from ..operators.PivotToLowest import PivotToLowestOperator
from ..operators.RenameByHerf import RenameByHerfOperator
from ..operators.ShapenAll import ShapenAllOperator


class OthersFunctionPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_OTHERS_FUNCTION'
    bl_label = '其它功能'
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

        layout.label(text='修改轴心')
        col = layout.column()
        row = col.row()
        row.operator(PivotToLowestOperator.bl_idname,text='批量轴心到低点',icon='EMPTY_AXIS')

        layout.label(text='参考平面')
        col = layout.column()
        row = col.row()
        row.operator(AddReferencePlaneOperator.bl_idname,text='新增参考平面',icon='SNAP_FACE')

        layout.label(text='锐化物体')
        col = layout.column()
        row = col.row()
        row.operator(ShapenAllOperator.bl_idname,text='锐化多个物体',icon='SNAP_VOLUME')

        layout.label(text='依图片源重命名')
        col = layout.column()
        row = col.row()
        row.operator(RenameByHerfOperator.bl_idname,text='依图片源重命名',icon='IMAGE_PLANE')

        layout.label(text='批量复制代理Pivot')
        col = layout.column()
        row = col.row()
        row.prop_search(context.scene, "sourceObj", bpy.data, "objects", icon='OBJECT_DATA')
        row = col.row() 
        row.prop(context.scene,"OriginScale")
        row = col.row() 
        row.operator(DistributeObToTargetsOperator.bl_idname,text="批量生成Pivot",icon="PIVOT_CURSOR")