import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td
import itertools
import pdb

class Unsei:

    meishiki = None
    birthday = dt.now()
    sex = -1
    daiun = []
    nenun = []

    def __init__(self, meishiki):

        self.meishiki = meishiki
        self.birthday = meishiki.birthday
        self.sex = meishiki.sex

        
    def convert_year_ratio(self):
        
        # ＜機能＞
        # 生年月日から前の節入日までの日数と、生年月日から次の節入日までの日数との比を、
        # 10年に占める割合に直す。
        # 例：8日：22日→3年：7年
        # ＜入力＞
        #   - brithday（datetime）：生年月日
        # ＜出力＞
        #   - year_ratio_list（list）：10年に占める割合
        
        for i, s in enumerate(kd.setsuiri):
            p = self.meishiki.is_setsuiri(self.birthday.month)
            if (s[0] == self.birthday.year) and (s[1] == self.birthday.month):
                if not p:
                    k = kd.setsuiri[i+1]
                    previous_setsuiri = dt(year = s[0], month = s[1], day = s[2], hour = s[3], minute = s[4])
                    next_setsuiri = dt(year = k[0], month = k[1], day = k[2], hour = k[3], minute = k[4])
                else:
                    k = kd.setsuiri[i-1]
                    previous_setsuiri = dt(year = k[0], month = k[1], day = k[2], hour = k[3], minute = k[4])
                    next_setsuiri = dt(year = s[0], month = s[1], day = s[2], hour = s[3], minute = s[4])
                break
            
        diff_previous = self.birthday - previous_setsuiri   # 生年月日から前の節入日までの日数
        diff_next = next_setsuiri - self.birthday           # 生年月日から次の節入日までの日数
        
        # ３日間を１年に置き換えるので、３除した値を丸める
        p_year = round((diff_previous.days + (diff_previous.seconds / 60 / 60 / 24)) / 3)
        n_year = round((diff_next.days + (diff_next.seconds / 60 / 60 / 24)) / 3)
        
        year_ratio_list = [p_year, n_year]

        return year_ratio_list


    def is_junun_gyakuun(self, y_kan):

        # ＜機能＞
        # 大運が順運か逆運かを判定する
        # ＜入力＞
        #   - y_kan（int）：年柱天干の番号
        #   - self.sex（int）：性別の番号
        # ＜出力＞
        #   - 順運（1）または逆運（0）の二値
        # ＜異常検出＞
        # 取得できなかった場合はエラーメッセージを出力して強制終了する
        
        if (((y_kan % 2) == 0) and (self.sex == 0)) or (((y_kan % 2) == 1) and (self.sex == 1)):
            return 1   # 年柱天干が陽干の男命 or 年柱天干が陰干の女命は、順運
        
        elif (((y_kan % 2) == 1) and (self.sex == 0)) or (((y_kan % 2) == 0) and (self.sex == 1)):
            return 0   # 年柱天干が陽干の女命 or 年柱天干が陰干の男命は、逆運
        
        else:
            print('大運の順逆を判定できませんでした。')
            exit()
    
            
    def find_kanshi_idx(self, kan, shi, p):
        
        # 六十干支表から所定の干支のインデクスを返す
        
        for idx, sk in enumerate(kd.sixty_kanshi):
            if (sk[0] == kan) and (sk[1] == shi):
                return idx + p
            
        print('干支が見つかりませんでした。')
        exit()
        

    def append_daiun(self):

        # ＜機能＞
        # 大運を命式に追加する
        # ＜入力＞
        #   - self.birthday（datetime）：生年月日
        #   - self.sex（int）：性別の番号
        # ＜出力＞
        #   - daiun（list）：大運のリスト
        
        year_ratio_list = self.convert_year_ratio()
        
        if self.is_junun_gyakuun(self.meishiki.meishiki["nenchu"][0]):  # 順運か逆運か？
            ry = year_ratio_list[1]  # 次の節入日が立運の起算日
            p = 1                    # 六十干支表を順にたどる
        else:
            ry = year_ratio_list[0]  # 前の節入日が立運の起算日
            p = -1                   # 六十干支表を逆にたどる
            
        idx = self.find_kanshi_idx(self.meishiki.meishiki["getchu"][0], self.meishiki.meishiki["getchu"][1], p)
        
        for n in list(range(10, 140, 10)):
            if idx >= 60:
                idx = 0
            kanshi_ = kd.sixty_kanshi[idx]
            tsuhen_ = self.meishiki.find_tsuhen(self.meishiki.meishiki["nitchu_tenkan"], kanshi_[0])
            t_fortune_ = self.meishiki.find_twelve_fortune(self.meishiki.meishiki["nitchu_tenkan"], kanshi_[1])
            self.daiun.append([ry, kanshi_[0], kanshi_[1], tsuhen_, t_fortune_])
            ry += 10
            idx += p


    def append_nenun(self):
        
        # ＜機能＞
        # 年運を命式に追加する
        # ＜入力＞
        #   - self.birthday（datetime）：生年月日
        # ＜出力＞
        #   - nenun（list）：年運のリスト
        
        idx = (self.birthday.year - 3) % 60 - 1 # + self.meishiki.is_setsuiri(2)
        
        for n in list(range(0, 120)):
            kanshi_ = kd.sixty_kanshi[idx]
            tsuhen_ = self.meishiki.find_tsuhen(self.meishiki.meishiki["nitchu_tenkan"], kanshi_[0])
            t_fortune_ = self.meishiki.find_twelve_fortune(self.meishiki.meishiki["nitchu_tenkan"], kanshi_[1])
            self.nenun.append([n, kanshi_[0], kanshi_[1], tsuhen_, t_fortune_])
            idx += 1
            if idx >= 60:
                idx = 0


    def append_unsei(self):

        for ne in self.nenun:

            # 天戦地冲運を見る
            if (ne[2] == kd.hitsuchu_rev[self.meishiki.meishiki["chishi"][2]]) and (ne[3] == 6):
                ne += ['天戦地冲運']
            else:
                ne += ['']

            du = (ne[0] - self.daiun[0][0]) // 10
            hogo_sango = self.meishiki.meishiki["chishi"] + [self.daiun[du][2]] + [ne[2]]
            hs_comb = itertools.permutations(hogo_sango, 3)
            hs_list = []
            for comb in hs_comb:
                hs_list.append(list(comb))
            
            # 方合を見る
            if not self.meishiki.meishiki["hogo"]:
                hg = -1
                for i, h in enumerate([kd.hogo[0][0]] + [kd.hogo[1][0]] + [kd.hogo[2][0]] + [kd.hogo[3][0]]):
                    if h in hs_list:
                        hg = i
                        break
                if hg == 0:
                    ne += ['水方合']
                elif hg == 1:
                    ne += ['木方合']
                elif hg == 2:
                    ne += ['火方合']
                elif hg == 3:
                    ne += ['金方合']
                else:
                    ne += ['']
            else:
                ne += ['']
            
            # 三合を見る
            if not self.meishiki.meishiki["sango"]:
                sg = -1
                for i, h in enumerate([kd.sango[0][0]] + [kd.sango[1][0]] + [kd.sango[2][0]] + [kd.sango[3][0]]):
                    if h in hs_list:
                        sg = i
                        break
                if sg == 0:
                    ne += ['三合木局']
                elif sg == 1:
                    ne += ['三合火局']
                elif sg == 2:
                    ne += ['三合金局']
                elif sg == 3:
                    ne += ['三合水局']
                else:
                    ne += ['']
            else:
                ne += ['']

                

    def show_daiun_nenun(self):
        
        year = self.birthday.year
        m = 0
        flag = False
        
        print()
        print()
        print('        '+ '年' + '        | ' + '年齢' + '  |    ' + '大運' + '     |      ' + '年運' + '   |    運勢    ')
        print('------------------+-------+-------------+-------------+-----')

        for n, nenun in enumerate(self.nenun):
            
            n_kan = kd.kan[nenun[1]]
            n_shi = kd.shi[nenun[2]]
            n_tsuhen = kd.tsuhen[nenun[3]]
            n_twelve_fortune = kd.twelve_fortune[nenun[4]]
            
            u = ''.join([n_kan, n_shi]) + ' (' + n_tsuhen + ')'
            wareki = kd.convert_to_wareki(dt(year=year, month=self.birthday.month, day=self.birthday.day))
            
            if len(str(n)) == 1:
                age = '  ' + str(n)
            elif len(str(n)) == 2:
                age = ' ' + str(n)
            else:
                age = str(n)
                
            daiun = self.daiun[m]
            d_kan = kd.kan[daiun[1]]
            d_shi = kd.shi[daiun[2]]
            d_tsuhen = kd.tsuhen[daiun[3]]
            d_twelve_fortune = kd.twelve_fortune[daiun[4]]
            
            if n == daiun[0]:
                d_un_ = ''.join([d_kan, d_shi]) + ' (' + d_tsuhen + ')'
                print('------------------+-------+-------------+-------------+-----')
                print('' + str(year) + '年（' + wareki + '）| ' + age + '歳' + ' | '+ d_un_ + ' | ' + u + ' | ' + nenun[5] + nenun[6] + nenun[7])
                m += 1
            else:
                print('' + str(year) + '年（' + wareki + '）| ' + age + '歳' + ' |' + '            ' + ' | ' + u + ' | ' + nenun[5] + nenun[6] + nenun[7])
            year += 1
                
