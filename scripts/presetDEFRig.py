#  DEF手动整理好继承关系，清除掉不可选骨骼，给面部和全身骨骼加好CopyTransform/CopyLocation/CopyRotation以后运行此脚本，运行时确保在PoseMode下

import bpy


#  所有子骨骼需要都有勾上inherit rotation/inherit location选项，填完所有的constraint里的主目标和次目标
bpy.ops.pose.select_all(action='SELECT')

controlRigName = bpy.context.object.name.replace(".GameRig", "")

for poseBone in bpy.context.selected_pose_bones:
    poseBone.bone.use_inherit_rotation = True
    for cs in poseBone.constraints:
        cs.target = bpy.context.scene.objects.get(controlRigName)
        cs.subtarget = poseBone.bone.name


#  把所有子骨骼去掉connected选项，去掉所有bendyBone的设置
bpy.ops.object.editmode_toggle()
bpy.ops.armature.select_all(action='SELECT')


for poseBone in bpy.context.selected_bones:
    poseBone.bbone_segments = 1

    try:
        if poseBone.parent:
            poseBone.use_connect = False
    except:
        pass



