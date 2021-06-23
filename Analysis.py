import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td

class Analysis:

    birthday = dt.now()
    sex = -1
    t_flag = False
    
    # 月令のスコア
    getsurei_score = [
        5,  # 月令を得て旺ず
        3,  # 月令を得て相す
        0,  # 月令を得て休す
        0,  # 月令を得て囚す
        0,  # 月令を得て死す
    ]

    # 十二運のスコア
    twelve_fortune_score = [
        3,   # 長生
        1.5, # 沐浴
        3,   # 冠帯
        3,   # 建禄
        3,   # 帝旺
        0,   # 衰
        0,   # 病
        0,   # 死
        1.5, # 墓
        0,   # 絶
        1.5, # 胎
        1.5, # 養
    ]

    # 通変のスコア
    tsuhen_score = [
        4,   # 比肩
        4,   # 劫財
        1,   # 食神
        1,   # 傷官
        0,   # 偏財
        0,   # 正財
        -1,  # 偏官
        -1,  # 正官
        3,   # 偏印
        3,   # 印綬
    ]
    

    def __init__(self, args):
        
        # 起動時の引数から生年月日・性別などのデータを構築する
        
        try:
            b = args[1]
            t = args[2]
            self.sex = int(args[3])
            self.birthday = dt.strptime(b + ' ' + t, '%Y-%m-%d %H:%M')
            self.t_flag = True
            # サマータイムを考慮する
            if (dt(year=1948, month=5, day=2) <= self.birthday < dt(year=1951, month=9, day=8)) and (hour is not None):
                self.birthday = dt(year = self.birthday.year, month = self.birthday.month, day = self.birthday.day,
                                   hour = self.birthday.hour - 1, minute = self.birthday.minute)
                
        except IndexError:
            try:
                b = args[1]
                self.sex = int(args[2])
                self.birthday = dt.strptime(b, '%Y-%m-%d')
                self.t_flag = False
                
            except IndexError:
                print('引数の指定を確認してください。')
                exit()
        

    def scoring_kan(self, ms):

        # 月令によるスコアリング
        ms.kan_score += self.getsurei_score[ms.meishiki["getsurei"]]

        # 十二運によるスコアリング
        for tf in ms.meishiki["twelve_fortune"]:
            if tf == -1:
                continue
            ms.kan_score += self.twelve_fortune_score[tf]

        # 通変によるスコアリング
        for th in ms.meishiki["tsuhen"]:
            if th == -1:
                continue
            ms.kan_score += self.tsuhen_score[th]

