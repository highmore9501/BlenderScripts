import bpy
import os

from mathutils import Matrix

from bpy_extras.io_utils import ExportHelper,axis_conversion

# 脚本目标，复制选中物体的矩阵，然后保存，以便发送给spoke

class GetSelectedObjectsMatricesOperator(bpy.types.Operator,ExportHelper):
    bl_idname = 'opr.object_get_selected_objects_matrices_operator'
    bl_label = 'Object GetSelectedObjectsMatrices'
    bl_info = "复制所有选中物体的矩阵，然后保存，以便发送给spoke"
    
    # ExportHelper mixin class uses this
    filename_ext = ""
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        
        # get the folder
        folder_path = os.path.dirname(self.filepath)
        file_path = os.path.join(folder_path, "{}.{}".format("SelectedObjectMatrices", "txt")) 
        
        blender_to_three_matrix = axis_conversion(from_forward='Y', from_up='Z', to_forward='-Z', to_up='Y')
        # 把blender_to_three_matrix转换为4x4矩阵
        blender_to_three_matrix = Matrix(blender_to_three_matrix.to_4x4())
        
        matrices = []
        
        for ob in objects:
            # 选择的物体必须是mesh
            if ob.type != 'MESH':
                continue
            
            # 读取物体的矩阵
            mat = ob.matrix_world
            # 转换为threejs的坐标系
            mat = blender_to_three_matrix @ mat
            matrices.append(mat)
            
        # 导出矩阵信息到file_path
        with open(file_path, 'w') as f:
            for m in matrices:
                f.write(str(m)+'\n')
        
        return {'FINISHED'}
            
    