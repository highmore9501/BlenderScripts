# 原理：
# 已知一个云朵初始位置cloud，一个风源，分别有风力强度WindStrength,扰动参数Noise,风向vectorWind，来计算云朵的行动轨迹。该轨迹符合以下要求：
# 轨迹的方向与风源的指向相同
# 轨迹的中点与原点的连线，与风源指向垂直
# 轨迹与云朵初始位置同直线(废话)

# 先计算可以求得的系数：
# 风速，也就是轨迹p0运动到p1需要的帧数，windFrame与风力强度成正比，与云朵体积成反比
# 所以windFrame= FactorSpeed * windStrength / (cloudSize.x * cloudSize.y  * cloudSize.z  )
#
# 先按风向windDirection和物体当前位置cloud.location求得与区域盒子的两个交汇点P0,P1，这两个点满足以下条件：
# P0 = cloud.location + t0 * vectorWind
# P1 = cloud.location + (t0 + windFrame) * vectorWind
# (P1+P0) 点乘 vectorWind = 0
#
# 现在来展开上面三项：
# 设Cloud.location = (x1,y1,z1), windVector = (x2,y2,z2),已知n的大小，求t0:
# （2*Cloud.location +2(t0+windFrame)vectorWind）@ VectorWind = 0
# 根据点乘公式 [x1x2+y1y2+z1z2 =0]
# 所以有：
# (x1+(t0+windFrame)x2)x2 + (y1+(t0+windFrame)y2)y2 + (z1+(t0+windFrame)z2)z2 =0
# t0 = [x1x2+y1y2+z1z2 / (x2^2 +y2^2+z2^2)] - windFrame
#
# 所以可以在m*windFrame+1以及m*windFrame处插帧(m为大于等于0的整数)，对应的位置分别为P0,P1.
#
# 增加位移的随机性：
# 根据风的Noise参数，增加额外的插帧点，
# Noise=0,无插帧点
# Noise>0时，插帧点数量为int(10*noise)+1，这些点将轨迹平分为int(10*Noise)+2段
#
# 第N个插帧点的位置是int(1 + N * windFrame / (int(10*noise)+2)),插入一个与Noise成正比的位移偏差值vector3(random(Noise * FactorOffset))
# 对应的，在插帧点+N*windFrame处也可以继续插帧，直到超出时间限制为止
#
# 关于旋转：
# 旋转速度与风力强度成正比
# 旋转只需要插两个帧，就是第一帧和最后一帧，第一帧为0，最后一帧直接插FinalRotation = FactorRotations * windStrength * TotalFrames
#
# 关于缩放：
# 缩放大小取决于Noise，设最大缩放值scaleMax = FactorScale * Noise
# 完成一次完整缩放周期需要的帧数与风力强度成反比，与云朵大小成正比，可以取
# ScaleOffsetFrame = FactorScaleSpeed *  (object . x * object . y * object . z ) / windStrength
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

# 现在，给每一朵云增加一个随机初始帧initFrame(<cycleFrames),让整个动画往前平移initFrame帧，所以出当帧数为frame时：
# 云朵当前位置为P0+(P1-P0)*（frame + initFrame -1）/windFrame
# 云朵当前的缩放值为abs(0.5*windFrame - frame - initFrame) * scaleMax
# 旋转帧仍然只在全局第一帧和最后一帧写入，第一帧为0，最后一帧为FinalRotation
#
# 综上所述，一朵云需要插帧的点分别是[1,TotalFrame,initFrame,initFrame+0.5*windFrame,initFrame+windFrame-1]五处
import bpy
import math


def insertKeyFrame(obj, frame, P0, P1, windFrame=1000, totalFrame=4000, initFrame=0, scaleMax=50):
    """
    插入云朵在第frame帧时的位移，缩放值
    :param obj: 需要插帧的物体
    :param frame: 需要插入的第几帧
    """
    while frame < totalFrame:
        bpy.context.scene.frame_set(frame)
        obj.location = P0 + (P1-P0) * (frame + initFrame - 1) / windFrame
        currentScale = abs(0.5 * windFrame - frame - initFrame) * scaleMax
        obj.scale[0] = currentScale
        obj.scale[1] = currentScale
        obj.scale[2] = currentScale
        obj.keyframe_insert('scale')
        obj.keyframe_insert('location')
        frame += windFrame

