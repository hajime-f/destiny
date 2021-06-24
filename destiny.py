#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Meishiki import Meishiki
from Unsei import Unsei
from Analysis import Analysis
import sys
            
if __name__ == '__main__':

    # 命式を作る（日干中心）
    meishiki1 = Meishiki(sys.argv)
    meishiki1.build_meishiki()
    meishiki1.append_tsuhen(2)
    meishiki1.append_twelve_fortune(2)
    meishiki1.append_additional_info(2)

    meishiki1.show_basic_info()

    # 命式を整形して出力する
    meishiki1.show_meishiki()
    meishiki1.show_additional_info()

    # 鑑定する
    analysis = Analysis(sys.argv)

    analysis.scoring_kan(meishiki1)
    print(meishiki1.kan_score)
    
    # 命式を作る（用神）
    meishiki2 = Meishiki(sys.argv)
    meishiki2.build_meishiki()
    meishiki2.append_tsuhen(5)
    meishiki2.append_twelve_fortune(5)
    meishiki2.append_additional_info(5)
    
    
    # 命式を整形して出力する
    meishiki2.show_meishiki()
    meishiki2.show_additional_info()

    analysis.scoring_kan(meishiki2)
    print(meishiki2.kan_score)

    
    # 運勢（大運・年運）を作る
    unsei = Unsei(meishiki1)
    unsei.append_daiun()
    unsei.append_nenun()

    # 運勢を整形して出力する
    # unsei.show_daiun_nenun()
    
