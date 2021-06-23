#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Meishiki import Meishiki
import kanshi_data as kd
import sys
from datetime import datetime as dt
from datetime import timedelta as td


def convert_year_ratio(birthday):

    # ＜機能＞
    # 生年月日から前の節入日までの日数と、生年月日から次の節入日までの日数との比を、
    # 10年に占める割合に直す。
    # 例：8日：22日→3年：7年
    # ＜入力＞
    #   - brithday（datetime）：生年月日
    # ＜出力＞
    #   - year_ratio_list（list）：10年に占める割合    
    
    for s in kd.setsuiri:
        p = is_setsuiri(dt(year = birthday.year, month = birthday.month, day = birthday.day), birthday.month)
        if (s[0] == birthday.year) and (s[1] == birthday.month):
            previous_setsuiri =  dt(year = s[0], month = s[1] + p, day = s[2], hour = s[3], minute = s[4])
            next_setsuiri = dt(year = s[0], month = s[1] + p + 1, day = s[2], hour = s[3], minute = s[4])
            break

    diff_previous = birthday - previous_setsuiri   # 生年月日から前の節入日までの日数
    diff_next = next_setsuiri - birthday           # 生年月日から次の節入日までの日数

    # ３日間を１年に置き換えるので、３除した値を丸める
    p_year = round((diff_previous.days + (diff_previous.seconds / 60 / 60 / 24)) / 3)
    n_year = round((diff_next.days + (diff_next.seconds / 60 / 60 / 24)) / 3)

    year_ratio_list = [p_year, n_year]
    
    return year_ratio_list


def is_junun_gyakuun(y_kan, sex):

    # ＜機能＞
    # 大運が順運か逆運かを判定する
    # ＜入力＞
    #   - y_kan（int）：年柱天干の番号
    #   - sex（int）：性別の番号
    # ＜出力＞
    #   - 順運（1）または逆運（0）の二値
    # ＜異常検出＞
    # 取得できなかった場合はエラーメッセージを出力して強制終了する

    if (((y_kan % 2) == 0) and (sex == 0)) or (((y_kan % 2) == 1) and (sex == 1)):
       return 1   # 年柱天干が陽干の男命 or 年柱天干が陰干の女命は、順運
   
    elif (((y_kan % 2) == 1) and (sex == 0)) or (((y_kan % 2) == 0) and (sex == 1)):
       return 0   # 年柱天干が陽干の女命 or 年柱天干が陰干の男命は、逆運
   
    else:
        print('大運の順逆を判定できませんでした。')
        exit()


def find_kanshi_idx(kan, shi):

    # 六十干支表から所定の干支のインデクスを返す
    
    for idx, sk in enumerate(kd.sixty_kanshi):
        if (sk[0] == kan) and (sk[1] == shi):
            return idx
    
    print('干支が見つかりませんでした。')
    exit()
        

def append_daiun(birthday, sex):

    # ＜機能＞
    # 大運を命式に追加する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    #   - sex（int）：性別の番号
    # ＜出力＞
    #   - daiun（list）：大運のリスト
    
    year_ratio_list = convert_year_ratio(birthday)
    
    if is_junun_gyakuun(meishiki["nenchu"][0], sex):  # 順運か逆運か？
        ry = year_ratio_list[1]  # 次の節入日が立運の起算日
        p = 1                    # 六十干支表を順にたどる
    else:
        ry = year_ratio_list[0]  # 前の節入日が立運の起算日
        p = -1                   # 六十干支表を逆にたどる

    idx = find_kanshi_idx(meishiki["getchu"][0], meishiki["getchu"][1])

    daiun = []
    for n in list(range(10, 140, 10)):
        kanshi_ = kd.sixty_kanshi[idx]
        tsuhen_ = find_tsuhen(meishiki["nitchu_tenkan"], kanshi_[0])
        t_fortune_ = find_twelve_fortune(meishiki["nitchu_tenkan"], kanshi_[1])
        daiun.append([ry, kanshi_[0], kanshi_[1], tsuhen_, t_fortune_])
        ry += 10
        idx += p
        if idx >= 60:
            idx = 0

    meishiki.update({"daiun": daiun})


def append_nenun(birthday):

    # ＜機能＞
    # 年運を命式に追加する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    # ＜出力＞
    #   - nenun（list）：年運のリスト
    
    idx = (birthday.year - 3) % 60 - 1 + is_setsuiri(birthday, 2)
    nenun = []
    for n in list(range(0, 120)):
        kanshi_ = kd.sixty_kanshi[idx]
        tsuhen_ = find_tsuhen(meishiki["nitchu_tenkan"], kanshi_[0])
        t_fortune_ = find_twelve_fortune(meishiki["nitchu_tenkan"], kanshi_[1])
        nenun.append([n, kanshi_[0], kanshi_[1], tsuhen_, t_fortune_])
        idx += 1
        if idx >= 60:
            idx = 0

    meishiki.update({"nenun": nenun})


    

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


# def is_sango(shi, day_kan):

#     sango_ = []
#     sango_flag = False
    
#     for s in kd.sango:
#         for v in itertools.permutations(list(range(0,len(shi))), 3):
#             if [shi[v[0]], shi[v[1]], shi[v[2]]] == s[0]:
#                 sango_.append([shi[v[0]], shi[v[1]], shi[v[2]]])
#                 shi_ = s[1]
#                 kan_ = s[2]
#                 sango_flag = True
#                 break
#         if sango_flag == True:
#             break

#     if not sango_:
#         return sango_
#     elif shi[2] in sango_[0]:
#         sango_.append(shi_)
#         sango_.append(kan_)
#         sango_.append(lookup_tsuhen(day_kan, kan_))
    
#     return sango_

# def disp_sango(sango):

#     if not sango:
#         print('三合なし')
#         return True

#     print('三合：')
#     if len(sango) > 1:
#         print(sango[0][0] + ', ' + sango[0][1] + ', ' + sango[0][2] + 'の三合' + sango[1] + '局により、月柱蔵干（用神）が' + sango[2] + '（' + sango[3] + '）に変化')
#     else:
#         print(sango[0][0] + ', ' + sango[0][1] + ', ' + sango[0][2] + 'の三合会局（用神変化なし）')
        
#     return True


       

        
        

def show_daiun_nenun(birthday):

    year = birthday.year
    m = 0
    flag = False

    print()
    print()
    print('        '+ '年' + '        | ' + '年齢' + '  |      ' + '大運' + '       |      ' + '年運')
    print('------------------+-------+-----------------+------------------')
    
    for n, nenun in enumerate(meishiki["nenun"]):

        n_kan = kd.kan[nenun[1]]
        n_shi = kd.shi[nenun[2]]
        n_tsuhen = kd.tsuhen[nenun[3]]
        n_twelve_fortune = kd.twelve_fortune[nenun[4]]
        
        u = ''.join([n_kan, n_shi]) + ' (' + n_tsuhen + '・' + n_twelve_fortune + ')'
        wareki = kd.convert_to_wareki(dt(year=year, month=birthday.month, day=birthday.day))
        
        if len(str(n)) == 1:
            age = '  ' + str(n)
        elif len(str(n)) == 2:
            age = ' ' + str(n)
        else:
            age = str(n)
        
        daiun = meishiki["daiun"][m]
        d_kan = kd.kan[daiun[1]]
        d_shi = kd.shi[daiun[2]]
        d_tsuhen = kd.tsuhen[daiun[3]]
        d_twelve_fortune = kd.twelve_fortune[daiun[4]]

        if n == daiun[0]:
            d_un_ = ''.join([d_kan, d_shi]) + ' (' + d_tsuhen + '・' + d_twelve_fortune + ')'
            print('' + str(year) + '年（' + wareki + '）| ' + age + '歳' + ' | '+ d_un_ + ' | ' + u)
            print('------------------+-------+-----------------+------------------')
            m += 1
        else:
            print('' + str(year) + '年（' + wareki + '）| ' + age + '歳' + ' |' + '                ' + ' | ' + u)
        year += 1
    


            
if __name__ == '__main__':

    meishiki = Meishiki(sys.argv)
    meishiki.build_meishiki()
    meishiki.append_tsuhen(2)
    meishiki.append_twelve_fortune(2)
    meishiki.append_additional_info()
    meishiki.show_basic_info()
    meishiki.show_meishiki()
    meishiki.show_additional_info()

    exit()

    
    # 起動時の引数から生年月日・性別などのデータを構築する
    birthday, sex, t_flag = build_birthday_data(sys.argv)

    # 命式に干支を追加する
    append_kanshi(birthday, t_flag)

    # 命式に通変と十二運を追加する
    append_tsuhen("nitchu_tenkan", "tenkan_tsuhen", "zokan_tsuhen")
    append_twelve_fortune("nitchu_tenkan", "twelve_fortune")

    # 命式に大運を追加する
    append_daiun(birthday, sex)

    # 命式に年運を追加する
    append_nenun(birthday)

    # 命式にその他の情報を追加する
    append_additional_info(birthday)
    
    # 生年月日・性別を出力する
    show_age(birthday, sex, t_flag)

    # 命式を出力する
    show_meishiki(t_flag)
    # show_daiun_nenun(birthday)
    show_additional_info(birthday, t_flag)
