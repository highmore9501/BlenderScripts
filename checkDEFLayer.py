#  检测DEF层里骨骼的parent-child关系，把所有父系对象不是DEF骨骼或者没有父系的给放置到第26层，方便手动来更改
#   执行脚本时先在PoseMode下将层切换到DEF层



import bpy

ErrorLayer = 26

def checkDEF(poseBone):
    try:
        if not poseBone.parent.name.__contains__("DEF"):
            poseBone.bone.layers[ErrorLayer] = True
    except:
        poseBone.bone.layers[ErrorLayer] = True


bpy.ops.pose.select_all(action='SELECT')

for poseBone in bpy.context.selected_pose_bones:
    checkDEF(poseBone)


