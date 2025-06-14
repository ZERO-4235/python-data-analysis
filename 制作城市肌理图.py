import osmnx as ox
import matplotlib.pyplot as plt

# 经纬度范围（你可以调整以精确匹配新隆沙）
north = 23.1245
south = 23.1185
east = 113.2355
west = 113.2290

# 设置标签（如提取建筑）
tags = {"building": True}

# 用 dict 格式传入 bbox 范围
bbox = (north, south, east, west)
gdf = ox.features.features_from_bbox(*bbox, tags=tags)  # 注意这里解包并使用 tags=...

# 有些旧版本返回的是 tuple，要手动取第一个
if isinstance(gdf, tuple):
    gdf = gdf[0]

# 画图
fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(ax=ax, color="black", edgecolor=None)
ax.set_facecolor("white")
plt.axis("off")

# 保存图片
plt.savefig("新隆沙_bbox_建筑肌理图.png", dpi=300, bbox_inches='tight')