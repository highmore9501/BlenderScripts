import bpy
# 脚本作用，在选定的多个目标位置上，根据一个复制源，生成一个具体相同位置，旋转，以及对应缩放值的代理Pivot，主要用于代理Pivot工作流程

class DistributeObToTargetsOperator(bpy.types.Operator):
    bl_idname = 'opr.object_distribute_ob_to_targets_operator'
    bl_label = 'Object DistributeObToTargets'

    def execute(self, context):
        sourceObj = context.scene.objects[context.scene.sourceObj]
        originScale = context.scene.OriginScale

        targetCol = bpy.context.scene.collection             
        for col in bpy.data.collections:           # 如果已经存在RepeatObjectsPivot这个文件夹，就将它定为目标文件夹             
            if col.name == "RepeatObjectsPivot":
                targetCol = col                              

        if targetCol is bpy.context.scene.collection:  # 如果不存在该文件夹，就新建，然后加在根文件夹下         
            targetCol = bpy.data.collections.new(name="RepeatObjectsPivot")
            bpy.context.scene.collection.children.link(targetCol)
        
        NewObjectsMap = []

        for item in bpy.context.selected_objects: 
            if item.type == "MESH":       
                # 先一对一复制生成obj         
                NewObj = sourceObj.copy()             
                for i in range(3):
                    NewObj.location[i] = item.location[i]
                    NewObj.rotation_euler[i] = item.rotation_euler[i]
                    NewObj.scale[i] = NewObj.scale[i] * item.scale[i] / originScale
            
                targetCol.objects.link(NewObj)  

        return {'FINISHED'}