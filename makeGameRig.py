#  为原Rig生成GameRig，并将原rig中的DEF功能全部去掉，将之变成一个TGTRig
#   在objectMode下选中原始Rig，然后执行脚本
#   执行脚本成功以后，要将已经绑定权重的Mesh里的Armature修改器内的参数改成新生成的GameRig


import bpy

deformLayerNo = 29

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


def uncheckDEFOption():
    for poseBone in bpy.context.active_object.pose.bones[:]:
        if poseBone.bone.use_deform:
            poseBone.bone.use_deform = False


def removeAllConstraint(ob):  #  清除目标上所有的constraints
    cl = len(ob.constraints)
    if cl != 0:
        for c in ob.constraints:
            ob.constraints.remove(c)


orgName = bpy.context.object.name
#  复制一个新rig出来
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#  新rig重命名为"orgName.GameRig"
bpy.context.object.name = orgName + ".GameRig"
#  切换至PoseMode下
bpy.ops.object.posemode_toggle()
# 将全部DEFBones移动到第29层
moveDEFBones()
# 切换界面至29层
bpy.context.object.data.layers[29] = True
# 全选
bpy.ops.pose.select_all(action='SELECT')
# 切换到EditMode
bpy.ops.object.editmode_toggle()
# 把所有层都激活
for i in range(32):
    bpy.context.object.data.layers[i] = True
# 反选
bpy.ops.armature.select_all(action='INVERT')
# 删除
bpy.ops.armature.delete()

#  切换到PoseMode，去掉骨骼上所有的constraint，然后全部新建对应原Rig上同名骨骼的CopyTransform:
bpy.ops.object.posemode_toggle()
bpy.ops.pose.select_all(action='SELECT')

for poseBone in bpy.context.selected_pose_bones:
    removeAllConstraint(poseBone)
    cs = poseBone.constraints.new('COPY_TRANSFORMS')
    cs.target = bpy.data.objects[orgName]
    cs.subtarget = poseBone.bone.name

#  切换到ObjectMode，选择原Rig，然后去掉原Rig所有骨骼的DEF功能
bpy.ops.object.posemode_toggle()
bpy.context.view_layer.objects.active = bpy.data.objects[orgName]
bpy.data.objects[orgName].select_set(True)
bpy.ops.object.posemode_toggle()
uncheckDEFOption()

