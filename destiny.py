#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Meishiki import Meishiki
from Unsei import Unsei
import sys

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
            
if __name__ == '__main__':

    meishiki = Meishiki(sys.argv)
    meishiki.build_meishiki()
    meishiki.append_tsuhen(2)
    meishiki.append_twelve_fortune(2)
    meishiki.append_additional_info(2)
    meishiki.show_basic_info()
    meishiki.show_meishiki()
    meishiki.show_additional_info()

    unsei = Unsei(meishiki)
    unsei.append_daiun()
    unsei.append_nenun()
    unsei.show_daiun_nenun()
    
