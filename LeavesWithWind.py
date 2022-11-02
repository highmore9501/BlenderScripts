import math
import random
import time

import bpy
import mathutils


# 假定有一片叶子，通常情况下它就是放在一个矩形图片上，带有alpha纹理。它的朝向就是图片的朝向，设为vectorLeaf.
# 再假定有一个风源，拥有windStrength,vectorWind,Noise三个参数,windStrength大于0小于10，Noise大于0于小0.25。
# 当风影响叶子时，影响的强度与vectorLeaf和vectorWind形成的夹角相关，当两者垂直时为最大，当两者平行时为0，所以实际上被风吹以后的矢量就是介于vectorWind和VectorLeaf之间的一个插值，插值的系数是当前风力强度:
#  vectorLeafMax = vectorLeaf + ( vectorWind - VectorLeaf) * windStrength / 10
# 当叶子弹回来以后，叶子的矢量为VectorLeafMin = vectorLeaf + (-vectorWind - VectorLeaf) * windStrength / 10

# 求得了叶子在两端的极值以后，需要来考虑叶子晃动的周期，它与叶片的大小成正比，叶子越大来回来一次的时间越长，所以,设叶子的周期为
# leafFrame = leafFactor * leafSize.y * leafSize.x * leafSize.z

# 那么，在一个周期内，需要插帧的时间点有四个，分别是[1, 1+0.25*leafFrame, 1+0.5*leafFrame, 1+0.75*leafFrame]
# 对应的四个角度偏移值为[VectorLeaf,vectorLeafMax,VectorLeaf,VectorLeafMin]

# 现在来考虑加上Noise以后的影响，Noise设定为大于0小于1/4的一个值。Noise影响偏移的角度，所以实际的偏移角度为:
# vectorLeafReal = CurrentVectorLeaf * (1 + Random(-Noise, Noise))

# 再给每个叶子加上随机的时间初始值initFrame（不超过leafFrame)，以及每个插帧时间点的扰动（与Noise成正比，不超过1/4个leafFrame）
# 所以，每个周期的四个插帧点分别是[initFrame,initFrame+0.25*leafFrame*(1+Random(-Noise, Noise), initFrame+0.5*leafFrame*(1+0.5*Random(-Noise, Noise),initFrame+0.75*leafFrame*(1+0.33*Random(-Noise, Noise)]
# 对应的四个角度偏移值为[VectorLeaf,vectorLeafMax,VectorLeaf,VectorLeafMin]

# 至于全局第一帧和最后一帧的角度，为了省事，全都设置为VectorLeaf

# 现在，加上缩放的考量。在叶子处于两端极值时，Z轴方向上的缩放为1+0.25*windStrength*0.1，也就是说缩放的极限为原大小的1.25倍。在其它插值点上，缩放值均为1.


class LeafWithWind:

    def __init__(self, totalFrame=1000):
        self.noise = 0.25
        self.vectorLeaf = mathutils.Vector((0, 0, 1))
        self.vectorWind = mathutils.Vector((0, 0, 1))
        self.leafFrame = 1
        self.totalFrame = totalFrame
        self.vectorLeafMax = mathutils.Vector((0, 0, 1))
        self.vectorLeafMin = mathutils.Vector((0, 0, 1))
        self.scaleMax = 1
        self.scaleInit = 1

    def calculateParms(self, leaf, wind, leafFrameFactor=1, windStrength=1):
        x = leaf.dimensions.x
        y = leaf.dimensions.y
        z = leaf.dimensions.z
        self.leafFrame = int(leafFrameFactor * max([x, y, z]))
        self.vectorLeaf = mathutils.Vector((leaf.rotation_euler[0], leaf.rotation_euler[1], leaf.rotation_euler[2]))
        self.vectorWind = mathutils.Vector((wind.rotation_euler[0], wind.rotation_euler[1], wind.rotation_euler[2]))
        self.vectorWind = mathutils.Euler.to_matrix(wind.rotation_euler) @ mathutils.Vector((0, 0, 1))

        self.vectorLeafMax = self.vectorLeaf.lerp(self.vectorWind, windStrength * 0.1)
        self.vectorWind.negate()
        self.vectorLeafMin = self.vectorLeaf.lerp(self.vectorWind, windStrength * 0.1)
        self.scaleInit = leaf.scale[2]
        self.scaleMax = (1 + 0.25 * windStrength * 0.1) * self.scaleInit
        self.noise = 0.25 * windStrength * 0.1
        if self.leafFrame > 0.5 * self.totalFrame:  # 幅度不能太大，至少也要在一个周期内来回摆动一次
            self.leafFrame = int(0.5 * self.totalFrame)

    def insertKeyframe(self, leaf):
        frames = [1, int(1 + 0.25 * self.leafFrame), int(1 + 0.5 * self.leafFrame), int(1 + 0.75 * self.leafFrame),
                  self.leafFrame]
        initFrame = random.randint(int(-self.leafFrame * self.noise * 0.25), int(self.leafFrame * self.noise * 0.25))

        if self.leafFrame > 5:  # 太小的叶子不做动画，不然会有一批小叶子差不多同频率振动看上去很奇怪
            for i in range(0, 4):
                currentFrame = frames[i]
                while currentFrame < self.totalFrame:
                    if i == 0 or i == 4:
                        bpy.context.scene.frame_set(currentFrame + initFrame)
                        leaf.rotation_euler = self.vectorLeaf
                        leaf.scale[2] = self.scaleInit
                        leaf.keyframe_insert('scale')
                        leaf.keyframe_insert('rotation_euler')
                        currentFrame += self.leafFrame
                    elif i == 1:
                        bpy.context.scene.frame_set(
                            currentFrame + initFrame + int(
                                0.25 * self.leafFrame * (1 + (random.random() - 0.5) * self.noise)))
                        leaf.rotation_euler = self.vectorLeafMax
                        leaf.scale[2] = self.scaleMax
                        leaf.keyframe_insert('scale')
                        leaf.keyframe_insert('rotation_euler')
                        currentFrame += self.leafFrame
                    elif i == 2:
                        bpy.context.scene.frame_set(
                            currentFrame + initFrame + int(
                                0.25 * self.leafFrame * (1 + (random.random() - 0.5) * self.noise)))
                        leaf.rotation_euler = self.vectorLeaf
                        leaf.scale[2] = self.scaleInit
                        leaf.keyframe_insert('scale')
                        leaf.keyframe_insert('rotation_euler')
                        currentFrame += self.leafFrame
                    else:
                        bpy.context.scene.frame_set(
                            currentFrame + initFrame + int(
                                0.25 * self.leafFrame * (1 + (random.random() - 0.5) * self.noise)))
                        leaf.rotation_euler = self.vectorLeafMin
                        leaf.scale[2] = self.scaleMax
                        leaf.keyframe_insert('scale')
                        leaf.keyframe_insert('rotation_euler')
                        currentFrame += self.leafFrame

            # 偷懒不可取，重新计算了公式以后，给出第一帧和最后一帧的值，这两个值取一样，方便动画循环
            for frame in [1, self.totalFrame]:
                bpy.context.scene.frame_set(frame)
                leaf.rotation_euler = self.vectorLeafMin + (self.vectorLeafMax - self.vectorLeafMin) * (
                        0.5 - 0.5 * math.sin(2 * 3.14159 * (1 - initFrame) / self.totalFrame))
                leaf.scale[2] = self.scaleInit + (self.scaleMax - self.scaleInit) * (
                        (1 - initFrame) % int(0.5 * self.totalFrame)) / int(
                    0.5 * self.totalFrame)
                leaf.keyframe_insert('scale')
                leaf.keyframe_insert('rotation_euler')

            return 1
        else:
            return 0


wind = bpy.data.objects['Wind']
windStrength = wind.field.strength
noise = wind.field.noise
totalFrame = 400
leafFrameFactor = 100
leafWithWind = LeafWithWind(totalFrame=totalFrame)
totalNumber = len(bpy.context.selected_objects)
count = 0
finished = 0
start = time.time()

for leaf in bpy.context.selected_objects:
    if leaf.type == 'MESH':
        leafWithWind.calculateParms(leaf, wind, leafFrameFactor, windStrength)
        finished += leafWithWind.insertKeyframe(leaf)
        count += 1
        print("当前进度为{:.2f}%".format(count / totalNumber * 100))

print("任务已完成，共{}个目标，完成{}个动画,总费时{:.2f}秒".format(totalNumber, finished, time.time() - start))
