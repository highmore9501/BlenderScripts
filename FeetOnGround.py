import bpy
import mathutils

#  基本原理
#  动捕出来的动作，经常出现各种奇怪的抖动。身体其它部分的抖动在平滑处理以后还基本可以接受，但脚部的移动会显得整个人没能踩在地上。
#  高度最低的那一只脚，肯定是应该着地的，这里暂时不考虑双脚离地的情况，如果确实有这种情况，再手动去调节。
#  着地的脚，应该是位置不动的，如果它在移动，就需要用身体的轴心移动来对冲掉脚的移动。
#  这个脚本的作用，就是每一帧检测着地的脚是哪一只，以及前一帧着地的脚是哪一只。如果两只相同的话，就用身体的移动对冲掉两帧之间脚的移动，使得着地的脚看上去是不滑动的。
#  如果相邻两帧着地的脚不同，不需要对冲移动。
#  在运行此脚本之前，需要给每只脚最低的骨骼绑定一个空轴，然后烘焙移动轨迹，取得每只脚的原始移动轨道。然后另用一个空轴当整个骨骼的父极，用它的移动来对冲脚部的滑动。

rightFootName = 'RightToePivot'
rightFoot = bpy.data.objects[rightFootName]
leftFootName = 'LeftToePivot'
leftFoot = bpy.data.objects[leftFootName]
bodyName = 'GalaxiaPivot'
body = bpy.data.objects[bodyName]

TotalFrame = 1850
currentBodyLocation = mathutils.Vector((0.0,0.0,0.0)) + body.location
currentRightFootLocation = mathutils.Vector((0.0,0.0,0.0)) + rightFoot.location
currentLeftFootLocation = mathutils.Vector((0.0,0.0,0.0)) + leftFoot.location
offset = mathutils.Vector((0.0,0.0,0.0))

lastFoot = 0  # 数字为0时表示上次着地的是右脚，为1时表示上次着地的是左脚
currentFoot = 0  # 当前着地的脚，意思同上

for frame in range(1, TotalFrame):
    bpy.context.scene.frame_set(frame)

    if rightFoot.location[2] <= leftFoot.location[2]:
        currentFoot = 0
        offset = rightFoot.location - currentRightFootLocation
    else:
        currentFoot = 1
        offset = leftFoot.location - currentLeftFootLocation

    if currentFoot == lastFoot:
        body.location = body.location - offset
        body.keyframe_insert('location')

    currentRightFootLocation = mathutils.Vector((0.0, 0.0, 0.0)) + rightFoot.location
    currentLeftFootLocation = mathutils.Vector((0.0, 0.0, 0.0)) + leftFoot.location
    lastFoot = currentFoot
