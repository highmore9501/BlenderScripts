import bpy

#  此脚本用于移动世界，以模拟静止物体移动的效果。在运行此脚本前需要做一些前置工作。以下会讲具体做法，但数学上的证明都略过。
#  如果我们希望某物体A，在世界中按曲线C_0的轨道运动，一般我们的操作是先把A的位置，旋转，缩放都重置，然后使用PathOf约束器，让它按曲线C_0的轨道运动。当然，约束器生效时，A的实际位置会移动到C曲线的开始处，尽管此时A的transform数据仍然是显示初始状态。我们把A的实际位置状态称为A_0
#  假使A实际不发生任何运动，而是由除A以外的世界运动，造成A在运动的假象。那就需要将整个世界绑定在一个轴心WorldPivot上，并且这个轴心沿另外一个曲线C_1运动，世界随着WorldPivot运动可以达到这样的效果。
#  上面所说的这个WorldPivot，它的初始位置，就是A_0相对于绝对坐标系的镜像位置，曲线C_1就是C_0相对绝对坐标系的镜像位置。

#  我们先选择曲线C，复制一条曲线，然后以绝对坐标系原点为轴心，缩放-1倍，得到的就是镜像曲线C_1。
#  在绝对坐标系原点片我们新建一个pivot，命名为offsetPivot，让它使用PathOf，目标是C_1。此时offsetPivot会移动到一个位置，这个位置就是A_0的初始位置，我们管它叫A_1。
#  在A_1处，我们新建一个pivot，命名为WorldPivot，然后把除物体A以外的所有东西都绑定到它上面，它就是世界轴心。
#   当offsetPivot沿着C_1运动时，每一帧都会发生位置和旋转的变化。WorldPivot需要复制offsetPivot的位移，并且对冲掉offsetPivot的旋转。
#   这种复制和对冲，不太容易理解，但可以按如下操作：
#   对冲旋转值：先取得offsetPivot的旋转值，如果是四元值，直接用invert()。如果是Euler值，先转化成Matrix或者四元值，然后Invert()。将计算得到的值赋值给worldPivot的旋转值。注意，此时的旋转实际上是以绝对坐标系原点为轴心完成的。
#   复制位移值：在得到worldPivot的旋转值以后，用它来计算出一个坐标转换矩阵T，用T左乘offsetPivot的位移，得到绝对坐标系下的位移newOffset，将此值赋值给worldPivot的位移值。
#   每一帧都进行以上计算，就得到了最终的模拟结果：从绝对坐标系来看，世界随着WorldPivot在运动，而在WorldPivot的坐标系来看，物体A在沿着一条类似C_0的曲线在运动。

import mathutils

frames = 2400  # 设置总帧数
currentFrame = 1

worldPivot = bpy.data.objects['WorldPivot']  # 如果各轴心和主体命名不一样，需要在这里更改
offsetPivot = bpy.data.objects['DirectPivot']
worldPivot.select_set(True)

for i in range(frames):
    bpy.context.scene.frame_set(i + 1)
    bpy.ops.object.location_clear(clear_delta=False)
    bpy.ops.object.rotation_clear(clear_delta=False)

    #  计算逆旋转，然后应用到世界轴心
    r = offsetPivot.rotation_euler
    q = mathutils.Euler.to_matrix(r)
    q.invert()
    r = mathutils.Matrix.to_euler(q)
    worldPivot.rotation_euler = r

    # 计算旋转后的世界位移，然后应用到世界轴心
    transMatrix = r.to_matrix()
    newOffset = transMatrix @ offsetPivot.location
    worldPivot.location = newOffset

    # k帧
    worldPivot.keyframe_insert('location')
    worldPivot.keyframe_insert('rotation_euler')

    currentFrame += 1
