simfang.ttf是中文字体，NanumGothic.ttf是朝鲜语字体，使用这两种字体绘图的程序如下：
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"simfang.ttf", size=14)
font_ko = FontProperties(fname=r"NanumGothic.ttf", size=14)