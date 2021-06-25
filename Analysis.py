import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td

class Analysis:

    birthday = dt.now()
    sex = -1
    t_flag = False
    
    # 月令のスコア
    getsurei_score = [
        [1, 1, 3, 3, 2, 1, 1, 0, 0, 0, 0, 1],
        [1, 1, 3, 3, 2, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 3, 3, 2, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 3, 3, 2, 0, 0, 1, 0],
        [0, 2, 0, 0, 2, 3, 3, 2, 0, 0, 2, 0],
        [0, 2, 0, 0, 2, 3, 3, 2, 0, 0, 2, 0],
        [1, 1, 0, 0, 0, 0, 0, 1, 3, 3, 2, 1],
        [1, 1, 0, 0, 0, 0, 0, 1, 3, 3, 2, 1],
        [3, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 3],
        [3, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 3],
    ]

    # 十二運のスコア
    twelve_fortune_score = [
        0,    # 長生
        0,    # 沐浴
        1,    # 冠帯
        1,    # 建禄
        1,    # 帝旺
        0,    # 衰
        -1,    # 病
        -1,    # 死
        -1,    # 墓
        -1,    # 絶
        0,    # 胎
        0,    # 養
    ]

    # 通変のスコア
    tsuhen_score = [
        1,    # 比肩
        1,    # 劫財
        -1,    # 食神
        -1,    # 傷官
        -1,    # 偏財
        -1,    # 正財
        -1,    # 偏官
        -1,    # 正官
        1,    # 偏印
        1,    # 印綬
    ]

    threshold = 0
    diff_threshold = 3
    

    def __init__(self, args):
        
        # 起動時の引数から生年月日・性別などのデータを構築する
        
        try:
            b = args[1]
            t = args[2]
            self.sex = int(args[3])
            self.birthday = dt.strptime(b + ' ' + t, '%Y-%m-%d %H:%M')
            self.t_flag = True
            # サマータイムを考慮する
            if (dt(year=1948, month=5, day=2) <= self.birthday < dt(year=1951,  month=9, day=8)) and (hour is not None):
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

        # ms（命式）をスコアリングして日干・月支蔵干の旺衰を計算する
        # (1) 月令
        # (2) 十二運
        # (3) 通変
        
        ms.analysis["kan_score"] = 0
        
        # 月令によるスコアリング
        ms.analysis["kan_score"] += self.getsurei_score[ms.meishiki["nitchu_tenkan"]][ms.meishiki["getchu_chishi"]]

        # 十二運によるスコアリング
        for tf in ms.meishiki["twelve_fortune"]:
            if tf == -1:
                continue
            ms.analysis["kan_score"] += self.twelve_fortune_score[tf]

        # 通変によるスコアリング
        for th in ms.meishiki["tsuhen"]:
            if th == -1:
                continue
            ms.analysis["kan_score"] += self.tsuhen_score[th]


    def evaluate_kan_strength(self, ms):

        # スコアがしきい値を上回っているか下回っているか？
        # （日干・月支蔵干が小強以上か未満か？）を評価する
        
        ms.analysis["kan_strength"] = -1
        
        if ms.analysis["kan_score"] >= self.threshold:
            ms.analysis["kan_strength"] = 1
        else:
            ms.analysis["kan_strength"] = 0

            
    def show_kan_strength(self, ms):
        if ms.analysis["kan_strength"]:
            print('小強以上：', ms.analysis["kan_score"])
        else:
            print('小強未満：', ms.analysis["kan_score"])

            
    def evaluate_kan_interval(self, ms1, ms2):

        # 日干のスコアと月支蔵干のスコアとの差が、所定値以上か否かを評価する

        ms1.analysis["kan_score_diff"] = -1
        ms2.analysis["kan_score_diff"] = -1
        
        s1 = ms1.analysis["kan_score"]
        s2 = ms2.analysis["kan_score"]

        if abs(s1 - s2) < self.diff_threshold:
            ms1.analysis["kan_score_diff"] = 1
            ms2.analysis["kan_score_diff"] = 1
        else:
            ms1.analysis["kan_score_diff"] = 0
            ms2.analysis["kan_score_diff"] = 0
            
    
    def evaluate_analysis_type(self, ms1, ms2):
        
        # 条件に応じて解析のタイプを決定する
        
        # 日干・月支蔵干がともに小強以上の強さを持ち、
        # その強さは均衡が取れている場合であって、かつ、
        if  (ms1.analysis["kan_strength"] and ms2.analysis["kan_strength"]) and ms1.analysis["kan_score_diff"]:
            
            if kd.tsuhen_gb[ms1.meishiki["tsuhen"][ms2.std_num]]:
                # (1) よい通変が用神格となっている場合
                ms1.analysis["type"] = 1
                ms2.analysis["type"] = 1
            else:
                # (2) 悪い通変が用神格となっている場合
                ms1.analysis["type"] = 2
                ms2.analysis["type"] = 2
            
        elif (ms1.analysis["kan_strength"] and ms2.analysis["kan_strength"]) and not ms1.analysis["kan_score_diff"]:
            # (3) 両方とも小強以上の強さを持っているが、一方が強すぎてバランスが崩れている場合
            ms1.analysis["type"] = 3
            ms2.analysis["type"] = 3
        
        elif ms1.analysis["kan_strength"] and not ms2.analysis["kan_strength"]:
            # (4) 日干が小強以上あるのに対し、用神格が小強に満たない場合
            ms1.analysis["type"] = 4
            ms2.analysis["type"] = 4

        elif not ms1.analysis["kan_strength"] and ms2.analysis["kan_strength"]:
            # (5) 用神格が小強以上あるのに対し、日干が小強に満たない場合
            ms1.analysis["type"] = 5
            ms2.analysis["type"] = 5
            
        else:
            ms1.analysis["type"] = -1
            ms2.analysis["type"] = -1
        

    
    
    # day_kanshi_character = [
    #     "温順・誠実で情が深く、従順で私心がありません。また、知恵・考えが深く、蓄財を得意とするタイプです。",  # 1. 甲子
    #     "控えめでおとなしく、言葉数が少ないため内気のようにみえますが、実は勝気な部分もあり、陰で活動的な努力をするタイプです。",  # 2. 乙丑
    #     "自発的に物事を進めようとする積極的なところがあります。行動が早く、派手を好み、議論が好きなタイプです。",  # 3. 丙寅
    #     "落ち着きがあり、注意深く、計画を立てることが得意ですが、計画当初の熱意が途中で動揺しやすいタイプです。",  # 4. 丁卯
    #     "自発的で発展性に富みながら、度を越すことのないバランス感覚を持つタイプです。一方で、プライドが高くなりがちで、外観を飾りたがり、短気を起こす場合がある点に注意が必要です。",  # 5. 戊辰
    #     "物事を探求する情熱にあふれるタイプです。規則を守り、注意深く、おとなしくて和を尊びます。少し度量が狭くなる場合があることに注意が必要です。",  # 6. 己巳
    #     "心が広く、人情味にあふれるタイプです。落ち着きがあり、物事に動じることが少ないでしょう。一方で、態度や考え方が目先の状況に対して過度に左右されやすい点に注意が必要です。",  # 7. 庚午
    #     "物事に対して少し消極的なところがあり、取り越し苦労が多くなる傾向があります。一方で、慎重で和を尊び、円満で控えめな部分は大きな長所となるでしょう。",  # 8. 辛未
    #     "明朗・温順で度量が広く、才智のあるタイプです。一方で、やや慎重さに欠け、他人をあてにしすぎる傾向がある点に注意が必要です。",  # 9. 壬申
    #     "プライドをもって意思を貫こうとする努力を惜しまないタイプです。慎重で正直なところも長所になるでしょう。一方で、情熱に欠ける場合があることに注意が必要です。", # 10. 癸酉
    #     "何に対しても情熱的で、他人の世話を焼くことが好きなタイプです。思慮分別があり、物事を探究する意欲もあります。一方で、干渉しすぎる点には注意が必要です。",  # 11. 甲戌
    #     "活動的な努力家タイプです。他人を頼りすぎることなく、臨機応変な対応ができる頼もしさがあります。一方で、落ち着きのない点に注意が必要です。",  # 12. 乙亥
    #     "プライドが高く、初志を貫こうとする実行力があるタイプです。派手を好み、蓄財を得意とします。一方で、義理人情に欠けるところがあります。",  # 13. 丙子
    #     "何事にも注意深いため外見は目立ちませんが、内心はプライドが高く進取の気があり、粘り強いタイプです。",  # 14. 丁丑
    #     "進取の気が旺盛で、積極的なタイプです。一方で、短気で損をする場合があることに注意が必要です。",  # 15. 戊寅
    #     "学術・技芸が得意で、注意深く、規則をよく守るタイプです。一方で、神経過敏・消極的なところがあり、気の動揺や取り越し苦労が多い点に注意が必要です。", # 16. 己卯
    # ]
