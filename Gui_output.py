import kanshi_data as kd
from datetime import datetime as dt
from datetime import timedelta as td
import tkinter as tk
import pdb

class Gui_output:

    meishiki = None
    birthday = dt.now()
    sex = -1
    
    def __init__(self, meishiki):

        self.meishiki = meishiki
        self.birthday = meishiki.birthday
        self.sex = meishiki.sex


    def meishiki_output(self):

        root = tk.Tk()

        root.geometry("350x100")

        root.mainloop()

        
