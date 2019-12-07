from tkinter import *
from tkinter import ttk

class progressbar(object):
    
    def __init__(self, window):
        self.window = window
    
    ''' 开启加载'''
    def start(self):
        try:
            loading_win = Toplevel()
            self.root = loading_win
            loading_win.overrideredirect(True)
            Label(loading_win, text="线程正在执行,请稍等……", fg="red").pack(pady=2)
            progressbar = ttk.Progressbar(loading_win, mode='indeterminate', length=200)
            progressbar.pack(pady=10, padx=35)
            progressbar.start()
            loading_win.update()
            loading_win.resizable(True, True)
            curWidth = loading_win.winfo_width()
            curHeight = loading_win.winfo_height()
            scnWidth, scnHeight = loading_win.maxsize() 
            geometry = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
            loading_win.geometry(geometry)
            #loading_win.attributes("-topmost", -1)
            loading_win.grab_set()
            loading_win.focus_set()
            loading_win.mainloop()
        except Exception as e:
            print(e)
            
    ''' 关闭加载'''
    def exit_(self):
        try:
            if self.root:
                self.root.destroy()
        except Exception as e:
            print(e)
            
