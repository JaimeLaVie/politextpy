# topic_models.py 主题模型，包括LDA等
import os
import gensim

def lda_model(inputfile, num_topics, num_words):
    # 获得词频。输入格式是[[], [], []]，list里的每个list都是已经分过词的句子；num_topics是返回的主题个数；num_words是每个主题返回的词的个数；
    # 返回值是1：类似[(0, '0.129*"friend" + 0.129*"we" + 0.129*"all"'), (1, '0.093*"is" + 0.093*"Kitty" + 0.093*"like"')]，
    #        2：topics_words，类似[(0, ['friend', 'we', 'all']), (1, ['is', 'Kitty', 'like'])]。
    from gensim import corpora
    Lda = gensim.models.ldamodel.LdaModel

    dictionary = corpora.Dictionary(inputfile)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in inputfile]
    ldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=50)

    topics = ldamodel.show_topics(num_topics=num_topics, num_words=num_words)
    topics_words = [(tp[0], [wd.split("*")[1].replace("\"", "").replace(" ", "") for wd in tp[1].split("+")]) for tp in topics]

    return ldamodel.print_topics(num_topics=num_topics, num_words=num_words), topics_words

def lda_further(target_path, topics_words, doc, doc_split):
    # 本程序接lda_model()，保存各关键词和拥有每一类关键词最多的句子。target_path是保存路径，不只是保存的文件夹，需要写到文件名加“.txt”为止；
    # topics_words就是lda_model()返回值中的topics_words；doc是分析的文本的原文的list（['', '', '']这样的）【最好是完全未经处理的（没变小
    # 写、没去除停用词等），以便最后显示出来容易看懂】，用来保存在txt文档中，方便阅读；doc_split是doc处理后的版本，格式为[[], [], []]，同
    # lda_model()的inputfile。
    score = {}
    with open(target_path, 'w') as f:
        for topic in topics_words:
            score[str(topic[0])] = {}
            for index in range(len(doc)):
                score[str(topic[0])][doc[index]] = 0
            f.write("---------------------------\nTopic " + str(topic[0]+1) + " Keywords: ")
            for word in topic[1]:
                for i in range(len(doc_split)):
                    score[str(topic[0])][doc[i]] += doc_split[i].count(word)
                f.write(word + " ")
            key_sentence = max(score[str(topic[0])], key=score[str(topic[0])].get)    # find the sentence with the largest score.
            f.write("\nKey sentence: " + key_sentence + "\n")

if __name__ == "__main__":
    pass