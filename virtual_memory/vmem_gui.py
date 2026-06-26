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

        ''' ---- SCROLLABLE PAGING CANVAS --- '''
        self.paging_frame = tk.Frame(self)
        self.paging_frame.place(x=19, y=170, width=1130, height=530)
        
        ''' ---- X AND Y SCROLLBARS ---- '''
        self.canvas_container = tk.Frame(self.paging_frame)
        self.canvas_container.pack(side="top", fill="both", expand="True")
        
        self.paging_canvas = tk.Canvas(self.canvas_container, bg="#b5c4ba", highlightthickness=0)
        self.paging_canvas.pack(side="left", fill="both", expand=True)

        self.cont_yscrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.paging_canvas.yview)
        self.cont_yscrollbar.pack(side="right", fill="y")

        self.cont_xscrollbar = tk.Scrollbar(self.paging_frame, orient="horizontal", command=self.paging_canvas.xview)
        self.cont_xscrollbar.pack(side="bottom", fill="x")

        self.paging_canvas.configure(yscrollcommand=self.cont_yscrollbar.set,xscrollcommand=self.cont_xscrollbar.set) 
        
        # button configuration
        button_config = {
            "font": ("Courier New", 11, "bold"), 
            "bg": "#cedbd0",         
            "fg": "#1a1a1a",      
            "activebackground": "#a1b2a6", 
            "activeforeground": "#000000",
            "bd": 3,
            "relief": "raised",       
            "width": 30           
        }

        ''' --- REFERENCE STRING LABELS ---- '''
        self.reference_label = tk.Label(
            self.canvas,
            text="Reference String: ",
            font=("Courier New", 13, "bold"),
            bg="#b5c4ba",
            justify="left"
        )
        
        self.random_ref_label = tk.Label(
            self.canvas,
            text="",
            font=("Courier New", 11, "bold"),
            bg="#b5c4ba",
            justify="left"
        )
        
        self.canvas.create_window(130, 140, window=self.reference_label)
        self.canvas.create_window(130, 140, window=self.reference_label)
        
        
        ''' ---- PAGE FRAME NUMBER LABEL, DROPDOWN, AND BUTTON ---- '''
        self.select_frame_num_label = tk.Label(
            self.canvas,
            text="Select the number of frames:",
            font=("Courier New", 13, "bold"),
            bg="#b5c4ba",
            justify="center"
        )
        
        self.dropdown_select = ttk.Combobox(
            self.canvas,
            values=["3", "4"],
            font=("Courier New", 13),
            width=6, state="readonly"
        )
        self.dropdown_select.set("3") 
        
        self.generate_btn = tk.Button(
            self,
            text="Generate!",
            command=lambda: controller.show_frame("HomePage"),
            **button_config
        )
        
        self.canvas.create_window(1335, 180, window=self.select_frame_num_label)
        self.canvas.create_window(1335,220, window=self.dropdown_select)
        self.canvas.create_window(1335, 280, window=self.generate_btn)
        
        ''' ---- PAGE FAULT DISPLAY TABLE ---- '''
        #generate table
        self.table_frame = tk.Frame(
            self,
            bg="#b5c4ba",
            bd=2, relief="groove"
        )
        self.canvas.create_window(1160, 393, window=self.table_frame, anchor="nw", width=350, height=300)
        
        tk.Label(
            self.table_frame, 
            text="Algorithm",
            font=("Courier New", 11, "bold"),
            bg="#8ba094", fg="white",
            bd=1, relief="solid"
        ).grid(row=0, column=0, sticky="nsew", ipady=4)
        
        tk.Label(
            self.table_frame, 
            text="Page Faults",
            font=("Courier New", 11, "bold"),
            bg="#8ba094", fg="white",
            bd=1, relief="solid"
        ).grid(row=0, column=1, sticky="nsew", ipady=4)        
        
        self.algo_list = ["FIFO", "OPTIMAL", "LRU", "LFU", "MFU"]
        self.fault_labels = {}
    
        for i, algo_name in enumerate(self.algo_list, start=1):
            tk.Label(
                self.table_frame,
                text=algo_name,
                font=("Courier New", 10, "bold"),
                bg="#b5c4ba", bd=1,
                padx=5, anchor="w", relief="solid"
            ).grid(row=i,column=0, sticky="nswew", ipady=6)
            
            labels = tk.Label(
                self.table_frame, 
                text="-",
                font=("Courier New", 10, "bold"),
                bg="#b5c4ba", bd=1, relief="solid"
            )
            labels.grid(row=i, column=1, sticky="nsew", ipady=6)
        
        self.table_frame.columnconfigure(0, weight=2)
        self.table_frame.columnconfigure(1, weight=1)

        ''' ---- HOME BUTTON  ---- '''
        btn_home = tk.Button(
            self,
            text="Home", 
            command=lambda: controller.show_frame("HomePage"), 
            **button_config
        )
        
        self.canvas.create_window(775, 730, window=btn_home)
        self.refresh_reference()
        
    def refresh_reference(self):
        randomizer = ReferenceStrGenerator(20)
        self.current_reference = randomizer.generate()
        format = " ".join(map(str, self.current_reference))
        
        self.reference_label.config(text=f"Reference String:  {format}")
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.vmem_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.vmem_bg)