import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import random

from virtual_memory.fifo_rep_logic import FIFORep
from virtual_memory.opt_rep_logic import OptimalRep
from virtual_memory.lru_rep_logic import LRURep
from virtual_memory.lfu_rep_logic import LFURep
from virtual_memory.mfu_rep_logic import MFURep

class ReferenceStrGenerator:
    def __init__(self, length):
        self.ref_len = length
    
    def generate(self):
        ref_string = []
        
        for i in range(self.ref_len):
            random_entry = random.randint(0, 9)
            ref_string.append(random_entry)
        
        return ref_string

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
        
        self.canvas.create_window(30, 140, window=self.reference_label, anchor="w")
        
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
            command=self.simulate,
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
            
            self.fault_labels[algo_name] = labels
        
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
        
        self.reference_label.config(text=f"Reference String:  [{format}]")
    
    def draw_page_table(self, title, result, ystart, fcount):
        xstart = 30
        xspacing = 60
        box_size = 40
        
        # for adding text titles per algorithm
        self.paging_canvas.create_text(
            xstart, ystart - 15,
            text=title,
            font=("Courier New", 12, "bold"), fill="#000000",
            anchor="w" 
        )
        
        for i, step in enumerate(result["steps"]):
            xcanvas = xstart + (i * xspacing)
            
            #row 1
            self.paging_canvas.create_rectangle(
                xcanvas, ystart, 
                xcanvas + box_size, ystart + box_size,
                fill="#cedbd0", outline="black", width=1.5
            )
            
            self.paging_canvas.create_text(
                xcanvas + (box_size/2),
                ystart + (box_size/2),
                text=str(step["page"]),
                font=("Courier New", 12, "bold")
            )
            
            #row 2 and proceeding rows
            for frame_num in range(fcount):
                ycanvas = ystart + 50 + (frame_num * box_size)
                
                self.paging_canvas.create_rectangle(
                    xcanvas, ycanvas, 
                    xcanvas + box_size, ycanvas + box_size,
                    fill="#ffffff", outline="#000000"
                )
                
                if frame_num < len(step["frames"]):
                    val = step["frames"][frame_num]
                    
                    if step["status"] == "HIT":
                        text_color = "#111184"
                    else:
                        text_color ="#06402B" 
                    
                    self.paging_canvas.create_text(
                        xcanvas + (box_size/2), ycanvas + (box_size/2),
                        text=str(val),
                        font=("Courier New", 12, "bold"), fill=text_color
                    )
                
            #add hit indication
            if step["status"] == "HIT":
                hit_coord = ystart + 60 + (fcount * box_size)
                self.paging_canvas.create_text(
                    xcanvas +  (box_size/2), hit_coord,
                    text="H",
                    font=("Courier New", 14, "bold"), fill="#111184"
                )
                
                self.paging_canvas.create_rectangle(
                    xcanvas - 3, ystart - 3, 
                    xcanvas + box_size + 3, ystart + 75 + (fcount * box_size),
                    outline="#111184", width=2
                )
        
        return ystart + 110 + (fcount * box_size)
    
    def simulate(self):
        self.refresh_reference()          # new ref str
        self.paging_canvas.delete("all")       # reset canvas
        fcount = int(self.dropdown_select.get())     #get # of frames'
        
        current_y = 30
        
        ''' ---- FOR FIFO UI INTEGRATION ---- '''
        fifo_algo = FIFORep(self.current_reference, fcount)
        fifo_run = fifo_algo.run()
        self.fault_labels["FIFO"].config(text=str(fifo_run["fault_total"]))
        
        current_y = self.draw_page_table("FIFO PAGE REPLACEMENT ALGORITHM", fifo_run, current_y, fcount)
        
        ''' ---- FOR OPTIMAL PAGE UI INTEGRATION ---- '''
        optimal_algo = OptimalRep(self.current_reference, fcount)
        optimal_run = optimal_algo.run()
        self.fault_labels["OPTIMAL"].config(text=str(optimal_run["fault_total"]))
        
        current_y = self.draw_page_table("OPTIMAL PAGE REPLACEMENT ALGORITHM", optimal_run, current_y, fcount)
        
        ''' ---- FOR LRU UI INTEGRATION ---- '''
        lru_algo = LRURep(self.current_reference, fcount)
        lru_run = lru_algo.run()
        self.fault_labels["LRU"].config(text=str(lru_run["fault_total"]))
        
        current_y = self.draw_page_table("LEAST RECENTLY USED (LRU) PAGE REPLACEMENT ALGORITHM", lru_run, current_y, fcount)
        
        ''' ---- FOR LFU UI INTEGRATION ---- '''
        lfu_algo = LFURep(self.current_reference, fcount)
        lfu_run = lfu_algo.run()
        self.fault_labels["LFU"].config(text=str(lfu_run["fault_total"]))
        
        current_y = self.draw_page_table("LEAST FREQUENTLY USED (LFU) PAGE REPLACEMENT ALGORITHM", lfu_run, current_y, fcount)
        
        ''' ---- FOR MFU UI INTEGRATION ---- '''
        mfu_algo = MFURep(self.current_reference, fcount)
        mfu_run = mfu_algo.run()
        self.fault_labels["MFU"].config(text=str(mfu_run["fault_total"]))
        
        current_y = self.draw_page_table("MOST FREQUENTLY USED (MFU) PAGE REPLACEMENT ALGORITHM", mfu_run, current_y, fcount)
        
         
        horizontal_limit = (len(self.current_reference) * 65) + 50
        vertical_limit = current_y + 40
        self.paging_canvas.configure(scrollregion=(0, 0, horizontal_limit, vertical_limit)) 
     
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.vmem_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.vmem_bg)