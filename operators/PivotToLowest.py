import bpy
import mathutils

class PivotToLowestOperator(bpy.types.Operator):
    bl_idname = 'opr.change_piovt_to_lowest_operator'
    bl_label = 'Object ChangePivot'


    def execute(self, context):   
        orginLoaction = mathutils.Vector((0,0,0)) + bpy.context.scene.cursor.location
        targetObjects = []

        for item in bpy.context.selected_objects:
            if item.type == "MESH":
                targetObjects.append(item)            
            item.select_set(False)
        
        for item in targetObjects:            
            item.select_set(True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            # get the minimum z-value of all vertices after converting to global transform
            lowest_pt = min([(item.matrix_world @ v.co).z for v in item.data.vertices])              
            
            # give 3dcursor new coordinates
            bpy.context.scene.cursor.location = mathutils.Vector((item.location.x,item.location.y,lowest_pt))

            # set the origin on the current object to the 3dcursor location
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

            item.select_set(False)
        
        bpy.context.scene.cursor.location = orginLoaction
    
        return {'FINISHED'}