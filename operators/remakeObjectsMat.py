import bpy

# 脚本目标，将所有选中的物体的材质不为principled BSDF的材质改成principled BSDF

def main():
    for obj in bpy.context.selected_objects:
        if obj.type != 'MESH':
            continue
        
        for slot in obj.material_slots:
            if slot.material.node_tree.nodes.get('Principled BSDF') is None:
                principled_node = slot.material.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
                # 查找材质中是否有Image texture节点
                texture_node = slot.material.node_tree.nodes.get('Image Texture')
                # 如果有,就新建一个Principled BSDF节点，把Image texture节点的color输出连接到Principled BSDF节点的Base Color输入
                if texture_node is not None:                    
                    slot.material.node_tree.links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])
                    # 连接Principled BSDF节点的输出到Material Output节点的Surface输入
                    slot.material.node_tree.links.new(principled_node.outputs['BSDF'], slot.material.node_tree.nodes['Material Output'].inputs['Surface'])
                    # 删除掉其它节点
                    for node in slot.material.node_tree.nodes:
                        if node != principled_node and node != slot.material.node_tree.nodes['Material Output'] and node != texture_node:
                            slot.material.node_tree.nodes.remove(node)                  
                    
                    continue
                # 如果没有，读取连接到surface的节点，查找上面是否有color属性，如果有，就复制这个颜色的值到Principled BSDF节点的Base Color输入
                surface_node = slot.material.node_tree.nodes.get('Principled BSDF')
                if surface_node is not None:
                    color = surface_node.inputs['Base Color'].default_value
                    if color is not None:
                        principled_node.inputs['Base Color'].default_value = color
                        # 连接Principled BSDF节点的输出到Material Output节点的Surface输入
                        slot.material.node_tree.links.new(principled_node.outputs['BSDF'], slot.material.node_tree.nodes['Material Output'].inputs['Surface'])
                        
                        # 删除掉其它节点
                        for node in slot.material.node_tree.nodes:
                            if node != principled_node and node != slot.material.node_tree.nodes['Material Output'] and node != texture_node:
                                slot.material.node_tree.nodes.remove(node)
            else:
                # 删除掉其图片纹理，principled BSDF节点，以及suface节点之外的所有节点
                for node in slot.material.node_tree.nodes:
                    if node != slot.material.node_tree.nodes['Material Output'] and node != slot.material.node_tree.nodes['Principled BSDF'] and node != slot.material.node_tree.nodes['Image Texture']:
                        slot.material.node_tree.nodes.remove(node)


main()