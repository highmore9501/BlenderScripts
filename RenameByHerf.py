import bpy
import re

# 脚本目标，将所有选中的物体。如果上面有加载hubs的图片插件，则根据图片插件里的herf值来重新命名为Position_XX


class RenameByHerfOperator(bpy.types.Operator):
    bl_idname = 'opr.object_rename_by_herf_operator'
    bl_label = 'Object RenameByHerf'    

    def execute(self, context):
        for item in bpy.context.selected_objects:
            try:    # https://api.xvr.art/api/v1/space/assets/getter?sid=91&position=18&type=image
                if item.hubs_component_image.src != 'https://mozilla.org':
                    src = item.hubs_component_image.src
                else:   
                    src = item.hubs_component_link.href
                position = re.findall(r"position=(.+?)&type",src)[0] or src.split("position=")[1]                
                item.name = "Position_{}".format(position)
            except:
                pass

        return {'FINISHED'}
