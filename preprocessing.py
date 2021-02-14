# preprocessing.py 中英日韩文本预处理
import os
import re
import sys
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
import thulac
import jieba
import MeCab    #日语分词
mecab_tagger = MeCab.Tagger("-Owakati")

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
        self.thuseg = thulac.thulac(seg_only = True, filt = False)
        self.stopwords = []
        with open (self.basic_path + "/stopwords/stopwords_zh.txt","r", encoding = 'UTF-8') as f:
            for lines in f:
                self.stopwords.append(lines.replace("\n", ""))
    
    def punctuations_zh(self, add_punc = ''):
        punc_zh = '，。；‘’“”？《》【】（）：、\"\'#・「」' + add_punc
        return punc_zh, list(punc_zh)

    def stopwords_zh(self, add_word = []):
        # 返回列表格式的中文停用词
        try:
            assert isinstance(add_word, list)
        except:
            print("ERROR! add_word must be a list!")
            sys.exit(0)
        # self.stopwords += add_word       # 不能用这两行！因为这会直接把self.stopwords修改掉，下次再调用这个程序时，无论是否希望删除上一次添加的新停用词，这个词都会被
        # return self.stopwords            # 删掉，因为它已经被写进了self.stopwords这个在整个class中都起作用的变量。
        return self.stopwords + add_word

    def twitter_dirty_words_zh(self):
        dirty_words = ['约炮', '约 炮', '约pa', '爆乳', '情趣', '迷奸', '内射', '吞精', '吞 精', '补肾', '偷情', '强奸', '捉奸', '轮奸', '献妻', '白翘', '宠幸', '屁眼', 'AV素人', '厕拍', '肥臀', '淫水', '啪啪', '女优', '女 优', '增大增粗', '潮吹', '潮 吹', '吃屌', '吃 屌', '裸照', '裸聊', '舔秃', '名器', 'porn']
        return dirty_words

    def seg(self, text, method = 'jieba'):
        # 中文分词
        if method == 'jieba':
            text = " ".join(jieba.lcut(text))
        elif method == 'thulac':
            text = self.thuseg.cut(text, text=True)
        else:
            print('中文分词方法错误！ERROR in Chinese segmentation: Wrong method!')
            sys.exit(0)
        # print(text)
        return text

    def auto_prep(self, input, seg_method = 'jieba', add_punc = '', add_word = []):
        # 综合运用以上子程序，自动完成一切文本预处理的程序，其输入应当是str格式。也可按需要单独执行以上各子程序。
        input = delurl(input)
        output = []
        # input = input.split('。')   # 分句
        input = re.split(r'[。？！\n]', input)  # 包含所有的句子结尾可能性
        for sentence in input:
            if sentence != '':
                sentence = self.seg(sentence, method = seg_method)
                sentence = sentence.split()
                # if add_punc != '':    # 为防止新加的标点符号在分词过程中未与词分开来，而是仍然连着，使得后续无法删除。停用词是完整的词整体删除，故没有标点这样的问题。
                punc, punc_list = self.punctuations_zh(add_punc)
                punc_all = '[' + punc + ']'    # 中括号是为了后面re.split准备的，必须要有才能准确删除中括号里的标点符号。
                sentence_new = []
                for word in sentence:
                    sentence_new = sentence_new + re.split(punc_all, word)
                sentence = [word for word in sentence_new if word != '']
                delete_words = self.stopwords_zh(add_word)
                sentence = [word for word in sentence if word not in delete_words]
                output.append(sentence)
        return output

class preprocessing_en():
    def __init__(self):
        ''' Constructor for this class. '''
        # print('Perform pre-processing to English text. The input data should be a str containing sentences. Pre-processing includes 1) to\
        #         lowercase, 2) delete stopwords and punctuations.')
        self.basic_path = Basic_Path
        self.stop_words_en = stopwords.words('english')
        self.stopwords_complementary = ['', 'would', "'s"]
        self.stopwords_txt = []
        with open (self.basic_path + "/stopwords/stopwords_en.txt","r", encoding = 'UTF-8') as f:
            for lines in f:
                self.stopwords_txt.append(lines.replace("\n", ""))
        self.stopwords = self.stopwords_txt + self.stop_words_en + self.stopwords_complementary

    def punctuations_en(self, add_punc = ''):
        punc_en = string.punctuation + add_punc
        return punc_en, list(punc_en)

    def stopwords_en(self, add_word = []):
        # Return English stopwords in list format
        try:
            assert isinstance(add_word, list)
        except:
            print("ERROR! add_word must be a list!")
            sys.exit(0)
        # self.stopwords = self.stopwords + add_word                  # these three lines are the original codes. They are abandoned because they modifies
        # self.stopwords = [word.lower() for word in self.stopwords]  # self.stopwords, which means that once we add a new stop word, although we don't want 
        # return self.stopwords                                       # to delete it the next time we call this function, it will be deleted since it has 
        return [word.lower() for word in self.stopwords + add_word]   # already been added into self.stopwords. So we cannot change self.stopwords.

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

    def auto_prep(self, input, add_punc = '', add_word = []):
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
                # if add_punc != '':    # Seperate added punctuations and the word it follows, or it will not be successfully deleted in the following step.
                punc, punc_list = self.punctuations_en(add_punc)
                punc_all = '[' + punc + ']'   # '[]' is necessary for re.split, only punctuations in '[]' can be successfully deleted.
                sentence_new = []
                for word in sentence:
                    sentence_new = sentence_new + re.split(punc_all, word)
                sentence = [word for word in sentence_new if word != '']
                delete_words = self.stopwords_en(add_word)
                sentence = [word for word in sentence if word not in delete_words]
                output.append(sentence)
        return output

class preprocessing_ja():
    def __init__(self):
        ''' Constructor for this class. '''
        # print('日语文本预处理，输入应当是str格式。预处理包括：1）分词，2）删除停用词和标点符号。同时，提供中文推特里常见的色情词汇以供删除不相关推文。')
        self.basic_path = Basic_Path
        self.stopwords = []
        with open (self.basic_path + "/stopwords/stopwords_ja.txt","r", encoding = 'UTF-8') as f:
            for lines in f:
                self.stopwords.append(lines.replace("\n", ""))
    
    def punctuations_ja(self, add_punc = ''):
        punc_ja = '，。；‘’“”？《》【】（）：、\"\'#・「」\[\]' + add_punc
        return punc_ja, list(punc_ja)

    def stopwords_ja(self, add_word = []):
        # 返回列表格式的日语停用词
        try:
            assert isinstance(add_word, list)
        except:
            print("ERROR! add_word must be a list!")
            sys.exit(0)
        # self.stopwords += add_word
        return self.stopwords + add_word

    def seg(self, text):
        # 日语分词
        text = mecab_tagger.parse(text)
        return text

    def auto_prep(self, input, add_punc = '', add_word = []):
        # 综合运用以上子程序，自动完成一切文本预处理的程序，其输入应当是str格式。也可按需要单独执行以上各子程序。
        input = delurl(input)
        output = []
        # input = input.split('。')   # 分句
        input = re.split(r'[。？！\n]', input)  # 包含所有的句子结尾可能性
        for sentence in input:
            if sentence != '':
                sentence = self.seg(sentence)
                sentence = sentence.split()
                # if add_punc != '':      # 为防止新加的标点符号在分词过程中未与词分开来，而是仍然连着，使得后续无法删除。停用词是完整的词整体删除，故没有标点这样的问题。
                punc, punc_list = self.punctuations_ja(add_punc)
                punc_all = '[' + punc + ']'    # 中括号是为了后面re.split准备的，必须要有才能准确删除中括号里的标点符号。
                sentence_new = []
                for word in sentence:
                    sentence_new = sentence_new + re.split(punc_all, word)
                sentence = [word for word in sentence_new if word != '']
                delete_words = self.stopwords_ja(add_word)
                sentence = [word for word in sentence if word not in delete_words]
                output.append(sentence)
        return output

class preprocessing_ko():
    def __init__(self):
        ''' Constructor for this class. '''
        # print('Perform pre-processing to English text. The input data should be a str containing sentences. Pre-processing includes 1) to\
        #         lowercase, 2) delete stopwords and punctuations.')
        self.basic_path = Basic_Path
        self.stopwords = []
        with open (self.basic_path + "/stopwords/stopwords_ko.txt","r", encoding = 'UTF-8') as f:
            for lines in f:
                self.stopwords.append(lines.replace("\n", ""))

    def punctuations_ko(self, add_punc = ''):
        punc_ko = string.punctuation + add_punc
        return punc_ko, list(punc_ko)

    def stopwords_ko(self, add_word = []):
        # 返回列表格式的朝鲜语停用词
        try:
            assert isinstance(add_word, list)
        except:
            print("ERROR! add_word must be a list!")
            sys.exit(0)
        # self.stopwords += add_word
        return self.stopwords + add_word

    def auto_prep(self, input, add_punc = '', add_word = []):
        # Complete preprocessing automatically using all the functions above. These functions may also be used seperatly subject to needs.
        input = delurl(input)
        output = []
        # input = input.split('. ')  # change the str format sentences into a list of sentences.
        input = re.split(r'[.?!\n]', input)  # To include all possible endings.
        for sentence in input:
            if sentence != '':
                sentence = sentence.split()
                # sentence = sentence.translate(str.maketrans('', '', string.punctuation))
                # sentence = sentence.split()
                # if add_punc != '':    # Seperate added punctuations and the word it follows, or it will not be successfully deleted in the following step.
                punc, punc_list = self.punctuations_ko(add_punc)
                punc_all = '[' + punc + ']'   # 中括号是为了后面re.split准备的，必须要有才能准确删除中括号里的标点符号。
                sentence_new = []
                for word in sentence:
                    sentence_new = sentence_new + re.split(punc_all, word)
                sentence = [word for word in sentence_new if word != '']
                delete_words = self.stopwords_ko(add_word)
                sentence = [word for word in sentence if word not in delete_words]
                output.append(sentence)
        return output