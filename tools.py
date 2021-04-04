# tools.py 一些文本处理工具，包括词频统计、关键词提取、语言识别、TSNE降维及画图等
import os
import re
import langid    # 需要经常反复执行的程序要用到的包在这里import，偶尔执行一次的程序在程序里import包
import numpy as np
import sys

Basic_Path = os.path.split(__file__)[0]

def words_frequency(inputfile, num):
    # 获得词频。输入格式是[[], [], []]，list里的每个list都是已经分过词的句子；num是返回的最高频词的个数；返回值是一个高频词的list。
    print ("1. Calculating word frequencies...")
    wordlist = []                     # 将分过词的句子合并，即[[], [], []]变成[]。
    for i in range(len(inputfile)):
        wordlist += inputfile[i]
    counted_words = []
    words_count = {}
    for i in range(len(wordlist)):
        if wordlist[i] not in counted_words:
            counted_words.append(wordlist[i])
            words_count[wordlist[i]] = 1
            for j in range(i+1, len(wordlist)):
                if wordlist[i] == wordlist[j]:
                    words_count[wordlist[i]] += 1

    # 合并词与对应频数
    print ("2. combining words and the corresponding frequencies...")
    words = []
    counts = []
    for items in words_count:
        words.append(items)
        counts.append(words_count[items])
    combined = list(zip(words, counts))

    # 冒泡法排大小，获得未去除停用词的词频表
    print ("3. Ranking...")
    for k in range(len(combined)-1):
        for i in range(len(combined)-1):
            if combined[i][1] < combined[i+1][1]:
                variable = combined[i]
                combined[i] = combined[i+1]
                combined[i+1] = variable

    # with open (file_result[:-5] + "{}.txt".format(outputfile1), "w", encoding='utf-8') as file:
    #     file.write(str(combined))

    words_to_return = []
    for i in range(num):
        words_to_return.append(combined[i][0])

    return words_to_return

def key_word_extraction(text, target_path):
    # Key word extraction, English only. 关键词提取，仅限英文
    # target_path should contain .txt, that is, it shoule be "xxx/xxx.txt"
    # if "OSError: [E050] Can't find model 'en_core_web_sm'. It doesn't seem to be a shortcut link, a Python package or a valid path to a data directory.", then in cmd: "python -m spacy download en_core_web_sm". Or download en_core_web_sm-2.3.1.tar.gz from https://github.com/explosion/spacy-models/releases//tag/en_core_web_sm-2.3.1, and then cd to the folder of the downloaded file and execute "pip install en_core_web_sm-2.3.1.tar.gz".
    import spacy
    import pytextrank

    nlp = spacy.load("en_core_web_sm")
    tr = pytextrank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name = "textrank", last = True)
    doc = nlp(text)

    with open(target_path, "w") as f:
        for p in doc._.phrases:
            f.write("{:.4f} {:5d}  {}\n".format(p.rank, p.count, p.text))
            f.write(str(p.chunks) + "\n")

def detect_lang(text):
    # 语言分类代码见https://zh.wikipedia.org/wiki/ISO_639-1%E4%BB%A3%E7%A0%81%E8%A1%A8
    # 或https://github.com/saffsd/langid.py
    lang = str(langid.classify(text)[0])
    return lang

def tsne_value(tokens):
    from sklearn.manifold import TSNE
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)
    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    return x, y

def tsne_plot(model, chosen_words, save_path, picname, lang):
    """ 
    Creates and TSNE model and plots it
    chsen_words should be like this {'b': ['happy', 'unhappy', 'sad', 'glad'], 'r': ['fear', 'fearless'], 'c': ['angry', 'pleased', 'pleasant']}
    'b', 'r', and 'c' are the color for the chosen words. Each color represent a category. Colors can be: 'b', 'r', 'c', 'g', 'k', 'm', 'w', and 'y'.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    if lang == 'zh' or 'ja':
        from matplotlib.font_manager import FontProperties
        font_path = os.path.join(Basic_Path, "fonts", "simfang.ttf")
        font = FontProperties(fname=font_path, size=14)
    if lang == 'ko':
        from matplotlib.font_manager import FontProperties
        font_path = os.path.join(Basic_Path, "fonts", "NanumGothic.ttf")
        font = FontProperties(fname=font_path, size=14)
    
    print("Start drawing " + picname + "...")
    labels = []
    tokens = []
    chosen_words_transformed = {}

    for item in chosen_words:
        for word in chosen_words[item]:
            chosen_words_transformed[word] = item
    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)
    
    print("Start TSNE...")

    x, y = tsne_value(tokens)

    plt.figure(figsize=(16, 16))
    print('len(x) = ', len(x))
    for i in range(len(x)):
        if labels[i] in chosen_words_transformed:
            plt.scatter(x[i], y[i], s=40, c=chosen_words_transformed[labels[i]], marker='o', edgecolors='none')
            if lang != 'en':
                plt.annotate(labels[i],
                            fontproperties=font,
                            xy=(x[i], y[i]),
                            xytext=(5, 2),
                            fontsize='xx-large',
                            textcoords='offset points',
                            color=chosen_words_transformed[labels[i]],
                            ha='right',
                            va='bottom')
            else:
                plt.annotate(labels[i],
                            xy=(x[i], y[i]),
                            xytext=(5, 2),
                            fontsize='xx-large',
                            textcoords='offset points',
                            color=chosen_words_transformed[labels[i]],
                            ha='right',
                            va='bottom')
    plt.savefig(os.path.join(save_path, '{}.png'.format(picname)))
    plt.clf()

def similarity(model, word1, word2):
    # 返回相似度，此处相似度定义是余弦相似度（即gensim内置的相似度）加一（否则出现负数会改变整个值的方向）再除以两个词向量的欧氏距离（向量之差的模）
    # model是gensim中word2vec模型保存的文件，读取例如：model = word2vec.Word2Vec.load(model_path)
    sim = (model.wv.similarity(word1, word2) + 1)/np.linalg.norm(model[word1]-model[word2])
    assert sim >= 0
    return sim

def diameter(model):
    tokens = []
    for word in model.wv.vocab:
        tokens.append(model[word])
    
    longest = []
    for i in range(len(tokens) - 1):
        longest_word = []
        for j in range(i+1, len(tokens)):
            longest_word.append(np.linalg.norm(tokens[i]-tokens[j]))
        longest.append(max(longest_word))
    
    return max(longest)

def list2str(input_list):
    # 将文本预处理后[[], [], []]格式转为''。
    list_ = []
    for list in input_list:
        list_ += list
    return " ".join(list_)

def performance_measures(performance_matrix):
    # 本程序求accuracy、precision、recall和F1。输入矩阵每一行代表label，每一列代表程序判断结果。例如如下矩阵：
    #       +1   0   -1
    #   +1  179  51   1
    #    0   8  598   5
    #   -1   1   34   45
    # 作为输入矩阵，这表示标签为1，判断也为1的样本共有179个，表示标签为-1，判断也为0的样本共有34个，等。
    # 本程序输出包括一个整体的accuracy，以及针对每一个结果的precision，recall和F1。
    # 输出矩阵每一行对应输入矩阵的每一行（列）所代表的结果，第一列是precision，第二列是recall，第三列是F1。
    performance_matrix = np.array(performance_matrix)
    shape = performance_matrix.shape
    assert len(shape) == 2 and shape[0] == shape[1]
    correct_all = np.trace(performance_matrix)
    all = np.sum(performance_matrix)
    accuracy = correct_all/all
    output_matrix = np.zeros((shape[0],3))
    for i in range(shape[0]):
        tp = performance_matrix[i][i]
        fp = np.sum(performance_matrix.transpose()[i]) - tp
        fn = np.sum(performance_matrix[i]) - tp
        print (tp, fp, fn)
        output_matrix[i][0] = tp/(tp+fp)   # precision
        output_matrix[i][1] = tp/(tp+fn)      # recall
        output_matrix[i][2] = 2*tp/(2*tp + fp+ fn)  # F1
    return accuracy, output_matrix

def ymd2mdy(input):
    # 将2021_03_30日期格式改为Mar 30, 2021格式，与下面的date()配合使用。
    month_name = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    mdy_name = month_name[input.split('_')[1]] + ' ' + input.split('_')[2] + ', ' + input.split('_')[0]
    return mdy_name

def date(start_year, start_month, end_year, end_month, period = 'week', mode = 'ymd'):
    # 返回一个以指定单位（period，如周或日或月)为周期的日期列表，可用在作图的横坐标上。
    # period可选'month'、'week'、'day'，mode可选'ymd'（按2021_03_30格式返回）或'mdy'（按Mar 30, 2021格式返回）
    import calendar
    calendar.setfirstweekday(firstweekday=0)
    months = {}
    whole_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for year in range(start_year, end_year + 1):
        months[year] = whole_month.copy()
        if year == start_year:
            for i in range(len(months[year])):
                if int(months[year][i]) == start_month:
                    months[year] = months[year][i:]
                    break
        if year == end_year:
            for i in range(len(months[year])):
                if int(months[year][i]) == end_month:
                    months[year] = months[year][:i + 1]
                    break
    if period == 'month' or period == 'day':
        return_month = []
        for year in months:
            for month in months[year]:
                # print(year + '_' + month)
                month_date = calendar.monthcalendar(year, int(month))
                month_day = []
                for week in month_date:
                    for day in week:
                        if day == 0:
                            continue
                        if len(str(day)) == 1:
                            day = '0' + str(day)
                        elif len(str(day)) == 2:
                            day = str(day)
                        else:
                            print('Date ERROR!')
                            sys.exit(0)
                        month_day.append(str(year )+ '_' + month + '_' + day)
                return_month.append(month_day)
        if period == 'month':
            if mode == 'ymd':
                return return_month
            if mode == 'mdy':
                return_month_mdy = []
                for month in return_month:
                    days = []
                    for day in month:
                        days.append(ymd2mdy(day))
                    return_month_mdy.append(days)
                return return_month_mdy
        if period == 'day':
            return_day = []
            for month in return_month:
                return_day += month
            if mode == 'ymd':
                return return_day
            if mode == 'mdy':
                return_day_mdy = []
                for day in return_day:
                    return_day_mdy.append(ymd2mdy(day))
                return return_day_mdy
    if period == 'week':
        week_raw = []
        for year in months:
            for month in months[year]:
                calendar_weeks = calendar.monthcalendar(year, int(month))
                for iw in range(len(calendar_weeks)):
                    for id in range(len(calendar_weeks[iw])):
                        if len(str(calendar_weeks[iw][id])) == 1:
                            calendar_weeks[iw][id] = '0' + str(calendar_weeks[iw][id])
                        elif len(str(calendar_weeks[iw][id])) == 2:
                            calendar_weeks[iw][id] = str(calendar_weeks[iw][id])
                        else:
                            print('Date ERROR!')
                            sys.exit(0)
                for i in range(len(calendar_weeks)):
                    week_raw.append([str(year)+ '_' + month + '_' + str(day) for day in calendar_weeks[i]])
        # print(week_raw)
        return_week = []
        for i in range(len(week_raw)):
            if week_raw[i][6].split('_')[-1] == '00':
                # print(return_week[i])
                week_across_month = []
                for j in range(len(week_raw[i])):
                    if week_raw[i][j].split('_')[-1] != '00':
                        week_across_month.append(week_raw[i][j])
                    elif i != len(week_raw) - 1:
                        week_across_month.append(week_raw[i+1][j])
                    else: # 最后一周的最后几天不在本月
                        pass
                return_week.append(week_across_month)
            elif week_raw[i][0].split('_')[-1] == '00' and i == 0:
                for j in range(len(week_raw[i])):
                    if week_raw[i][j].split('_')[-1] != '00':
                        week_raw[i] = week_raw[i][j:]
                        break
                return_week.append(week_raw[i])
            elif week_raw[i][0].split('_')[-1] == '00' and i != 0:
                continue
            else:
                return_week.append(week_raw[i])
        if mode == 'ymd':
            return return_week
        if mode == 'mdy':
            return_week_mdy = []
            for week in return_week:
                days = []
                for day in week:
                    days.append(ymd2mdy(day))
                return_week_mdy.append(days)
            return return_week_mdy

if __name__ == "__main__":
    pass