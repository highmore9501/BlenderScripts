import bpy

bl_info ="把所有带deform的骨骼移动到第29层，即Rigify默认的DEF层，运行时需要在PoseMode下"

deformLayerNo = 29
mchLayerNo = 28
orgLayerNo = 30

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
        if poseBone.bone.use_deform and poseBone.bone.layers[deformLayerNo] is False:
            moveToLayer(poseBone, deformLayerNo)

moveDEFBones()