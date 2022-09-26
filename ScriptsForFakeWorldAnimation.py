import bpy

# 起始时设置帧在第一帧，世界轴心为初始值
# 每一帧都将世界轴心移动到offsetPivot,就是根据主体移动轨道生成的反向移动轴心
# 完成移动以后，让世界轴心以主体为轴心旋转，旋转的值为negativePivot。所谓negativePivot，就是DirectionPivot相反旋转方向的轴心。而DirectionPivot，是沿着世界移动轨道（由主体移动轨道反过来）移动并跟随曲线的轴心
# 移动与旋转都完成以后，抽入帧，然后将当前帧+1

frames = 2400  # 设置总帧数
currentFrame = 1
bpy.context.scene.frame_set(1)
worldPivot = bpy.data.objects['WorldPivot']  # 如果轴心命名不一样，需要在这一块更改
negativePivot = bpy.data.objects['NegativePivot']
offsetPivot = bpy.data.objects['offsetPivot']

for i in range(frames):
    worldPivot.rotation_clear(clear_delta=False)
    bpy.ops.transform.translate(value=offsetPivot.position)


