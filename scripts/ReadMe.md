## Blender Scripts


这仓库里存放的是我平时常用的一些Blender脚本，每个脚本内附有简单功能说明。

### 从blender导出到引擎
基于Youtube上的系列视频[Blender to GameEngines](https://www.youtube.com/watch?v=6nCriSbfHjc&list=PLdcL5aF8ZcJvCyqWeCBYVGKbQgrQngen3) ，
自己写了一些脚本来完成其中的部分工序。具体思路以及其它需要手工完成的部分，还是需要去看原视频系列。

作者的基本思路是：
1. 把原有的rig分离成两个rig，一个用来控制，一个用来施加变形。用于控制的骨骼没有变形功能；用于变形的骨骼只有deform功能，没有复杂的constraint。
2. 两个rig通过CopyTransform来完成关联.
3. 变形rig内的Parent-Child关系需要重构，使之简约又清晰。
4. 变形rig内的面部骨骼，全部直接绑定到唯一的头部骨骼上，使它们的继承关系变得扁平，容易添加拉伸变形效果而不带来副作用。
5. 其它部分的骨骼，如果没有太大变形需求，就把原来的CopyTransform改为CopyLocation加CopyRotation，并且把连接父系的选项去掉，使之可以轻微位移，形成类似变形效果。当然这样的效果有会改变Mesh的体积，不适用于太大的变形。
6. 原有的动作，全部Bake到变形rig上。
7. 去掉变形Rig上的所有Transform，输出变形rig以及Bake好的动作到游戏引擎中。

结合作者的思路，以及自写的脚本，目前的工作流程是：

1. 选中原始rig，运行ArrangeBoneLayers.py，使所有变形骨骼都移动到第29层（因为我使用Rigify，它默认的DEF层就是29层）。
2. 切换回ObjectMode，运行makeGameRig.py。会生成一个后缀名为.GameRig的变形rig，而原始rig里的所有的变形功能会被去掉。_
   所以，如果想恢复原来的变形功能，需要回到第29层，全选骨骼并且按alt后勾选deform。_
3. 切换到变形rig的PoseMode，切换到变形层（默认是29层），运行checkDEFLayer.py。运行结束后，所有父系对象不是DEF骨骼会放置到第26层，方便手动来更改。
4. 手工重整所有骨骼继承关系，面部骨骼全部直接设置成parent为头部骨骼，其它骨骼按常规理解设置继承关系。
5. 手工添加面部骨骼CopyTransform，其它骨骼添加CopyLocation和CopyRotation，目标和次目标都设置为空
6. 手工删除所有不可选骨骼
7. 手工查找并删除所有自定义属性，所有driver
8. 运行presetDEFRig，会把所有骨骼的connected/inherit location/inherit rotation，以及bendyBone的设置自动完成
9. 前面工作完成后，可以开始Bake需要导出的动作。
10. 动作Bake完成以后，disable所有的constraint，然后导出到引擎。

### 伪造世界移动

当我们坐在一个小车上，想沿着公路绕行一个城市时，我们发现小车没有油了，它只能停在原地不动。而此时上帝给予了你移动除了小车以外的整个世界的魔力，那我们要怎么样移动整个世界，来模拟小车沿公路绕行的效果呢？

FakeWorldAnimation.py就是用于完成这类任务的脚本，具体如何使用，请结合脚本内注释来进行。

### 按材质分类

有时候我们拿到一个模型，想根据材质来对模型里的对象进行分组，这时候就是用到GroupByMaterials这个脚本的时候了

### Bake系列

当你需要批量烘焙，然后应用烘焙后UV时，可以使用以下脚本。
> AddNewUVMap：批量给对象增加名为"Bake"的UVMap
>
>RemoveBakeUV：删除所有名为"Bake"的UVMap
>
>RemoveUnBakeUV：删除所有名字不为"Bake"的UVMap
>

### 其它

CloudsWithPath：基于轨道的云朵动画
cloudsWithWind：基于风的云朵动画
exportAvatarWithArmature:批量导出人物组件与骨骼的脚本
ExportMultiGltfFiles：批量导出Gltf文件，别人的脚本，为了配合blender3.3的使用，改了里面一个参数
ParticleToAnimation：粒子动画转glb，别人的脚本





