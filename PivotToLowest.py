import bpy
import mathutils

class PivotToLowestOperator(bpy.types.Operator):
    bl_idname = 'opr.change_piovt_to_lowest_operator'
    bl_label = 'Object ChangePivot'


    def execute(self, context):   
        for item in bpy.context.selected_objects:
            if item.type == "MESH":
                bpy.context.view_layer.objects.active = item
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

                # get the minimum z-value of all vertices after converting to global transform
                lowest_pt = min([(item.matrix_world @ v.co).z for v in item.data.vertices])              
                
                # give 3dcursor new coordinates
                bpy.context.scene.cursor.location = mathutils.Vector((item.location.x,item.location.y,lowest_pt))

                # set the origin on the current object to the 3dcursor location
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    
        return {'FINISHED'}