# visualization.py 画图
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plotbar(self, types, values, picname, top_k = 10, title = ""):
    '''
    画柱状图
    :param types: 词语
    :param values: 词语对应的频数
    :param top_k: 柱子总数
    :return:
    '''
    y_lab_seg = max(values) // 10
    # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
    plt.figure(figsize=(8, 6), dpi=600)
    #plt.figure(figsize=(max(values)//y_lab_seg + 1 * (1 if max(values) % y_lab_seg!=0 else 0), top_k//2), dpi=600)

    # 再创建一个规格为 1 x 1 的子图
    plt.subplot(1, 1, 1)

    # 包含每个柱子下标的序列
    index = np.arange(top_k)

    # 柱子的宽度
    width = 0.35

    # 绘制柱状图, 每根柱子的颜色为紫罗兰色
    p2 = plt.bar(index, values, width, label="", color="#87CEFA")

    # 设置横轴标签
    plt.xlabel('词语')
    # 设置纵轴标签
    plt.ylabel('频数')

    # 添加标题
    plt.title(title)

    # 添加纵横轴的刻度
    plt.xticks(index, types)
    plt.yticks(np.arange(0, max(values), 500))

    # 添加图例
    #plt.legend(loc="upper right")
    #plt.show()
    plt.savefig("./{}.tiff".format(picname), format='tiff')

def plotline(h, record, picname, xname, yname, Ylim, picsize, file_target):
    # 绘制折线图
    y = []
    for t in h:
        y.append(float(record[t]))
    lenh = range(len(h))
    # print ('h = ', h)
    # print ('y = ', y)
    plt.figure(figsize = picsize)
    plt.plot(lenh, y, linewidth = 3, color = 'blue')
    plt.xticks(lenh, h, rotation = 45)
    plt.tick_params(axis='x', labelsize = 16)
    plt.tick_params(axis='y', labelsize = 25)
    plt.ylim(Ylim)
    font_x = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_y = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_title = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 40}
    plt.xlabel(xname, font_x)
    plt.ylabel(yname, font_y)
    plt.title(picname, font_title)
    # for a, b in zip(lenh, y):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=20)
    plt.savefig(file_target + "/{}.jpg".format(picname))
    plt.clf()

def plottriline(h, record1, record2, record3, picname, xname, yname, Ylim, picsize, file_target):
    # 绘制包含三条曲线的折线图
    y1 = []
    y2 = []
    y3 = []
    for t in h:
        y1.append(float(record1[t]))
        y2.append(float(record2[t]))
        y3.append(float(record3[t]))
    lenh = range(len(h))
    # print ('h = ', h)
    # print ('y = ', y)
    plt.figure(figsize = picsize)
    plt.plot(lenh, y1, linewidth = 3, color = 'blue', label='Positive Percentage')
    plt.plot(lenh, y2, linewidth = 3, color = 'green', label='Negative Percentage')
    plt.plot(lenh, y3, linewidth = 3, color = 'red', label='Overall Sentiment')
    plt.xticks(lenh, h, rotation = 45)
    plt.tick_params(axis='x', labelsize = 16)
    plt.tick_params(axis='y', labelsize = 25)
    plt.ylim(Ylim)
    font_x = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_y = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_title = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 40}
    plt.xlabel(xname, font_x)
    plt.ylabel(yname, font_y)
    plt.title(picname, font_title)
    plt.legend()
    plt.savefig(file_target + "/{}.jpg".format(picname))
    plt.clf()

def draw3dpic(x, y, z, save_path, x_label = 'x', y_label = 'y', z_label = 'z'):
    """ 
    绘制三维散点图，x、y、z分别是散点的三个坐标的dataframe。本程序来源于D:\GitHub\draw3dpic\draw_pic.py，dataframe读自Excel，来源如下：
    data_frame = pd.read_excel('LCOE_data_1.xlsx',sheet_name='Sheet1')
    x = data_frame['Net Capacity Factor']
    y = data_frame['Generation Equipment']
    z = data_frame['LCOE'] 
    """
    ax = plt.subplot(111, projection='3d')
    ax.scatter(x, y, z, c='y')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
    plt.savefig(save_path)   # 例如'lcoe_pic_1.jpg'

def drawwordcloud(text, file_target):
    # 绘制词云，text是以空格分开各个单词的str，也就是已经经过预处理（去除停用词和标点符号、已经英文词形还原或中文分词）的原始文本
    from wordcloud import WordCloud
    font = basic_path + '/simfang.ttf'
    wordcloud = WordCloud(background_color="white", font_path=font, collocations=False, width=1000, height=860, margin=2).generate(text)
    wordcloud.to_file(file_target)

if __name__ == "__main__":
    pass