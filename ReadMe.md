## Blender Scripts


这仓库里存放的是我平时常用的一些Blender脚本，每个脚本内附有简单功能说明。

###  Blender to GameEngines
基于Youtube上的系列视频[Blender to GameEngines](https://www.youtube.com/watch?v=6nCriSbfHjc&list=PLdcL5aF8ZcJvCyqWeCBYVGKbQgrQngen3)
自己写了一些脚本用来完成其中的一些工序。具体思路以及其中一些需要手工完成的部分，还是需要去看原视频系列。

作者的基本思路是：
1. 把原有的rig分离成两个rig，一部分用来控制，一部分用来施加变形。控制的那部分骨骼没有变形功能；变形的部分只有deform功能，没有复杂的constraint。
2. 两部分只通过CopyTransform来完成关联.
3. 变形rig内的Parent-Child关系需要重构，使之简约又清晰。
4. 原有的动作，全部Bake到变形rig上。
5. 最终只输出变形rig以及Bake完成的动作到游戏引擎中。

结合作者的思路，我目前的工作流程是：
1. 选中原始rig，运行ArrangeBoneLayers.py，使所有变形骨骼都移动到第29层（因为我使用Rigify，它默认的DEF层就是29层）。
2. 切换回ObjectMode，运行makeGameRig.py。会生成一个后缀名为.GameRig的变形rig，而原始rig里的变形骨骼，所有的变形功能会被去掉。_所以，如果想恢复原来的变形功能，需要回到第29层，全选骨骼并且按alt后勾选deform。_**
3. 切换到变形rig的PoseMode，切换到变形层（默认是29层），运行checkDEFLayer.py。运行结束后，所有父系对象不是DEF骨骼会放置到第26层，方便手动来更改。
4. 前面工作完成后，可以开始Bake需要导出的动作。

未完待续....