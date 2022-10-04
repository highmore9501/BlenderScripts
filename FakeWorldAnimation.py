import bpy

#  此脚本用于移动世界，以模拟静止物体移动的效果。在运行此脚本前需要做一些前置工作。以下会讲具体做法，但数学上的证明都略过。
#  如果我们希望某物体carPivot，在世界中按曲线C的轨道运动，一般我们的操作是先把carPivot的位置，旋转，缩放都重置，然后使用PathOf约束器，让它按曲线C的轨道运动。当然，约束器生效时，A的实际位置会移动到C曲线的开始处，尽管此时A的transform数据仍然是显示初始状态。
#  烘焙carPivot的运动轨迹
#  新建一个worldPivot，然后把除carPivot以外的整个世界都绑定在它上面
#  设置好总帧数，设置好物体和世界轴心的名字，然后运行以下脚本

import mathutils

frames = 1600  # 设置总帧数
currentFrame = 1

worldPivot = bpy.data.objects['WorldPivot']  # 如果世界轴心和car的命名和代码里的不一样，可以在这里更改
worldPivotInitLocation = worldPivot.location + mathutils.Vector((0, 0, 0))

carPivot = bpy.data.objects['CarPivot']
carInitLocation = carPivot.location + mathutils.Vector((0, 0, 0))

for i in range(frames):
    bpy.context.scene.frame_set(i + 1)

    #  计算逆旋转
    r = carPivot.rotation_euler
    q = mathutils.Euler.to_matrix(r)
    q.invert()
    r = mathutils.Matrix.to_euler(q)
    worldPivot.rotation_euler = r

    # 计算旋转后的世界位移
    transMatrix = r.to_matrix()
    worldPivot.location = carInitLocation + transMatrix @ (worldPivotInitLocation - carPivot.location)

    # k帧
    worldPivot.keyframe_insert('location')
    worldPivot.keyframe_insert('rotation_euler')

    #  四元数版本
    # r = carPivot.rotation_quaternion
    # q = mathutils.Euler.to_matrix(r)
    # q.invert()
    # r = mathutils.Matrix.to_quaternion(q)
    # worldPivot.rotation_quaternion = r
    # transMatrix = r.to_matrix()
    # worldPivot.location = carInitLocation + transMatrix @ (worldPivotInitLocation - carPivot.location)
    # worldPivot.keyframe_insert('location')
    # worldPivot.keyframe_insert('rotation_quaternion')

    currentFrame += 1
