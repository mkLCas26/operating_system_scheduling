import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


#CPU SCHED files
#from [foldername.filename] import ClassName

#MEMORY MANAGEMENT files
#from [foldername.filename] import ClassName

#VIRTUAL MEMORY files
from virtual_memory.fifo_replacement import VirMemPage

#DISK SCHED files
#from [foldername.filename] import ClassName

class MainApp(tk.Tk):
    def __init__(self):     
        super().__init__()   # initialize parent class
        
        self.queue_mode = "MANUAL"  # default value
        
        # general window title, dimension, and allow fullscreen
        self.title("OS SIMULATOR")
        self.geometry("1920x1080")
        self.resizable(True, True)
        
        # for holding pages as frames (allow smooth change of windows)
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        # list of pages included (so if may dinedevelop na page i-add ung class dito para magpakita pag ni-run)
        for page in (HomePage, VirMemPage, DevPage):  
            frame = page(container, self)
            self.frames[page.__name__] = frame
            frame.place(relwidth=1, relheight=1)
        
        self.show_frame("HomePage")   # first page shown will be the Start Page
        
    def show_frame(self, page_name):
        self.frames[page_name].tkraise()
    
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)                # start page is the parent class
        self.controller = controller
        
        ''' FOR BACKGROUND SETUP '''
        # canvas for storing the background of start page
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load the background image in canvas
        self.bg_img = Image.open("assets/main_menu.png")
        self.home_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.home_bg, anchor="nw")
        
        # auto resize of background
        self.canvas.bind("<Configure>", self.resize_bg)
        
        ''' FOR BUTTONS AND LABELS '''
        # button configuration
        button_config = {
            "font": ("Courier New", 11, "bold"), 
            "bg": "#cedbd0",         
            "fg": "#1a1a1a",         
            "activebackground": "#a1b2a6", 
            "activeforeground": "#000000",
            "bd": 3,
            "relief": "raised",    
            "width": 60
        }
        
        # cpu button -> cpu page
        btn_cpu = tk.Button(
            self,
            text="💻 CPU SCHEDULING", 
            command=lambda: controller.show_frame("CpuPage"), 
            **button_config
        )
        
        self.canvas.create_window(775, 360, window=btn_cpu)
        
        # memory management btn  ->  mem man page
        btn_mem = tk.Button(
            self,
            text="📟 MEMORY MANAGEMENT",
            command=lambda: controller.show_frame("MemoryPage"),
            **button_config
        )
        
        self.canvas.create_window(775, 420, window=btn_mem)
        
        # virmem button -> virmem page
        btn_vmem = tk.Button(
            self,
            text="📁 VIRTUAL MEMORY", 
            command=lambda: controller.show_frame("VirMemPage"),
            **button_config
        )
        
        self.canvas.create_window(775, 480, window=btn_vmem)
        
        # disk button -> disk sched page
        btn_disk = tk.Button(
            self,
            text="💾 DISK MANAGEMENT", 
            command=lambda: controller.show_frame("DiskManPage"), 
            **button_config
        )
        
        self.canvas.create_window(775, 540, window=btn_disk)
        
        # dev button -> dev page
        btn_dev = tk.Button(
            self,
            text="👥 Meet The Developers", 
            command=lambda: controller.show_frame("DevPage"), 
            **button_config
        )
        
        self.canvas.create_window(775, 600, window=btn_dev)
    
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.start_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.start_bg)
        
class DevPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        ''' FOR BACKGROUND SETUP '''
        # canvas for storing the background of start page
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load the background image in canvas
        self.bg_img = Image.open("assets/background.png")
        self.dev_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg 
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.dev_bg, anchor="nw")
        
        # auto resize of background
        self.canvas.bind("<Configure>", self.resize_bg) 
        
        ''' FOR BUTTONS AND LABELS '''
    
        # button configuration
        button_config = {
            "font": ("Courier New", 11, "bold"), 
            "bg": "#cedbd0",         
            "fg": "#1a1a1a",         
            "activebackground": "#a1b2a6", 
            "activeforeground": "#000000",
            "bd": 3,
            "relief": "raised",       
            "width": 24,            
            "height": 1
        }
        
        btn_home = tk.Button(
            self,
            text="back 2 home", 
            command=lambda: controller.show_frame("HomePage"), 
            **button_config
        )
        
        self.canvas.create_window(103, 38, window=btn_home)
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.dev_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.dev_bg)


if __name__ == "__main__":
    run_app = MainApp()
    run_app.mainloop()