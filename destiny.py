#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td

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


def find_month_kanshi(birthday, year_kan):

    # ＜機能＞
    # birthday で与えられた生年月日の月干支を取得する
    # ＜入力＞
    #   - birthday（datetime）：生年月日
    #   - year_kan（string）：年干の番号
    # ＜出力＞
    #   - m_kan（int）：月干の番号
    #   - m_shi（int）：月支の番号
    # ＜異常検出＞
    # 取得できなかった場合はエラーメッセージを出力して強制終了する

    month = birthday.month - 1 + is_setsuiri(birthday, birthday.month)
    try:
        m_kan, m_shi = kd.month_kanshi[year_kan][month]
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
    # - birthday（datetime）：生年月日
    # - shi（int）：年支、月支、日支、時支の番号
    # ＜出力＞
    # - z_kan（int）：蔵干の番号
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


def build_meishiki(birthday, t_flag):

    # birthday で与えられた生年月日の命式を組み立てる
    
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

    meishiki = {
        "tenkan": tenkan,
        "chishi": chishi,
        "zokan" : zokan,
        "nenchu": nenchu,
        "getchu": getchu,
        "nitchu": nitchu,
        "jichu" : jichu,
    }

    return meishiki
    
        
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
        t_flag = False
    else:
        birthday = dt(year = year, month = month, day = day, hour = hour, minute = minute)
        # サマータイムを考慮する
        if (dt(year=1948, month=5, day=2) <= birthday < dt(year=1951, month=9, day=8)) and (hour is not None):
            birthday = dt(year = birthday.year, month = birthday.month, day = birthday.day,
                          hour = birthday.hour - 1, minute = birthday.minute)
        t_flag = True

    # 命式を組成する
    meishiki = build_meishiki(birthday, t_flag)
    
    print(meishiki)
