from tkinter import *
from tkinter import ttk, messagebox, filedialog
from threading import Thread
import os
import queue
import loadingDialog
import re


class Application_UI(object):
    # 默认查找路径
    search_path = os.path.abspath("./")
    # 是否开始查找标志
    is_start = 0
    
    def __init__(self):
        # 设置UI界面
        self.window = Tk()
        win_width = 600
        win_height = 500
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width - win_width) / 2)
        y = int((screen_height - win_height) / 2)
        self.window.title("磁盘文件搜索工具")
        self.window.geometry("%sx%s+%s+%s" % (win_width, win_height, x, y))
        # 最好用绝对路径
        self.window.iconbitmap(r"G:\PyCharm 2019.1\project\TK\项目\磁盘搜索工具\icon.ico")
        #
        
        top_frame = Frame(self.window)
        top_frame.pack(side = TOP, padx = 5, pady = 20, fill = X)
        
        self.search_val = StringVar()
        entry = Entry(top_frame, textvariable = self.search_val)
        entry.pack(side = LEFT, expand = True, fill = X, ipady = 4.5)
        
        search_btn = Button(top_frame, text = "搜索", width = 10, command = self.search_file)
        search_btn.pack(padx = 10)
        
        bottom_frame = Frame(self.window)
        
        bottom_frame.pack(side = LEFT, expand = True, fill = BOTH, padx = 5)
        
        tree = ttk.Treeview(bottom_frame, show = "headings", columns = ("name", "path"))
        self.treeView = tree
        y_scroll = Scrollbar(bottom_frame)
        y_scroll.config(command = tree.yview)
        y_scroll.pack(side = RIGHT, fill = Y)
        x_scroll = Scrollbar(bottom_frame)
        x_scroll.config(command = tree.yview, orient = HORIZONTAL)
        x_scroll.pack(side = BOTTOM, fill = X)
        tree.config(xscrollcommand = x_scroll.set, yscrollcommand = y_scroll.set)
        
        tree.column("name", anchor = "w", width = 8)
        tree.column("path", anchor = "w")
        tree.heading("name", text = "文件名称", anchor = "w")
        tree.heading("path", text = "路径", anchor = "w")
        tree.pack(side = LEFT, fill = BOTH, expand = True, ipady = 20)
        
        menu = Menu(self.window)
        self.window.config(menu = menu)
        
        set_path = Menu(menu, tearoff = 0)
        set_path.add_command(label = "设置路径", accelerator="Ctrl + F", command = self.open_dir)
        set_path.add_command(label = "开始扫描", accelerator="Ctrl + T", command = self.search_file)
        
        menu.add_cascade(label = "文件", menu = set_path)
        
        about = Menu(menu, tearoff = 0)
        about.add_command(label = "版本", accelerator = "v1.0.0")
        about.add_command(label = "作者", accelerator = "样子")
        menu.add_cascade(label = "关于", menu = about)
        
        self.progressbar = loadingDialog.progressbar(self.window)
        # 设置队列，保存查找完毕标志
        self.queue = queue.Queue()
        # 开始监听进度条
        self.listen_progressBar()
        
        self.window.bind("<Control-Key-f>", lambda event: self.open_dir())
        self.window.bind("<Control-Key-r>", lambda event: self.search_file())
        self.window.protocol("WM_DELETE_WINDOW", self.call_close_window)
        self.window.mainloop()

class Application(Application_UI):
    def __init__(self):
        Application_UI.__init__(self)
        
        
    def call_close_window(self):
        self.progressbar.exit_()
        self.window.destroy()
    
    ''' 监听进度条'''
    def listen_progressBar(self):
        # 窗口每隔一段时间执行一个函数
        self.window.after(400, self.listen_progressBar)
        while not self.queue.empty():
            queue_data = self.queue.get()
            if queue_data == 1:
                # 关闭进度条
                self.progressbar.exit_()
                self.is_start = 0
    
    ''' 设置默认搜索路径'''
    def open_dir(self):
        path = filedialog.askdirectory(title = u"设置目录", initialdir = self.search_path)
        print("设置路径："+path)
        self.search_path = path
    
    ''' 开始搜索'''
    def search_file(self):
        def scan(self, keyword):
            # 清空表格数据
            for _ in map(self.treeView.delete, self.treeView.get_children()):
                pass
            
            # 筛选文件
            self.find_file_insert(keyword)
                
            # 设置查找完毕标志
            self.queue.put(1)
        
        if self.is_start == 0:
            # 获取查找关键词
            keyword = str.strip(self.search_val.get())
            if not keyword:
                messagebox.showerror("提示", "请输入文件名称")
                self.search_val.set("")
                return
            
            # 设置已经开始查找状态
            self.is_start = 1
            # 开启线程
            self.thread = Thread(target = scan, args = (self, keyword))
            self.thread.setDaemon(True)
            self.thread.start()
            
             # 显示进度条
            self.progressbar.start()
        else:
            pass
        
    
    ''' 查找设置目录下所有文件并插入表格'''
    def find_file_insert(self, keyword):
        try:
            for root, dirs, files in os.walk(self.search_path, topdown = True):
                for file in files:
                    match_result = self.file_match(file, keyword)
                    if match_result is True: 
                        file_path = os.path.join(root, file)
                        # 插入数据到表格
                        self.treeView.insert('', END, values = (file, file_path))
                        # 更新表格
                        self.treeView.update()
        except Exception as e:
            print(e)
        
        return True
    
    ''' 名称匹配'''
    def file_match(self, file, keyword):
        print("文件匹配：",keyword, file)
        result = re.search(r'(.*)'+keyword+'(.*)', file, re.I)
        if result:
            return True
        return False
    
if __name__ == "__main__":
    Application()
