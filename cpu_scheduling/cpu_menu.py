import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk

class CpuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load bg image
        self.bg_img = Image.open("assets/cpu_bg_main.png")
        self.virmem_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg 
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.virmem_bg, anchor="nw")
        
        # auto resizing bg 
        self.canvas.bind("<Configure>", self.resize_bg)
        
        
        ''' FOR CPU ALGO BUTTONS '''
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
        
        # fcfs button -> fcfs page
        btn_fcfs = tk.Button(
            self,
            text="🗃️ FCFS (FIRST-COME, FIRST SERVED)", 
            command=lambda: controller.show_frame("FcfsPage"), 
            **button_config
        )
        
        self.canvas.create_window(775, 360, window=btn_fcfs)
        
        # sjf btn  ->  preemp & non-preemp page
        btn_sjf = tk.Button(
            self,
            text="🗃️ SJF (SHORTEST JOB FIRST)",
            command=lambda: controller.show_frame("SjfMenu"),
            **button_config
        )
        
        self.canvas.create_window(775, 420, window=btn_sjf)
        
        # prio button -> preemp & non-preemp page
        btn_prio = tk.Button(
            self,
            text="🗃️ PRIORITY SCHEDULING", 
            command=lambda: controller.show_frame("PrioMenu"),
            **button_config
        )
        
        self.canvas.create_window(775, 480, window=btn_prio)
        
        # rr button -> rr page
        btn_rr = tk.Button(
            self,
            text="🗃️ Round Robin Scheduling", 
            command=lambda: controller.show_frame("RoundRobinPage"), 
            **button_config
        )
        
        self.canvas.create_window(775, 540, window=btn_rr)
        
        # home button -> main menu page
        btn_home = tk.Button(
            self,
            text="🏠 Home", 
            command=lambda: controller.show_frame("HomePage"), 
            **button_config
        )
        
        self.canvas.create_window(775, 600, window=btn_home)

    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.virmem_bg = ImageTk.PhotoImage(resized)

        self.canvas.itemconfig(self.canvas_bg, image=self.virmem_bg)