#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kanshi_data as kd
import sys
from datetime import datetime as dt
from datetime import timedelta as td

meishiki = {}

def build_birthday_data(args):

    # 起動時の引数から生年月日・性別などのデータを構築する
    
    args = sys.argv
    try:
        b = args[1]
        t = args[2]
        sex = int(args[3])
        birthday = dt.strptime(b + ' ' + t, '%Y-%m-%d %H:%M')
        t_flag = True
        # サマータイムを考慮する
        if (dt(year=1948, month=5, day=2) <= birthday < dt(year=1951, month=9, day=8)) and (hour is not None):
            birthday = dt(year = birthday.year, month = birthday.month, day = birthday.day,
                          hour = birthday.hour - 1, minute = birthday.minute)
        
    except IndexError:
        try:
            b = args[1]
            sex = int(args[2])
            birthday = dt.strptime(b, '%Y-%m-%d')
            t_flag = False
            
        except IndexError:
            print('引数の指定を確認してください。')
            exit()
            
    return birthday, sex, t_flag


def is_setsuiri(birthday, month):
    
    # ＜機能＞
    # birthday で与えられた年月日が、month で与えられた月に対して節入りしているか否かを判定する
    # ＜入力＞
    #   - birthday（datetime）：判定したい年月日
    #   - month（int）：基準となる月
    # ＜出力＞
    #   - 節入りしている（0）またはしていない（-1）の二値
    # ＜異常検出＞
    # 判定不可能の場合はエラーメッセージを出力して強制終了する

    for s in kd.setsuiri:
        if (s[0] == birthday.year) and (s[1] == month):
            setsuiri_ = dt(year = s[0], month = s[1], day = s[2], hour = s[3], minute = s[4])
            if setsuiri_ < birthday:
                return 0    # 節入りしている
            else:
                return -1   # 節入りしていない

    print('節入りを判定できませんでした。')
    exit()


def find_year_kanshi(birthday):

    # ＜機能＞
    # birthday で与えられた生年月日の年干支を取得する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    # ＜出力＞
    #   - y_kan（int）：年干の番号
    #   - y_shi（int）：年支の番号
    # ＜異常検出＞
    # 取得できなかった場合はエラーメッセージを出力して強制終了する

    sixty_kanshi_idx = (birthday.year - 3) % 60 - 1 + is_setsuiri(birthday, 2)
    try:
        y_kan, y_shi = kd.sixty_kanshi[sixty_kanshi_idx]
        return y_kan, y_shi
    except:
        print('年干支の計算で例外が送出されました。')
        exit()


def find_month_kanshi(birthday, y_kan):

    # ＜機能＞
    # birthday で与えられた生年月日の月干支を取得する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    #   - y_kan（string）：年干の番号
    # ＜出力＞
    #   - m_kan（int）：月干の番号
    #   - m_shi（int）：月支の番号
    # ＜異常検出＞
    # 取得できなかった場合はエラーメッセージを出力して強制終了する

    month = birthday.month - 1 + is_setsuiri(birthday, birthday.month)
    try:
        m_kan, m_shi = kd.month_kanshi[y_kan][month]
        return m_kan, m_shi
    except:
        print('月干支の計算で例外が送出されました。')
        exit()


def find_day_kanshi(birthday):

    # ＜機能＞
    # birthday で与えられた生年月日の日干支を取得する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    # ＜出力＞
    #   - d_kan（int）：日干の番号
    #   - d_shi（int）：日支の番号
    # ＜異常検出＞
    # 取得できなかった場合はエラーメッセージを出力して強制終了する
    
    d = birthday.day + kd.kisu_table[birthday.year - 1926][birthday.month - 1] - 1
    if d >= 60:
        d -= 60  # d が 60 を超えたら 60 を引く
    
    try:
        d_kan, d_shi = kd.sixty_kanshi[d]
        return d_kan, d_shi
    except:
        print('日干支の計算で例外が送出されました。')
        exit()


def find_time_kanshi(birthday, day_kan):

    # ＜機能＞
    # birthday で与えられた生年月日の時干支を取得する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    #   - day_kan（int）：日干の番号
    # ＜出力＞
    #   - t_kan（int）：時干の番号
    #   - t_shi（int）：時支の番号
    # ＜異常検出＞
    # 取得できなかった場合はエラーメッセージを出力して強制終了する
    
    time_span = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 24]
    
    for i in range(len(time_span) - 1):
        
        from_dt = dt(year = birthday.year, month = birthday.month, day = birthday.day,
                     hour = time_span[i], minute = 0)
        if (i == 0) or (i == len(time_span)):
            to_dt = from_dt + td(hours = 0, minutes = 59)
        else:
            to_dt = from_dt + td(hours = 1, minutes = 59)
        
        if from_dt <= birthday < to_dt:
            try:
                t_kan, t_shi = kd.time_kanshi[day_kan][i]
                return t_kan, t_shi
            except:
                print('時干支の計算で例外が送出されました。')
                exit()

    print('時干支を得られませんでした。')
    exit()        


def find_zokan(birthday, shi):

    # ＜機能＞
    # birthday で与えられた生年月日の shi に対応する蔵干を取得する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    #   - shi（int）：年支、月支、日支、時支の番号
    # ＜出力＞
    #   - z_kan（int）：蔵干の番号
    # ＜異常検出＞
    # 取得できなかった場合はエラーメッセージを出力して強制終了する

    p = is_setsuiri(dt(year = birthday.year, month = birthday.month, day = birthday.day), birthday.month)
    for s in kd.setsuiri:
        if (s[0] == birthday.year) and (s[1] == birthday.month):
            setsuiri_ =  dt(year = s[0], month = s[1] + p, day = s[2], hour = s[3], minute = s[4])

    delta = td(days = kd.zokan_time[shi][0], hours = kd.zokan_time[shi][1])
    
    try:
        if setsuiri_ + delta >= birthday:
            zokan = kd.zokan[shi][0]
        else:
            zokan = kd.zokan[shi][1]
        return zokan
    except:
        print('蔵干の計算で例外が送出されました。')
        exit()


def append_kanshi(birthday, t_flag):

    # ＜機能＞
    # birthday で与えられた生年月日の命式を組み立てる
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    # ＜出力＞
    #   - meishiki（dict）：命式の情報を含む辞書型の変数
    
    # 天干・地支を得る
    y_kan, y_shi = find_year_kanshi(birthday)
    m_kan, m_shi = find_month_kanshi(birthday, y_kan)
    d_kan, d_shi = find_day_kanshi(birthday)
    if t_flag:
        t_kan, t_shi = find_time_kanshi(birthday, d_kan)
    else:
        t_kan = -1
        t_shi = -1

    tenkan = [y_kan, m_kan, d_kan, t_kan]
    chishi = [y_shi, m_shi, d_shi, t_shi]

    # 蔵干を得る
    y_zkan = find_zokan(birthday, y_shi)
    m_zkan = find_zokan(birthday, m_shi)
    d_zkan = find_zokan(birthday, d_shi)
    if t_flag:
        t_zkan = find_zokan(birthday, t_shi)
    else:
        t_zkan = -1

    zokan = [y_zkan, m_zkan, d_zkan, t_zkan]

    # 四柱を得る
    nenchu = [y_kan, y_shi, y_zkan]
    getchu = [m_kan, m_shi, m_zkan]
    nitchu = [d_kan, d_shi, d_zkan]
    jichu  = [t_kan, t_shi, t_zkan]

    # グローバル変数 meishiki に情報を追加していく
    meishiki.update({"tenkan": tenkan})
    meishiki.update({"chishi": chishi})
    meishiki.update({"zokan" : zokan})
    meishiki.update({"nenchu": nenchu})
    meishiki.update({"getchu": getchu})
    meishiki.update({"nitchu": nitchu})
    meishiki.update({"jichu" : jichu})
    meishiki.update({"nitchu_tenkan": d_kan})
    meishiki.update({"getchu_zokan": m_zkan})


def find_tsuhen(s_kan, kan_list):

    # s_kan に対する kan_ の通変を取得する
    
    kl = []
    for kan_ in kan_list:
        kl.append(kd.kan_tsuhen[s_kan].index(kan_))
        
    return kl


def append_tsuhen():

    # 命式に通変を追加する
    
    kl1 = find_tsuhen(meishiki["nitchu_tenkan"], meishiki["tenkan"])
    meishiki.update({"tenkan_tsuhen": kl1})
    
    kl2 = find_tsuhen(meishiki["nitchu_tenkan"], meishiki["zokan"])
    meishiki.update({"zokan_tsuhen": kl2})


def find_twelve_fortune(s_shi, shi_list):

    # s_shi に対する shi_ の十二運を取得する

    sl = []
    for shi_ in shi_list:
        sl.append(kd.twelve_table[s_shi][shi_])

    return sl


def append_twelve_fortune():

    # 命式に十二運を追加する

    sl = find_twelve_fortune(meishiki["nitchu_tenkan"], meishiki["chishi"])
    meishiki.update({"twelve_fortune": sl})


def append_additional_info():

    # ＜機能＞
    # 命式に通変と十二運を追加する
    # ＜入力＞
    # なし
    # ＜出力＞
    #   - グローバル変数 meishiki に下記の情報を追加する
    #     - tenkan_tsuhen（list）：天干の通変の番号
    #     - zokan_tsuhen（list）：蔵干の通変の番号
    #     - twelve_fortune（list）：地支の十二運
    append_tsuhen()
    append_twelve_fortune()
    

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
    
    for idx, sk in kd.sixty_kanshi:
        if (sk[0] == kan) and (sk[1] == shi):
            return idx
    
    print('干支が見つかりませんでした。')
    exit()
        

def generate_daiun(birthday, sex):

    # ＜機能＞
    # 大運を導出する
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
    

def show_age(birthday, sex, t_flag):

    if sex == 0:
        sex_str = '男命'
    else:
        sex_str = '女命'
    
    wareki = kd.convert_to_wareki(birthday)

    if t_flag:
        print(str(birthday.year) + '年（' + wareki + '）' + str(birthday.month) + '月' + str(birthday.day) + '日 ' + str(birthday.hour) + '時' + str(birthday.minute) + '分生 ' + sex_str)
    else:
        print(str(birthday.year) + '年（' + wareki + '）' + str(birthday.month) + '月' + str(birthday.day) + '日生（時刻不明） ' + sex_str)


def show_meishiki(meishiki):

    tenkan = [kd.kan[i] for i in meishiki["tenkan"]]
    tenkan_tsuhen = [kd.tsuhen[i] for i in meishiki["tenkan_tsuhen"]]
    chishi = [kd.shi[i] for i in meishiki["chishi"]]
    twelve_fortune = [kd.twelve_fortune[i] for i in meishiki["twelve_fortune"]]
    zokan = [kd.kan[i] for i in meishiki["zokan"]]
    zokan_tsuhen = [kd.tsuhen[i] for i in meishiki["zokan_tsuhen"]]

    print()
    print('|   生  時   |   生  日   |   生  月   |   生  年   |')    
    print('+============+============+============+============+')   # 56文字
    print('| ' + tenkan[3] + '（' + tenkan_tsuhen[3] + '） ' +
          '|     ' + tenkan[2] +
          '     | ' + tenkan[1] + '（' + tenkan_tsuhen[1] + '） ' +
          '| ' + tenkan[0] + '（' + tenkan_tsuhen[0] + '）' +
          ' |')
    print('+------------+------------+------------+------------+')
    print('|  ' + chishi[3] + '（' + twelve_fortune[3] + '）  ' +
          '|  ' + chishi[2] + '（' + twelve_fortune[2] + '）  ' +
          '|  ' + chishi[1] + '（' + twelve_fortune[1] + '）  ' +
          '|  ' + chishi[0] + '（' + twelve_fortune[0] + '）  ' +
          '|')
    print('+------------+------------+------------+------------+')
    print('| ' + zokan[3] + '（' + zokan_tsuhen[3] + '） ' +
          '| ' + zokan[2] + '（' + zokan_tsuhen[2] + '） ' +
          '| ' + zokan[1] + '（' + zokan_tsuhen[1] + '） ' +
          '| ' + zokan[0] + '（' + zokan_tsuhen[0] + '） ' +
          '|')
    
        
if __name__ == '__main__':

    # 起動時の引数から生年月日・性別などのデータを構築する
    birthday, sex, t_flag = build_birthday_data(sys.argv)

    # 命式を組成する
    append_kanshi(birthday, t_flag)

    # 命式に通変と十二運を追加する
    append_additional_info()

    # 生年月日・性別を出力する
    show_age(birthday, sex, t_flag)

    # 命式を出力する
    show_meishiki(meishiki)
    print(meishiki)
