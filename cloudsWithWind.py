# 原理：
# 已知一个云朵初始位置cloud，一个风源，分别有风力强度WindStrength,扰动参数Noise,风向vectorWind，来计算云朵的行动轨迹。该轨迹符合以下要求：
# 轨迹的方向与风源的指向相同
# 轨迹的中点与原点的连线，与风源指向垂直
# 轨迹与云朵初始位置同直线(废话)

import math
# 先计算可以求得的系数：
#
# 先按风向windDirection和物体当前位置cloud.location求得与区域盒子的两个交汇点P0,P1，这两个点满足以下条件：
# P0 = cloud.location + t0 * vectorWind * factorSpeed * windStrength
# P1 = cloud.location + (t0 + cloudFrame) * vectorWind * factorSpeed * windStrength
# (P1+P0) 点乘 vectorWind = 0
#
# 现在来展开上面三项：
# 设Cloud.location = (x1,y1,z1), windVector = (x2,y2,z2),已知n的大小，求t0:
# （2*Cloud.location +2(t0+windFrame)vectorWind）@ VectorWind = 0
# 根据点乘公式 [x1x2+y1y2+z1z2 =0]
# 所以有：
# (x1+(t0+windFrame)x2)x2 + (y1+(t0+windFrame)y2)y2 + (z1+(t0+windFrame)z2)z2 = 0
# t0 = [x1x2+y1y2+z1z2 / (x2^2 +y2^2+z2^2)] - windFrame
#
# 所以可以在m*windFrame+1以及m*windFrame处插帧(m为大于等于0的整数)，对应的位置分别为P0,P1
#
# 关于旋转：
# 旋转速度与风力强度成正比
# 旋转只需要插两个帧，就是第一帧和最后一帧，第一帧为0，最后一帧直接插FinalRotation = FactorRotations * windStrength * TotalFrames
#
# 关于缩放：
# 缩放大小取决于Noise，设最大缩放值scaleMax = FactorScale * Noise
# 完成一次完整缩放周期需要的帧数与风力强度成反比，与云朵大小成正比，可以取
# cloudFrame = Max(object . x * object . y * object . z ) / (windStrength * factorSpeed)
# 在一个缩放周期内，第一帧，中间那一帧，还有最后一帧需要插帧，插入的scale值分别为0，scaleMax，0
#
# 总结上面，每一个周期有三个点需要插帧，分别是第一帧，正中间那一帧，最后一帧。
# 第一帧位置为P0,缩放为0
# 中间那一帧位置为0.5 *(P1 + P0)，缩放为ScaleMax
# 最后一帧位置为P1，缩放为0
# 以上可以推导出当帧数为frame时，
# 云朵当前位置为P0+(P1-P0)*（frame-1）/windFrame
# 云朵当前的缩放值为abs(0.5*windFrame - frame) * scaleMax
# 至于旋转帧只在全局第一帧和最后一帧写入，第一帧为0，最后一帧为FinalRotation
# 现在，给每一朵云增加一个随机初始帧initFrame(<windFrames),让整个动画往前平移initFrame帧，所以出当帧数为frame时：
# 云朵当前位置为P0+(P1-P0)*（frame + initFrame -1）/windFrame
# 云朵当前的缩放值为abs(0.5*windFrame - frame - initFrame) * scaleMax
# 旋转帧仍然只在全局第一帧和最后一帧写入，第一帧为0，最后一帧为FinalRotation
#
# 综上所述，一朵云需要插帧的点分别是[1,TotalFrame,initFrame,initFrame+0.5*windFrame,initFrame+windFrame-1]五处
import random
import time

import bpy
import mathutils


class CloudWithWind:
    def __init__(self):
        self.factorScale = 20
        self.factorSpeed = 1
        self.p0 = mathutils.Vector((0.0, 0.0, 0.0))
        self.p1 = mathutils.Vector((0.0, 0.0, 0.0))
        self.cloudFrame = 100
        self.vectorWind = mathutils.Vector((0, 0, 1))
        self.scaleMax = 50

    def calculateWindPrams(self, cloud, wind):
        self.vectorWind = mathutils.Vector((wind.rotation_euler[0], wind.rotation_euler[1], wind.rotation_euler[2]))
        self.vectorWind = mathutils.Euler.to_matrix(wind.rotation_euler) @ mathutils.Vector((0, 0, 1))
        self.cloudFrame = 100 * int(max(cloud.dimensions.x, cloud.dimensions.y, cloud.dimensions.z) / (
                self.factorSpeed * wind.field.strength))
        if self.cloudFrame < 1500:   # 云朵周期太短会不真实，所以小于1500的强制设置为1500帧
            self.cloudFrame = 1500
        cloudLocation = cloud.location
        x1 = cloudLocation[0]
        y1 = cloudLocation[1]
        z1 = cloudLocation[2]
        x2 = self.vectorWind[0]
        y2 = self.vectorWind[1]
        z2 = self.vectorWind[2]
        t0 = (x1 * x2 + y1 * y2 + z1 * z2 / (x2 * x2 + y2 * y2 + z2 * z2)) - self.cloudFrame

        self.p0 = cloudLocation + t0 * self.vectorWind * self.factorSpeed * wind.field.strength
        self.p1 = cloudLocation + (t0 + self.cloudFrame) * self.vectorWind * self.factorSpeed * wind.field.strength

        self.scaleMax = self.factorScale * wind.field.noise
        print('当前云朵是{},它的P0值是{},P1值是{},周期帧数是{},最大变化值是{}'.format(cloud.name, self.p0, self.p1,
                                                                                      self.cloudFrame, self.scaleMax))

    def insertKeyFrame(self, cloud, totalFrame=4000):
        """
        插入云朵在第frame帧时的位移，缩放值
        :param cloud: 需要插帧的物体
        :param totalFrame: 总帧数
        """
        initFrame = random.randint(0, int(0.5 * self.cloudFrame))
        frames = [initFrame, initFrame + int(0.5 * self.cloudFrame), initFrame + self.cloudFrame - 1]
        for i in range(3):
            frame = frames[i]
            if i == 0:
                while frame <= totalFrame:
                    bpy.context.scene.frame_set(frame)
                    cloud.location = self.p0
                    cloud.scale[0] = 0
                    cloud.scale[1] = 0
                    cloud.scale[2] = 0
                    cloud.keyframe_insert('scale')
                    cloud.keyframe_insert('location')
                    frame += self.cloudFrame
            elif i == 1:
                while frame <= totalFrame:
                    bpy.context.scene.frame_set(frame)
                    cloud.scale[0] = self.scaleMax
                    cloud.scale[1] = self.scaleMax
                    cloud.scale[2] = self.scaleMax
                    cloud.keyframe_insert('scale')
                    frame += self.cloudFrame
            else:
                while frame <= totalFrame:
                    bpy.context.scene.frame_set(frame)
                    cloud.location = self.p1
                    cloud.scale[0] = 0
                    cloud.scale[1] = 0
                    cloud.scale[2] = 0
                    cloud.keyframe_insert('scale')
                    cloud.keyframe_insert('location')
                    frame += self.cloudFrame

        for frame in [1, totalFrame]:
            bpy.context.scene.frame_set(frame)
            cloud.location = self.p0.lerp(self.p1, (frame + initFrame - 1) / self.cloudFrame)
            currentScale = abs(
                0.5 * self.cloudFrame - (frame + initFrame) % (0.5 * self.cloudFrame)) * self.scaleMax / (
                                   0.5 * self.cloudFrame)
            cloud.scale[0] = currentScale
            cloud.scale[1] = currentScale
            cloud.scale[2] = currentScale
            cloud.keyframe_insert('scale')
            cloud.keyframe_insert('location')
            frame += self.cloudFrame

        bpy.context.scene.frame_set(1)
        cloud.keyframe_insert('rotation_euler')
        bpy.context.scene.frame_set(totalFrame)
        cloud.rotation_euler = (0.0, 0.0, math.radians(360))
        cloud.keyframe_insert('rotation_euler')

        return 1


wind = bpy.data.objects['Wind']
windStrength = wind.field.strength
noise = wind.field.noise
totalFrame = 4000

cloudWithWind = CloudWithWind()
cloudWithWind.factorScale = 20  # 决定云朵最大变化值
cloudWithWind.factorSpeed = 1  # 速度越快云的周期越短
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
