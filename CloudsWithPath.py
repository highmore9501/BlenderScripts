import bpy
import random
import math

#  原理：
#  给所有目标插缩放大小的帧，物体在轨道动画的一开始缩放值为0，到达轨道中段时为最大，再到轨道终点时为0，所以，缩放值取决于该物体跟随的路径动画长短。
#  基本公式是：
#  Scale = ScaleMax * (1 - abs(1 - frame%Path_Duration / 0.5*Path_Duration)
#  即
#  Scale = ScaleMax * (1-abs(1-2 * ((i+1+initFrame) % Duration)/Duration))
#  而物体的旋转值是动画开始时为0，到轨道终点时为360度，所以有：
#  Rotate = 360 * (frame % Duration) / Duration
#
# 在原始曲线起点帧时，scale = 0 rotate.z = 0
# 在原始曲线正中帧时取scale = maxScale
# 在最终点帧PathFrame时取scale = 0 Rotate.z=360
#
# 现在加上一个随机的偏移帧数initFrame<PathFrame/2，所以当前实际位置帧 RealFrame = CurrentFrame + initFrame
# 即CurrentFrame = RealFrame - initFrame
#
# 当RealFrame = 0 时，CurrentFrame = PathFrame + 1 - initFrame
# 当RealFrame = 0.5* PathFrame时， CurrentFrame = 0.5*PathFrame - initFrame
# 当RealFrame = PathFrame时， CurrentFrame = PathFrame - initFrame
#
# 另外，在第一帧和最后一帧时也需要加关键帧，所以可以计算此时物体的scale和rotate
#
# 根据：
# Scale = ScaleMax * (1-abs(1-2 * ((i+1+initFrame) % Duration)/Duration))
# Rotate = 360 *  ((i+1+initFrame) % Duration) / Duration
#
# 可以推算出，一个动画周期需要在五个Frame上加关键帧，分别是:
#
# CurrentFrame = 1时，
# Scale =  ScaleMax * (1-abs(1-2 * ((1+initFrame) % PathFrame)/PathFrame)),
# Rotate = 360 *  ((1+initFrame) % Duration) / Duration
#
# CurrentFrame = PathFrame时，
# Scale = ScaleMax * (1-abs(1-2 * ((PathFrame+initFrame) % PathFrame)/PathFrame)),
# Rotate = 360 *  ((PathFrame+initFrame) % Duration) /Duration
#
# CurrentFrame = PathFrame + 1 - initFrame时， Scale = 0, Rotate.z = 0
# CurrentFrame = 0.5*PathFrame - initFrame时，Scale = MaxScale, Rotate.z = 180
# CurrentFrame = PathFrame - initFrame时,Scale = 0, Rotate.z = 360
#
# 使用方法
# 配合文件Asset/cloudsWithPath.blend使用
# 如果要新增云朵或路径都可以自定义或者复制新增，只要确保文件里的每一朵云都是约束在一条路径上的
# 使用时全选所有云朵，清空云朵的关键帧，然后运行脚本
# 运行后可得到依路径长度计算出来的云朵随机缩放和旋转动画
# 如果需要导出动画，在导出前需要将路径动画烘焙好再导出

TotalFrames = 2400  # 设置总帧数
ScaleMax = 50  # 设置云朵最大缩放值

for obj in bpy.context.selected_objects:
    if obj.constraints["Follow Path"]:
        PathName = obj.constraints["Follow Path"].target.name
        Duration = bpy.data.curves[PathName].path_duration
        initFrame = random.randint(1, int(Duration/2))

        #  五个需要插帧的时间点，以及最后一帧-1
        keyFrames = [1, Duration, Duration+1 - initFrame, int(0.5*Duration) - initFrame, Duration - initFrame, TotalFrames-1]

        for keyFrame in keyFrames:
            while keyFrame < TotalFrames:
                bpy.context.scene.frame_set(keyFrame)
                Scale = ScaleMax * (1 - abs(1 - 2 * ((keyFrame + initFrame) % Duration) / Duration))
                Rotate = 360 * ((keyFrame + initFrame) % Duration) / Duration
                obj.scale[0] = Scale
                obj.scale[1] = Scale
                obj.scale[2] = Scale
                obj.rotation_euler = (0.0, 0.0, math.radians(Rotate))
                obj.keyframe_insert('scale')
                obj.keyframe_insert('rotation_euler')
                keyFrame += Duration
