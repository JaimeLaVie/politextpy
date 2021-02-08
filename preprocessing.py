# preprocessing.py 中英文文本预处理
import os
import string
from nltk.corpus import stopwords
stop_words_en = stopwords.words('english')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
import re
import thulac
thuseg = thulac.thulac(seg_only = True, filt = False)
import jieba

Basic_Path = os.path.split(__file__)[0]    # 定位本程序所在的文件夹，而不是调用本包的程序所在的文件夹，后者可使用os.getcwd()

def delphrase(text, phrase):
    # 删除指定语句
    for i in range (len(phrase)):
        text = text.replace(str(phrase[i]), '')
    return text

def delurl(text):
    # 识别并删除各种网址
    url = re.findall(r'http[a-zA-Z0-9\.\?\/\&\=\:\^\%\$\#\!]*', text)
    return delphrase(text, url)

class preprocessing_zh():
    def __init__(self):
        ''' Constructor for this class. '''
        # print('中文文本预处理，输入应当是str格式。预处理包括：1）分词，2）删除停用词和标点符号。同时，提供中文推特里常见的色情词汇以供删除不相关推文。')
        self.basic_path = Basic_Path
    
    def punctuations_zh(self):
        punc_zh = '，。；‘’“”？《》【】（）：、\"\'#'
        return list(punc_zh)

    def stopwords_zh(self):
        # 返回列表格式的中文停用词
        self.stopwords = []
        with open (self.basic_path + "/stopwords_zh.txt","r", encoding = 'UTF-8') as f:
            for lines in f:
                self.stopwords.append(lines.replace("\n", ""))
        return self.stopwords

    def twitter_dirty_words_zh(self):
        dirty_words = ['约炮', '约 炮', '约pa', '爆乳', '情趣', '迷奸', '内射', '吞精', '吞 精', '补肾', '偷情', '强奸', '捉奸', '轮奸', '献妻', '白翘', '宠幸', '屁眼', 'AV素人', '厕拍', '肥臀', '淫水', '啪啪', '女优', '女 优', '增大增粗', '潮吹', '潮 吹', '吃屌', '吃 屌', '裸照', '裸聊', '舔秃', '名器', 'porn']
        return dirty_words

    def seg(self, text, method = 'jieba'):
        # 中文分词
        if method == 'jieba':
            text = " ".join(jieba.lcut(text))
        elif method == 'thulac':
            text = thuseg.cut(text, text=True)
        else:
            print('中文分词方法错误！ERROR in Chinese segmentation: Wrong method!')
        # print(text)
        return text

    def auto_prep(self, input):
        # 综合运用以上子程序，自动完成一切文本预处理的程序，其输入应当是str格式。也可按需要单独执行以上各子程序。
        input = delurl(input)
        output = []
        # input = input.split('。')   # 分句
        input = re.split(r'[。？！\n]', input)  # 包含所有的句子结尾可能性
        for sentence in input:
            if sentence != '':
                sentence = self.seg(sentence)
                sentence = sentence.split()
                delete_words = self.punctuations_zh() + self.stopwords_zh()
                sentence = [word for word in sentence if word not in delete_words]
                output.append(sentence)
        return output

class preprocessing_en():
    def __init__(self):
        ''' Constructor for this class. '''
        # print('Perform pre-processing to English text. The input data should be a str containing sentences. Pre-processing includes 1) to\
        #         lowercase, 2) delete stopwords and punctuations.')
        self.basic_path = Basic_Path

    def punctuations_en(self):
        punc_en = string.punctuation
        return list(punc_en)

    def stopwords_en(self):
        # Return English stopwords in list format
        self.stopwords = []
        stopwords_complementary = ['', 'would', "'s"]
        with open (self.basic_path + "/stopwords_en.txt","r", encoding = 'UTF-8') as f:
            for lines in f:
                self.stopwords.append(lines.replace("\n", ""))
        self.stopwords = self.stopwords + stop_words_en + stopwords_complementary
        return self.stopwords

    def to_lower(self, text):
        # print('To lowercase...')
        text = [sentences.lower() for sentences in text]
        return text

    def get_wordnet_pos(self, treebank_tag):
        # 判别词性
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    def lemmatize_sentence(self, sentence):
        # Together with get_wordnet_pos(), this function performs lemmatization to sentences. 使用nltk判别词性以更准确的实现lemmatization。  
        lemmatized_output = []
        for word, pos in pos_tag(word_tokenize(sentence)):
            wordnet_pos = self.get_wordnet_pos(pos) or wordnet.NOUN
            lemmatized_output.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
        return lemmatized_output

    def auto_prep(self, input):
        # Complete preprocessing automatically using all the functions above. These functions may also be used seperatly subject to needs.
        input = delurl(input)
        output = []
        # input = input.split('. ')  # change the str format sentences into a list of sentences.
        input = re.split(r'[.?!\n]', input)  # To include all possible endings.
        input = self.to_lower(input)
        for sentence in input:
            if sentence != '':
                sentence = self.lemmatize_sentence(sentence)
                # sentence = sentence.translate(str.maketrans('', '', string.punctuation))
                # sentence = sentence.split()
                delete_words = self.punctuations_en() + self.stopwords_en()
                sentence = [word for word in sentence if word not in delete_words]
                output.append(sentence)
        return output

