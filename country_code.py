# -*- coding: UTF-8 -*-
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
        '印度尼西亚共和国': 'id', '印度尼西亚': 'id', '印度尼西亞': 'id', '印尼': 'id',
        '马来西亚王国': 'my', '马来西亚': 'my', '馬來西亞': 'my', '大马': 'my', '马国': 'my',
        '菲律宾共和国': 'pl', '菲律宾': 'pl', '菲律賓': 'pl',
        '泰王国': 'th', '泰国': 'th', '泰國': 'th',
        '新加坡共和国': 'sg', '新加坡': 'sg',
        '文莱达鲁萨兰国': 'bn', '文莱和平之国': 'bn', '文莱': 'bn', '文萊': 'bn', '汶莱': 'bn',
        '柬埔寨王国': 'kh', '柬埔寨': 'kh',
        '老挝人民民主共和国':'la', '老挝':'la', '寮國':'la',
        '缅甸联邦共和国': 'mm', '缅甸': 'mm', '緬甸': 'mm',
        '越南社会主义共和国': 'vn', '越南': 'vn',
        '印度共和国': 'in', '印度': 'in',
        '巴基斯坦伊斯兰共和国': 'pk', '巴基斯坦': 'pk', '巴铁': 'pk',
        '哈萨克斯坦共和国': 'kz', '哈萨克斯坦': 'kz', '哈薩克斯坦': 'kz',
        '吉尔吉斯共和国': 'kg', '吉尔吉斯斯坦': 'kg', '吉爾吉斯斯坦': 'kg',
        '塔吉克斯坦共和国': 'tj', '塔吉克斯坦': 'tj', 'Tajikistan': 'tj',
        '乌兹别克斯坦共和国': 'uz', '乌兹别克斯坦': 'uz', '烏茲別克斯坦': 'uz',
        '阿富汗伊斯兰共和国': 'af', '阿富汗': 'af',
        '伊朗伊斯兰共和国': 'ir', '伊朗': 'ir',
        '蒙古国': 'mn', '蒙古': 'mn',
        '土耳其共和国': 'tr', '土耳其': 'tr',
        '沙特阿拉伯王国': 'sa', '沙特阿拉伯': 'sa', '沙特': 'sa',
        '以色列国': 'il', '以色列': 'il',
        '大不列颠及北爱尔兰联合王国': 'uk', '联合王国': 'uk', '不列颠': 'uk', '英国': 'uk', '英國': 'uk', '英议会': 'uk',
        '法兰西共和国': 'fr', '法国': 'fr', '法國': 'fr',
        '德意志联邦共和国': 'de', '德国': 'de', '德國': 'de',
        '意大利共和国': 'it', '意大利': 'it', '意国': 'it',
        '奥地利共和国': 'at', '奥地利': 'at', '奧地利': 'at',
        '比利时王国': 'be', '比利时': 'be', '比利時': 'be',
        '丹麦王国': 'dk', '丹麦': 'dk', '丹麥': 'dk',
        '希腊共和国': 'gr', '希腊': 'gr', '希臘': 'gr',
        '冰岛': 'is', '冰島': 'is',
        '爱尔兰共和国': 'ie', '爱尔兰': 'ie', '愛爾蘭': 'ie',
        '卢森堡大公国': 'lu', '卢森堡': 'lu', '盧森堡': 'lu',
        '荷兰王国': 'nl', '荷兰': 'nl', '荷蘭': 'nl',
        '挪威王国': 'no', '挪威': 'no',
        '葡萄牙共和国': 'pt', '葡萄牙': 'pt',
        '西班牙王国': 'es', '西班牙': 'es',
        '瑞典王国': 'se', '瑞典': 'se',
        '瑞士联邦': 'ch', '瑞士': 'ch',
        '芬兰共和国': 'fi', '芬兰': 'fi', '芬蘭': 'fi',
        '捷克共和国': 'cz', '捷克': 'cz',
        '匈牙利': 'hu',
        '波兰共和国': 'pl', '波兰': 'pl', '波蘭': 'pl',
        '斯洛伐克共和国': 'sk', '斯洛伐克': 'sk',
        '斯洛文尼亚共和国': 'si', '斯洛文尼亚': 'si', '斯洛文尼亞': 'si',
        '爱沙尼亚共和国': 'ee', '爱沙尼亚': 'ee', '愛沙尼亞': 'ee',
        '拉脱维亚共和国': 'lv', '拉脱维亚': 'lv', '拉脫維亞': 'lv',
        '立陶宛共和国': 'lt', '立陶宛': 'lt',
        '乌克兰共和国': 'ua', '乌克兰': 'ua',
        '俄罗斯联邦': 'ru', '俄罗斯': 'ru', '俄羅斯': 'ru',
        '白俄罗斯': 'by', '白罗斯': 'by', '白俄羅斯': 'by', '白羅斯': 'by',
        '欧盟': 'eu', '歐盟': 'eu',
        '美国': 'us', '美國': 'us', '美参议院': 'us', '美参议员': 'us', '美众议院': 'us', '美众议员': 'us',
        '加拿大': 'ca',
        '墨西哥合众国': 'mx', '墨西哥': 'mx',
        '巴西联邦共和国': 'br', '巴西': 'br',
        '阿根廷共和国': 'ar', '阿根廷': 'ar',
        '智利共和国': 'cl', '智利': 'cl',
        '南非共和国': 'za', '南非': 'za',
        '澳大利亚联邦': 'au', '澳大利亚': 'au', '澳大利亞': 'au',
        '新西兰王国': 'nz', '新西兰': 'nz', '新西蘭': 'nz'
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
        'Ukraine': 'ua',
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
    # 日语国家名词典 (感谢@shadowless95)
    'dictionary_ja': {
        '中国': 'cn', '中華人民共和国': 'cn',
        '日本国':'jp', '日本':'jp',
        '韓国': 'kr', '大韓民国': 'kr',
        '朝鮮民主主義人民共和国': 'kp', '北朝鮮': 'kp', '朝鮮': 'kp',
        'モンゴル国': 'mn', 'モンゴル': 'mn',
        'インドネシア共和国': 'id', 'インドネシア': 'id',
        'マレーシア': 'my',
        'フィリピン共和国': 'pl', 'フィリピン': 'pl',
        'タイ王国': 'th', 'タイ': 'th',
        'シンガポール共和国': 'sg', 'シンガポール': 'sg',
        'ブルネイ・ダルサラーム国': 'bn', 'ブルネイ': 'bn',
        'カンボジア王国': 'kh', 'カンボジア': 'kh',
        'ラオス人民民主共和国':'la', 'ラオス':'la',
        'ミャンマー連邦共和国': 'mm', 'ミャンマー': 'mm',
        'ベトナム社会主義共和国': 'vn', 'ベトナム': 'vn',
        'インド': 'in',
        'パキスタン・イスラム共和国': 'pk', 'パキスタン': 'pk',
        'モルディブ共和国': 'pk', 'モルディブ': 'pk',
        'ブータン王国': 'bt', 'ブータン': 'bt',
        'スリランカ民主社会主義共和国': 'lk', 'スリランカ': 'lk',
        '東ティモール民主共和国': 'tl', '東ティモール': 'tl',
        'ネパール連邦民主共和国': 'np', 'ネパール': 'np',
        'カザフスタン共和国': 'kz', 'カザフスタン': 'kz',
        'キルギス共和国': 'kg', 'キルギス': 'kg',
        'トルクメニスタン': 'tj',
        'ウズベキスタン共和国': 'uz', 'ウズベキスタン': 'uz',
        'アフガニスタン・イスラム共和国': 'af', 'アフガニスタン': 'af',
        'アラブ首長国連邦': 'ae',
        'イエメン共和国': 'ye', 'イエメン': 'ye',
        'イラク共和国': 'iq', 'イラク': 'iq',
        'イラン・イスラム共和国': 'ir', 'イラン': 'ir',
        'オマーン国': 'om', 'オマーン': 'om',
        'カタール国': 'qa', 'カタール': 'qa',
        'クウェート国': 'kw', 'クウェート': 'kw',
        'サウジアラビア王国': 'sa', 'サウジアラビア': 'sa',
        'シリア・アラブ共和国': 'sy', 'シリア': 'sy',
        'トルコ共和国': 'tr', 'トルコ': 'tr',
        'イスラエル国': 'il', 'イスラエル': 'il',
        'バーレーン王国': 'bh', 'バーレーン': 'bh',
        'ヨルダン・ハシミテ王国': 'jo', 'ヨルダン': 'jo',
        'レバノン共和国': 'lb', 'レバノン': 'lb',
        '英国': 'uk', 'グレートブリテン及び北アイルランド連合王国': 'uk', 'イギリス': 'uk',
        'フランス共和国': 'fr', 'フランス': 'fr', '仏国': 'fr',
        'ドイツ連邦共和国': 'de', 'ドイツ': 'de', '独国': 'de',
        'イタリア共和国': 'it', 'イタリア': 'it',
        'オーストリア共和国': 'at', 'オーストリア': 'at',
        'ベルギー王国': 'be', 'ベルギー': 'be',
        'デンマーク王国': 'dk', 'デンマーク': 'dk',
        'ギリシャ共和国': 'gr', 'ギリシャ': 'gr',
        'アイスランド共和国': 'is', 'アイスランド': 'is',
        'アイルランド': 'ie',
        'ルクセンブルク大公国': 'lu', 'ルクセンブルク': 'lu',
        'オランダ王国': 'nl', 'オランダ': 'nl',
        'ノルウェー王国': 'no', 'ノルウェー': 'no',
        'ポルトガル共和国': 'pt', 'ポルトガル': 'pt',
        'スペイン王国': 'es', 'スペイン': 'es',
        'スウェーデン王国': 'se', 'スウェーデン': 'se',
        'スイス連邦': 'ch', 'スイス': 'ch',
        'フィンランド共和国': 'fi', 'フィンランド': 'fi',
        'チェコ共和国': 'cz', 'チェコ': 'cz',
        'ハンガリー': 'hu',
        'ポーランド共和国': 'pl', 'ポーランド': 'pl',
        'スロバキア共和国': 'sk', 'スロバキア': 'sk',
        'スロベニア共和国': 'si', 'スロベニア': 'si',
        'エストニア共和国': 'ee', 'エストニア': 'ee',
        'ラトビア共和国': 'lv', 'ラトビア': 'lv',
        'リトアニア共和国': 'lt', 'リトアニア': 'lt',
        'ウクライナ': 'ua',
        'ロシア連邦': 'ru', 'ロシア': 'ru', '露連邦': 'ru', '露国': 'ru',
        'バチカン市国': 'va', 'バチカン': 'va',
        'ベラルーシ共和国': 'by', 'ベラルーシ': 'by',
        '欧州連合': 'eu', 'EU': 'eu',
        'アメリカ合衆国': 'us', 'アメリカ': 'us', '米国': 'us', '亜米利加': 'us',
        'カナダ': 'ca',
        'メキシコ合衆国': 'mx', 'メキシコ': 'mx',
        'ブラジル連邦共和国': 'br', 'ブラジル': 'br',
        'アルゼンチン共和国': 'ar', 'アルゼンチン': 'ar',
        'ウルグアイ東方共和国': 'uy', 'ウルグアイ': 'uy',
        'エクアドル共和国': 'ec', 'エクアドル': 'ec',
        'ガイアナ共和国': 'gy', 'ガイアナ': 'gy',
        'キューバ共和国': 'cu', 'キューバ': 'cu',
        'グアテマラ共和国': 'gt', 'グアテマラ': 'gt',
        'コスタリカ共和国': 'cr', 'コスタリカ': 'cr',
        'コロンビア共和国': 'co', 'コロンビア': 'co',
        'ドミニカ国': 'dm', 'アルゼンチン': 'dm',
        'ドミニカ共和国': 'do', 'ドミニカ': 'do',
        'ニカラグア共和国': 'ni', 'ニカラグア': 'ni',
        'ハイチ共和国': 'ht', 'ハイチ': 'ht',
        'バハマ国': 'bs', 'バハマ': 'bs',
        'パナマ共和国': 'pa', 'パナマ': 'pa',
        'パラグアイ共和国': 'py', 'パラグアイ': 'py',
        'ベネズエラ・ボリバル共和国': 've', 'ベネズエラ': 've',
        'ベリーズ': 'bz',
        'ペルー共和国': 'pe', 'ペルー': 'pe',
        'ボリビア多民族国': 'bo', 'ボリビア': 'bo',
        'チリ共和国': 'cl', 'チリ': 'cl',
        'ホンジュラス共和国': 'hn', 'ホンジュラス': 'hn',
        'スリナム共和国': 'sr', 'スリナム': 'sr',
        '南アフリカ共和国': 'za', '南アフリカ': 'za',
        'オーストラリア連邦': 'au', 'オーストラリア': 'au',
        'ニュージーランド': 'nz',
        'パプアニューギニア独立国': 'pg', 'パプアニューギニア': 'pg',
    },
    # 朝鲜语国家名词典
    'dictionary_ko': {
        '중국': 'cn', '중화 인민 공화국': 'cn',
        '일본':'jp',
        '대한민국': 'kr', '한국': 'kr',
        '조선민주주의인민공화국': 'kp', '조선 민주주의 인민 공화국': 'kp', '조선': 'kp', '북한': 'kp',
        '인도네시아 공화국':'id', '리퍼블릭 인도네시아':'id', '인도네시아':'id',
        '말레이시아':'my', '위키백과':'my', '우리 모두의 백과사전':'my',
        '필리핀 공화국':'pl', '필리핀':'pl',
        '타이 왕국':'th', '태국':'th',
        '싱가포르 공화국':'sg', '싱가포르':'sg',
        '브루나이 다루살람':'bn', '브루나이':'bn',
        '캄보디아 왕국':'kh', '캄보디아':'kh',
        '라오스 인민민주공화국':'la', '라오스':'la',
        '미얀마 연방공화국':'mm', '미얀마':'mm',
        '베트남 사회주의 공화국':'vn', '베트남':'vn',
        '인도 공화국':'in', '인도':'in',
        '파키스탄 이슬람 공화국':'pk', '파키스탄':'pk',
        '카자흐스탄 공화국':'kz', '카자흐스탄':'kz',
        '키르기즈 공화국':'kg', '키르기스스탄':'kg',
        '타지키스탄 공화국':'tj', '타지키스탄':'tj',
        '우즈베키스탄 공화국':'uz', '우즈베키스탄':'uz',
        
        
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
