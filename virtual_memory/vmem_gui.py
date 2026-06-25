import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk

class VirMemPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # canvas for binary tree bg 
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load bg image
        self.bg_img = Image.open("assets/background.png")
        self.virmem_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg 
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.virmem_bg, anchor="nw")
        
        # auto resizing bg 
        self.canvas.bind("<Configure>", self.resize_bg)
        
        
        ''' test home button '''
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
            command=lambda: controller.show_frame("HomePage") 
            **button_config
        )
        
        self.canvas.create_window(103, 38, window=btn_home)
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.vmem_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.vmem_bg)