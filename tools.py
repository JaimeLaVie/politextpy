# tools.py 一些文本处理工具，包括词频统计、关键词提取、语言识别、TSNE降维及画图等
import os
import langid    # 需要经常反复执行的程序要用到的包在这里import，偶尔执行一次的程序在程序里import包
import numpy as np

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

def tsne_plot(model, chosen_words, save_path, picname):
    """ 
    Creates and TSNE model and plots it
    chsen_words should be like this {'b': ['happy', 'unhappy', 'sad', 'glad'], 'r': ['fear', 'fearless'], 'c': ['angry', 'pleased', 'pleasant']}
    'b', 'r', and 'c' are the color for the chosen words. Each color represent a category. Colors can be: 'b', 'r', 'c', 'g', 'k', 'm', 'w', and 'y'.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
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
            plt.annotate(labels[i],
                        # fontproperties=font,
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
    assert sim > 0
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

if __name__ == "__main__":
    pass