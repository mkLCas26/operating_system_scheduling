import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import random

class VirMemPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # canvas for binary tree bg 
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load bg image
        self.bg_img = Image.open("assets/vmem_bg.png")
        self.virmem_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg 
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.virmem_bg, anchor="nw")
        
        # auto resizing bg 
        self.canvas.bind("<Configure>", self.resize_bg)
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.vmem_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.vmem_bg)