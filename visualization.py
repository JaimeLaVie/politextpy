# visualization.py 画图
# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import jsonlines
from wordcloud import WordCloud
from pyecharts.charts import Map,Geo

Basic_Path = os.path.split(__file__)[0]    # 定位本程序所在的文件夹，而不是调用本包的程序所在的文件夹，后者可使用os.getcwd()
font = os.path.join(Basic_Path, 'fonts', 'simfang.ttf')

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

def plotline(h, record, picname, xname, yname, picsize, file_target):
    # 绘制折线图
    y = []
    for t in h:
        y.append(float(record[t]))
    lenh = range(len(h))
    Ylim_lower = min(y)
    Ylim_upper = max(y)
    margin = 0.05 * (Ylim_upper - Ylim_lower)
    Ylim = [Ylim_lower - margin, Ylim_upper + margin]
    # print ('h = ', h)
    # print ('y = ', y)
    plt.figure(figsize=picsize)
    plt.plot(lenh, y, linewidth = 3, color = 'blue')
    plt.xticks(lenh, h, rotation = 45)
    plt.tick_params(axis='x', labelsize = 16)
    plt.tick_params(axis='y', labelsize = 25)
    plt.ylim(Ylim)
    font_x = {'family': 'Times New Roman', 'weight': 'normal', 'size': 28}
    font_y = {'family': 'Times New Roman', 'weight': 'normal', 'size': 28}
    font_title = {'family': 'Times New Roman', 'weight': 'normal', 'size': 40}
    plt.xlabel(xname, font_x)
    plt.ylabel(yname, font_y)
    plt.title(picname, font_title)
    # for a, b in zip(lenh, y):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=20)
    plt.savefig(os.path.join(file_target, "{}.jpg".format(picname)))
    plt.clf()

def plottriline(h, record1, record2, record3, picname, xname, yname, picsize, file_target, color1='blue', color2='green', color3='red', legend_loc = 'best'):
    # 绘制包含三条曲线的折线图
    # h是横坐标的具体内容的list，如日期，可以用来控制绘图的先后顺序（例如时间顺序，list里先出现的先画）；
    # record123是三条折线的数值，使用字典{}格式，字典里的每一个item都对应h里的一个值
    # picname是图中显示的标题，也是保存的文件名。xname和yname是横纵坐标的名称，Ylim是纵坐标范围，格式为[下限, 上限]
    # picsize是图片大小，格式为[长度, 宽度]，file_target是保存地址。
    y1 = []
    y2 = []
    y3 = []
    for t in h:
        y1.append(float(record1[t]))
        y2.append(float(record2[t]))
        y3.append(float(record3[t]))
    lenh = range(len(h))
    Ylim_lower = min([min(y1), min(y2), min(y3)])
    Ylim_upper = max([max(y1), max(y2), max(y3)])
    margin = 0.05 * (Ylim_upper - Ylim_lower)
    Ylim = [Ylim_lower - margin, Ylim_upper + margin]
    # print ('h = ', h)
    # print ('y = ', y)
    plt.figure(figsize = picsize)
    plt.plot(lenh, y1, linewidth = picsize[0]*picsize[1]/2500, color = color1, label = 'Positive Percentage')
    plt.plot(lenh, y2, linewidth = picsize[0]*picsize[1]/2500, color = color2, label = 'Negative Percentage')
    plt.plot(lenh, y3, linewidth = picsize[0]*picsize[1]/2500, color = color3, label = 'Overall Sentiment')
    plt.xticks(lenh, h, rotation = 45)
    plt.tick_params(axis='x', labelsize = picsize[0]*picsize[1]/520)
    plt.tick_params(axis='y', labelsize = picsize[0]*picsize[1]/100)
    plt.ylim(Ylim)
    font_x = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : picsize[0]*picsize[1]/40}
    font_y = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : picsize[0]*picsize[1]/40}
    font_title = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : picsize[0]*picsize[1]/35}
    plt.xlabel(xname, font_x)
    plt.ylabel(yname, font_y)
    plt.title(picname, font_title)
    plt.legend(loc = legend_loc, fontsize = picsize[0]*picsize[1]/150)
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

def drawwordcloud(text, file_target):
    # 绘制词云，text是以空格分开各个单词的str，也就是已经经过预处理（去除停用词和标点符号、已经英文词形还原或中文分词）的原始文本
    Wordcloud = WordCloud(background_color='white', font_path=font, collocations=False, width=1000, height=860, margin=2).generate(text)
    Wordcloud.to_file(file_target)

def drawmap(inputfile, outputfile, name, name_minor = ''):
    # 绘制交互式地图，输入文件inputfile应为jsonl格式，内容为{"China": 1943, "NotACountry": 311, "Japan": 92, "Spain": 11, "Vietnam": 9, "Thailand": 16}格式
    # 输出文件名outputfile应以.html结尾。name是文件绘制的图里显示的大标题，name_minor是小标题，默认没有
    # 本程序来源为2019中国国庆研究，这是最早使用的可视化程序
    with open(inputfile, 'r') as fi:
        for line in jsonlines.Reader(fi):
            # print (line)
            countries = list(line.keys())
            numbers = list(line.values())
            # print ("numbers: ", numbers)
            MAX = max(numbers)
            MIN = min(numbers)
            numbers_modified = []
            for i in range(len(numbers)):
                numbers_modified.append(round((numbers[i] - MIN) * 100 / (MAX - MIN)))
            # print ("numbers: ", numbers)
            # print ("numbers_modified: ", numbers_modified)
            map0 = Map(name, name_minor, width=1400, height=700)
            map0.add(name, attr = countries, value = numbers, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
            map0.add('modified to a 0-100 scale', attr = countries, value = numbers_modified, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
            map0.render(path=outputfile)

def drawreletivemap(inputfile_pos, inputfile_neg, outputfile, min_valid_number, name, name_minor = ''):
    # 基本功能同drawmap，但是会计算积极情感和消极情感在各个国家的三种比较值（差、差x50、差归一化到0-100区间）
    country_names = []
    reletive = {}
    divide = {}
    with open(inputfile_pos, 'r') as fp:
        for lp in jsonlines.Reader(fp):
            pos = lp
            for itemsp in lp:
                country_names.append(str(itemsp))
    with open(inputfile_neg, 'r') as fn:
        for ln in jsonlines.Reader(fn):
            neg = ln
            for itemsn in ln:
                if str(itemsn) not in country_names:
                    country_names.append(str(itemsn))
    for country_name in country_names:
        try:
            reletive[country_name] = pos[country_name] - neg[country_name]
            divide[country_name] = pos[country_name] / neg[country_name]
        except:
            try:
                reletive[country_name] = pos[country_name]
                if pos[country_name] > min_valid_number:
                    # divide[country_name] = 2
                    divide[country_name] = 0.99999995577455632789      # 需要绘制出归一化到0-100的图，和直接*50的图，为了程序简洁，后者在只有pos没有neg推文的情况下，
            except:                                                    # 可以与前者共享一个很奇怪的数，后面再直接赋值为100（原本也是赋值为2，后面和别的数一起*50）
                reletive[country_name] = - neg[country_name]
                if neg[country_name] > min_valid_number:
                    divide[country_name] = 0
    countries = list(reletive.keys())
    numbers = list(reletive.values())
    MAX = max(numbers)
    MIN = min(numbers)
    for i in range(len(numbers)):
        numbers[i] = round((numbers[i] - MIN) * 100 / (MAX - MIN))
    ZERO = round((0 - MIN) * 100 / (MAX - MIN))
    countries_division = list(divide.keys())
    numbers_division = list(divide.values())
    numbers_division_scaleto100 = list(divide.values())
    # for i in range(len(numbers_division)):
    #     numbers_division[i] = numbers_division[i] * 50
    MAX_d = max(numbers_division_scaleto100)
    MIN_d = min(numbers_division_scaleto100)
    assert numbers_division == numbers_division_scaleto100
    for i in range(len(numbers_division)):
        if numbers_division[i] == 0.99999995577455632789:
            numbers_division[i] = 100
            numbers_division_scaleto100[i] = 100
        else:
            numbers_division[i] = numbers_division[i] * 50
            numbers_division_scaleto100[i] = round((numbers_division_scaleto100[i] - MIN_d) * 100 / (MAX_d - MIN_d))
    ONE = round((1 - MIN_d) * 100 / (MAX_d - MIN_d))
    plan = Map(name, name_minor, width=1400, height=700)
    plan.add('minus，{}等效为中性情感'.format(ZERO), countries, numbers, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    plan.add('division，并x50，即50等效为中性情感', countries_division, numbers_division, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    plan.add('division，并归一化到0-100，{}等效为中性情感'.format(ONE), countries_division, numbers_division_scaleto100, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    plan.render(path=outputfile)

def drawheatmap(cities, air_quality):
    # 绘制热力图，该程序从未实际在我的研究里使用过，请先测试。
    geo = Geo("全国主要城市空气质量热力图", "data from pm2.5", title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
    geo.add("空气质量热力图", cities, air_quality, visual_range=[0, 25], type='heatmap',visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=False)
    # geo.show_config()
    geo.render(path="空气质量热力图.html") 

######################################################################
# 以下使用pygal绘制地图，可能比上面的方法要好看一点，但是代码稍复杂
# 本程序来源为2019中国国庆研究，这是IMITEC 2020论文中使用的可视化程序
######################################################################

country_codes = {"Russia": "ru", "Côte d'Ivoire": "ci", "Dominican Rep.": "do", "Venezuela": "ve", "Tanzania": "tz", "Vietnam": "vn", "Macedonia": "mk", "Korea": "kr",
                "Bosnia and Herz.": "ba", "Palestine": "ps", "New Caledonia": "fr", "Czech Rep.": "cz", "Iran": "ir", "Hrvatska": "hr"}

def get_country_code_pygal(country_name):
    #根据指定的国家，返回Pygal使用的两个字母的国别码
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    for name in country_codes:
        if name == country_name:
            return country_codes[name]
    print (country_name)
    return None

def TransformCountryCode_pygal(inputjson):
    outputjson = {}
    for items in inputjson:
        countryCode = get_country_code(items)
        outputjson[countryCode] = inputjson[items]
    outputjson["tw"] = outputjson["cn"]
    return outputjson

def classification_pygal(inputjson, isDivide):
    numbers = list(inputjson.values())
    if isDivide == True:
        n9 = 2
        n7 = 1.5
        n5 = 1
        n3 = 0.667
        n1 = 0.333
    else:
        MAX = max(numbers)
        MIN = min(numbers)
        n9 = round((MAX - MIN) * 0.9) + MIN
        n7 = round((MAX - MIN) * 0.7) + MIN
        n5 = round((MAX - MIN) * 0.5) + MIN
        n3 = round((MAX - MIN) * 0.3) + MIN
        n1 = round((MAX - MIN) * 0.1) + MIN
    out90, out79, out57, out35, out13, out01 = {}, {}, {}, {}, {}, {}
    for councode,num in inputjson.items():
        if num >= n9:
            out90[councode] = num
        elif num >= n7:
            out79[councode] = num
        elif num >= n5:
            out57[councode] = num
        elif num >= n3:
            out35[councode] = num
        elif num >= n1:
            out13[councode] = num
        else:
            out01[councode] = num
    return out90, out79, out57, out35, out13, out01, n9, n7, n5, n3, n1


def drawmap_pygal(inputfile, outputfile, name):
    # 绘制jpg、png地图，输入文件inputfile应为jsonl格式，内容为{"China": 1943, "NotACountry": 311, "Japan": 92, "Spain": 11, "Vietnam": 9, "Thailand": 16}格式
    # 输出文件名以.jpg、.png或.svg结尾，name是图里显示的名称
    with open(inputfile, 'r') as fi:
        for line in jsonlines.Reader(fi):
            # print (line)
            """ countries = list(line.keys())
            numbers = list(line.values()) """
            # print ("numbers: ", numbers)
            newline = TransformCountryCode(line)
            country90, country79, country57, country35, country13, country01, n9, n7, n5, n3, n1 = classification(newline, False)
            wm_style=pygal.style.RotateStyle('#D35400',base_style=pygal.style.LightColorizedStyle)
            wm = pygal_maps_world.maps.World(style = wm_style)
            wm.title = name
            wm.add('>' + str(n9), country90)
            wm.add(str(n7) + '-' + str(n9), country79)
            wm.add(str(n5) + '-' + str(n7), country57)
            wm.add(str(n3) + '-' + str(n5), country35)
            wm.add(str(n1) + '-' + str(n3), country13)
            wm.add('<' + str(n1), country01)
            wm.render_to_file(outputfile)

def drawreletivemap_pygal(inputfile_pos, inputfile_neg, outputfile, min_valid_number, name):
    # 功能基本同drawmap_pygal，只不过会对比两个量。参见drawmap_pygal()和drawreletivemap()
    country_names = []
    # reletive = {}
    divide = {}
    with open(inputfile_pos, 'r') as fp:
        for lp in jsonlines.Reader(fp):
            pos = lp
            for itemsp in lp:
                country_names.append(str(itemsp))
    with open(inputfile_neg, 'r') as fn:
        for ln in jsonlines.Reader(fn):
            neg = ln
            for itemsn in ln:
                if str(itemsn) not in country_names:
                    country_names.append(str(itemsn))
    for country_name in country_names:
        try:
            # reletive[country_name] = pos[country_name] - neg[country_name]
            divide[country_name] = pos[country_name] / neg[country_name]
        except:
            try:
                # reletive[country_name] = pos[country_name]
                if pos[country_name] > min_valid_number:
                    # divide[country_name] = 2
                    divide[country_name] = pos[country_name]
            except:                                            
                # reletive[country_name] = - neg[country_name]
                if neg[country_name] > min_valid_number:
                    divide[country_name] = 0
    # countries = list(reletive.keys())
    # numbers = list(reletive.values())
    # MAX = max(numbers)
    # MIN = min(numbers)
    # for i in range(len(numbers)):
    #     numbers[i] = round((numbers[i] - MIN) * 100 / (MAX - MIN))
    # ZERO = round((0 - MIN) * 100 / (MAX - MIN))
    # countries_division = list(divide.keys())
    # numbers_division = list(divide.values())
    newline = TransformCountryCode(divide)
    country90, country79, country57, country35, country13, country01, n9, n7, n5, n3, n1 = classification(newline, True)
    wm_style=pygal.style.RotateStyle('#D35400',base_style=pygal.style.LightColorizedStyle)
    wm = pygal_maps_world.maps.World(style = wm_style)
    wm.title = name
    wm.add('>' + str(n9), country90)
    wm.add(str(n7) + '-' + str(n9), country79)
    wm.add(str(n5) + '-' + str(n7), country57)
    wm.add(str(n3) + '-' + str(n5), country35)
    wm.add(str(n1) + '-' + str(n3), country13)
    wm.add('<' + str(n1), country01)
    wm.render_to_file(outputfile)

######################################################################
# pygal绘图结束
######################################################################


if __name__ == "__main__":
    pass