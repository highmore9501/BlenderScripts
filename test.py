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

orgName = "DEF-spine.00x.001"

proName = orgName.split(".")

print(getTGTName(orgName))

