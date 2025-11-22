import json
import requests
from googletrans import Translator

RANK_URL = "https://mlol.qt.qq.com/go/lgame_battle_info/hero_rank_list_v2"
CHAMP_URL = "https://game.gtimg.cn/images/lgamem/act/lrlib/js/heroList/hero_list.js"

POSITIONS = {
    '1': 'mid',
    '2': 'top',
    '3': 'adc',
    '4': 'support',
    '5': 'jungler'
}

DICT_CHAMP = {
    '凯尔': 'Kayle',
    '莫甘娜': 'Morgana',
    '提莫': 'Teemo',
    '婕拉': 'Zyra',
    '布兰德': 'Brand',
    '阿狸': 'Ahri',
    '凯南': 'Kennen',
    '内瑟斯': 'Nasus',
    '安妮': 'Annie',
    '斯维因': 'Swain',
    '维迦': 'Veigar',
    '阿萝拉': 'Aurora',
    '奥莉安娜': 'Oriana',
    '薇古丝': 'Vex',
    '拉克丝': 'Lux',
    '永恩': 'Yone',
    '崔斯特': 'Twisted Fate',
    '黑默丁格': 'Heimerdinger',
    '辛德拉': 'Sindra',
    '丽桑卓': 'Lissandra',
    '维克托': 'Viktor',
    '亚索': 'Yasuo',
    '弗拉基米尔': 'Vladimir',
    '卡萨丁': 'Kassadin',
    '维克兹': 'VelKoz',
    '菲兹': 'Fizz',
    '加里奥': 'Galio',
    '奥瑞利安·索尔': 'Aurelion Sol',
    '瑞兹': 'Ryze',
    '吉格斯': 'Zigs',
    '阿卡丽': 'Akali',
    '崔丝塔娜': 'Tristana',
    '卡特琳娜': 'Katarina',
    '艾克': 'Ekko',
    '劫': 'Zed',
    '黛安娜': 'Diana',
    '杰斯': 'Jayce',
    '艾瑞莉娅': 'Irelia',
    '墨菲特': 'Malphite',
    '安蓓萨': 'Ambessa',
    '孙悟空': 'Wukong',
    '嘉文四世': 'Jarvan IV',
    '兰博': 'Rumble',
    '莫德凯撒': 'Mordekaiser',
    '盖伦': 'Garen',
    '诺提勒斯': 'Nautilus',
    '辛吉德': 'Singed',
    '卡蜜尔': 'Camille',
    '波比': 'Poppy',
    '慎': 'Shen',
    '菲奥娜': 'Fiora',
    '奥恩': 'Ornn',
    '沃利贝尔': 'Volibear',
    '薇恩': 'Vayne',
    '纳尔': 'Gnar',
    '赛恩': 'Sion',
    '贾克斯': 'Jax',
    '泰达米尔': 'Tryndamere',
    '德莱厄斯': 'Darius',
    '瑟提': 'Sett',
    '亚托克斯': 'Aatrox',
    '蒙多医生': 'Dr. Mundo',
    '厄加特': 'Urgot',
    '格温': 'Gwen',
    '雷克顿': 'Renekton',
    '锐雯': 'Riven',
    '古拉加斯': 'Gragas',
    '厄运小姐': 'Miss Fortune',
    '艾希': 'Ashe',
    '霞': 'Xayah',
    '卢锡安': 'Lucian',
    '希维尔': 'Sivir',
    '烬': 'Jhin',
    '金克丝': 'Jinx',
    '韦鲁斯': 'Varus',
    '泽丽': 'Zeri',
    '库奇': 'Corki',
    '凯特琳': 'Caitlyn',
    '德莱文': 'Draven',
    '莎弥拉': 'Samira',
    '伊泽瑞尔': 'Ezreal',
    '卡莎': 'KaiSa',
    '图奇': 'Twitch',
    '卡莉丝塔': 'Kalista',
    '巴德': 'Bardo',
    '布隆': 'Braum',
    '基兰': 'Zilean',
    '蕾欧娜': 'Leona',
    '娜美': 'Nami',
    '茂凯': 'Maokai',
    '迦娜': 'Janna',
    '米利欧': 'Milio',
    '赛娜': 'Senna',
    '派克': 'Pyke',
    '卡尔玛': 'Karma',
    '娑娜': 'Sona',
    '芮尔': 'Rell',
    '索拉卡': 'Soraka',
    '布里茨': 'Blitzcrank',
    '璐璐': 'Lulu',
    '洛': 'Rakan',
    '萨勒芬妮': 'Seraphine',
    '阿利斯塔': 'Alistar',
    '悠米': 'Yuumi',
    '锤石': 'Thresh',
    '阿木木': 'Amumu',
    '莉莉娅': 'Lillia',
    '希瓦娜': 'Shivana',
    '拉莫斯': 'Ramus',
    '赵信': 'Xin Zhao',
    '奈德丽': 'Nidalee',
    '沃里克': 'Warwick',
    '千珏': 'Kindred',
    '努努和威朗普': 'Nunu',
    '蔚': 'Vi',
    '潘森': 'Pantheon',
    '费德提克': 'Fiddlesticks',
    '格雷福斯': 'Graves',
    '魔腾': 'Nocturne',
    '凯隐': 'Kayn',
    '卡兹克': 'KhaZix',
    '佛耶戈': 'Viego',
    '雷恩加尔': 'Rengar',
    '易': 'Maestro Yi',
    '李青': 'Lee Sin',
    '赫卡里姆': 'Hecarim',
    '奥拉夫': 'Olaf',
    '伊芙琳': 'Evelynn',
    '泰隆': 'Talon'
}

translator = Translator()

# Hacemos la request a la API rank
resp_rank = requests.get(RANK_URL, timeout=15)
resp_rank.raise_for_status()   # Si hay error, que explote

# Hacemos la request a la API champs
resp_champ = requests.get(CHAMP_URL, timeout=15)
resp_champ.raise_for_status()   # Si hay error, que explote


data_rank = resp_rank.json()  # Convertimos a JSON
data_champ = resp_champ.json() 

for posicion in data_rank['data']['2']:
    list_data = []
    for campeon in data_rank['data']['2'][posicion]:
        champ = data_champ['heroList'][campeon['hero_id']]
        #print("'" + champ['name'] + "'" + ":" + " ,")
        champ['win_rate_percent'] = campeon['win_rate_percent']
        champ['appear_rate_percent'] = campeon['appear_rate_percent']
        champ['forbid_rate_percent'] = campeon['forbid_rate_percent']
        champ['name_es'] = DICT_CHAMP[champ['name']]
        list_data.append(champ)

    with open(POSITIONS[posicion] + '.json', 'x', encoding="utf-8") as file:
        file.write(json.dumps(list_data, ensure_ascii=False, indent=2))