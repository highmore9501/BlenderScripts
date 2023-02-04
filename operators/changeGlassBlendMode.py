import bpy


# 脚本目标，将所有选中的物体的材料中，alpha不为1的混合方式设置为为Alpha Blend

class ChangeGlassBlendeModeOperator(bpy.types.Operator):
    bl_idname = 'opr.change_glass_blender_mode_operator'
    bl_label = 'Object ChangeGlass'

    def execute(self, context):
        matList = []

        for item in bpy.context.selected_objects:
            if item.type == "MESH":
                for slot in item.material_slots:
                    try:
                        mat = slot.material
                        materialName = mat.name
                        if materialName not in matList:
                            matList.append(materialName)
                            inputs = mat.node_tree.nodes["Principled BSDF"].inputs

                            if inputs['Alpha'].default_value < 1:
                                mat.blend_method = 'BLEND'
                    except:
                        pass
        print(matList)
        print('以上材质已被按玻璃修改。')

        return {'FINISHED'}


class DisableGlassBlendeModeOperator(bpy.types.Operator):
    bl_idname = 'opr.disable_glass_blender_mode_operator'
    bl_label = 'Object disableGlass'

    def execute(self, context):
        matList = []

        for item in bpy.context.selected_objects:
            if item.type == "MESH":
                for slot in item.material_slots:
                    try:
                        mat = slot.material
                        materialName = mat.name
                        if materialName not in matList:
                            matList.append(materialName)
                            inputs = mat.node_tree.nodes["Principled BSDF"].inputs

                            mat.blend_method = 'OPAQUE'
                            mat.shadow_method = 'OPAQUE'

                    except:
                        pass
        print(matList)
        print('以上材质已全部取消透明模式。')

        return {'FINISHED'}
