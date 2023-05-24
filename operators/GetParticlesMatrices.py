import bpy
from mathutils import Matrix
import os

from bpy_extras.io_utils import ExportHelper,axis_conversion

# 脚本目标，复制选中粒子系统所有粒子的矩阵，然后保存，以便发送给spoke

class GetParticlesMatricesOperator(bpy.types.Operator,ExportHelper):
    bl_idname = 'opr.object_get_particles_matrices_operator'
    bl_label = 'Object GetParticlesMatrices'
    bl_info = "复制选中粒子系统所有粒子的矩阵，然后保存，以便发送给spoke"
    
    # ExportHelper mixin class uses this
    filename_ext = ""

    def execute(self, context):  
        # get the depsgraph and the evaluated object   
        dg = context.evaluated_depsgraph_get()
        ob = context.object.evaluated_get(dg)
        # assume context object has a ps, use active
        ps = ob.particle_systems.active     
        
        # get the folder
        folder_path = os.path.dirname(self.filepath)
        file_path = os.path.join(folder_path, "{}{}.{}".format(ps.name,"PartilcesInfo", "txt"))  
        
        blender_to_three_matrix = axis_conversion(from_forward='Y', from_up='Z', to_forward='-Z', to_up='Y')
        # 把blender_to_three_matrix转换为4x4矩阵
        blender_to_three_matrix = Matrix(blender_to_three_matrix.to_4x4())
        matrices = []

        for p in ps.particles:    
                    
            mat_loc = Matrix.Translation(p.location)           
            mat_rot = p.rotation.to_matrix().to_4x4()            
            mat_sca = Matrix.Scale(p.size, 4)            
            mat = blender_to_three_matrix @ mat_loc @ mat_rot @ mat_sca            
            matrices.append(mat)
        
        # 导出矩阵信息到file_path
        with open(file_path, 'w') as f:
            for m in matrices:
                f.write(str(m)+'\n')                                               
        
                
        return {'FINISHED'}
        
