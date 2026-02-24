import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 设置中文字体（根据系统环境可能需要调整）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 原始数据 ----------
schools = ['清华大学', '北京大学', '复旦大学', '厦门大学',
           '上海交通大学', '同济大学', '武汉大学',
           '西安交通大学', '浙江大学', '中南大学']

# 校园文化与情感共鸣
campus_total_views = [5398000, 9713127, 2556510, 2010332, 3031763,
                      922026, 2213061, 1868302, 241226, 50175]
campus_total_likes = [145694, 219707, 41297, 45154, 45002,
                      14153, 33531, 30851, 4108, 3122]
campus_total_shares = [253901, 386758, 93245, 70915, 79501,
                       33498, 61522, 2895, 4457, 4429]
campus_total_comments = [3490, 7909, 213, 1056, 2225,
                         405, 1543, 885, 2244, 377]
campus_counts = [88, 147, 154, 86, 85, 47, 46, 105, 132, 59]

# 学术科研与学科特色
academic_total_views = [1604000, 4271455, 758140, 365768, 4073520,
                        1251595, 1862779, 841331, 242167, 897637]
academic_total_likes = [19057, 66764, 10025, 5794, 41838,
                        14325, 21304, 9725, 2413, 13004]
academic_total_shares = [34557, 166348, 28490, 9844, 103124,
                         29621, 49647, 334, 4841, 16047]
academic_total_comments = [317, 1282, 157, 102, 670,
                           63, 923, 82, 364, 508]
academic_counts = [32, 71, 51, 25, 98, 50, 51, 53, 72, 37]

# ---------- 计算平均值 ----------
campus_avg_views = np.array(campus_total_views) / np.array(campus_counts)
campus_avg_likes = np.array(campus_total_likes) / np.array(campus_counts)
campus_avg_shares = np.array(campus_total_shares) / np.array(campus_counts)
campus_avg_comments = np.array(campus_total_comments) / np.array(campus_counts)

academic_avg_views = np.array(academic_total_views) / np.array(academic_counts)
academic_avg_likes = np.array(academic_total_likes) / np.array(academic_counts)
academic_avg_shares = np.array(academic_total_shares) / np.array(academic_counts)
academic_avg_comments = np.array(academic_total_comments) / np.array(academic_counts)

# 计算篇幅占比
total_counts = [sum(campus_counts), sum(academic_counts)]
campus_ratio = sum(campus_counts) / (sum(campus_counts) + sum(academic_counts))
academic_ratio = sum(academic_counts) / (sum(campus_counts) + sum(academic_counts))

# ---------- 绘图：校园文化与情感共鸣 ----------
fig1 = plt.figure(figsize=(18, 12))

# 创建3D子图
ax1 = fig1.add_subplot(2, 3, 1, projection='3d')
ax2 = fig1.add_subplot(2, 3, 2, projection='3d')
ax3 = fig1.add_subplot(2, 3, 3, projection='3d')
ax4 = fig1.add_subplot(2, 3, 4, projection='3d')
ax5 = fig1.add_subplot(2, 3, 5, projection='3d')
ax6 = fig1.add_subplot(2, 3, 6)

x = np.arange(len(schools))  # 学校位置
y = np.zeros(len(schools))   # y坐标
z = np.zeros(len(schools))   # z坐标（底部）
dx = 0.6                      # 柱子宽度
dy = 0.6                      # 柱子深度

# 绘制校园文化与情感共鸣类的四个指标（3D柱状图）
for i in range(len(schools)):
    ax1.bar3d(x[i], y[i], z[i], dx, dy, campus_avg_views[i], color='#4C72B0', alpha=0.8)
ax1.set_title('校园文化与情感共鸣 - 平均浏览量', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax1.set_zlabel('浏览量')

for i in range(len(schools)):
    ax2.bar3d(x[i], y[i], z[i], dx, dy, campus_avg_likes[i], color='#4C72B0', alpha=0.8)
ax2.set_title('校园文化与情感共鸣 - 平均点赞量', fontsize=12)
ax2.set_xticks(x)
ax2.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax2.set_zlabel('点赞量')

for i in range(len(schools)):
    ax3.bar3d(x[i], y[i], z[i], dx, dy, campus_avg_shares[i], color='#4C72B0', alpha=0.8)
ax3.set_title('校园文化与情感共鸣 - 平均转发数', fontsize=12)
ax3.set_xticks(x)
ax3.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax3.set_zlabel('转发数')

for i in range(len(schools)):
    ax4.bar3d(x[i], y[i], z[i], dx, dy, campus_avg_comments[i], color='#4C72B0', alpha=0.8)
ax4.set_title('校园文化与情感共鸣 - 平均评论数', fontsize=12)
ax4.set_xticks(x)
ax4.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax4.set_zlabel('评论数')

# 绘制3D饼图
labels = ['校园文化与情感共鸣', '学术科研与学科特色']
sizes = [campus_ratio, academic_ratio]
colors = ['#4C72B0', '#DD8452']
explode = (0.1, 0)  # 突出显示第一块

# 创建3D饼图
ax5.axis('equal')
ax5.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
ax5.set_title('文章篇幅占比', fontsize=12)

# 隐藏第6个子图（空白）
ax6.axis('off')

plt.suptitle('各高校"校园文化与情感共鸣"类文章平均指标对比', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# 保存图片（可选）
# plt.savefig('校园文化与情感共鸣对比图.png', dpi=300, bbox_inches='tight')
plt.show()

# ---------- 绘图：学术科研与学科特色 ----------
fig2 = plt.figure(figsize=(18, 12))

# 创建3D子图
ax1_2 = fig2.add_subplot(2, 3, 1, projection='3d')
ax2_2 = fig2.add_subplot(2, 3, 2, projection='3d')
ax3_2 = fig2.add_subplot(2, 3, 3, projection='3d')
ax4_2 = fig2.add_subplot(2, 3, 4, projection='3d')
ax5_2 = fig2.add_subplot(2, 3, 5, projection='3d')
ax6_2 = fig2.add_subplot(2, 3, 6)

# 绘制学术科研与学科特色类的四个指标（3D柱状图）
for i in range(len(schools)):
    ax1_2.bar3d(x[i], y[i], z[i], dx, dy, academic_avg_views[i], color='#DD8452', alpha=0.8)
ax1_2.set_title('学术科研与学科特色 - 平均浏览量', fontsize=12)
ax1_2.set_xticks(x)
ax1_2.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax1_2.set_zlabel('浏览量')

for i in range(len(schools)):
    ax2_2.bar3d(x[i], y[i], z[i], dx, dy, academic_avg_likes[i], color='#DD8452', alpha=0.8)
ax2_2.set_title('学术科研与学科特色 - 平均点赞量', fontsize=12)
ax2_2.set_xticks(x)
ax2_2.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax2_2.set_zlabel('点赞量')

for i in range(len(schools)):
    ax3_2.bar3d(x[i], y[i], z[i], dx, dy, academic_avg_shares[i], color='#DD8452', alpha=0.8)
ax3_2.set_title('学术科研与学科特色 - 平均转发数', fontsize=12)
ax3_2.set_xticks(x)
ax3_2.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax3_2.set_zlabel('转发数')

for i in range(len(schools)):
    ax4_2.bar3d(x[i], y[i], z[i], dx, dy, academic_avg_comments[i], color='#DD8452', alpha=0.8)
ax4_2.set_title('学术科研与学科特色 - 平均评论数', fontsize=12)
ax4_2.set_xticks(x)
ax4_2.set_xticklabels(schools, rotation=45, ha='right', fontsize=8)
ax4_2.set_zlabel('评论数')

# 绘制3D饼图
labels = ['校园文化与情感共鸣', '学术科研与学科特色']
sizes = [campus_ratio, academic_ratio]
colors = ['#4C72B0', '#DD8452']
explode = (0.1, 0)  # 突出显示第一块

ax5_2.axis('equal')
ax5_2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
ax5_2.set_title('文章篇幅占比', fontsize=12)

# 隐藏第6个子图（空白）
ax6_2.axis('off')

plt.suptitle('各高校"学术科研与学科特色"类文章平均指标对比', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])

# 保存图片（可选）
# plt.savefig('学术科研与学科特色对比图.png', dpi=300, bbox_inches='tight')
plt.show()
