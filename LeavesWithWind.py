import random

import bpy


# 假定有一片叶子，通常情况下它就是放在一个矩形图片上，带有alpha纹理。它的朝向就是图片的朝向，设为vectorLeaf.
# 再假定有一个风源，拥有windStrength,vectorWind,Noise三个参数
# 当风影响叶子时，影响的强度与vectorLeaf和vectorWind形成的夹角相关，当两者垂直时为最大，当两者平行时为0，所以可以设定：
#  rotationByWind = windFactor * windStrength * sin (angleDelta)

# 因为两矢量的夹角公式，可知cos(angleDelta) = vectorLeaf.dot(vectorWind) / (vectorLeaf.length * vectorWind.length)
# 用sin(angleDelta) = 1  -  cos(angleDelta) ^2 可求得 sin(angleDelta)

# 在世界坐标系内，叶子旋转了rotationByWind以后的方向，可以在风向与叶向之间进行线性插值求得，即
# vectorAfterRotate = VectorLeaf + sin(angleDelta) * (VectorWind - VectorLeaf)
# 当叶片晃动了1/2个周期以后会摆回来，此时的方向为VectorLeaf + sin(angleDelta) * (-VectorWind - VectorLeaf)
# 这两个值就是叶片晃动的极值，它们在叶片坐标系里的值需要用矩阵乘法，乘以叶子方向对应的旋转矩阵

# 求得了夹角以后，需要来考虑叶子晃动的周期，它与叶片的长度成正比，叶子越大来回来一次的时间越长，所以,设叶子的周期为
# leafFrame = leafFactor * leafSize.y

# 那么，在一个周期内，需要插帧的时间点有四个，分别是[1, 1+0.25*leafFrame, 1+0.5*leafFrame,,1+0.75*leafFrame]
# 对应的四个角度偏移值为[0,rotationByWind,0,-rotationByWind]

# 现在来考虑加上Noise以后的影响。Noise影响偏移的角度，所以实际的偏移角度为:
# rotationReal = rotationByWind * (1 + Random(-Noise, Noise))

# 再给每个叶子加上随机的时间初始值initFrame（不超过leafFrame)，以及每个插帧时间点的扰动（与Noise成正比，不超过1/4个leafFrame）
# 所以，每个周期的四个插帧点分别是[initFrame,initFrame+0.25*leafFrame*(1+Random(-Noise, Noise), initFrame+0.5*leafFrame*(1+0.5*Random(-Noise, Noise),initFrame+0.75*leafFrame*(1+0.33*Random(-Noise, Noise)]
# 对应的四个角度偏移值为[0, rotationReal,0,-rotationReal]


def insertKeyframe(leaf, rotationA, rotationB, noise, leafFrame, totalFrame):
    frames = [1, int(1 + 0.25 * leafFrame), 1 + 0.5 * leafFrame, 1 + 0.75 * leafFrame]
    initFrame = random.randint(-0.25 * leafFrame * noise, 0.25 * leafFrame * noise)

    for i in range(4):
        currentFrame = frames[i]
        if i == 1:
            while currentFrame < totalFrame:
                bpy.context.scene.frame_set(currentFrame + initFrame)
                leaf.rotation_euler = rotationA
                leaf.keyframe_insert('rotation_euler')
                frames += leafFrame
        elif i == 3:
            while currentFrame < totalFrame:
                bpy.context.scene.frame_set(
                    currentFrame + initFrame + int(0.25 * leafFrame * (i + (random.random() - 0.5) * noise)))
                leaf.rotation_euler = rotationB
                leaf.keyframe_insert('rotation_euler')
                frames += leafFrame
        else:
            while currentFrame < totalFrame:
                bpy.context.scene.frame_set(
                    currentFrame + initFrame + int(0.25 * leafFrame * (i + (random.random() - 0.5) * noise)))
                leaf.rotation_euler = (0.0, 0.0, 0.0)
                leaf.keyframe_insert('rotation_euler')
                frames += leafFrame

        # 最后为了省事，给第一帧和最后一帧都打上rotation为原始值
        bpy.context.scene.frame_set(1)
        leaf.rotation_euler = (0.0, 0.0, 0.0)
        leaf.keyframe_insert('rotation_euler')

        bpy.context.scene.frame_set(totalFrame)
        leaf.rotation_euler = (0.0, 0.0, 0.0)
        leaf.keyframe_insert('rotation_euler')
