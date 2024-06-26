import bpy
import mathutils


# 脚本目标，在当前目标处生成一个符合spoke默认方向，大小刚刚好覆盖当前目标的平面，做为图片动态链接的载体


class AddReferencePlaneOperator(bpy.types.Operator):
    bl_idname = 'opr.object_add_reference_plane_operator'
    bl_label = 'Object AddReferencePlane'

    def execute(self, context):    
        orginLoaction = mathutils.Vector((0,0,0)) + bpy.context.scene.cursor.location #  记住当前游标位置
        targetObjects = []         

        for item in bpy.context.selected_objects:  #  生成要处理对象的列表
            if item.type == "MESH":
                targetObjects.append(item)            
            item.select_set(False)
        
        for currentObj in targetObjects:
            currentObj.select_set(True)
            maxdimension = max(d for d in currentObj.dimensions)  # 得到当前图片最大边距
            currentNormal = currentObj.rotation_euler.to_matrix() @ currentObj.data.polygons[0].normal

            bpy.ops.view3d.snap_cursor_to_selected()  #  游标移动到当前物体，新增平面，旋转，调整大小为1，然后应用变化。
            bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=bpy.context.scene.cursor.location, scale=(1, 1, 1))
            currentObj.select_set(False)
            plane = context.active_object
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.transform.resize(value=(0.5, 0.5, 0.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            plane.scale.x = maxdimension  # 调整新增平面大小至刚好覆盖之前目标
            plane.scale.z = maxdimension

            planeNormal = plane.data.polygons[0].normal  #  计算新平面与目标平面的法线角度，并且旋转新平面与原目标平面垂直
            rot = planeNormal.rotation_difference( currentNormal ).to_euler()
            plane.rotation_euler = rot
            plane.name = '{}_P'.format(currentObj.name)
            plane.select_set(False)

        bpy.context.scene.cursor.location = orginLoaction  #  游标归位

        return {'FINISHED'}