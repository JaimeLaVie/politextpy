# country_code.py 将文本中的各种国家的各种称谓统一

# 以下国家编码参照ISO 3166-1标准，见https://zh.wikipedia.org/wiki/ISO_3166-1
# 包含：世界主要国家（联合国常任理事国、G7、G20、OECD国家）+与中国关系密切国家（上合组织成员国（含观察员）、东盟成员国、朝鲜）。

dictionary = {
    # 中文国家名词典
    'dictionary_zh': {
        '中国': 'cn', '中國': 'cn', '中华人民共和国': 'cn', '中華人民共和國': 'cn', '中華人民共和国': 'cn',
        '日本国':'jp', '日本國':'jp', '日本':'jp',             # 包含短名称的长名称在前，优先识别，避免出现"countrynamejp国"的情况
        '韩国': 'kr', '韓國': 'kr', '韓国': 'kr', '大韩民国': 'kr', '大韓民國': 'kr', '大韓民国': 'kr', '南朝鲜': 'kr', '南朝鮮': 'kr', '南韩': 'kr',
        '朝鲜民主主义人民共和国': 'kp', '北朝鲜': 'kp', '朝鲜': 'kp', '朝鮮民主主義人民共和國': 'kp', '北朝鮮': 'kp', '朝鮮': 'kp', '北韩': 'kp',
        '印度尼西亚': 'id', '印度尼西亞': 'id', '印尼': 'id',
        '马来西亚': 'my', '馬來西亞': 'my',
        '菲律宾': 'pl', '菲律賓': 'pl',
        '泰国': 'th', '泰國': 'th',
        '新加坡': 'sg',
        '文莱': 'bn', '文萊': 'bn',
        '柬埔寨': 'kh',
        '老挝':'la', '寮國':'la',
        '缅甸': 'mm', '緬甸': 'mm',
        '越南': 'vn',
        '印度': 'in',
        '巴基斯坦': 'pk', '巴铁': 'pk',
        '哈萨克斯坦': 'kz', '哈薩克斯坦': 'kz',
        '吉尔吉斯斯坦': 'kg', '吉爾吉斯斯坦': 'kg',
        '塔吉克斯坦': 'tj', 'Tajikistan': 'tj', 
        '乌兹别克斯坦': 'uz', '烏茲別克斯坦': 'uz',
        '阿富汗': 'af',
        '伊朗': 'ir',
        '蒙古': 'mn',
        '土耳其': 'tr',
        '沙特': 'sa',
        '以色列': 'il',
        '英国': 'uk', '英國': 'uk', '英议会': 'uk',
        '法国': 'fr', '法國': 'fr',
        '德国': 'de', '德國': 'de',
        '意大利': 'it',
        '奥地利': 'at', '奧地利': 'at',
        '比利时': 'be', '比利時': 'be',
        '丹麦': 'dk', '丹麥': 'dk',
        '希腊': 'gr', '希臘': 'gr',
        '冰岛': 'is', '冰島': 'is',
        '爱尔兰': 'ie', '愛爾蘭': 'ie',
        '卢森堡': 'lu', '盧森堡': 'lu',
        '荷兰': 'nl', '荷蘭': 'nl',
        '挪威': 'no',
        '葡萄牙': 'pt',
        '西班牙': 'es',
        '瑞典': 'se',
        '瑞士': 'ch',
        '芬兰': 'fi', '芬蘭': 'fi',
        '捷克': 'cz',
        '匈牙利': 'hu',
        '波兰': 'pl', '波蘭': 'pl',
        '斯洛伐克': 'sk',
        '斯洛文尼亚': 'si', '斯洛文尼亞': 'si',
        '爱沙尼亚': 'ee', '愛沙尼亞': 'ee',
        '拉脱维亚': 'lv', '拉脫維亞': 'lv',
        '立陶宛': 'lt',
        '俄罗斯': 'ru', '俄羅斯': 'ru',
        '白俄罗斯': 'by', '白罗斯': 'by', '白俄羅斯': 'by', '白羅斯': 'by',
        '欧盟': 'eu', '歐盟': 'eu',
        '美国': 'us', '美國': 'us', '美参议院': 'us', '美参议员': 'us', '美众议院': 'us', '美众议员': 'us',
        '加拿大': 'ca',
        '墨西哥': 'mx',
        '巴西': 'br',
        '阿根廷': 'ar',
        '智利': 'cl',
        '南非': 'za',
        '澳大利亚': 'au', '澳大利亞': 'au',
        '新西兰': 'nz', '新西蘭': 'nz'
    },
    # 英文国家名词典
    'dictionary_en': {
        "People's Republic of China": 'cn', 'China': 'cn', 'the PRC': 'cn', 'P.R.C.': 'cn',#长名称在前优先识别，避免出现"People's Republic of countrynamecn"的情况
        'Japan':'jp',
        'Republic of Korea': 'kr', 'SouthKorea': 'kr', 'South Korea': 'kr', 'R.O. Korea': 'kr', 'R.O.K.': 'kr', 'the ROK': 'kr',
        "Democratic People's Republic of Korea": 'kp', 'NorthKorea': 'kp', 'North Korea': 'kp', 'DPR Korea': 'kp', 'D.P.R. Korea': 'kp', 'D.P.R.K.': 'kp', 'the DPRK': 'kp',
        'Indonesia': 'id', 
        'Malaysia': 'my', 
        'Philippines': 'pl',
        'Thailand': 'th', 
        'Singapore': 'sg',
        'Brunei': 'bn', 
        'Cambodia': 'kh', 
        'Laos':'la', 
        'Myanmar': 'mm', 
        'Vietnam': 'vn', 'Viet nam': 'vn', 
        'India': 'in', 
        'Pakistan': 'pk', 
        'Kazakhstan': 'kz', 
        'Kyrgyzstan': 'kg',
        'Tajikistan': 'tj', 
        'Uzbekistan': 'uz', 
        'Afghanistan': 'af', 'Afghan': 'af', 
        'Iran': 'ir', 
        'Mongolia': 'mn', 
        'Turkey': 'tr', 
        'SaudiArabia': 'sa', 'Saudi Arabia': 'sa', 
        'Israel': 'il', 
        'UnitedKingdom': 'uk', 'United Kingdom': 'uk', 'the UK': 'uk', 'U.K.': 'uk', 'Britain': 'uk', 
        'France': 'fr', 
        'Germany': 'de', 
        'Italy': 'it', 
        'Austria': 'at', 
        'Belgium': 'be', 
        'Denmark': 'dk', 
        'Greece': 'gr', 
        'Iceland': 'is',
        'Ireland': 'ie',
        'Luxembourg': 'lu',
        'Netherlands': 'nl', 'Holland': 'nl',
        'Norway': 'no',
        'Portugal': 'pt',
        'Spain': 'es',
        'Sweden': 'se',
        'Switzerland': 'ch', 'Swiss': 'ch',
        'Finland': 'fi',
        'Czech': 'cz',
        'Hungary': 'hu',
        'Poland': 'pl',
        'Slovakia': 'sk',
        'Slovenia': 'si',
        'Estonia': 'ee',
        'Latvia': 'lv',
        'Lithuania': 'lt',
        'Russia': 'ru',
        'Belarus': 'by', 
        'EuropeanUnion': 'eu', 'European Union': 'eu', 'the EU': 'eu', 'E.U.': 'eu', ' EU ': 'eu',
        'UnitedStates': 'us', 'United States': 'us', 'the US': 'us', 'U.S.': 'us', 'USA': 'us', 'American': 'us', # 没有America以避免和北美南美的称呼相混淆。
        'Canada': 'ca', 
        'Mexico': 'mx',
        'Brazil': 'br',
        'Argentina': 'ar',
        'Chile': 'cl',
        'SouthAfrica': 'za', 'South Africa': 'za',
        'Australia': 'au', 'Aussie': 'au',
        'NewZealand': 'nz', 'New Zealand': 'nz'
    },
    # 日语国家名词典
    'dictionary_ja': {
        '中国': 'cn', '中華人民共和国': 'cn',
        '日本国':'jp', '日本':'jp',
        '韓国': 'kr', '大韓民国': 'kr',
        '朝鮮民主主義人民共和国': 'kp', '朝鮮': 'kp',
        'モンゴル': 'mn'
    },
    # 朝鲜语国家名词典
    'dictionary_ko': {
        '중국': 'cn', '중화 인민 공화국': 'cn',
        '일본':'jp',
        '대한민국': 'kr', '한국': 'kr',
        '조선민주주의인민공화국': 'kp', '조선 민주주의 인민 공화국': 'kp', '조선': 'kp', '북한': 'kp'
    }
}

def rename_country(text, lang = 'any'):
    if lang == 'any':
        dic = {**dictionary['dictionary_zh'], **dictionary['dictionary_en'], **dictionary['dictionary_ja'], **dictionary['dictionary_ko']}
    else:
        dic = dictionary['dictionary_' + lang]
    for item in dic:
        if item in text:
            text = text.replace(item, ' countryname' + dic[item] + ' ')  # 前后加空格以免出现countrynamejpese、countrynameusa这种情况
    
    return text

if __name__ == "__main__":
    pass