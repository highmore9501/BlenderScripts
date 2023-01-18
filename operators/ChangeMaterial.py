import bpy


# 脚本目标，将所有选中的物体的材料属性进行批量修改


class ChangerMatOperator(bpy.types.Operator):
    bl_idname = 'opr.changer_materials_operator'
    bl_label = 'Object ChangeMat'

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

                            if context.scene.ChangeRoughness:
                                inputs["Roughness"].default_value = context.scene.Roughness
                            if context.scene.ChangeColor:
                                R = context.scene.BaseColor[0]
                                G = context.scene.BaseColor[1]
                                B = context.scene.BaseColor[2]
                                inputs["Base Color"].default_value = (R, G, B, 1)
                            if context.scene.ChangeMetalness:
                                inputs["Metallic"].default_value = context.scene.Metalness
                            if context.scene.ChangeEmitColor:
                                R = context.scene.EmitColor[0]
                                G = context.scene.EmitColor[1]
                                B = context.scene.EmitColor[2]
                                inputs["Emission"].default_value = (R, G, B, 1)
                            if context.scene.ChangeEmitStrength:
                                inputs["Emission Strength"].default_value = context.scene.EmitStrength
                    except:
                        pass
        print(matList)
        print('以上材质已被修改。')

        return {'FINISHED'}
