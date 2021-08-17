import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td
import pdb

class Meishiki:

    birthday = None
    sex = None
    t_flag = None
    std_num = None
    
    meishiki = None
    analysis = None
    
    
    def __init__(self, args, std_num):
        
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

        # クラス変数を初期化する
        self.meishiki = {}
        self.analysis = {}

        # std_num は、天干・蔵干を通算した場合の干の番号
        # 通常は、日干：２、月支蔵干５を指定する
        # 日干と月支蔵干が同じ場合は、時支天干：３、年支天干：０などを指定する        
        self.std_num = std_num

                
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
            m_kan, m_shi = self.month_kanshi[y_kan][month]
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
        
        d = self.birthday.day + self.kisu_table[self.birthday.year - 1926][self.birthday.month - 1] - 1
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
                
            if from_dt <= self.birthday <= to_dt:
                try:
                    t_kan, t_shi = self.time_kanshi[day_kan][i]
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
                if s[1] + p <= 0:
                    y = s[0] - 1
                    m = 12
                else:
                    y = s[0]
                    m = s[1] + p
                setsuiri_ =  dt(year = y, month = m, day = s[2], hour = s[3], minute = s[4])
                
        delta = td(days = self.zokan_time[shi][0], hours = self.zokan_time[shi][1])
        
        try:
            if setsuiri_ + delta >= self.birthday:
                zokan = self.zokan[shi][0]
            else:
                zokan = self.zokan[shi][1]
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

        # 五行（木火土金水）のそれぞれの数を得る
        gogyo = [0] * 5
        for t in tenkan:
            if t != -1:
                gogyo[kd.gogyo_kan[t]] += 1
        for s in chishi:
            if s != -1:
                gogyo[kd.gogyo_shi[s]] += 1

        # 陰陽のそれぞれの数を得る
        inyo = [0] * 2
        for t in tenkan:
            inyo[t % 2] += 1
        for s in chishi:
            inyo[s % 2] += 1
        
        # クラス変数 meishiki に情報を追加していく
        self.meishiki.update({"tenkan": tenkan})
        self.meishiki.update({"chishi": chishi})
        self.meishiki.update({"zokan" : zokan})
        self.meishiki.update({"nenchu": nenchu})
        self.meishiki.update({"getchu": getchu})
        self.meishiki.update({"nitchu": nitchu})
        self.meishiki.update({"jichu" : jichu})
        self.meishiki.update({"gogyo" : gogyo})
        self.meishiki.update({"inyo"  : inyo})
        self.meishiki.update({"nitchu_tenkan": d_kan})
        self.meishiki.update({"getchu_chishi": m_shi})
        self.meishiki.update({"getchu_zokan" : m_zkan})


    def find_tsuhen(self, s_kan, kan_):
        try:
            if kan_ == -1:
                return -1
            else:
                return kd.kan_tsuhen[s_kan].index(kan_)
        except:
            return -1
        

    def append_tsuhen(self):
        
        kan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        std = kan[self.std_num]

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
            

    def append_twelve_fortune(self):
        
        kan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        std = kan[self.std_num]
        
        f = []
        for s in self.meishiki["chishi"]:
            f.append(self.find_twelve_fortune(std, s))

        self.meishiki.update({"twelve_fortune": f})


    def append_getsurei(self):
        
        # ＜機能＞
        # 月令の旺衰強弱を命式に追加する
        # ＜入力＞
        #   - self.birthday（datetime）：生年月日
        # ＜出力＞
        #   - kd.getsurei に対応する番号

        kan = self.meishiki["tenkan"] + self.meishiki["zokan"]
        std = kan[self.std_num]
        
        bm = self.birthday.month + self.is_setsuiri(self.birthday.month)
        
        if bm == 12:
            bm = 0
        shi_ = kd.shi[bm]    # 生まれ月の地支を引く（節入りを考慮している？？？）→見直しの余地あり
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
        
        d = self.birthday.day + self.kisu_table[self.birthday.year - 1926][self.birthday.month - 1] - 1
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


    def append_sango(self):

        # ＜機能＞
        # 三合会局の有無を判定し、あれば命式に追加する
        # 追加されるのは、
        # [[支１, 支２, 支３], 五行, 変化した後の干, 変化する前の干, 変化する前の干の通変, 変化した後の干の通変]
        
        chishi = self.meishiki["chishi"]

        sango = []
        for s in kd.sango:
            if (s[0][0] in chishi) and (s[0][1] in chishi) and (s[0][2] in chishi):
                sango = s + [self.meishiki["zokan"][1], self.meishiki["tsuhen"][5]]
                self.meishiki["zokan"][1] = s[2]
                self.meishiki["getchu"][2] = s[2]
                self.append_tsuhen()
                self.append_twelve_fortune()
                sango += [self.meishiki["tsuhen"][5]]
                break
        
        self.meishiki.update({"sango": sango})


    def append_hankai(self):

        # 半会の有無を判定し、命式に追加する
        # [[支１, 支２], 足りない支, 五行, 変化した後の干]
        
        chishi = self.meishiki["chishi"]

        hankai = []
        for h in kd.hankai:
            if (h[0][0] in chishi) and (h[0][1] in chishi):
                hankai.append(h)
                
        self.meishiki.update({"hankai": hankai})
        

    def append_additional_info(self):
        
        # 命式にその他の情報を追加する
        
        self.append_sango()      # 三合会局を追加
        self.append_getsurei()   # 月令を追加
        self.append_kango()      # 干合を追加
        self.append_shigo()      # 支合を追加
        self.append_hogo()       # 方合を追加
        self.append_kei()        # 刑を追加
        self.append_gai()        # 害を追加
        self.append_kubo()       # 空亡を追加
        self.append_hankai()     # 半会を追加
        self.append_hitsuchu()   # 七冲を追加

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
                  '| ' + tenkan[2] + '（' + tsuhen[2] + '） ' +
                  '| ' + tenkan[1] + '（' + tsuhen[1] + '） ' +
                  '| ' + tenkan[0] + '（' + tsuhen[0] + '） ' +
                  '|')            
            # print('| ' + tenkan[3] + '（' + tsuhen[3] + '） ' +
            #       '|     ' + tenkan[2] +
            #       '     | ' + tenkan[1] + '（' + tsuhen[1] + '） ' +
            #       '| ' + tenkan[0] + '（' + tsuhen[0] + '）' +
            #       ' |')
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
            


    def show_additional_info(self, flag):

        if flag:
            print()
            print('＜五行＞')
            for i, g in enumerate(self.meishiki["gogyo"]):
                print(kd.gogyo[i] + '：' + str(g))
            print()
            print('＜陰陽のバランス＞')
            print('陰：' + str(self.meishiki["inyo"][1]))
            print('陽：' + str(self.meishiki["inyo"][0]))

        print()
        print('＜月令＞')
        print(kd.getsurei[self.meishiki["getsurei"]])

        if flag:
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
                    
            print()
            print('＜三合会局＞')
            if not self.meishiki["sango"]:
                print('三合会局なし')
            else:
                sango = self.meishiki["sango"]
                print(kd.shi[sango[0][0]] + ', ' + kd.shi[sango[0][1]] + ', ' + kd.shi[sango[0][2]] + 'の三合' + kd.gogyo[sango[1]]+ '局により、月支蔵干が' + kd.kan[sango[3]] + '（' + kd.tsuhen[sango[4]] + '）から' + kd.kan[sango[2]] + '（' + kd.tsuhen[sango[5]] +'）に変化する')

            print()
            print('＜半会＞')
            if not self.meishiki["hankai"]:
                print('半会なし')
            else:
                hankai = self.meishiki["hankai"]
                for h in hankai:
                    print(kd.shi[h[0][0]] + ', ' + kd.shi[h[0][1]] + 'が' + kd.gogyo[h[2]] + '局半会')
                    

    month_kanshi = [
        [ [3, 1,],  # 甲
          [2, 2,],
          [3, 3,],
          [4, 4,],
          [5, 5,],
          [6, 6,],
          [7, 7,],
          [8, 8,],
          [9, 9,],
          [0, 10,],
          [1, 11,],
          [2, 0,], ],
        [ [5, 1,],  # 乙
          [4, 2,],
          [5, 3,],
          [6, 4,],
          [7, 5,],
          [8, 6,],
          [9, 7,],
          [0, 8,],
          [1, 9,],
          [2, 10,],
          [3, 11,],
          [4, 0,], ],
        [ [7, 1,],  # 丙
          [6, 2,],
          [7, 3,],
          [8, 4,],
          [9, 5,],
          [0, 6,],
          [1, 7,],
          [2, 8,],
          [3, 9,],
          [4, 10,],
          [5, 11,],
          [6, 0,], ],
        [ [9, 1,],  # 丁
          [8, 2,],
          [9, 3,],
          [0, 4,],
          [1, 5,],
          [2, 6,],
          [3, 7,],
          [4, 8,],
          [5, 9,],
          [6, 10,],
          [7, 11,],
          [8, 0,], ],
        [ [1, 1,],  # 戊
          [0, 2,],
          [1, 3,],
          [2, 4,],
          [3, 5,],
          [4, 6,],
          [5, 7,],
          [6, 8,],
          [7, 9,],
          [8, 10,],
          [9, 11,],
          [0, 0,], ],
        [ [3, 1,],  # 己
          [2, 2,],
          [3, 3,],
          [4, 4,],
          [5, 5,],
          [6, 6,],
          [7, 7,],
          [8, 8,],
          [9, 9,],
          [0, 10,],
          [1, 11,],
          [2, 0,], ],
        [ [5, 1,],  # 庚
          [4, 2,],
          [5, 3,],
          [6, 4,],
          [7, 5,],
          [8, 6,],
          [9, 7,],
          [0, 8,],
          [1, 9,],
          [2, 10,],
          [3, 11,],
          [4, 0,], ],
        [ [7, 1,],  # 辛
          [6, 2,],
          [7, 3,],
          [8, 4,],
          [9, 5,],
          [0, 6,],
          [1, 7,],
          [2, 8,],
          [3, 9,],
          [4, 10,],
          [5, 11,],
          [6, 0,], ],
        [ [9, 1,],  # 壬
          [8, 2,],
          [9, 3,],
          [0, 4,],
          [1, 5,],
          [2, 6,],
          [3, 7,],
          [4, 8,],
          [5, 9,],
          [6, 10,],
          [7, 11,],
          [8, 0,], ],
        [ [1, 1,],  # 癸
          [0, 2,],
          [1, 3,],
          [2, 4,],
          [3, 5,],
          [4, 6,],
          [5, 7,],
          [6, 8,],
          [7, 9,],
          [8, 10,],
          [9, 11,],
          [0, 0,], ],
    ]

    time_kanshi = [
        [ [0, 0],    # 甲
          [1, 1],
          [2, 2],
          [3, 3],
          [4, 4],
          [5, 5],
          [6, 6],
          [7, 7],
          [8, 8],
          [9, 9],
          [0, 10],
          [1, 11],
          [2, 0], ],
        [ [2, 0],    # 乙
          [3, 1],
          [4, 2],
          [5, 3],
          [6, 4],
          [7, 5],
          [8, 6],
          [9, 7],
          [0, 8],
          [1, 9],
          [2, 10],
          [3, 11],
          [4, 0], ],
        [ [4, 0],    # 丙
          [5, 1],
          [6, 2],
          [7, 3],
          [8, 4],
          [9, 5],
          [0, 6],
          [1, 7],
          [2, 8],
          [3, 9],
          [4, 10],
          [5, 11],
          [6, 0], ],
        [ [6, 0],   # 丁
          [7, 1],
          [8, 2],
          [9, 3],
          [0, 4],
          [1, 5],
          [2, 6],
          [3, 7],
          [4, 8],
          [5, 9],
          [6, 10],
          [7, 11],
          [8, 0], ],
        [ [8, 0],   # 戊
          [9, 1],
          [0, 2],
          [1, 3],
          [2, 4],
          [3, 5],
          [4, 6],
          [5, 7],
          [6, 8],
          [7, 9],
          [8, 10],
          [9, 11],
          [0, 0], ],
        [ [0, 0],    # 己
          [1, 1],
          [2, 2],
          [3, 3],
          [4, 4],
          [5, 5],
          [6, 6],
          [7, 7],
          [8, 8],
          [9, 9],
          [0, 10],
          [1, 11],
          [2, 0], ],
        [ [2, 0],    # 庚
          [3, 1],
          [4, 2],
          [5, 3],
          [6, 4],
          [7, 5],
          [8, 6],
          [9, 7],
          [0, 8],
          [1, 9],
          [2, 10],
          [3, 11],
          [4, 0], ],
        [ [4, 0],    # 辛
          [5, 1],
          [6, 2],
          [7, 3],
          [8, 4],
          [9, 5],
          [0, 6],
          [1, 7],
          [2, 8],
          [3, 9],
          [4, 10],
          [5, 11],
          [6, 0], ],
        [ [6, 0],   # 壬
          [7, 1],
          [8, 2],
          [9, 3],
          [0, 4],
          [1, 5],
          [2, 6],
          [3, 7],
          [4, 8],
          [5, 9],
          [6, 10],
          [7, 11],
          [8, 0], ],
        [ [8, 0],   # 癸
          [9, 1],
          [0, 2],
          [1, 3],
          [2, 4],
          [3, 5],
          [4, 6],
          [5, 7],
          [6, 8],
          [7, 9],
          [8, 10],
          [9, 11],
          [0, 0], ],
    ]

    kisu_table = [
        [26, 57, 25, 56, 26, 57, 27, 58, 29, 59, 30,  0], # 昭和1(1926年)
        [31,  2, 30,  1, 31,  2, 32,  3, 34,  4, 35,  5], # 昭和2
        [36,  7, 36,  7, 37,  8, 38,  9, 40, 10, 41, 11], # 昭和3
        [42, 13, 41, 12, 42, 13, 43, 14, 45, 15, 46, 16], # 昭和4
        [47, 18, 46, 17, 47, 18, 48, 19, 50, 20, 51, 21], # 昭和5
        [52, 23, 51, 22, 52, 23, 53, 24, 55, 25, 56, 26], # 昭和6
        [57, 28, 57, 28, 58, 29, 59, 30,  1, 31,  2, 32], # 昭和7
        [ 3, 34,  2, 33,  3, 34,  4, 35,  6, 36,  7, 37], # 昭和8
        [ 8, 39,  7, 38,  8, 39,  9, 40, 11, 41, 12, 42], # 昭和9
        [13, 44, 12, 43, 13, 44, 14, 45, 16, 46, 17, 47], # 昭和10
        [18, 49, 18, 49, 19, 50, 20, 51, 22, 52, 23, 53], # 昭和11
        [24, 55, 23, 54, 24, 55, 25, 56, 27, 57, 28, 58], # 昭和12
        [29,  0, 28, 59, 29,  0, 30,  1, 32,  2, 33,  3], # 昭和13
        [34,  5, 33,  4, 34,  5, 35,  6, 37,  7, 38,  8], # 昭和14
        [39, 10, 39, 10, 40, 11, 41, 12, 43, 13, 44, 14], # 昭和15
        [45, 16, 44, 15, 45, 16, 46, 17, 48, 18, 49, 19], # 昭和16
        [50, 21, 49, 20, 50, 21, 51, 22, 53, 23, 54, 24], # 昭和17
        [55, 26, 54, 25, 55, 26, 56, 27, 58, 28, 59, 29], # 昭和18
        [ 0, 31,  0, 31,  1, 32,  2, 33,  4, 34,  5, 35], # 昭和19
        [ 6, 37,  5, 36,  6, 37,  7, 38,  9, 39, 10, 40], # 昭和20
        [11, 42, 10, 41, 11, 42, 12, 43, 14, 44, 15, 45], # 昭和21
        [16, 47, 15, 46, 16, 47, 17, 48, 19, 49, 20, 50], # 昭和22
        [21, 52, 21, 52, 22, 53, 23, 54, 25, 55, 26, 56], # 昭和23(1948)
        [27, 58, 26, 57, 27, 58, 28, 59, 30,  0, 31,  1], # 昭和24
        [32,  3, 31,  2, 32,  3, 33,  4, 35,  5, 36,  6], # 昭和25
        [37,  8, 36,  7, 37,  8, 38,  9, 40, 10, 41, 11], # 昭和26
        [42, 13, 42, 13, 43, 14, 44, 15, 46, 16, 47, 17], # 昭和27
        [48, 19, 47, 18, 48, 19, 49, 20, 51, 21, 52, 22], # 昭和28
        [53, 24, 52, 23, 53, 24, 54, 25, 56, 26, 57, 27], # 昭和29
        [58, 29, 57, 28, 58, 29, 59, 30,  1, 31,  2, 32], # 昭和30
        [ 3, 34,  3, 34,  4, 35,  5, 36,  7, 37,  8, 38], # 昭和31
        [ 9, 40,  8, 39,  9, 40, 10, 41, 12, 42, 13, 43], # 昭和32
        [14, 45, 13, 44, 14, 45, 15, 46, 17, 47, 18, 48], # 昭和33
        [19, 50, 18, 49, 19, 50, 20, 51, 22, 52, 23, 53], # 昭和34
        [24, 55, 24, 55, 25, 56, 26, 57, 28, 58, 29, 59], # 昭和35
        [30,  1, 29,  0, 30,  1, 31,  2, 33,  3, 34,  4], # 昭和36
        [35,  6, 34,  5, 35,  6, 36,  7, 38,  8, 39,  9], # 昭和37
        [40, 11, 39, 10, 40, 11, 41, 12, 43, 13, 44, 14], # 昭和38
        [45, 16, 45, 16, 46, 17, 47, 18, 49, 19, 50, 20], # 昭和39
        [51, 22, 50, 21, 51, 22, 52, 23, 54, 24, 55, 25], # 昭和40
        [56, 27, 55, 26, 56, 27, 57, 28, 59, 29,  0, 30], # 昭和41
        [ 1, 32,  0, 31,  1, 32,  2, 33,  4, 34,  5, 35], # 昭和42
        [ 6, 37,  6, 37,  7, 38,  8, 39, 10, 40, 11, 41], # 昭和43
        [12, 43, 11, 42, 12, 43, 13, 44, 15, 45, 16, 46], # 昭和44
        [17, 48, 16, 47, 17, 48, 18, 49, 20, 50, 21, 51], # 昭和45
        [22, 53, 21, 52, 22, 53, 23, 54, 25, 55, 26, 56], # 昭和46
        [27, 58, 27, 58, 28, 59, 29,  0, 31,  1, 32,  2], # 昭和47
        [33,  4, 32,  3, 33,  4, 34,  5, 36,  6, 37,  7], # 昭和48
        [38,  9, 37,  8, 38,  9, 39, 10, 41, 11, 42, 12], # 昭和49
        [43, 14, 42, 13, 43, 14, 44, 15, 46, 16, 47, 17], # 昭和50
        [48, 19, 48, 19, 49, 20, 50, 21, 52, 22, 53, 23], # 昭和51
        [54, 25, 53, 24, 54, 25, 55, 26, 57, 27, 58, 28], # 昭和52
        [59, 30, 58, 29, 59, 30,  0, 31,  2, 32,  3, 33], # 昭和53
        [ 4, 35,  3, 34,  4, 35,  5, 36,  7, 37,  8, 38], # 昭和54
        [ 9, 40,  9, 40, 10, 41, 11, 42, 13, 43, 14, 44], # 昭和55
        [15, 46, 14, 45, 15, 46, 16, 47, 18, 48, 19, 49], # 昭和56
        [20, 51, 19, 50, 20, 51, 21, 52, 23, 53, 24, 54], # 昭和57
        [25, 56, 24, 55, 25, 56, 26, 57, 28, 58, 29, 59], # 昭和58
        [30,  1, 30,  1, 31,  2, 32,  3, 34,  4, 35,  5], # 昭和59
        [36,  7, 35,  6, 36,  7, 37,  8, 39,  9, 40, 10], # 昭和60
        [41, 12, 40, 11, 41, 12, 42, 13, 44, 14, 45, 15], # 昭和61
        [46, 17, 45, 16, 46, 17, 47, 18, 49, 19, 50, 20], # 昭和62
        [51, 22, 51, 22, 52, 23, 53, 24, 55, 25, 56, 26], # 昭和63
        [57, 28, 56, 27, 57, 28, 58, 29,  0, 30,  1, 31], # 平成1
        [ 2, 33,  1, 32,  2, 33,  3, 34,  5, 35,  6, 36], # 平成2
        [ 7, 38,  6, 37,  7, 38,  8, 39, 10, 40, 11, 41], # 平成3
        [12, 43, 12, 43, 13, 44, 14, 45, 16, 46, 17, 47], # 平成4
        [18, 49, 17, 48, 18, 49, 19, 50, 21, 51, 22, 52], # 平成5
        [23, 54, 22, 53, 23, 54, 24, 55, 26, 56, 27, 57], # 平成6
        [28, 59, 27, 58, 28, 59, 29,  0, 31,  1, 32,  2], # 平成7
        [33,  4, 33,  4, 34,  5, 35,  6, 37,  7, 38,  8], # 平成8
        [39, 10, 38,  9, 39, 10, 40, 11, 42, 12, 43, 13], # 平成9
        [44, 15, 43, 14, 44, 15, 45, 16, 47, 17, 48, 18], # 平成10
        [49, 20, 48, 19, 49, 20, 50, 21, 52, 22, 53, 23], # 平成11
        [54, 25, 54, 25, 55, 26, 56, 27, 58, 28, 59, 29], # 平成12
        [ 0, 31, 59, 30,  0, 31,  1, 32,  3, 33,  4, 34], # 平成13
        [ 5, 36,  4, 35,  5, 36,  6, 37,  8, 38,  9, 39], # 平成14
        [10, 41,  9, 40, 10, 41, 11, 42, 13, 43, 14, 44], # 平成15
        [15, 46, 15, 46, 16, 47, 17, 48, 19, 49, 20, 50], # 平成16
        [21, 52, 20, 51, 21, 52, 22, 53, 24, 54, 25, 55], # 平成17
        [26, 57, 25, 56, 26, 57, 27, 58, 29, 59, 30,  0], # 平成18
        [31,  2, 30,  1, 31,  2, 32,  3, 34,  4, 35,  5], # 平成19
        [36,  7, 36,  7, 37,  8, 38,  9, 40, 10, 41, 11], # 平成20
        [42, 13, 41, 12, 42, 13, 43, 14, 45, 15, 46, 16], # 2009年
        [47, 18, 46, 17, 47, 18, 48, 19, 50, 20, 51, 21], # 2010年
        [52, 23, 51, 22, 52, 23, 53, 24, 55, 25, 56, 26], # 2011年
        [57, 28, 57, 28, 58, 29, 59, 30,  1, 31,  2, 32], # 2012年
        [ 3, 34,  2, 33,  3, 34,  4, 35,  6, 36,  7, 37], # 2013年
        [ 8, 39,  7, 38,  8, 39,  9, 40, 11, 41, 12, 42], # 2014年
        [13, 44, 12, 43, 13, 44, 14, 45, 16, 46, 17, 47], # 2015年
        [18, 49, 18, 49, 19, 50, 20, 51, 22, 52, 23, 53], # 2016年
        [24, 55, 23, 54, 24, 55, 25, 56, 27, 57, 28, 58], # 2017年
        [29,  0, 28, 59, 29,  0, 30,  1, 32,  2, 33,  3], # 2018年
        [34,  5, 33,  4, 34,  5, 35,  6, 37,  7, 38,  8], # 2019年
        [39, 10, 39, 10, 40, 11, 41, 12, 43, 13, 44, 14], # 2020年
        [45, 16, 44, 15, 45, 16, 46, 17, 48, 18, 49, 19], # 2021年
        [50, 21, 49, 20, 50, 21, 51, 22, 53, 23, 54, 24], # 2022年
        [55, 26, 54, 25, 55, 26, 56, 27, 58, 28, 59, 29], # 2023年
        [ 0, 31,  0, 31,  1 ,32,  2, 33,  4, 34,  5, 35], # 2024年
        [ 6, 37,  5, 36,  6, 37,  7, 38,  9, 39, 10, 40], # 2025年
        [11, 42, 10, 41, 11, 42, 12, 43, 14, 44, 15, 45], # 2026年
        [16, 47, 15, 46, 16, 47, 17, 48, 19, 49, 20, 50], # 2027年
        [21, 52, 21, 52, 22, 53, 23, 54, 25, 55, 26, 56], # 2028年
        [27, 58, 26, 57, 27, 58, 28, 59, 30,  0, 31,  1], # 2029年
        [32,  3, 31,  2, 32,  3, 33,  4, 35,  5, 36,  6], # 2030年
        [37,  8, 36,  7, 37,  8, 38,  9, 40, 10, 41, 11], # 2031年
        [42, 13, 42, 13, 43, 14, 44, 15, 46, 16, 47, 17], # 2032年
        [48, 19, 47, 18, 48, 19, 49, 20, 51, 21, 52, 22], # 2033年
        [53, 24, 52, 23, 53, 24, 54, 25, 56, 26, 57, 27], # 2034年
        [58, 29, 57, 28, 58, 29, 59, 30,  1, 31,  2, 32], # 2035年
        [ 3, 34,  3, 34,  4, 35,  5, 36,  7, 37,  8, 38], # 2036年
        [44, 15, 43, 14, 44, 15, 45, 16, 47, 17, 48, 18], # 2037年
    ]

    zokan = [
        [8, 9,],  # 子
        [9, 5,],  # 丑
        [4, 0,],  # 寅
        [0, 1,],  # 卯
        [1, 4,],  # 辰
        [4, 2,],  # 巳
        [2, 3,],  # 午
        [3, 5,],  # 未
        [4, 6,],  # 申
        [6, 7,],  # 酉
        [7, 4,],  # 戌
        [4, 8,],  # 亥
    ]
    
    zokan_time = [
        [10, 1],
        [9, 3],
        [7, 2],
        [10, 3],
        [9, 3],
        [7, 2],
        [10, 0],
        [9, 3],
        [7, 2],
        [10, 3],
        [9, 3],
        [7, 2],
    ]

    
# def is_kakikaku(kango, month_shi):

#     henkaku = ''
#     p = -1
#     for k in kango:
#         if 1 in k[0] and 2 in k[1]:
#             henkaku = k[2]
#             p = 1
#             break
#         elif 2 in k[0] and 3 in k[1]:
#             henkaku = k[2]
#             p = 3
#             break
#         else:
#             pass

#     if henkaku == kd.gogyo_shi[kd.shi.index(month_shi)] and p != -1:
#         henkaku = kd.chu[p] + 'との干合により化気' + henkaku + '格となる'
#     else:
#         henkaku = '化気格なし'

#     return henkaku
