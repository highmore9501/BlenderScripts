# import bpy

import numpy as np

def compute_min_bbox(points,center):
    """
    计算三维点云数据的最小包围盒
    :param points: 三维点云数据，N*3的numpy array
    :return: 最小包围盒的八个顶点坐标
    """   

    # 将points里的每个点都减去center，使得center成为坐标原点
    centered_points = []
    for point in points:
        temp = point - center
        centered_points.append([temp[0], temp[1], temp[2]])

    # 计算协方差矩阵
    cov_matrix = np.cov(centered_points)

    # 求解协方差矩阵的特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # 计算特征向量对应的最大和最小特征值的下标
    min_eigval_index = np.argmin(eigenvalues)
    max_eigval_index = np.argmax(eigenvalues)

    # 使用最大和最小特征向量构建包围盒的坐标轴
    axis1 = eigenvectors[:, max_eigval_index]
    axis2 = eigenvectors[:, min_eigval_index]
    print(axis1)
    print(axis2)
    axis3 = np.cross(axis1, axis2)

    # 计算点云数据在坐标轴上的投影坐标
    proj_points = np.dot(centered_points, np.vstack((axis1, axis2, axis3)).T)

    # 计算点云数据在不同坐标轴上的最大和最小值
    min_values = np.min(proj_points, axis=0)
    max_values = np.max(proj_points, axis=0)

    # 构建包围盒的八个顶点坐标
    bbox_points = np.empty((8, 3))
    bbox_points[0] = center + min_values[0] * axis1 + min_values[1] * axis2 + min_values[2] * axis3
    bbox_points[1] = center + min_values[0] * axis1 + min_values[1] * axis2 + max_values[2] * axis3
    bbox_points[2] = center + min_values[0] * axis1 + max_values[1] * axis2 + min_values[2] * axis3
    bbox_points[3] = center + min_values[0] * axis1 + max_values[1] * axis2 + max_values[2] * axis3
    bbox_points[4] = center + max_values[0] * axis1 + min_values[1] * axis2 + min_values[2] * axis3
    bbox_points[5] = center + max_values[0] * axis1 + min_values[1] * axis2 + max_values[2] * axis3
    bbox_points[6] = center + max_values[0] * axis1 + max_values[1] * axis2 + min_values[2] * axis3
    bbox_points[7] = center + max_values[0] * axis1 + max_values[1] * axis2 + max_values[2] * axis3

    return bbox_points

def execute():
    # 所有选中的物体
    selected_objects = bpy.context.selected_objects
    
    for object in selected_objects:
        # 如果物体是网格
        if object.type == 'MESH':
            # 保存物体的中心点坐标
            object_center_original= object.location
            
            # set origin to geometry
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            
            # 重新获取物体的中心点坐标
            object_center_new = object.location
            
            # 获取物体里所有顶点的坐标
            points = [object.matrix_world @ v.co for v in object.data.vertices] 
            
            # 给object生成最小包围盒
            bbox_points = compute_min_bbox(points, object_center_new)
            
            # 计算包围盒的长宽深
            bbox_width = np.linalg.norm(bbox_points[0] - bbox_points[1])
            bbox_height = np.linalg.norm(bbox_points[0] - bbox_points[2])
            bbox_depth = np.linalg.norm(bbox_points[0] - bbox_points[4])
            
            # 取长宽深三者中最小值，以判断哪个轴是最短的
            bbox_min = min(bbox_width, bbox_height, bbox_depth)
            
            # 如果最小值是长
            if bbox_min == bbox_width:
                #计算将point0与point1连线旋转到y轴所需要的角度
                angle = np.arctan2(bbox_points[1][2] - bbox_points[0][2], bbox_points[1][1] - bbox_points[0][1])
                #以及旋转的轴
                axis = 0
            # 如果最小值是宽
            elif bbox_min == bbox_height:
                #计算将point0与point2连线旋转到y轴所需要的角度
                angle = np.arctan2(bbox_points[2][2] - bbox_points[0][2], bbox_points[2][0] - bbox_points[0][0])
                #以及旋转的轴
                axis = 1
            # 如果最小值是深
            else:
                #计算将point0与point4连线旋转到y轴所需要的角度
                angle = np.arctan2(bbox_points[4][1] - bbox_points[0][1], bbox_points[4][0] - bbox_points[0][0])
                #以及旋转的轴
                axis = 2
            
            # 将物体沿axis轴旋转angle角度
            object.rotation_euler[axis] = angle
            
            # 将物体中心点移动到原来的位置
            object.location = object_center_original
                
def test(centered_points,center):
    # 计算协方差矩阵
    cov_matrix = np.cov(centered_points)

    # 求解协方差矩阵的特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # 计算特征向量对应的最大和最小特征值的下标
    min_eigval_index = np.argmin(eigenvalues)
    max_eigval_index = np.argmax(eigenvalues)

    # 使用最大和最小特征向量构建包围盒的坐标轴
    axis1 = eigenvectors[:, max_eigval_index]
    axis2 = eigenvectors[:, min_eigval_index]
    axis3 = np.cross(axis1, axis2)

    # 计算点云数据在坐标轴上的投影坐标
    proj_points = np.dot(centered_points, np.vstack((axis1, axis2, axis3)).T)

    # 计算点云数据在不同坐标轴上的最大和最小值
    min_values = np.min(proj_points, axis=0)
    max_values = np.max(proj_points, axis=0)

    # 构建包围盒的八个顶点坐标
    bbox_points = np.empty((8, 3))
    bbox_points[0] = center + min_values[0] * axis1 + min_values[1] * axis2 + min_values[2] * axis3
    bbox_points[1] = center + min_values[0] * axis1 + min_values[1] * axis2 + max_values[2] * axis3
    bbox_points[2] = center + min_values[0] * axis1 + max_values[1] * axis2 + min_values[2] * axis3
    bbox_points[3] = center + min_values[0] * axis1 + max_values[1] * axis2 + max_values[2] * axis3
    bbox_points[4] = center + max_values[0] * axis1 + min_values[1] * axis2 + min_values[2] * axis3
    bbox_points[5] = center + max_values[0] * axis1 + min_values[1] * axis2 + max_values[2] * axis3
    bbox_points[6] = center + max_values[0] * axis1 + max_values[1] * axis2 + min_values[2] * axis3
    bbox_points[7] = center + max_values[0] * axis1 + max_values[1] * axis2 + max_values[2] * axis3

    return bbox_points

centered_points = np.array([
    [0,5,0],
    [1,0,0],
    [3,1,0],
    [6,0,1],
    [1,1,0],
    [1,8,1],
    [0,1,10],
    [1,12,1]    
])

test(centered_points, np.array([1,1,1]))