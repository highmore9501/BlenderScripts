# 去掉顶点组中所有权重为0的顶点组，用来清理刷好骨骼权重后的物体，运行时需在ObjectMode下选中要清理的物体

import bpy

def survey(obj):
    maxWeight = {}
    for i in obj.vertex_groups:
        maxWeight[i.index] = 0

    for v in obj.data.vertices:
        for g in v.groups:
            gn = g.group
            w = obj.vertex_groups[g.group].weight(v.index)
            if (maxWeight.get(gn) is None or w>maxWeight[gn]):
                maxWeight[gn] = w
    return maxWeight

obj = bpy.context.active_object
maxWeight = survey(obj)
# fix bug pointed out by user2859
ka = []
ka.extend(maxWeight.keys())
ka.sort(key=lambda gn: -gn)
print (ka)
for gn in ka:
    if maxWeight[gn]<=0:
        print ("delete %d"%gn)
        obj.vertex_groups.remove(obj.vertex_groups[gn]) # actually remove the group
