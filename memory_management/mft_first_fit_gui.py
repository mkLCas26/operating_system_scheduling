import tkinter as tk
from tkinter import messagebox
try:
    from mft_first_fit_process import MFTProcessEngine as MFTfirstFit
except Exception:
    from .mft_first_fit_process import MFTProcessEngine as MFTfirstFit

class TransparentMFTFirstFitSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MFT: First-Fit")
        self.geometry("1920x1080") 

        self.colors = {
            "text_dark": "#2e1065",    
            "text_light": "#ffffff",   
            "entry_bg": "#ffffff",     
            "border": "#c084fc",       
            "block_proc": "#fbcfe8",   
            "canvas_bg": "#1e1135"     
        }
        
        self.partitions = []
        self.max_render_scale = 60

        self.setup_background()
        self.setup_layout()
        self.reset_to_defaults()

    def setup_background(self):
        try:
            self.bg_image = tk.PhotoImage(file=r"C:\Users\Precious Nicole\Documents\assets\background.png")
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Image load skipped: {e}")
            self.configure(bg="#1e1135")

    def setup_layout(self):
        self.main_container = tk.Frame(self, bg="#1e1135")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.92)

        header = tk.Frame(self.main_container, bg="#2e1a50")
        header.pack(fill="x", pady=(0, 15))
        self.lbl_title = tk.Label(header, text="MFT MEMORY ALLOCATION & ANALYSIS ENGINE (FIRST-FIT STRATEGY)", 
                                  font=("Comic Sans MS", 16, "bold"), fg=self.colors["text_light"], bg="#2e1a50")
        self.lbl_title.pack(pady=10)

        self.workspace = tk.Frame(self.main_container, bg="#1e1135") 
        self.workspace.pack(fill="both", expand=True)

        self.left_side = tk.Frame(self.workspace, bg="#1e1135")
        self.left_side.pack(side="left", fill="y", padx=(0, 15))

        self.right_side = tk.Frame(self.workspace, bg="#1e1135")
        self.right_side.pack(side="right", fill="both", expand=True)

        sys_card = tk.LabelFrame(self.left_side, text=" SYSTEM CONFIGURATION ", font=("Comic Sans MS", 9, "bold"),
                                 bg="#2e1a50", fg=self.colors["text_light"], bd=1, relief="solid", padx=10, pady=8)
        sys_card.pack(fill="x", pady=(0, 10))

        tk.Label(sys_card, text="Total Memory Size (k):", font=("Comic Sans MS", 9, "bold"), bg="#2e1a50", fg="#38bdf8").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_total_mem = tk.Entry(sys_card, font=("Consolas", 10, "bold"), width=8, justify="center", bg=self.colors["entry_bg"], bd=0)
        self.ent_total_mem.grid(row=0, column=1, padx=5, pady=2)

        part_label_frame = tk.LabelFrame(self.left_side, text=" PARTITION SIZES (k) ", font=("Comic Sans MS", 9, "bold"),
                                         bg="#2e1a50", fg=self.colors["text_light"], bd=1, relief="solid", padx=5, pady=5)
        part_label_frame.pack(fill="x", pady=(0, 10))

        self.part_entries = []
        for i in range(5):
            tk.Label(part_label_frame, text=f"Partition {i+1}: ", font=("Comic Sans MS", 9), bg="#2e1a50", fg=self.colors["text_light"]).grid(row=i, column=0, padx=5, pady=2, sticky="e")
            ent_p = tk.Entry(part_label_frame, font=("Consolas", 9, "bold"), width=10, justify="center", bg=self.colors["entry_bg"], bd=0)
            ent_p.grid(row=i, column=1, padx=5, pady=2)
            self.part_entries.append(ent_p)

        input_card = tk.LabelFrame(self.left_side, text=" INPUT PROCESS SIZES (k) ", font=("Comic Sans MS", 9, "bold"),
                                   bg="#2e1a50", fg=self.colors["text_light"], bd=1, relief="solid", padx=5, pady=5)
        input_card.pack(fill="x", pady=(0, 10))

        tk.Label(input_card, text="Job ID", font=("Comic Sans MS", 8, "bold"), bg=self.colors["border"], fg=self.colors["text_light"], width=12).grid(row=0, column=0, padx=5, pady=2)
        tk.Label(input_card, text="Process Size", font=("Comic Sans MS", 8, "bold"), bg=self.colors["border"], fg=self.colors["text_light"], width=12).grid(row=0, column=1, padx=5, pady=2)

        self.jobs_list = ["Job B", "Job C", "Job E", "Job A", "Job D", "Job H", "Job I"]
        self.entry_matrix = {}
        for r, jid in enumerate(self.jobs_list):
            lbl = tk.Label(input_card, text=jid, font=("Comic Sans MS", 9, "bold"), bg="#2e1a50", fg=self.colors["text_light"], width=12)
            lbl.grid(row=r+1, column=0, padx=5, pady=1)
            ent_sz = tk.Entry(input_card, font=("Consolas", 9, "bold"), width=12, justify="center", bg=self.colors["entry_bg"], bd=0)
            ent_sz.grid(row=r+1, column=1, padx=5, pady=1)
            self.entry_matrix[jid] = ent_sz

        btn_pane = tk.Frame(self.left_side, bg="#1e1135")
        btn_pane.pack(fill="x", pady=5)

        self.btn_calc = tk.Button(btn_pane, text="▶ Allocate", font=("Comic Sans MS", 10, "bold"), bg="#22c55e", fg="#ffffff", bd=0, width=12, pady=5, command=self.run_first_fit_allocation)
        self.btn_calc.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_reset = tk.Button(btn_pane, text="🔄 Reset", font=("Comic Sans MS", 10, "bold"), bg="#ef4444", fg="#ffffff", bd=0, width=12, pady=5, command=self.reset_to_defaults)
        self.btn_reset.pack(side="right", padx=5, expand=True, fill="x")

        # 4. SIMULATION SUMMARY DASHBOARD
        self.metrics_card = tk.LabelFrame(self.left_side, text=" REAL-TIME SIMULATION SUMMARY ", font=("Comic Sans MS", 9, "bold"),
                                          bg="#2e1a50", fg=self.colors["text_light"], bd=1, relief="solid", padx=10, pady=5)
        self.metrics_card.pack(fill="x", pady=(5, 0))

        self.metrics_labels = {}
        metrics_keys = ["Total Memory", "Total Partition Size", "Allocated Jobs", "Waiting Jobs", "Internal Fragmentation", "Memory Utilization"]
        for idx, key in enumerate(metrics_keys):
            lbl_key = tk.Label(self.metrics_card, text=f"{key}:", font=("Comic Sans MS", 8), bg="#2e1a50", fg="#a78bfa")
            lbl_key.grid(row=idx, column=0, sticky="w", pady=1)
            lbl_val = tk.Label(self.metrics_card, text="--", font=("Consolas", 9, "bold"), bg="#2e1a50", fg="#ffffff")
            lbl_val.grid(row=idx, column=1, sticky="w", padx=10, pady=1)
            self.metrics_labels[key] = lbl_val

        # 5. ALLOCATION DIARY TEXT LOG
        log_card = tk.LabelFrame(self.right_side, text=" [ ALLOCATION DIARY ] ", font=("Comic Sans MS", 9, "bold"),
                                 bg="#2e1a50", fg=self.colors["text_light"], bd=1, relief="solid", padx=5, pady=5)
        log_card.pack(fill="x", side="bottom", pady=(5, 0))

        log_container = tk.Frame(log_card, bg="#110722")
        log_container.pack(fill="both", expand=True)

        self.txt_log = tk.Text(log_container, font=("Consolas", 9), bg="#110722", fg="#f5d0fe", bd=0, wrap="word", height=8)
        self.txt_log.pack(side="left", fill="both", expand=True)

        log_scroll = tk.Scrollbar(log_container, orient="vertical", command=self.txt_log.yview)
        log_scroll.pack(side="right", fill="y")
        self.txt_log.config(yscrollcommand=log_scroll.set)

        # 6. VECTOR CANVAS DRAWING MAP RENDER VIEWPORT
        self.lbl_canvas_title = tk.Label(self.right_side, text="📊 Dynamic Memory Map Visualizer", font=("Comic Sans MS", 11, "bold"), bg="#1e1135", fg=self.colors["text_light"])
        self.lbl_canvas_title.pack(anchor="w", pady=(0, 5))

        self.canvas = tk.Canvas(self.right_side, bg=self.colors["canvas_bg"], highlightthickness=1, highlightbackground=self.colors["border"])
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.render_canvas())

    def update_log(self, text):
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.insert("end", text)
        self.txt_log.config(state="disabled")

    def reset_to_defaults(self):
        self.ent_total_mem.delete(0, tk.END)
        self.ent_total_mem.insert(0, "60")
        default_partitions = ["12", "12", "12", "12", "12"]
        for idx, entry in enumerate(self.part_entries):
            entry.delete(0, tk.END)
            entry.insert(0, default_partitions[idx])
        default_job_sizes = {"Job B": "9", "Job C": "12", "Job E": "2", "Job A": "3", "Job D": "4", "Job H": "4", "Job I": "12"}
        for jid, entry in self.entry_matrix.items():
            entry.delete(0, tk.END)
            entry.insert(0, default_job_sizes[jid])
        self.run_first_fit_allocation()

    def run_first_fit_allocation(self):
        try:
            total_mem_limit = int(self.ent_total_mem.get())
            part_sizes = [int(ent.get()) for ent in self.part_entries]
            process_sizes = {jid: int(self.entry_matrix[jid].get()) for jid in self.entry_matrix if jid in self.jobs_list}
        except ValueError:
            messagebox.showerror("Validation Error", "Error: Siguraduhing mga positibong numero ang inilagay sa lahat ng fields!")
            return

        try:
            result = MFTfirstFit.calculate_allocation(total_mem_limit, part_sizes, process_sizes)
        except ValueError as err:
            messagebox.showerror("Simulation Error", str(err))
            return

        self.partitions = result["partitions"]
        self.max_render_scale = total_mem_limit

        self.metrics_labels["Total Memory"].config(text=f"{total_mem_limit} KB", fg="#38bdf8")
        self.metrics_labels["Total Partition Size"].config(text=f"{result['total_parts_sum']} KB", fg="#e9d5ff")
        self.metrics_labels["Allocated Jobs"].config(text=", ".join(result["allocated_jobs"]) if result["allocated_jobs"] else "None", fg="#22c55e")
        self.metrics_labels["Waiting Jobs"].config(text=", ".join(result["waiting_jobs"]) if result["waiting_jobs"] else "None", fg="#ef4444")
        self.metrics_labels["Internal Fragmentation"].config(text=f"{result['total_internal_frag']} KB", fg="#fb923c")
        self.metrics_labels["Memory Utilization"].config(text=f"{result['mem_utilization_pct']:.2f} %", fg="#a855f7")

        self.update_log(result["diary_report"])
        self.render_canvas()

    def render_canvas(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 1 or h <= 1: return

        top_limit, bottom_limit = 50, h - 50
        scale = (bottom_limit - top_limit) / float(self.max_render_scale if self.max_render_scale > 0 else 60)

        middle_x = w / 2
        bar_w = 260
        x1, x2 = middle_x - bar_w/2, middle_x + bar_w/2

        self.canvas.create_text(middle_x, top_limit - 20, text=f"LIVE MFT MAP (0k - {self.max_render_scale}k)", fill=self.colors["text_light"], font=("Comic Sans MS", 12, "bold"))

        for p in self.partitions:
            y1 = top_limit + (p["start"] * scale)
            y2 = top_limit + (p["end"] * scale)

            if p["type"] == "unpartitioned":
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="#fb7185", width=2, dash=(5, 4))
                display_text = f"⚠️ Unused Space ({p['size']}k)\n[ UNPARTITIONED MEMORY ]"
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=display_text, fill="#fb7185", font=("Comic Sans MS", 10, "bold", "italic"), justify="center")
            elif p["assigned_job"]:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.colors["block_proc"], outline=self.colors["border"], width=2)
                display_text = f"{p['id']} ({p['size']}k)\n👉 {p['assigned_job']} ({p['job_size']}k)\nFrag: {p['internal_frag']}k"
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=display_text, fill=self.colors["text_dark"], font=("Comic Sans MS", 10, "bold"), justify="center")
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="#a855f7", width=1.5)
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=f"{p['id']} ({p['size']}k)\n[ FREE ]", fill="#a78bfa", font=("Comic Sans MS", 9, "italic"), justify="center")

            self.canvas.create_text(x1 - 35, y1, text=f"{p['start']}k", font=("Consolas", 10, "bold"), fill=self.colors["text_light"])
            self.canvas.create_text(x1 - 35, y2, text=f"{p['end']}k", font=("Consolas", 10, "bold"), fill=self.colors["text_light"])

if __name__ == "__main__":
    app = TransparentMFTFirstFitSimulator()
    app.mainloop()