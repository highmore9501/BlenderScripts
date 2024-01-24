import bpy
import os
import csv


#  遍历文件中所有对象，以及它们的材质
#  如果材质使用纹理，pass
#   如果不使用纹理，保存它到清单中，同时保存它的着色器类型，颜色，
#   如果是标准材质，记录粗糙度，金属度，发光颜色，发光强度


def execute():
    matList = []
    outputFile = bpy.path.abspath("//csv_export\\matList.csv")
    for item in bpy.context.selected_objects:
        if item.type == "MESH":
            length = len(item.data.materials)
            if length >= 1:  # 有材料
                for i in range(length):
                    mat = item.material_slots[i].material
                    materialName = mat.name
                    if materialName not in matList:
                        matList.append(materialName)
                        try:
                            inputs = mat.node_tree.nodes["Principled BSDF"].inputs
                            color = inputs["Base Color"].default_value
                            metal = str(inputs["Metallic"].default_value)
                            roughness = str(inputs["Roughness"].default_value)
                            emitColor = inputs["Emission"].default_value
                            emitStrength = str(inputs["Emission Strength"].default_value)

                            fieldnames = ['materialName', 'color0', 'color1', 'color2', 'metal', 'roughness', 'emit0',
                                          'emit1', 'emit2', 'emitStrength']
                            csvLine = {'materialName': materialName, 'color0': color[0], 'color1': color[1],
                                       'color2': color[2], 'metal': metal, 'roughness': roughness,
                                       'emit0': emitColor[0], 'emit1': emitColor[1], 'emit2': emitColor[2],
                                       'emitStrength': emitStrength}
                            with open(outputFile, 'w') as file:
                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                writer.writerow(csvLine)
                        except:
                            pass
    print(matList)


execute()
