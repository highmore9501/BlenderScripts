import bpy

import sys

# 获取命令行参数（跳过第一个参数，因为它是脚本名称）
args = sys.argv[1:]

# 第一个参数是要导入的glb文件路径
src = args[0]
src_path = src.split("\\")[:-1]
file_name = src.split("\\")[-1]

target_name = file_name.split(".")[0] + "_animated"

if len(args) > 1:
    # 第二个参数是要导出的glb文件路径
    target = src_path + args[1]
else:
    target = src_path + target_name + ".glb"

# 打开并导入glb文件
bpy.ops.import_scene.gltf(
    filepath=src,
    files=[{"name": file_name, "name": file_name}],
    loglevel=50
)


# 将当前选中的目标重命名为AvatarRoot
bpy.context.selected_objects[0].name = "AvatarRoot"

# 如果当前物体状态不是posemode，就切换到posemode
if bpy.context.object.mode != 'POSE':
    bpy.ops.object.mode_set(mode='POSE')


if bpy.context.object.animation_data is None:
    bpy.context.object.animation_data_create()


action_list = ['idle', 'Walk', 'Run', 'Sit']

# 找到名为"Animations"的workspace
workspace = bpy.data.workspaces['Animation']
# 设置当前的workspace
bpy.context.window.workspace = workspace

for action_name in action_list:
    # 找到动画里名字包含action_list元素的动画，然后把它添加到当前物体的NLA_tracks里
    for action in bpy.data.actions:
        if action_name in action.name:
            bpy.context.object.animation_data.nla_tracks.new()
            bpy.context.object.animation_data.nla_tracks[-1].name = action_name
            bpy.context.object.animation_data.nla_tracks[-1].strips.new(
                action.name, 0, action)
            bpy.context.object.animation_data.nla_tracks[-1].strips[action.name].action_frame_start = 0
            bpy.context.object.animation_data.nla_tracks[-1].strips[
                action.name].action_frame_end = action.frame_range[1] - action.frame_range[0]
            bpy.context.object.animation_data.nla_tracks[-1].strips[action.name].frame_start = 0
            bpy.context.object.animation_data.nla_tracks[-1].strips[action.name].frame_end = action.frame_range[1] - action.frame_range[0]
            bpy.context.object.animation_data.nla_tracks[-1].strips[action.name].blend_type = 'REPLACE'
            break

# 将当前选中对象以gltf格式导出
file_path = bpy.path.abspath(target)
try:
    bpy.ops.export_scene.gltf(
        filepath=file_path,
        use_selection=True,
        export_image_format='JPEG',
        export_colors=False,
        export_tangents=True,
        export_morph=False,
        export_anim_single_armature=False
    )
except:
    pass

# 删除当前选中的对象
bpy.ops.object.delete()
