#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td

def is_setsuiri_year(d_time):

    # 生誕年の年月日時分が、その年２月の節入りの前か後かを判定する（年干支の計算用）
    for s in kd.setsuiri:
        if (s[0] == d_time.year) and (s[1] == 2):
            setsuiri_ = dt(year = s[0], month = s[1], day = s[2], hour = s[3], minute = s[4])
            if setsuiri_ < d_time:
                return 0    # 節入りしている
            else:
                return -1   # 節入りしていない（１つ前の六十干支表を参照する必要がある）

    return None


def obtain_year_kanshi(d_time):

    # 年干支を得る
    try:
        return kd.sixty_kanshi[(d_time.year - 3) % 60 - 1 + is_setsuiri_year(d_time)]
    except:
        print('年干支の計算で例外が送出されました。')
        exit()

        
def is_setsuiri_month(d_time):

    # 生誕月の日時分が、その月の節入りの前か後かを判定する（月干支の計算用）
    for s in kd.setsuiri:
        if (s[0] == d_time.year) and (s[1] == d_time.month):
            setsuiri_ = dt(year = s[0], month = s[1], day = s[2], hour = s[3], minute = s[4])
            if setsuiri_ < d_time:
                return 0    # 節入りしている
            else:
                return -1   # 節入りしていない（１つ前の月干支表を参照する必要がある）

    return None


def obtain_month_kanshi(d_time, year_kanshi):

    # 月干支を得る
    try:
        return kd.month_kanshi[kd.kan.index(year_kanshi)][d_time.month - 1 + is_setsuiri_month(d_time)]
    except:
        print('月干支の計算で例外が送出されました。')
        exit()


def obtain_day_kanshi(d_time):

    # 日干支を得る
    d = d_time.day + kd.kisu_table[d_time.year - 1926][d_time.month - 1]
    if d >= 60:
        d -= 60

    try:
        return kd.sixty_kanshi[d - 1]
    except:
        print('日干支の計算で例外が送出されました。')
        exit()        


def obtain_time_kanshi(d_time, day_kanshi, none_flag):
    
    # 時干支を得る
    if none_flag:
        return ['--', '--']
    
    time_span = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 24]
    
    for i in range(len(time_span) - 1):
        
        from_dt = dt(year = d_time.year, month = d_time.month, day = d_time.day,
                     hour = time_span[i], minute = 0)
        if (i == 0) or (i == len(time_span)):
            to_dt = from_dt + td(hours = 0, minutes = 59)
        else:
            to_dt = from_dt + td(hours = 1, minutes = 59)
        
        if from_dt <= d_time < to_dt:
            try:
                return kd.time_kanshi[kd.kan.index(day_kanshi)][i]
            except:
                print('時干支の計算で例外が送出されました。')
                exit()        

    print('時干支を得られませんでした。')
    exit()        


def calc_gogyo_haibun(year_kanshi, month_kanshi, day_kanshi, time_kanshi, none_flag):

    # 五行の配分を計算する
    g1 = kd.gogyo_kan[kd.kan.index(year_kanshi[0])]
    g2 = kd.gogyo_kan[kd.kan.index(month_kanshi[0])]
    g3 = kd.gogyo_kan[kd.kan.index(day_kanshi[0])]
    if none_flag:
        g4 = '--'
    else:
        g4 = kd.gogyo_kan[kd.kan.index(time_kanshi[0])]

    g5 = kd.gogyo_shi[kd.shi.index(year_kanshi[1])]
    g6 = kd.gogyo_shi[kd.shi.index(month_kanshi[1])]
    g7 = kd.gogyo_shi[kd.shi.index(day_kanshi[1])]
    if none_flag:
        g8 = '--'
    else:
        g8 = kd.gogyo_shi[kd.shi.index(time_kanshi[1])]

    gg = [g1, g2, g3, g4, g5, g6, g7, g8]
    
    n = [0] * len(kd.gogyo)
    for g in gg:
        if g == '--':
            continue
        else:
            n[kd.gogyo.index(g)] += 1
    return n


def obtain_setsuiri_datetime(d_time):

    # ある年・ある月・ある日の節入りの日時を datetime 型で得る
    for s in kd.setsuiri:

        p = is_setsuiri_month(dt(year = d_time.year, month = d_time.month, day = d_time.day))
        if (s[0] == d_time.year) and (s[1] == d_time.month):
            return dt(year = s[0], month = s[1] + p, day = s[2], hour = s[3], minute = s[4])

    print('節入りの日時を得られませんでした。')
    exit()        
    

def obtain_zokan(d_time, shi_):

    # 蔵干を得る
    shi_idx = kd.shi.index(shi_)
    delta = td(days = kd.zokan_time[shi_idx][0], hours = kd.zokan_time[shi_idx][1])
    setsuiri_ = obtain_setsuiri_datetime(d_time)

    if setsuiri_ + delta >= d_time:
        zokan_ = kd.zokan[shi_idx][0]
    else:
        zokan_ = kd.zokan[shi_idx][1]

    return zokan_


def lookup_tsuhen(day_kanshi, kan_):

    # 通変表から通変を引く
    kan_idx1 = kd.kan.index(day_kanshi)
    kan_idx2 = kd.kan_tsuhen[kan_idx1].index(kan_)
    
    return kd.tsuhen[kan_idx2]


def calc_ritsuun_year(d_time):

    # 立運年数を計算する
    for s in kd.setsuiri:
        p = is_setsuiri_month(dt(year = d_time.year, month = d_time.month, day = d_time.day))
        if (s[0] == d_time.year) and (s[1] == d_time.month):
            previous_setsuiri =  dt(year = s[0], month = s[1] + p, day = s[2], hour = s[3], minute = s[4])
            next_setsuiri = dt(year = s[0], month = s[1] + p + 1, day = s[2], hour = s[3], minute = s[4])
            break

    diff_previous = d_time - previous_setsuiri
    diff_next = next_setsuiri - d_time

    previous_ritsuun_year = round((diff_previous.days + (diff_previous.seconds / 60 / 60 / 24)) / 3)
    next_ritsuun_year = round((diff_next.days + (diff_next.seconds / 60 / 60 / 24)) / 3)

    return [previous_ritsuun_year, next_ritsuun_year]


def is_inyo(kan_):
    
    # 十干の陰陽を判定する（1なら陽、0なら陰）
    try:
        if kd.kan.index(kan_) % 2:
            return 0
        else:
            return 1
    except:
        print('十干の陰陽を判定できませんでした。')
        exit()


def is_junun_gyakuun(year_kan, sex):

    # 大運の順と逆を判定する
    if ((is_inyo(year_kan) == 1) and (sex == 0)) or ((is_inyo(year_kan) == 0) and (sex == 1)):
       return 1   # 年柱干が陽干の男命 or 年柱干が陰干の女命は、順運
   
    elif ((is_inyo(year_kan) == 0) and (sex == 0)) or ((is_inyo(year_kan) == 1) and (sex == 1)):
       return 0   # 年柱干が陽干の女命 or 年柱干が陰干の男命は、逆運
   
    else:
        print('大運の順逆を判定できませんでした。')
        exit()


def lookup_twelve_fortune(kan_, shi_):

    # 十二運表から十二運を引く
    tw_idx1 = kd.kan.index(kan_)
    tw_idx2 = kd.twelve_table[tw_idx1].index(shi_)
    
    return kd.twelve_fortune[tw_idx2]


def calc_ritsuun(month_kanshi, day_kan, ritsuun_year, jun_gyaku_flag):

    # 立運計算
    if jun_gyaku_flag == 1:
        ry_ = ritsuun_year[1]  # 次の節入日が立運の起算日
        p = 1   # 六十干支表を順にたどる
    else:
        ry_ = ritsuun_year[0] # 前の節入日が立運の起算日
        p = -1  # 六十干支表を逆にたどる
                
    for idx, sk in enumerate(kd.sixty_kanshi):
        if month_kanshi == sk:
            break

    daiun_kanshi = []
    for n in list(range(10, 120, 10)):
        kanshi_ = kd.sixty_kanshi[idx]
        tsuhen_ = lookup_tsuhen(day_kan, kanshi_[0])
        t_fortune_ = lookup_twelve_fortune(day_kan, kanshi_[1])
        daiun_kanshi.append([ry_, ''.join(kanshi_) + ' (' + tsuhen_ + '・' + t_fortune_ + ')'])
        ry_ += 10
        idx += p
        if idx >= 60:
            idx = 0

    return daiun_kanshi


def calc_nenun(d_time, kan_):

    idx = (d_time.year - 3) % 60 - 1
    nenun = []
    for n in list(range(0, 120)):
        k = kd.sixty_kanshi[idx]
        tsuhen_ = lookup_tsuhen(kan_, k[0])
        t_fortune_ = lookup_twelve_fortune(kan_, k[1])
        nenun.append([n, ''.join(k) + ' (' + tsuhen_ + '・' + t_fortune_ + ')'])
        idx += 1
        if idx >= 60:
            idx = 0

    return nenun


def calc_getsurei(d_time, kan_):

    shi_ = kd.shi[d_time.month]  # 生まれ月の地支を引く（節入りを考慮している？？？）
    
    gr_idx1 = kd.kan.index(kan_)
    getsurei_ = kd.getsurei_table[gr_idx1]

    p = False
    for idx1, gr_ in enumerate(getsurei_):
        for idx2, g in enumerate(gr_):
            if shi_ in g:
                p = True
                break
        if p:
            break

    return kd.getsurei[idx1], g

        
if __name__ == '__main__':

    year = 1978
    month = 9
    day = 26
    hour = 13
    minute = 51
    sex = 0  # 0->男, 1->女

    # 生まれの年月日時分の datetime を生成する
    if (hour is None) or (minute is None):
        birthday = dt(year = year, month = month, day = day)
        none_flag = True
    else:
        birthday = dt(year = year, month = month, day = day, hour = hour, minute = minute)
        none_flag = False

    # 天干・地支を得る
    year_kanshi = obtain_year_kanshi(birthday)
    month_kanshi = obtain_month_kanshi(birthday, year_kanshi[0])
    day_kanshi = obtain_day_kanshi(birthday)
    time_kanshi = obtain_time_kanshi(birthday, day_kanshi[0], none_flag)

    # 五行の配分を計算する
    haibun = calc_gogyo_haibun(year_kanshi, month_kanshi, day_kanshi, time_kanshi, none_flag)
    
    # 蔵干を得る
    year_zokan = obtain_zokan(birthday, year_kanshi[1])
    month_zokan = obtain_zokan(birthday, month_kanshi[1])
    day_zokan = obtain_zokan(birthday, day_kanshi[1])
    if none_flag:
        time_zokan = ['--', '--']
    else:
        time_zokan = obtain_zokan(birthday, time_kanshi[1])

    # 通変を得る
    year_tsuhen_tenkan = lookup_tsuhen(day_kanshi[0], year_kanshi[0])
    month_tsuhen_tenkan = lookup_tsuhen(day_kanshi[0], month_kanshi[0])
    day_tsuhen_tenkan = lookup_tsuhen(day_kanshi[0], day_kanshi[0])
    if none_flag:
        time_tsuhen_tenkan = '--'
    else:
        time_tsuhen_tenkan = lookup_tsuhen(day_kanshi[0], time_kanshi[0])
    year_tsuhen_zokan = lookup_tsuhen(day_kanshi[0], year_zokan[0])
    month_tsuhen_zokan = lookup_tsuhen(day_kanshi[0], month_zokan[0])
    day_tsuhen_zokan = lookup_tsuhen(day_kanshi[0], day_zokan[0])
    if none_flag:
        time_tsuhen_zokan = '--'
    else:
        time_tsuhen_zokan = lookup_tsuhen(day_kanshi[0], time_zokan[0])

    # 十二運を得る
    year_twelve_day = lookup_twelve_fortune(day_kanshi[0], year_kanshi[1])
    month_twelve_day = lookup_twelve_fortune(day_kanshi[0], month_kanshi[1])
    day_twelve_day = lookup_twelve_fortune(day_kanshi[0], day_kanshi[1])
    if none_flag:
        time_twelve_day = '--'
    else:
        time_twelve_day = lookup_twelve_fortune(day_kanshi[0], time_kanshi[1])
    year_twelve_zokan = lookup_twelve_fortune(month_zokan[0], year_kanshi[1])
    month_twelve_zokan = lookup_twelve_fortune(month_zokan[0], month_kanshi[1])
    day_twelve_zokan = lookup_twelve_fortune(month_zokan[0], day_kanshi[1])
    if none_flag:
        time_twelve_zokan = '--'
    else:
        time_twelve_zokan = lookup_twelve_fortune(day_kanshi[0], time_kanshi[1])

    # 大運干支を得る
    ritsuun_year = calc_ritsuun_year(birthday)
    jun_gyaku_flag = is_junun_gyakuun(year_kanshi[0], sex)
    daiun_kanshi = calc_ritsuun(month_kanshi, day_kanshi[0], ritsuun_year, jun_gyaku_flag)

    # 年干支を得る
    nenun = calc_nenun(birthday, day_kanshi[0])

    # 月令を計算する
    getsurei_day, umare_day = calc_getsurei(birthday, day_kanshi[0])
    getsurei_zokan, umare_zokan = calc_getsurei(birthday, month_zokan[0])

    # 和暦を得る
    wareki = kd.convert_to_wareki(birthday)

    # 性別を得る
    if sex == 0:
        sex_str = '男命'
    else:
        sex_str = '女命'

    print('')
    print(str(year) + '年（' + wareki + '）' + str(month) + '月' + str(day) + '日 ' + str(hour) + '時' + str(minute) + '分 ' + sex_str)

    print('+---------------------------------------------------+')
    print('|   時 柱    |   日 柱    |   月 柱    |   年 柱    |')
    print('+===================================================+')
    print('| ' + 
          time_kanshi[0] + ' （' + time_tsuhen_tenkan + '）' + '|     ' +
          day_kanshi[0] + '     ' + '| ' +
          month_kanshi[0] + ' （' + month_tsuhen_tenkan + '）' + '| ' +
          year_kanshi[0] + ' （' + year_tsuhen_tenkan + '）' + '| ' )
    print('+---------------------------------------------------+')
    print('|     ' + 
          time_kanshi[1]  + '     |     ' +
          day_kanshi[1]   + '     |     ' +
          month_kanshi[1] + '     |    ' +
          year_kanshi[1]  + '      |    ')
    print('|  ' +
          time_twelve_zokan + ' , ' + time_twelve_day + '   |  ' +
          day_twelve_zokan + ' , ' + day_twelve_day + '   |  ' +
          month_twelve_zokan + ' , ' + month_twelve_day + '   |  ' +
          year_twelve_zokan + ' , ' + year_twelve_day + '   | '
          )
    print('+---------------------------------------------------+')
    print('| ' + 
          time_zokan[0] + ' （' + time_tsuhen_zokan + '）' + '| ' +
          day_zokan[0] + ' （' + day_tsuhen_zokan + '）' + '| ' +
          month_zokan[0] + ' （' + month_tsuhen_zokan + '）' + '| ' +
          year_zokan[0] + ' （' + year_tsuhen_zokan + '）' + '| ' )
    print('+---------------------------------------------------+')
    
    print('')
    
    print('木：' + str(haibun[0]))
    print('火：' + str(haibun[1]))
    print('土：' + str(haibun[2]))
    print('金：' + str(haibun[3]))
    print('水：' + str(haibun[4]))
    
    print('')

    print('生まれ：', umare_day)
    print('旺衰（日柱）：', getsurei_day)
    print('旺衰（月蔵）：', getsurei_zokan)

    print(daiun_kanshi)

    print(nenun)
