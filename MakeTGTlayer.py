#  为骨骼生成TGT层，放在第27层
#   运行时要先讲所有带deform功能的骨骼都已经移动到了29层，即DEF层
#   骨骼中不要有XXX.000这种后缀为000的命名


import bpy

TGTLayer = 27


def getTGTName(orgName):
    """
    修改DEF骨骼名字到对应的TGT名字
    :param orgName:
    :return: 修改后的TGT名字
    """

    if orgName.__contains__("DEF"):
        modName = orgName.replace("DEF", "TGT")
    else:
        modName = "TGT-" + orgName  # 这里得到个性后的前缀命名，如果原名中包含DEF就把它替换成TGT，如果不包含，就直接在前面加上“TGT-”

    return modName


def changeDEF2TGT(poseBone, boneDict):
    """
    把DEF骨骼改成TGT
    :param boneDict: 骨骼名称重复次数字典
    :param poseBone: 需要进行更改的骨骼
    :return:
    """
    # 先去掉后缀，因为是复制出来的，所以必定有后缀，而且后缀必定为数字
    names = poseBone.bone.name.split(".")
    suffix = int(names[-1])  # 后缀数字
    prefix = ".".join(names[:-1])

    suffix -= boneDict[prefix]  # 去boneDict里查询前缀出现的前次，修正实际后缀数字大小

    modName = getTGTName(prefix)

    if suffix == 0:
        poseBone.bone.name = modName
    elif suffix < 10:
        poseBone.bone.name = modName + ".00" + str(suffix)
    elif suffix < 100:
        poseBone.bone.name = modName + ".0" + str(suffix)
    else:
        poseBone.bone.name = modName + "." + str(suffix)

    poseBone.bone.use_deform = False  # 去掉了deform功能



def sortBonesName():
    """
    扫描当前所有能见骨骼的名字，得到一个字典，包含前缀，以及对应的重复次数
    :return: dict[prefix:repeat]
    """
    seriesBoneNames = []
    boneDict = {}

    for poseBone in bpy.context.selected_pose_bones:
        CurrentName = poseBone.bone.name
        names = CurrentName.split(".")
        try:
            if int(names[-1]) > -1:
                seriesBoneNames.append(".".join(names[:-1]))  # 如果有后缀并且是数字，就去掉后缀，把前面的名字加到列表中
        except:
            seriesBoneNames.append(CurrentName)  # 如果后缀不是数字，直接把整个名字加到列表中


    for BonesName in seriesBoneNames:
        boneDict[BonesName] = boneDict.get(BonesName,
                                           0) + 1  # 得到了一个包含所有骨骼名称的字典boneDict，如果骨骼名字没有重复，那么对应的值为1；如果有重复，对应的值为重复次数
    return boneDict


def removeAllConstraint(ob):  #  清除目标上所有的constraints
    cl = len(ob.constraints)
    if cl != 0:
        for c in ob.constraints:
            ob.constraints.remove(c)


bpy.context.object.data.layers[29] = True

bpy.ops.object.editmode_toggle()
bpy.ops.armature.select_all(action='SELECT')

bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={"do_flip_names": False},
                                TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_axis_ortho": 'X',
                                                        "orient_type": 'GLOBAL',
                                                        "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                                        "orient_matrix_type": 'GLOBAL',
                                                        "constraint_axis": (False, False, False), "mirror": False,
                                                        "use_proportional_edit": False,
                                                        "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                                        "use_proportional_connected": False,
                                                        "use_proportional_projected": False, "snap": False,
                                                        "snap_target": 'CLOSEST', "snap_point": (0, 0, 0),
                                                        "snap_align": False, "snap_normal": (0, 0, 0),
                                                        "gpencil_strokes": False, "cursor_transform": False,
                                                        "texture_space": False, "remove_on_cancel": False,
                                                        "view2d_edge_pan": False, "release_confirm": False,
                                                        "use_accurate": False, "use_automerge_and_split": False})

# 第27层为True，如果需要改到别的层，请在这语句里修改
bpy.ops.armature.bone_layers(layers=(
False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
False, False, False, False, False, False, False, False, False, False, True, False, False, False, False))

bpy.ops.object.posemode_toggle()

bpy.context.object.data.layers[29] = True
bpy.ops.pose.select_all(action='SELECT')

#  这里我们已经切换到了原DEF层了，此时需要对所有骨骼名字先进行一次扫描，判断每个骨骼它们对应复制生成的TGT骨骼此时叫什么名字
boneDict = sortBonesName()

print(boneDict)

#  切换到TGT层，去掉所有骨骼的deform功能，并且把骨骼的名字改成TGT-原骨骼名
bpy.context.object.data.layers[27] = True
bpy.context.object.data.layers[29] = False
bpy.ops.pose.select_all(action='SELECT')

for poseBone in bpy.context.selected_pose_bones:
    changeDEF2TGT(poseBone, boneDict)

#  切换到DEF层，去掉骨骼上所有的constraint，然后全部新建对应TGT骨骼的CopyTransform:
bpy.context.object.data.layers[29] = True
bpy.context.object.data.layers[27] = False
bpy.ops.pose.select_all(action='SELECT')

for poseBone in bpy.context.selected_pose_bones:
    removeAllConstraint(poseBone)
    cs = poseBone.constraints.new('COPY_TRANSFORMS')
    cs.target = bpy.context.object
    subtargetName = getTGTName(poseBone.bone.name)
    cs.subtarget = subtargetName


