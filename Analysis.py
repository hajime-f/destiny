import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td

class Analysis:

    meishiki1 = None
    meishiki2 = None
    
    birthday = dt.now()
    sex = -1
    t_flag = False
    
    daiun = None
    nenun = None

    def __init__(self, meishiki1, meishiki2, unsei):

        self.meishiki1 = meishiki1.meishiki
        self.meishiki2 = meishiki2.meishiki
        
        self.birthday = meishiki1.birthday
        self.sex = meishiki1.sex
        self.t_flag = meishiki1.t_flag
        
        self.daiun = unsei.daiun
        self.nenun = unsei.nenun

    
