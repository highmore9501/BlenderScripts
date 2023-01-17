


def calculate_angle_betweent_end_and_target(index, chain_list, in_end_chain, in_target):
    ic = index + 1
    icc = index + 2
    cur_link = chain_list[index]
    

    # 到末端关节的向量
    to_end = in_end_chain.global_location - cur_link.global_location
    # 到目标点的向量
    to_target = in_target - cur_link.global_location

    to_end = get_nor(to_end)
    to_target = get_nor(to_target)

    # 两向量之间的夹角
    rotation_radius = np.arccos(np.dot(to_end, to_target))    

    # 旋转轴
    rotation_axis = np.cross(to_end, to_target)

    rotation_axis = get_nor(rotation_axis) 
   

    # 计算出轴和角度后，cur_link做旋转
    chain_list[ic].local_location = rotate_with_axis_angle(chain_list[ic].local_location, rotation_axis, rotation_radius)

    # cur_link旋转后，更新子链的变换信息
    chain_list[ic].global_location = chain_list[i].global_location + chain_list[ic].local_location

    for j in range(icc, tipbone_index + 1):
        print('index j', j)
        chain_list[j].global_location = chain_list[j - 1].global_location + chain_list[j].local_location

    