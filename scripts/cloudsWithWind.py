import math
import random
import time

import bpy
import mathutils


# 原理：
# 已知一个云朵初始位置cloud，一个风源，分别有风力强度WindStrength,扰动参数Noise,风向vectorWind，来计算云朵的行动轨迹。该轨迹符合以下要求：
# 轨迹的方向与风源的指向相同
# 轨迹的中点与原点的连线，与风源指向垂直
# 轨迹与云朵初始位置同直线(废话)

# 先按P0P1线段总长L和物体当前位置cloud.location求得与区域盒子的两个交汇点P0,P1，这两个点满足以下条件：
#  1. P1- P0 = L * vectorWind
#  2. (P1 + P0) @ vectorWind = 0
#  3. cloud.location = P0 + (P1-P0) * t

# 结合1，3，可以得到
# P0 = cloud.location - L * vectorWind * t
# P1 = L * vectorWind * (1-t) + cloud.location

# 再结合2，有
# (2*cloud.location - 2 * L * vectorWind * t + L * vectorWind) @ vectorWind = 0

# 设cloud.location = (x1,y1,z1), vectorWind = (x2,y2,z2)
# 有: x2 * (2x1-2t*L*X2+L*X2) + y2 * (2y1-2t*L*y2+L*y2) +z2 * (2z1-2t*L*z2+L*z2) = 0
# 2x1x2  +L* x2^2 + 2y1y2 +L* y2^2 + 2z1z2 +L* z2^2 = 2t*L(x2^2 + y2^2 + z2^2)
# t = (2x1x2  +L* x2^2 + 2y1y2 +L* y2^2 + 2z1z2 +L* z2^2) / 2L(x2^2 + y2^2 + z2^2)
# 求得t以后，就可以算出来P0和P1

# 每朵云的周期windFrame = L * Speed / windStrength  ，周期不能小于某固定值，否则太快显得不真实
#  速度应当与云朵大小成反比，所以speed = factorSpeed / (cloud.volume)

# 关于旋转：
# 旋转速度与风力强度成正比
# 旋转只需要插两个帧，就是第一帧和最后一帧，第一帧为0，最后一帧直接插FinalRotation = FactorRotations * windStrength * TotalFrames

# 关于缩放：
# 在一个缩放周期内，第一帧，中间那一帧，还有最后一帧需要插帧，插入的scale值分别为0，scaleMax，0

# 总结上面，每一个周期有三个点需要插帧，分别是第一帧，正中间那一帧，最后一帧。
# 第一帧位置为P0,缩放为0
# 中间那一帧位置为缩放为ScaleMax
# 最后一帧位置为P1，缩放为0

# 以上可以推导出当帧数为frame时，
# 云朵当前位置为P0+(P1-P0) *((frame-1) %windFrame) / windFrame
# 云朵当前的缩放值为2 * (frame% (0.5*windFrame)) * scaleMax/windFrame
# 至于旋转帧只在全局第一帧和最后一帧写入，第一帧为0，最后一帧为FinalRotation


class CloudWithWind:
    def __init__(self):
        self.factorSpeed = 1
        self.p0 = mathutils.Vector((0.0, 0.0, 0.0))
        self.p1 = mathutils.Vector((0.0, 0.0, 0.0))
        self.L = 1000
        self.vectorWind = mathutils.Vector((0, 0, 1))
        self.scaleMax = 50
        self.cloudFrame = 100
        self.minFrame = 800

    def calculateWindPrams(self, cloud, wind):
        self.vectorWind = mathutils.Vector((wind.rotation_euler[0], wind.rotation_euler[1], wind.rotation_euler[2]))
        self.vectorWind = mathutils.Euler.to_matrix(wind.rotation_euler) @ mathutils.Vector((0, 0, 1))

        self.p0 = cloud.location
        self.p1 = self.p0 + self.L * self.vectorWind

        self.cloudFrame = int((0.5 + random.random()) * self.cloudFrame)

        if self.cloudFrame < self.minFrame:
            self.cloudFrame = self.minFrame

        print('当前目标是{}, 周期值为{}'.format(cloud.name, self.cloudFrame))

    def insertKeyFrame(self, cloud, totalFrame=4000):
        """
        插入云朵在第frame帧时的位移，缩放值
        :param cloud: 需要插帧的物体
        :param totalFrame: 总帧数
        """
        initFrame = random.randint(0, self.cloudFrame)
        scaleOrg = cloud.scale[0]
        if self.cloudFrame > totalFrame:  # 云朵周期不得超过整个动画的周期
            self.cloudFrame = int(0.5 * totalFrame)
        frames = [initFrame, initFrame + int(0.5 * self.cloudFrame), initFrame + self.cloudFrame - 1]
        for i in range(3):
            frame = frames[i]
            if i == 0:
                while frame <= totalFrame:
                    bpy.context.scene.frame_set(frame)
                    cloud.location = self.p0
                    cloud.scale[0] = scaleOrg
                    cloud.scale[1] = scaleOrg
                    cloud.scale[2] = scaleOrg
                    cloud.keyframe_insert('scale')
                    cloud.keyframe_insert('location')
                    frame += self.cloudFrame
            elif i == 1:
                while frame <= totalFrame:
                    bpy.context.scene.frame_set(frame)
                    cloud.scale[0] = self.scaleMax * scaleOrg
                    cloud.scale[1] = self.scaleMax * scaleOrg
                    cloud.scale[2] = self.scaleMax * scaleOrg
                    cloud.keyframe_insert('scale')
                    frame += self.cloudFrame
            else:
                while frame <= totalFrame:
                    bpy.context.scene.frame_set(frame)
                    cloud.location = self.p1
                    cloud.scale[0] = scaleOrg
                    cloud.scale[1] = scaleOrg
                    cloud.scale[2] = scaleOrg
                    cloud.keyframe_insert('scale')
                    cloud.keyframe_insert('location')
                    frame += self.cloudFrame

        bpy.context.scene.frame_set(1)
        cloud.location = self.p0
        cloud.scale[0] = scaleOrg
        cloud.scale[1] = scaleOrg
        cloud.scale[2] = scaleOrg
        cloud.keyframe_insert('scale')
        cloud.keyframe_insert('location')

        cloud.rotation_euler = (0.0, 0.0, math.radians(initFrame))
        cloud.keyframe_insert('rotation_euler')
        cloud.keyframe_insert('location')

        bpy.context.scene.frame_set(totalFrame)
        cloud.location = self.p0.lerp(self.p1, (totalFrame + initFrame - 1) / self.cloudFrame)
        currentScale = abs(
            0.5 * self.cloudFrame - (totalFrame + initFrame) % (0.5 * self.cloudFrame)) * self.scaleMax / (
                               0.5 * self.cloudFrame) * scaleOrg
        cloud.scale[0] = currentScale
        cloud.scale[1] = currentScale
        cloud.scale[2] = currentScale
        cloud.keyframe_insert('scale')
        cloud.keyframe_insert('location')

        cloud.rotation_euler = (0.0, 0.0, math.radians(initFrame + 360))
        cloud.keyframe_insert('rotation_euler')

        return 1


wind = bpy.data.objects['Wind']

cloudWithWind = CloudWithWind()
cloudWithWind.scaleMax = 2  # 决定云朵最大变化值
cloudWithWind.L = 200  # 云朵运行的轨道长度
cloudWithWind.factorSpeed = 1  # 速度越快云的周期越短，但这个参数最终还是受最小周期值影响
cloudWithWind.minFrame = 80  # 最小周期80帧

totalFrame = 1200  # 动画总长4000帧

totalNumber = len(bpy.context.selected_objects)
count = 0
finished = 0
start = time.time()

for cloud in bpy.context.selected_objects:
    if cloud.type == 'MESH':
        cloudWithWind.calculateWindPrams(cloud, wind)
        finished += cloudWithWind.insertKeyFrame(cloud, totalFrame)
        count += 1
        print("当前进度为{:.2f}%".format(count / totalNumber * 100))

print("任务已完成，共{}个目标，完成{}个动画,总费时{:.2f}秒".format(totalNumber, finished, time.time() - start))
