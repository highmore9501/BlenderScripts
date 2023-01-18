import bpy

class ShapenAllOperator(bpy.types.Operator):
    bl_idname = 'opr.shapen_objects_operator'
    bl_label = 'Objects Shapen'

    def execute(self, context):
        targetObjects = []         

        for item in bpy.context.selected_objects:
            if item.type == "MESH":
                targetObjects.append(item)            
            item.select_set(False)
        
        for item in targetObjects:            
            item.select_set(True)
            bpy.ops.hops.sharpen()        
            item.select_set(False)      
            
        return {'FINISHED'}