import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False

data = pd.read_excel('data.xlsx', sheet_name=0)

# pd.set_option('display.max_columns', None)  # 设置显示最大列数
# pd.set_option('display.width', None)  # pandas设置显示宽度
# pd.set_option('display.max_colwidth', None)  # 值的最大宽度
# pd.set_option("display.max_rows", None)  # 设置显示最大行数
# np.set_printoptions(threshold=np.inf)

HandleGe = data['Constitution'].tolist()
HandleGe_new = []
for i in HandleGe:
    if i == 'good':
        HandleGe_new.append(80)
    elif i == 'general':
        HandleGe_new.append(70)
    elif i == 'bad':
        HandleGe_new.append(60)
    elif i == 'excellent':
        HandleGe_new.append(100)
    else:
        HandleGe_new.append(70)
data['Constitution'] = HandleGe_new

# 1、以课程1成绩为x轴，体能成绩为y轴，画出散点图
plt.title("以课程1成绩为x轴，体能成绩为y轴的散点图")  # 标题
plt.xlabel('课程1成绩')  # 设置坐标轴的标签
plt.ylabel('体育成绩')  # 设置坐标轴的标签

plt.xlim(xmax=100, xmin=60)  # 设置坐标轴
plt.ylim(ymax=110, ymin=50)  # 设置坐标轴

plt.scatter(data['C1'].tolist(), HandleGe_new, s=50, alpha=0.4, c='red')
plt.savefig('散点图.png', dpi=300)
plt.show()
plt.close('散点图.png')

# 2、以5分为间隔，画出课程1的成绩直方图
plt.title("课程1成绩直方图")  # 标题
plt.xlabel('课程1成绩')  # 设置坐标轴的标签
plt.ylabel('频数')  # 设置坐标轴的标签

plt.xlim(xmax=100, xmin=60)
plt.ylim(ymax=50, ymin=0)

x1 = data['C1'].tolist()
plt.hist(x1, bins=10, edgecolor='black')  # 指定绘图数据 指定直方图中条块的个数 指定直方图的边框色
# 设置y轴间隔
plt.yticks(np.arange(0, 40, 5))  # 最低 最高 间隔
plt.xticks([60, 65, 70, 75, 80, 85, 90, 95, 100])  # 根据分布频率手动设置x轴的刻度
plt.savefig('直方图.png', dpi=300)
plt.show()
plt.close('直方图.png')


# 3. 对每门成绩进行z-score归一化，得到归一化的数据矩阵。
def search2(xx):
    if xx == 'excellent':
        return 100
    elif xx == 'good':
        return 80
    elif xx == 'general':
        return 70
    elif xx == 'bad':
        return 60
    else:
        return xx


# 求数组平均数
def aveg1(xx):
    xx_list = data[xx].tolist()
    sum1 = 0
    for i in xx_list:
        sum1 += search2(i)
    average = float('%0.1f' % (sum1 / len(xx_list)))
    return average


# 求数组标准差
def fang1(xx, ave):
    xx_list = data[xx].tolist()
    sums = 0
    for iii in xx_list:
        sums = sums + pow(search2(iii) - ave, 2)
    sums = sums / (len(xx_list) - 1)
    sums = np.sqrt(sums)
    return sums


# z-score函数
def zscore(xx):
    score = data[xx].tolist()
    score_new = []
    for iiii in score:
        score_new.append((search2(iiii) - aveg1(xx)) / fang1(xx, aveg1(xx)))
    return score_new


# 构造数据矩阵
df = pd.DataFrame({'C1': zscore('C1'), 'C2': zscore('C2'),
                   'C3': zscore('C3'), 'C4': zscore('C4'),
                   'C5': zscore('C5'), 'C6': zscore('C6'),
                   'C7': zscore('C7'), 'C8': zscore('C8'),
                   'C9': zscore('C9'), 'Constitution': zscore('Constitution')})
# Dataframe转矩阵
df1 = df.values

# 输出归一化数据矩阵
print('归一化数据矩阵:\n', +df1)
np.savetxt('归一化数据矩阵.txt', df1, fmt='%f', delimiter="\t")


# 4.计算出100x100的相关矩阵，并可视化出混淆矩阵
# 求数组平均数
def get_average(records):
    return sum(records) / len(records)


# 求数组方差
def get_variance(records):
    average = get_average(records)
    return sum([(x - average) ** 2 for x in records]) / len(records)


# 求数组标准差
def get_standard_deviation(records):
    variance = get_variance(records)
    return np.math.sqrt(variance)


# 生成Datafram类型
df2 = pd.DataFrame({'C1': data['C1'], 'C2': data['C2'], 'C3': data['C3'], 'C4': data['C4'],
                    'C5': data['C5'], 'C6': data['C6'], 'C7': data['C7'], 'C8': data['C8'],
                    'C9': data['C9'], 'Constitution': data['Constitution']})

# Dataframe转矩阵
df3 = df2.values


# 相关系数函数
def CORRELATION(dfx, dfy):
    STD_df1df2 = sum([(k - get_average(dfx)) * (j - get_average(dfy)) for k, j in zip(dfx, dfy)]) / (len(dfx) - 1)
    return STD_df1df2 / (get_standard_deviation(dfx) * get_standard_deviation(dfy))


# 相关矩阵函数
def correlation_matrix(dfn):
    result = np.zeros((len(dfn), len(dfn)))
    for n in range(len(dfn)):
        for m in range(len(dfn)):
            result[n][m] = CORRELATION(dfn[n], dfn[m])
    return result


# 输出相关矩阵
corr_result = np.corrcoef(df3)
print('\n\n\n\n相关矩阵:')
print(corr_result)

# 可视化混淆矩阵
df_cm = pd.DataFrame(corr_result)  # 矩阵转DataFrame
sn.heatmap(df_cm)  # 生成混淆矩阵（用热力图方式展示）
plt.savefig('混淆矩阵.png', dpi=300)

# 输出图像
plt.show()
plt.close('混淆矩阵.png')


# 5.根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）输出到txt文件中，以\t,\n间隔。
# 100*3矩阵函数
def Nearest(df):
    value = [0, 0, 0]
    result_value = np.zeros((len(df), 3))
    result_ID = np.zeros((len(df), 3))
    for i in range(len(df)):
        temp = sorted(df[i])
        value[0], value[1], value[2] = temp[-2], temp[-3], temp[-4]
        result_value[i][0], result_value[i][1], result_value[i][2] = value[0], value[1], value[2]
        result_ID[i][0], result_ID[i][1], result_ID[i][2] = df[i].tolist().index(result_value[i][0]), df[
            i].tolist().index(result_value[i][1]), df[i].tolist().index(result_value[i][2])
    return result_ID


# 输出矩阵
print('\n\n\n\n100x3矩阵:')
print(Nearest(corr_result))

# 保存txt文件
np.savetxt('100x3矩阵.txt', Nearest(corr_result), fmt='%d', delimiter="\t")
