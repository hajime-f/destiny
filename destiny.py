#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta as td

class Destiny:

    k = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸',]
    j = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥',]
    tsuhen = ['比肩', '劫財', '食神', '傷官', '偏財', '正財', '偏官', '正官', '偏印', '印綬', ]
    gogyo = ['木', '火', '土', '金', '水',]
    gogyo1 = ['木', '木', '火', '火', '土', '土', '金', '金', '水', '水',]
    gogyo2 = ['水', '土', '木', '木', '土', '火', '火', '土', '金', '金', '土', '水',]

    k_tsuhen = [
        ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸',],
        ['乙', '甲', '丁', '丙', '己', '戊', '辛', '庚', '癸', '壬',],
        ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙',],
        ['丁', '丙', '己', '戊', '辛', '庚', '癸', '壬', '乙', '甲',],
        ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁',],
        ['己', '戊', '辛', '庚', '癸', '壬', '乙', '甲', '丁', '丙',],
        ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己',],
        ['辛', '庚', '癸', '壬', '乙', '甲', '丁', '丙', '己', '戊',],
        ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛',],
        ['癸', '壬', '乙', '甲', '丁', '丙', '己', '戊', '辛', '庚',],
    ]
    
    sixty_kanshi = [
        ['甲', '子',],
        ['乙', '丑',],
        ['丙', '寅',],
        ['乙', '卯',],
        ['戊', '辰',],
        ['己', '巳',],
        ['庚', '午',],
        ['辛', '未',],
        ['壬', '申',],
        ['癸', '酉',],
        ['甲', '戌',],
        ['乙', '亥',],
        ['丙', '子',],
        ['丁', '丑',],
        ['戊', '寅',],
        ['己', '卯',],
        ['庚', '辰',],
        ['辛', '巳',],
        ['壬', '午',],
        ['癸', '未',],
        ['甲', '申',],
        ['乙', '酉',],
        ['丙', '戌',],
        ['丁', '亥',],
        ['戊', '子',],
        ['己', '丑',],
        ['庚', '寅',],
        ['辛', '卯',],
        ['壬', '辰',],
        ['癸', '巳',],
        ['甲', '午',],
        ['乙', '未',],
        ['丙', '申',],
        ['丁', '酉',],
        ['戊', '戌',],
        ['己', '亥',],
        ['庚', '子',],
        ['辛', '丑',],
        ['壬', '寅',],
        ['癸', '卯',],
        ['甲', '辰',],
        ['乙', '巳',],
        ['丙', '午',],
        ['丁', '未',],
        ['戊', '申',],
        ['己', '酉',],
        ['庚', '戌',],
        ['辛', '亥',],
        ['壬', '子',],
        ['癸', '丑',],
        ['甲', '寅',],
        ['乙', '卯',],
        ['丙', '辰',],
        ['丁', '巳',],
        ['戊', '午',],
        ['己', '未',],
        ['庚', '申',],
        ['辛', '酉',],
        ['壬', '戌',],
        ['癸', '亥',],
    ]

    kubo = [
        ['戌', '亥',],
        ['申', '酉',],
        ['午', '未',],
        ['辰', '巳',],
        ['寅', '卯',],
        ['子', '丑',],
    ]

    month_kanshi = [
        [ ['丁', '丑',],  # 甲
          ['丙', '寅',],
          ['丁', '卯',],
          ['戊', '辰',],
          ['己', '巳',],
          ['庚', '午',],
          ['辛', '未',],
          ['壬', '申',],
          ['癸', '酉',],
          ['甲', '戌',],
          ['乙', '亥',],
          ['丙', '子',], ],
        [ ['己', '丑',],  # 乙
          ['戊', '寅',],
          ['己', '卯',],
          ['庚', '辰',],
          ['辛', '巳',],
          ['壬', '午',],
          ['癸', '未',],
          ['甲', '申',],
          ['乙', '酉',],
          ['丙', '戌',],
          ['丁', '亥',],
          ['戊', '子',], ],
        [ ['辛', '丑',],  # 丙
          ['庚', '寅',],
          ['辛', '卯',],
          ['壬', '辰',],
          ['癸', '巳',],
          ['甲', '午',],
          ['乙', '未',],
          ['丙', '申',],
          ['丁', '酉',],
          ['戊', '戌',],
          ['己', '亥',],
          ['庚', '子',], ],
        [ ['癸', '丑',],  # 丁
          ['壬', '寅',],
          ['癸', '卯',],
          ['甲', '辰',],
          ['乙', '巳',],
          ['丙', '午',],
          ['丁', '未',],
          ['戊', '申',],
          ['己', '酉',],
          ['庚', '戌',],
          ['辛', '亥',],
          ['壬', '子',], ],
        [ ['乙', '丑',],  # 戊
          ['甲', '寅',],
          ['乙', '卯',],
          ['丙', '辰',],
          ['丁', '巳',],
          ['戊', '午',],
          ['己', '未',],
          ['庚', '申',],
          ['辛', '酉',],
          ['壬', '戌',],
          ['癸', '亥',],
          ['甲', '子',], ],
        [ ['丁', '丑',],  # 己
          ['丙', '寅',],
          ['丁', '卯',],
          ['戊', '辰',],
          ['己', '巳',],
          ['庚', '午',],
          ['辛', '未',],
          ['壬', '申',],
          ['癸', '酉',],
          ['甲', '戌',],
          ['乙', '亥',],
          ['丙', '子',], ],
        [ ['己', '丑',],  # 庚
          ['戊', '寅',],
          ['己', '卯',],
          ['庚', '辰',],
          ['辛', '巳',],
          ['壬', '午',],
          ['癸', '未',],
          ['甲', '申',],
          ['乙', '酉',],
          ['丙', '戌',],
          ['丁', '亥',],
          ['戊', '子',], ],
        [ ['辛', '丑',],  # 辛
          ['庚', '寅',],
          ['辛', '卯',],
          ['壬', '辰',],
          ['癸', '巳',],
          ['甲', '午',],
          ['乙', '未',],
          ['丙', '申',],
          ['丁', '酉',],
          ['戊', '戌',],
          ['己', '亥',],
          ['庚', '子',], ],
        [ ['癸', '丑',],  # 壬
          ['壬', '寅',],
          ['癸', '卯',],
          ['甲', '辰',],
          ['乙', '巳',],
          ['丙', '午',],
          ['丁', '未',],
          ['戊', '申',],
          ['己', '酉',],
          ['庚', '戌',],
          ['辛', '亥',],
          ['壬', '子',], ],
        [ ['乙', '丑',],  # 癸
          ['甲', '寅',],
          ['乙', '卯',],
          ['丙', '辰',],
          ['丁', '巳',],
          ['戊', '午',],
          ['己', '未',],
          ['庚', '申',],
          ['辛', '酉',],
          ['壬', '戌',],
          ['癸', '亥',],
          ['甲', '子',], ],
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
        [21, 52, 21, 52, 22, 53, 23, 54, 25, 55, 26, 56], # 昭和23
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

    time_kanshi = [
        [ ['甲', '子'],    # 甲
          ['乙', '丑'],
          ['丙', '寅'],
          ['丁', '卯'],
          ['戊', '辰'],
          ['己', '巳'],
          ['庚', '午'],
          ['辛', '未'],
          ['壬', '申'],
          ['癸', '酉'],
          ['甲', '戌'],
          ['乙', '亥'],
          ['丙', '子'], ],
        [ ['丙', '子'],    # 乙
          ['丁', '丑'],
          ['戊', '寅'],
          ['己', '卯'],
          ['庚', '辰'],
          ['辛', '巳'],
          ['壬', '午'],
          ['癸', '未'],
          ['甲', '申'],
          ['乙', '酉'],
          ['丙', '戌'],
          ['丁', '亥'],
          ['戊', '子'], ],
        [ ['戊', '子'],    # 丙
          ['己', '丑'],
          ['庚', '寅'],
          ['辛', '卯'],
          ['壬', '辰'],
          ['癸', '巳'],
          ['甲', '午'],
          ['乙', '未'],
          ['丙', '申'],
          ['丁', '酉'],
          ['戊', '戌'],
          ['己', '亥'],
          ['庚', '子'], ],
        [ ['庚', '子'],   # 丁
          ['辛', '丑'],
          ['壬', '寅'],
          ['癸', '卯'],
          ['甲', '辰'],
          ['乙', '巳'],
          ['丙', '午'],
          ['丁', '未'],
          ['戊', '申'],
          ['己', '酉'],
          ['庚', '戌'],
          ['辛', '亥'],
          ['壬', '子'], ],
        [ ['壬', '子'],   # 戊
          ['癸', '丑'],
          ['甲', '寅'],
          ['乙', '卯'],
          ['丙', '辰'],
          ['丁', '巳'],
          ['戊', '午'],
          ['己', '未'],
          ['庚', '申'],
          ['辛', '酉'],
          ['壬', '戌'],
          ['癸', '亥'],
          ['甲', '子'], ],
        [ ['甲', '子'],    # 己
          ['乙', '丑'],
          ['丙', '寅'],
          ['丁', '卯'],
          ['戊', '辰'],
          ['己', '巳'],
          ['庚', '午'],
          ['辛', '未'],
          ['壬', '申'],
          ['癸', '酉'],
          ['甲', '戌'],
          ['乙', '亥'],
          ['丙', '子'], ],
        [ ['丙', '子'],    # 庚
          ['丁', '丑'],
          ['戊', '寅'],
          ['己', '卯'],
          ['庚', '辰'],
          ['辛', '巳'],
          ['壬', '午'],
          ['癸', '未'],
          ['甲', '申'],
          ['乙', '酉'],
          ['丙', '戌'],
          ['丁', '亥'],
          ['戊', '子'], ],
        [ ['戊', '子'],    # 辛
          ['己', '丑'],
          ['庚', '寅'],
          ['辛', '卯'],
          ['壬', '辰'],
          ['癸', '巳'],
          ['甲', '午'],
          ['乙', '未'],
          ['丙', '申'],
          ['丁', '酉'],
          ['戊', '戌'],
          ['己', '亥'],
          ['庚', '子'], ],
        [ ['庚', '子'],   # 壬
          ['辛', '丑'],
          ['壬', '寅'],
          ['癸', '卯'],
          ['甲', '辰'],
          ['乙', '巳'],
          ['丙', '午'],
          ['丁', '未'],
          ['戊', '申'],
          ['己', '酉'],
          ['庚', '戌'],
          ['辛', '亥'],
          ['壬', '子'], ],
        [ ['壬', '子'],   # 癸
          ['癸', '丑'],
          ['甲', '寅'],
          ['乙', '卯'],
          ['丙', '辰'],
          ['丁', '巳'],
          ['戊', '午'],
          ['己', '未'],
          ['庚', '申'],
          ['辛', '酉'],
          ['壬', '戌'],
          ['癸', '亥'],
          ['甲', '子'], ],
    ]

    def __init__(self):
        pass
    
    def get_year_kanshi(self, year):
        return self.sixty_kanshi[(year - 3) % 60 - 1]

    def get_k_number(self, jk):
        return self.k.index(jk)

    def get_j_number(self, js):
        return self.j.index(js)
    
    def get_month_kanshi(self, jk, month):
        k_number = self.get_k_number(jk)
        return self.month_kanshi[k_number][month - 1]

    def get_day_kanshi(self, year, month, day):
        d = day + self.kisu_table[year - 1926][month - 1]
        if d > 60:
            d = d - 60
        return self.sixty_kanshi[d - 1]

    def get_time_kanshi(self, dk, b_time):

        time_span = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 24]

        for i in range(len(time_span) - 1):
            
            from_dt = dt(year = b_time.year, month = b_time.month, day = b_time.day,
                         hour = time_span[i], minute = 0)
            to_dt = dt(year = b_time.year, month = b_time.month, day = b_time.day,
                       hour = time_span[i + 1], minute = 0)
            
            if from_dt <= b_time < to_dt:
                k_number = self.get_k_number(dk)
                return self.time_kanshi[k_number][i]

        return ['Non', 'Non']

    def is_inyo(self, jk):
        return False if self.get_k_number(jk) == 0 else True

    def get_tsuhen_list(self, nk):
        rt = []
        k_number = self.get_k_number(nk)
        for i in [((n - 1) % 10) for n in range(k_number, k_number + 10)]:
            rt.append(self.k_tsuhen[k_number][i - k_number + 1])
            
        return rt

    def get_gogyo1(self, gg1):
        k_number = self.get_k_number(gg1)
        return self.gogyo1[k_number]

    def get_gogyo2(self, gg2):
        j_number = self.get_j_number(gg2)
        return self.gogyo2[j_number]

    def get_gg(self, yk, mk, dk, tk):

        g1 = self.get_gogyo1(yk[0])
        g2 = self.get_gogyo1(mk[0])
        g3 = self.get_gogyo1(dk[0])
        g4 = self.get_gogyo1(tk[0])

        g5 = self.get_gogyo2(yk[1])
        g6 = self.get_gogyo2(mk[1])
        g7 = self.get_gogyo2(dk[1])
        g8 = self.get_gogyo2(tk[1])

        gg = [g1, g2, g3, g4, g5, g6, g7, g8]
        return gg

    def get_tsuhen(self, yk, mk, dk, tk):

        th_list = self.get_tsuhen_list(dk[0])
        t1 = self.tsuhen[th_list.index(yk[0])]
        t2 = self.tsuhen[th_list.index(mk[0])]
        t3 = self.tsuhen[th_list.index(dk[0])]
        t4 = self.tsuhen[th_list.index(tk[0])]
        return [t1, t2, t3, t4]
        

    def get_haibun(self, yk, mk, dk, tk):

        gg = self.get_gg(yk, mk, dk, tk)
        n = [0] * len(self.gogyo)
        for g in gg:
            n[self.gogyo.index(g)] += 1
        return n
    

if __name__ == '__main__':

    year = 1978
    month = 9
    day = 26
    hour = 13
    minute = 51

    dest = Destiny()
    birthday = dt(year=year, month=month, day=day, hour=hour, minute=minute)
    
    year_kanshi = dest.get_year_kanshi(year)
    month_kanshi = dest.get_month_kanshi(year_kanshi[0], month)
    day_kanshi = dest.get_day_kanshi(year, month, day)
    time_kanshi = dest.get_time_kanshi(day_kanshi[0], birthday)
    haibun = dest.get_haibun(year_kanshi, month_kanshi, day_kanshi, time_kanshi)
    tsuhen = dest.get_tsuhen(year_kanshi, month_kanshi, day_kanshi, time_kanshi)
    
    print('年干：', year_kanshi)
    print('月干：', month_kanshi)
    print('日干：', day_kanshi)
    print('時干：', time_kanshi)
    print('蔵干：', )
    print('')

    print('通変：', tsuhen)
    print('五行配分：', haibun)
