import bpy

bl_info ="把所有带deform的骨骼移动到第29层，即Rigify默认的DEF层，运行时需要在PoseMode下"
#  带变形功能又带有Modifier的骨骼移动到第17层，带Modifier但不带变形功能的骨骼移动到第18层，什么也不带的移动到第19层，带变形但不带Modifer的骨骼移到29层

deformLayer = 29
mchLayer = 28
orgLayer = 30
deformWithModifier = 8
modifierLayer = 16
normalLayer = 1

bpy.ops.pose.select_all()

def moveToLayer(poseBone, layerNumber):
    poseBone.bone.layers[layerNumber] = True  # move bone to DEF Layer
    poseBone.custom_shape = None
    for i in range(32):
        if i != layerNumber:
            poseBone.bone.layers[i] = False  # set other layer to False


def moveDEFBones():
    # If there ARE objects selected then act on all objects
    for poseBone in bpy.context.active_object.pose.bones[:]:  
        try:
            hasConstraints = poseBone.constraints[0]
        except:
            hasConstraints = False

        print(poseBone.name,":变形功能",poseBone.bone.use_deform,", 约束器", hasConstraints)
        if poseBone.bone.use_deform and hasConstraints:
            targetLayer = deformWithModifier      
        elif poseBone.bone.use_deform :
            targetLayer = deformLayer      
        elif hasConstraints:
            targetLayer = modifierLayer     
        else:
            targetLayer = normalLayer
        
        moveToLayer(poseBone, targetLayer)

moveDEFBones()