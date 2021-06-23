import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td

class Meishiki:

    meishiki = {}
    birthday = dt.now()
    sex = -1
    t_flag = False

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

                
    def is_setsuiri(self, month):
        
        # ＜機能＞
        # self.birthday の年月日が、month で与えられた月に対して節入りしているか否かを判定する
        # ＜入力＞
        #   - month（int）：基準となる月
        # ＜出力＞
        #   - 節入りしている（0）またはしていない（-1）の二値
        # ＜異常検出＞
        # 判定不可能の場合はエラーメッセージを出力して強制終了する
        
        for s in kd.setsuiri:
            if (s[0] == self.birthday.year) and (s[1] == month):
                setsuiri_ = dt(year = s[0], month = s[1], day = s[2], hour = s[3], minute = s[4])
                if setsuiri_ < self.birthday:
                    return 0    # 節入りしている
                else:
                    return -1   # 節入りしていない
                
        print('節入りを判定できませんでした。')
        exit()

        
    def find_year_kanshi(self):
        
        # ＜機能＞
        # self.birthday の生年月日の年干支を取得する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - y_kan（int）：年干の番号
        #   - y_shi（int）：年支の番号
        # ＜異常検出＞
        # 取得できなかった場合はエラーメッセージを出力して強制終了する
        
        sixty_kanshi_idx = (self.birthday.year - 3) % 60 - 1 + self.is_setsuiri(2)
        try:
            y_kan, y_shi = kd.sixty_kanshi[sixty_kanshi_idx]
            return y_kan, y_shi
        except:
            print('年干支の計算で例外が送出されました。')
            exit()


    def find_month_kanshi(self, y_kan):
        
        # ＜機能＞
        # self.birthday の生年月日の月干支を取得する
        # ＜入力＞
        #   - y_kan（string）：年干の番号
        # ＜出力＞
        #   - m_kan（int）：月干の番号
        #   - m_shi（int）：月支の番号
        # ＜異常検出＞
        # 取得できなかった場合はエラーメッセージを出力して強制終了する
        
        month = self.birthday.month - 1 + self.is_setsuiri(self.birthday.month)
        try:
            m_kan, m_shi = kd.month_kanshi[y_kan][month]
            return m_kan, m_shi
        except:
            print('月干支の計算で例外が送出されました。')
            exit()
                

    def find_day_kanshi(self):
        
        # ＜機能＞
        # self.birthday で与えられた生年月日の日干支を取得する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - d_kan（int）：日干の番号
        #   - d_shi（int）：日支の番号
        # ＜異常検出＞
        # 取得できなかった場合はエラーメッセージを出力して強制終了する
        
        d = self.birthday.day + kd.kisu_table[self.birthday.year - 1926][self.birthday.month - 1] - 1
        if d >= 60:
            d -= 60  # d が 60 を超えたら 60 を引く
            
        try:
            d_kan, d_shi = kd.sixty_kanshi[d]
            return d_kan, d_shi
        except:
            print('日干支の計算で例外が送出されました。')
            exit()
            
            
    def find_time_kanshi(self, day_kan):
        
        # ＜機能＞
        # self.birthday で与えられた生年月日の時干支を取得する
        # ＜入力＞
        #   - day_kan（int）：日干の番号
        # ＜出力＞
        #   - t_kan（int）：時干の番号
        #   - t_shi（int）：時支の番号
        # ＜異常検出＞
        # 取得できなかった場合はエラーメッセージを出力して強制終了する
        
        time_span = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 24]
        
        for i in range(len(time_span) - 1):
            
            from_dt = dt(year = self.birthday.year, month = self.birthday.month, day = self.birthday.day,
                         hour = time_span[i], minute = 0)
            if (i == 0) or (i == len(time_span)):
                to_dt = from_dt + td(hours = 0, minutes = 59)
            else:
                to_dt = from_dt + td(hours = 1, minutes = 59)
                
            if from_dt <= self.birthday < to_dt:
                try:
                    t_kan, t_shi = kd.time_kanshi[day_kan][i]
                    return t_kan, t_shi
                except:
                    print('時干支の計算で例外が送出されました。')
                    exit()

        print('時干支を得られませんでした。')
        exit()        


    def find_zokan(self, shi):
        
        # ＜機能＞
        # self.birthday で与えられた生年月日の shi に対応する蔵干を取得する
        # ＜入力＞
        #   - self.birthday（datetime）：生年月日
        #   - shi（int）：年支、月支、日支、時支の番号
        # ＜出力＞
        #   - z_kan（int）：蔵干の番号
        # ＜異常検出＞
        # 取得できなかった場合はエラーメッセージを出力して強制終了する
        
        p = self.is_setsuiri(self.birthday.month)
        for s in kd.setsuiri:
            if (s[0] == self.birthday.year) and (s[1] == self.birthday.month):
                setsuiri_ =  dt(year = s[0], month = s[1] + p, day = s[2], hour = s[3], minute = s[4])
                
        delta = td(days = kd.zokan_time[shi][0], hours = kd.zokan_time[shi][1])
        
        try:
            if setsuiri_ + delta >= self.birthday:
                zokan = kd.zokan[shi][0]
            else:
                zokan = kd.zokan[shi][1]
            return zokan
        except:
            print('蔵干の計算で例外が送出されました。')
            exit()
            
            
    def build_meishiki(self):
        
        # self.birthday の生年月日の干支を命式に追加する
        
        # 天干・地支を得る
        y_kan, y_shi = self.find_year_kanshi()
        m_kan, m_shi = self.find_month_kanshi(y_kan)
        d_kan, d_shi = self.find_day_kanshi()
        if self.t_flag:
            t_kan, t_shi = self.find_time_kanshi(d_kan)
        else:
            t_kan = -1
            t_shi = -1
            
        tenkan = [y_kan, m_kan, d_kan, t_kan]
        chishi = [y_shi, m_shi, d_shi, t_shi]
        
        # 蔵干を得る
        y_zkan = self.find_zokan(y_shi)
        m_zkan = self.find_zokan(m_shi)
        d_zkan = self.find_zokan(d_shi)
        if self.t_flag:
            t_zkan = self.find_zokan(t_shi)
        else:
            t_zkan = -1
            
        zokan = [y_zkan, m_zkan, d_zkan, t_zkan]
        
        # 四柱を得る
        nenchu = [y_kan, y_shi, y_zkan]
        getchu = [m_kan, m_shi, m_zkan]
        nitchu = [d_kan, d_shi, d_zkan]
        jichu  = [t_kan, t_shi, t_zkan]
        
        # クラス変数 meishiki に情報を追加していく
        self.meishiki.update({"tenkan": tenkan})
        self.meishiki.update({"chishi": chishi})
        self.meishiki.update({"zokan" : zokan})
        self.meishiki.update({"nenchu": nenchu})
        self.meishiki.update({"getchu": getchu})
        self.meishiki.update({"nitchu": nitchu})
        self.meishiki.update({"jichu" : jichu})
        self.meishiki.update({"nitchu_tenkan": d_kan})
        

    def find_tsuhen(self, s_kan, kan_):
        try:
            if kan_ == -1:
                return -1
            else:
                return kd.kan_tsuhen[s_kan].index(kan_)
        except:
            return -1
        

    def append_tsuhen(self, std_num):
        
        # 命式に通変を追加する
        # std_num は、天干・蔵干を通算した場合の干の番号
        # 通常は、日干：２、月支蔵干５を指定する
        # 日干と月支蔵干が同じ場合は、時支天干：３、年支天干：０などを指定する
        
        kan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        std = kan[std_num]

        t = []
        for k in kan:
            t.append(self.find_tsuhen(std, k))
            
        self.meishiki.update({"tsuhen": t})

            
    def find_twelve_fortune(self, kan, shi_):
        
        try:
            if shi_ == -1:
                return -1
            else:
                return kd.twelve_table[kan][shi_]
        except:
            return -1
            

    def append_twelve_fortune(self, std_num):
        
        # 命式に十二運を追加する
        # std_num は、天干・蔵干を通算した場合の干の番号
        # 通常は、日干：２、月支蔵干５を指定する
        # 日干と月支蔵干が同じ場合は、時支天干：３、年支天干：０などを指定する
        
        kan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        std = kan[std_num]
        
        f = []
        for s in self.meishiki["chishi"]:
            f.append(self.find_twelve_fortune(std, s))

        self.meishiki.update({"twelve_fortune": f})


    def append_getsurei(self, std_num):
        
        # ＜機能＞
        # 月令の旺衰強弱を命式に追加する
        # ＜入力＞
        #   - self.birthday（datetime）：生年月日
        # ＜出力＞
        #   - kd.getsurei に対応する番号

        kan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        std = kan[std_num]
        
        shi_ = kd.shi[self.birthday.month]  # 生まれ月の地支を引く（節入りを考慮している？？？）
        getsurei_ = kd.getsurei_table[std]
        
        p = False
        for idx1, gr_ in enumerate(getsurei_):
            for idx2, g in enumerate(gr_):
                if shi_ in g:
                    p = True
                    break
            if p:
                break

        self.meishiki.update({"getsurei": idx1})


    def append_kango(self):
        
        # ＜機能＞
        # 干合を命式に追加する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - 干合のリスト
        #     [[干合する干１, 干１の場所（0〜7）], [干合する干２, 干２の場所], 変化する五行]
        
        tenkan_zokan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        
        kango = []
        for i, tz1 in enumerate(tenkan_zokan):
            if tz1 == -1:
                continue
            for j in list(range(i, len(tenkan_zokan))):
                if kd.kango[tz1] == tenkan_zokan[j] and i != j:
                    kango.append([[tz1, i], [tenkan_zokan[j], j], kd.kango_henka[tz1]])

        self.meishiki.update({"kango": kango})
    

    def append_shigo(self):
        
        # ＜機能＞
        # 支合を命式に追加する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - 支合のリスト
        #     [[支合する支１, 支１の場所（0〜3）], [支合する支２, 支２の場所]]
        
        chishi = self.meishiki["chishi"]
        
        shigo = []
        for i, s in enumerate(chishi):
            if s == -1:
                continue
            for j in list(range(i, len(chishi))):
                if kd.shigo[s] == chishi[j] and i != j:
                    shigo.append([[s, i], [kd.shigo[s], j]])
                    
        self.meishiki.update({"shigo": shigo})


    def append_hogo(self):
        
        # ＜機能＞
        # 方合を命式に追加する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - 方合する地支のリスト
        
        hogo = False
        chishi = self.meishiki["chishi"]
        for i, h in enumerate(kd.hogo):
            if h in chishi:
                hogo = True
                break
            
        if hogo:
            self.meishiki.update({"hogo": kd.hogo[i]})
        else:
            self.meishiki.update({"hogo": []})
            
            
    def append_hitsuchu(self):
        
        # ＜機能＞
        # 七冲を命式に追加する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - 七冲のリスト
        
        chishi = self.meishiki["chishi"]
        
        hitsuchu = []
        for i, s in enumerate(chishi):
            if s == -1:
                continue
            for j in list(range(i, len(chishi))):
                if kd.hitsuchu[s] == chishi[j] and i != j:
                    hitsuchu.append([[s, i], [kd.hitsuchu[s], j]])
                    
        self.meishiki.update({"hitsuchu": hitsuchu})
        
        
    def append_kei(self):
        
        # ＜機能＞
        # 刑を命式に追加する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - 刑のリスト
        
        chishi = self.meishiki["chishi"]
        
        kei = []
        for i, s in enumerate(chishi):
            if s == -1:
                continue
            for j in list(range(0, len(chishi))):
                if kd.kei[s] == chishi[j] and i != j:
                    kei.append([[s, i], [kd.kei[s], j]])
                    
        self.meishiki.update({"kei": kei})
        
        
    def append_gai(self):
        
        # ＜機能＞
        # 害を命式に追加する
        # ＜入力＞
        #   なし
        # ＜出力＞
        #   - 害のリスト
        
        chishi = self.meishiki["chishi"]
        
        gai = []
        for i, s in enumerate(chishi):
            if s == -1:
                continue
            for j in list(range(i, len(chishi))):
                if kd.gai[s] == chishi[j] and i != j:
                    gai.append([[s, i], [kd.gai[s], j]])
                    
        self.meishiki.update({"gai": gai})
            

    def append_kubo(self):
        
        # ＜機能＞
        # 空亡を命式に追加する
        # ＜入力＞
        #   - self.birthday（datetime）：生年月日
        # ＜出力＞
        #   - kubo（list）：空亡となる地支の番号と位置
        
        d = self.birthday.day + kd.kisu_table[self.birthday.year - 1926][self.birthday.month - 1] - 1
        if d >= 60:
            d -= 60  # d が 60 を超えたら 60 を引く
            
        try:
            kubo = kd.kubo[d // 10]
        except:
            print('空亡が計算できませんでした。')
            exit()
        
        chishi = self.meishiki["chishi"]
        k = []
        for i, c in enumerate(chishi):
            if c in kubo:
                k.append([c, i])
                
        self.meishiki.update({"kubo": k})


    def append_additional_info(self, std_num):
        
        # 命式にその他の情報を追加する
        
        self.append_getsurei(std_num)   # 月令を追加
        self.append_kango()      # 干合を追加
        self.append_shigo()      # 支合を追加
        self.append_hogo()       # 方合を追加
        self.append_hitsuchu()   # 七冲を追加
        self.append_kei()        # 刑を追加
        self.append_gai()        # 害を追加
        self.append_kubo()       # 空亡を追加

    def find_kan(num):
        kan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        return kan[num]
        
        
    def show_basic_info(self):
        
        # 生年月日・年齢・性別などの基本情報を出力する
        
        if self.sex == 0:
            sex_str = '男命'
        else:
            sex_str = '女命'
            
        wareki = kd.convert_to_wareki(self.birthday)
        
        print()
        if self.t_flag:
            print(str(self.birthday.year) + '年（' + wareki + '）' + str(self.birthday.month) + '月' + str(self.birthday.day) + '日 ' + str(self.birthday.hour) + '時' + str(self.birthday.minute) + '分生 ' + sex_str)
        else:
            print(str(self.birthday.year) + '年（' + wareki + '）' + str(self.birthday.month) + '月' + str(self.birthday.day) + '日生（時刻不明） ' + sex_str)

            
    def show_meishiki(self):
        
        # 命式を整形して出力する
        
        tenkan = [kd.kan[i] for i in self.meishiki["tenkan"]]
        chishi = [kd.shi[i] for i in self.meishiki["chishi"]]
        zokan = [kd.kan[i] for i in self.meishiki["zokan"]]
        tsuhen = [kd.tsuhen[i] for i in self.meishiki["tsuhen"]]
        twelve_fortune = [kd.twelve_fortune[i] for i in self.meishiki["twelve_fortune"]]
        
        print()
        print('|   生  時   |   生  日   |   生  月   |   生  年   |')    
        print('+============+============+============+============+')   # 56文字
        if self.t_flag:
            print('| ' + tenkan[3] + '（' + tsuhen[3] + '） ' +
                  '|     ' + tenkan[2] +
                  '     | ' + tenkan[1] + '（' + tsuhen[1] + '） ' +
                  '| ' + tenkan[0] + '（' + tsuhen[0] + '）' +
                  ' |')
            print('+------------+------------+------------+------------+')
            print('|  ' + chishi[3] + '（' + twelve_fortune[3] + '）  ' +
                  '|  ' + chishi[2] + '（' + twelve_fortune[2] + '）  ' +
                  '|  ' + chishi[1] + '（' + twelve_fortune[1] + '）  ' +
                  '|  ' + chishi[0] + '（' + twelve_fortune[0] + '）  ' +
                  '|')
            print('+------------+------------+------------+------------+')
            print('| ' + zokan[3] + '（' + tsuhen[7] + '） ' +
                  '| ' + zokan[2] + '（' + tsuhen[6] + '） ' +
                  '| ' + zokan[1] + '（' + tsuhen[5] + '） ' +
                  '| ' + zokan[0] + '（' + tsuhen[4] + '） ' +
                  '|')
        else:
            print('|    ----    ' +
                  '|     ' + tenkan[2] +
                  '     | ' + tenkan[1] + '（' + tsuhen[1] + '） ' +
                  '| ' + tenkan[0] + '（' + tsuhen[0] + '）' +
                  ' |')
            print('+------------+------------+------------+------------+')
            print('|    ----    ' +
                  '|  ' + chishi[2] + '（' + twelve_fortune[2] + '）  ' +
                  '|  ' + chishi[1] + '（' + twelve_fortune[1] + '）  ' +
                  '|  ' + chishi[0] + '（' + twelve_fortune[0] + '）  ' +
                  '|')
            print('+------------+------------+------------+------------+')
            print('|    ----    ' +
                  '| ' + zokan[2] + '（' + tsuhen[6] + '） ' +
                  '| ' + zokan[1] + '（' + tsuhen[5] + '） ' +
                  '| ' + zokan[0] + '（' + tsuhen[4] + '） ' +
                  '|')
            


    def show_additional_info(self):
        
        print()
        print('＜月令＞')
        print(kd.getsurei[self.meishiki["getsurei"]])
        
        print()
        print('＜干合＞')
        if not self.meishiki["kango"]:
            print('干合なし')
        else:
            for k in self.meishiki["kango"]:
                b1 = kd.kango_chu[k[0][1]]   # 干１の場所
                k1 = kd.kan[k[0][0]]         # 干１
                b2 = kd.kango_chu[k[1][1]]   # 干２の場所
                k2 = kd.kan[k[1][0]]         # 干２
                g  = kd.gogyo[k[2]]
                print(b1 + 'の「' + k1 + '」が、' + b2 + 'の「' + k2 + '」と干合して「' + g + '」に五行変化')
                
        print()
        print('＜支合＞')
        if not self.meishiki["shigo"]:
            print('支合なし')
        else:
            for s in self.meishiki["shigo"]:
                b1 = kd.shigo_chu[s[0][1]]   # 支１の場所
                k1 = kd.shi[s[0][0]]         # 支１
                b2 = kd.shigo_chu[s[1][1]]   # 支２の場所
                k2 = kd.shi[s[1][0]]         # 支２
                print(b1 + 'の「' + k1 + '」と' + b2 + 'の「' + k2 + '」とが支合')
                
        print()
        print('＜方合＞')
        if not self.meishiki["hogo"]:
            print('方合なし')
        else:
            print(self.meishiki["hogo"][0] + ', ' + self.meishiki["hogo"][1] + ', ' + self.meishiki["hogo"][2] + 'で方合')
            
        print()
        print('＜七冲＞')
        if not self.meishiki["hitsuchu"]:
            print('七冲なし')
        else:
            for h in self.meishiki["hitsuchu"]:
                b1 = kd.shigo_chu[h[0][1]]   # 支１の場所
                k1 = kd.shi[h[0][0]]         # 支１
                b2 = kd.shigo_chu[h[1][1]]   # 支２の場所
                k2 = kd.shi[h[1][0]]         # 支２
                print(b1 + 'の「' + k1 + '」と' + b2 + 'の「' + k2 + '」とが冲')
                
        print()
        print('＜刑＞')
        if not self.meishiki["kei"]:
            print('刑なし')
        else:
            for k in self.meishiki["kei"]:
                b1 = kd.shigo_chu[k[0][1]]   # 支１の場所
                k1 = kd.shi[k[0][0]]         # 支１
                b2 = kd.shigo_chu[k[1][1]]   # 支２の場所
                k2 = kd.shi[k[1][0]]         # 支２
                print(b1 + 'の「' + k1 + '」が、' + b2 + 'の「' + k2 + '」を刑する')
                
        print()
        print('＜害＞')
        if not self.meishiki["gai"]:
            print('害なし')
        else:
            for g in self.meishiki["gai"]:
                b1 = kd.shigo_chu[g[0][1]]   # 支１の場所
                k1 = kd.shi[g[0][0]]         # 支１
                b2 = kd.shigo_chu[g[1][1]]   # 支２の場所
                k2 = kd.shi[g[1][0]]         # 支２
                print(b1 + 'の「' + k1 + '」と' + b2 + 'の「' + k2 + '」とが害')
                
        print()
        print('＜空亡＞')
        if not self.meishiki["kubo"]:
            print('空亡なし')
        else:
            for k in self.meishiki["kubo"]:
                b1 = kd.shigo_chu[k[1]]
                k1 = kd.shi[k[0]]
                print(b1 + 'の「' + k1 + '」が空亡')
