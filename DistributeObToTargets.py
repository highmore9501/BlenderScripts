import bpy


class DistributeObToTargetsOperator(bpy.types.Operator):
    bl_idname = 'opr.object_distribute_ob_to_targets_operator'
    bl_label = 'Object DistributeObToTargets'

    def execute(self, context):
        ob = context.scene.objects[context.scene.Prototype]
        targetObjects = []

        for item in bpy.context.selected_objects:
                if item.type == "MESH":
                    targetObjects.append(item)            
                item.select_set(False)
            
        for item in targetObjects:   
            # 先复制一个ob         
            NewOb = ob.copy()
            # 然后将item的position和rotation复制过来，应用到ob上
            NewOb.location = item.location
            NewOb.rotation = item.rotation
           
        
        return {'FINISHED'}