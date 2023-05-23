import bpy
from mathutils import Matrix

import os

from bpy_extras.io_utils import ExportHelper

# 脚本目标，复制选中粒子系统所有粒子的矩阵，然后保存，以便发送给spoke

class GetParticlesMatricesOperator(bpy.types.Operator,ExportHelper):
    bl_idname = 'opr.object_get_particles_matrices_operator'
    bl_label = 'Object GetParticlesMatrices'
    bl_info = "复制选中粒子系统所有粒子的矩阵，然后保存，以便发送给spoke"
    
    # ExportHelper mixin class uses this
    filename_ext = ""

    def execute(self, context):
        # get the folder
        folder_path = os.path.dirname(self.filepath)
        file_path = os.path.join(folder_path, "{}.{}".format("partilcesMappingInfomatio", "txt"))
        context = bpy.context

        # get the depsgraph and the evaluated object   
        dg = context.evaluated_depsgraph_get()
        ob = context.object.evaluated_get(dg)
        # assume context object has a ps, use active
        ps = ob.particle_systems.active        
        
        matrices = []

        for p in ps.particles:
            # print(p.location, p.rotation, p.size)
            # make a matrix for the particles
            M = p.rotation.to_matrix().to_4x4()
            M.translation = p.location
            M[0][0] *= p.size
            M[1][1] *= p.size
            M[2][2] *= p.size
            matrices.append(M)
        
        # 导出矩阵信息到file_path
        with open(file_path, 'w') as f:
            for m in matrices:
                f.write(str(m)+'\n')                                               
        
                
        return {'FINISHED'}
        
