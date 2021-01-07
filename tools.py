# tools.py 一些文本处理工具，包括词频统计等
import os

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

if __name__ == "__main__":
    pass