import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils import resource_path

from cpu_scheduling.rr_process import calculate_rr

class RRPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        self.process_queue = [] 
        self.process_counter = 1  
        
        # Background Canvas
        self.bg_canvas = tk.Canvas(self, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1) 
        
        # Load bg image
        self.bg_img = Image.open(resource_path("assets/rr_bg.png"))
        self.virmem_bg = ImageTk.PhotoImage(self.bg_img)
        
        # Draw bg 
        self.canvas_bg = self.bg_canvas.create_image(0, 0, image=self.virmem_bg, anchor="nw")
        
        # Auto resizing bg 
        self.bg_canvas.bind("<Configure>", self.resize_bg)

        # Call UI setup
        self.setup_ui()

    def setup_ui(self):
        # --- 1. INPUT FRAME (Top Left) ---
        input_frame = tk.Frame(self, bg="#b5c4ba", bd=4, relief="ridge") 
        # FIX 1: Made the box taller (0.38) to fit 3 rows
        input_frame.place(relx=0.03, rely=0.16, relwidth=0.32, relheight=0.20)

        input_frame.columnconfigure(0, weight=1) 
        input_frame.columnconfigure(1, weight=2)

        # Styling dictionaries
        lbl_style = {"bg": "#b5c4ba", "fg": "#2b1f47", "font": ("Courier", 11, "bold")}
        
        entry_style = {
            "width": 10, 
            "bg": "#cedbd0", 
            "fg": "#1a1a1a", 
            "font": ("Courier", 11, "bold"), 
            "relief": "solid", 
            "bd": 1
        }
        
        btn_style = {
            "font": ("Courier", 10),
            "bg": "#cedbd0", 
            "fg": "#1a1a1a",
            "activebackground": "#a1b2a6",
            "relief": "solid",
            "bd": 1
        }

        # ROW 0 & 1: Labels and Entries
        tk.Label(input_frame, text="Arrival Time:", **lbl_style).grid(row=0, column=0, padx=(10, 5), pady=(15, 2), sticky="e")
        self.entry_at = tk.Entry(input_frame, **entry_style)
        self.entry_at.grid(row=0, column=1, padx=5, pady=(15, 2), sticky="w")

        tk.Label(input_frame, text="Burst Time:", **lbl_style).grid(row=1, column=0, padx=(10, 5), pady=2, sticky="e")
        self.entry_bt = tk.Entry(input_frame, **entry_style)
        self.entry_bt.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # ROW 2: Time Quantum Input
        tk.Label(input_frame, text="Time Quantum:", **lbl_style).grid(row=2, column=0, padx=(10, 5), pady=(2, 10), sticky="e")
        self.entry_tq = tk.Entry(input_frame, **entry_style)
        self.entry_tq.grid(row=2, column=1, padx=5, pady=(2, 10), sticky="w")

        # ROW 3: The Button Frame 
        # FIX 2: Changed to row=3 so it doesn't crush the Time Quantum!
        btn_frame = tk.Frame(input_frame, bg="#b5c4ba")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 15), padx=10, sticky="ew")
        
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_frame.columnconfigure(2, weight=1)

        tk.Button(btn_frame, text="Add Process", command=self.add_process, **btn_style).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Start RR", command=self.run_algorithm, **btn_style).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Clear", command=self.clear_all, **btn_style).grid(row=0, column=2, padx=5, sticky="ew")

        # --- 2. TABLE FRAME (Bottom Left) ---
        table_frame = tk.Frame(self, bg="#b5c4ba", bd=4, relief="ridge")
        # FIX 3: Pushed the table down to 0.56 and shrunk its height to 0.32 so it fits perfectly
        table_frame.place(relx=0.03, rely=0.38, relwidth=0.32, relheight=0.50)

        style = ttk.Style()
        style.theme_use("clam") 
        
        style.configure("Treeview", 
                        background="#cedbd0", 
                        foreground="#1a1a1a", 
                        fieldbackground="#cedbd0",
                        rowheight=25,
                        bordercolor="#99aab5", 
                        font=("Courier", 8))
        
        style.configure("Treeview.Heading", 
                        background="#a1b2a6", 
                        foreground="black", 
                        relief="solid",
                        borderwidth=1,
                        bordercolor="#18301f",
                        font=("Courier", 9, "bold"))
        
        style.map('Treeview', background=[('selected', '#8a2be2')])

        cols = ("PID", "AT", "BT", "CT", "TAT", "WT")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=40, anchor="center") # Shrunk width to fit nicely
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # --- 3. RIGHT FRAME (Gantt Chart & Stats) ---
        right_frame = tk.Frame(self, bg="#b5c4ba", bd=4, relief="ridge")
        right_frame.place(relx=0.38, rely=0.16, relwidth=0.59, relheight=0.72)

        self.lbl_stats = tk.Label(right_frame, text="Avg TAT: 0.00 | Avg WT: 0.00 | CPU Utilization: 0.00%", font=("Courier", 14, "bold"), bg="#b5c4ba")
        self.lbl_stats.pack(anchor="w", padx=20, pady=15)

        tk.Label(right_frame, text="Gantt Chart:", font=("Courier", 12, "bold"), bg="#b5c4ba").pack(anchor="w", padx=20)
        
        self.canvas = tk.Canvas(right_frame, bg="#cedbd0", height=200, highlightthickness=0, relief="solid", bd=2)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

    def resize_bg(self, event):
        new_width = event.width
        new_height = event.height
        
        if new_width > 0 and new_height > 0:
            resized_image = self.bg_img.resize((new_width, new_height), Image.LANCZOS)
            self.virmem_bg = ImageTk.PhotoImage(resized_image)
            self.bg_canvas.itemconfig(self.canvas_bg, image=self.virmem_bg)

    # --- FUNCTIONS ---
    def add_process(self):
        at = self.entry_at.get()
        bt = self.entry_bt.get()

        if not at.isdigit() or not bt.isdigit():
            messagebox.showerror("Error", "Please enter valid integers for AT and BT.")
            return

        pid = f"P{self.process_counter}" 
        self.process_counter += 1  

        self.process_queue.append({'pid': pid, 'at': int(at), 'bt': int(bt)})
        
        self.tree.insert("", "end", values=(pid, at, bt, "-", "-", "-"))
        
        self.entry_at.delete(0, tk.END)
        self.entry_bt.delete(0, tk.END)

    def run_algorithm(self):
        if not self.process_queue:
            messagebox.showwarning("Warning", "Add some processes first!")
            return
        
        # NEW: Validate and grab the Time Quantum
        tq_str = self.entry_tq.get()
        if not tq_str.isdigit() or int(tq_str) <= 0:
            messagebox.showerror("Error", "Please enter a valid positive integer for Time Quantum.")
            return
        
        time_quantum = int(tq_str)

        calculated_data, avg_tat, avg_wt, cpu_util, timeline = calculate_rr(self.process_queue, time_quantum)

        for item in self.tree.get_children():
            self.tree.delete(item) 
            
        for p in calculated_data:
            self.tree.insert("", "end", values=(p['pid'], p['at'], p['bt'], p['ct'], p['tat'], p['wt']))

        self.lbl_stats.config(text=f"Avg TAT: {avg_tat} | Avg WT: {avg_wt} | CPU Utilization: {cpu_util}%")
        self.draw_gantt(timeline)

    def draw_gantt(self, timeline):
        self.canvas.delete("all") 
        if not timeline: return

        total_time = timeline[-1][2]
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 10: canvas_width = 600 
        
        scale = (canvas_width - 40) / (total_time if total_time > 0 else 1)
        
        x_start = 20
        y_top = 40
        y_bottom = 100

        self.canvas.create_text(x_start, y_bottom + 15, text="0", font=("Courier", 10, "bold"))

        for entry in timeline:
            pid, start, end = entry
            duration = end - start
            width = duration * scale
            x_end = x_start + width

            color = "#cccccc" if pid == "IDLE" else "#8a2be2"

            self.canvas.create_rectangle(x_start, y_top, x_end, y_bottom, fill=color, outline="black", width=2)
            self.canvas.create_text(x_start + (width / 2), (y_top + y_bottom) / 2, text=pid, fill="white" if pid != "IDLE" else "black", font=("Courier", 10, "bold"))
            self.canvas.create_text(x_end, y_bottom + 15, text=str(end), font=("Courier", 10, "bold"))

            x_start = x_end

    def clear_all(self):
        self.process_queue.clear()
        self.process_counter = 1 
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.canvas.delete("all")
        self.lbl_stats.config(text="Avg TAT: 0.00 | Avg WT: 0.00 | CPU Util: 0.00%")
        self.entry_tq.delete(0, tk.END)