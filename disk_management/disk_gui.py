import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils import resource_path

from disk_management.fcfs_disk import calculate_fcfs
from disk_management.sstf_disk import calculate_sstf
from disk_management.scan_disk import calculate_scan
from disk_management.c_scan_disk import calculate_c_scan
from disk_management.look_disk import calculate_look
from disk_management.c_look_disk import calculate_c_look


class DiskManPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        # background canvas
        self.bg_canvas = tk.Canvas(self, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.bg_img = Image.open(resource_path("assets/background.png"))
        self.disk_bg = ImageTk.PhotoImage(self.bg_img)

        # draw bg
        self.canvas_bg = self.bg_canvas.create_image(0, 0, image=self.disk_bg, anchor="nw")

        # auto resize bg
        self.bg_canvas.bind("<Configure>", self.resize_bg)

        self.setup_ui()

    def setup_ui(self):
        # INPUT FRAME (Top Left) ---
        input_frame = tk.Frame(self, bg="#b5c4ba", bd=4, relief="ridge")
        input_frame.place(relx=0.03, rely=0.16, relwidth=0.33, relheight=0.48)

        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=2)

        lbl_style = {"bg": "#b5c4ba", "fg": "#2b1f47", "font": ("Courier", 11, "bold")}
        entry_style = {"bg": "#cedbd0", "fg": "#1a1a1a", "font": ("Courier", 11, "bold"), "relief": "solid", "bd": 1}
        btn_style = {"font": ("Courier", 10), "bg": "#cedbd0", "fg": "#1a1a1a", "activebackground": "#a1b2a6",
                     "relief": "solid", "bd": 1}

        # Form Inputs
        tk.Label(input_frame, text="Initial Head:", **lbl_style).grid(row=0, column=0, padx=10, pady=(15, 5),
                                                                      sticky="e")
        self.entry_head = tk.Entry(input_frame, **entry_style)
        self.entry_head.grid(row=0, column=1, padx=5, pady=(15, 5), sticky="w")

        tk.Label(input_frame, text="Total Cylinders:", **lbl_style).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_cylinders = tk.Entry(input_frame, **entry_style)
        self.entry_cylinders.insert(0, "200")  # Default value
        self.entry_cylinders.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Requests (csv):", **lbl_style).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_reqs = tk.Entry(input_frame, **entry_style)
        self.entry_reqs.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # selectable buttons for algorithms (using Radiobuttons with indicatoron=False)
        tk.Label(input_frame, text="Algorithm:", **lbl_style).grid(row=3, column=0, padx=10, pady=10, sticky="ne")

        self.algo_var = tk.StringVar(value="FCFS")  # default selection
        algo_frame = tk.Frame(input_frame, bg="#b5c4ba")
        algo_frame.grid(row=3, column=1, padx=5, pady=10, sticky="w")

        algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
        for i, alg in enumerate(algorithms):
            rb = tk.Radiobutton(
                algo_frame,
                text=alg,
                variable=self.algo_var,
                value=alg,
                indicatoron=False,  # this makes it look like a standard button
                width=8,
                bg="#cedbd0",
                fg="#1a1a1a",
                selectcolor="#8a2be2",  # purple highlight when selected
                font=("Courier", 9, "bold"),
                relief="solid",
                bd=1
            )
            # 3-column, 2-row grid
            rb.grid(row=i // 3, column=i % 3, padx=2, pady=2)

        # directions
        style = ttk.Style()
        style.theme_use('clam')

        tk.Label(input_frame, text="Direction:", **lbl_style).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.combo_dir = ttk.Combobox(input_frame, values=["Left", "Right"], state="readonly", font=("Courier", 10),
                                      width=10)
        self.combo_dir.current(1)
        self.combo_dir.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Action Button Frame
        btn_frame = tk.Frame(input_frame, bg="#b5c4ba")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 10), padx=10, sticky="ew")

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_frame.columnconfigure(2, weight=1)

        tk.Button(btn_frame, text="Calculate", command=self.run_algorithm, **btn_style).grid(row=0, column=0, padx=5,
                                                                                             sticky="ew")
        tk.Button(btn_frame, text="Clear", command=self.clear_all, **btn_style).grid(row=0, column=1, padx=5,
                                                                                     sticky="ew")
        tk.Button(btn_frame, text="Home", command=lambda: self.controller.show_frame("HomePage"), **btn_style).grid(
            row=0, column=2, padx=5, sticky="ew")

        # RIGHT FRAME (Graph & Stats)
        right_frame = tk.Frame(self, bg="#b5c4ba", bd=4, relief="ridge")
        right_frame.place(relx=0.38, rely=0.16, relwidth=0.59, relheight=0.72)

        self.lbl_stats = tk.Label(right_frame, text="Total Head Movement: 0 Cylinders", font=("Courier", 14, "bold"),
                                  bg="#b5c4ba")
        self.lbl_stats.pack(anchor="w", padx=20, pady=15)

        self.lbl_sequence = tk.Label(right_frame, text="Seek Sequence: []", font=("Courier", 10, "bold"), bg="#b5c4ba",
                                     wraplength=700, justify="left")
        self.lbl_sequence.pack(anchor="w", padx=20, pady=(0, 10))

        self.canvas = tk.Canvas(right_frame, bg="#cedbd0", highlightthickness=0, relief="solid", bd=2)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

    def resize_bg(self, event):
        new_width = event.width
        new_height = event.height
        if new_width > 0 and new_height > 0:
            resized_image = self.bg_img.resize((new_width, new_height), Image.LANCZOS)
            self.disk_bg = ImageTk.PhotoImage(resized_image)
            self.bg_canvas.itemconfig(self.canvas_bg, image=self.disk_bg)

    def run_algorithm(self):
        try:
            head = int(self.entry_head.get())
            cylinders = int(self.entry_cylinders.get())
            reqs_raw = self.entry_reqs.get().split(",")
            requests = [int(r.strip()) for r in reqs_raw if r.strip().isdigit()]

            if not requests:
                messagebox.showerror("Error", "Please enter valid requests separated by commas.")
                return
            if head < 0 or head >= cylinders:
                messagebox.showerror("Error", "Initial Head must be within 0 and Total Cylinders - 1.")
                return

        except ValueError:
            messagebox.showerror("Error", "Please make sure Head and Total Cylinders are valid integers.")
            return

        algo = self.algo_var.get()  # Getting value from the selectable buttons variable
        direction = self.combo_dir.get()

        if algo == "FCFS":
            seek_sequence, total_movement = calculate_fcfs(requests, head)
        elif algo == "SSTF":
            seek_sequence, total_movement = calculate_sstf(requests, head)
        elif algo == "SCAN":
            seek_sequence, total_movement = calculate_scan(requests, head, cylinders, direction)
        elif algo == "C-SCAN":
            seek_sequence, total_movement = calculate_c_scan(requests, head, cylinders, direction)
        elif algo == "LOOK":
            seek_sequence, total_movement = calculate_look(requests, head, direction)
        elif algo == "C-LOOK":
            seek_sequence, total_movement = calculate_c_look(requests, head, direction)

        self.lbl_stats.config(text=f"Total Head Movement: {total_movement} Cylinders")
        self.lbl_sequence.config(text=f"Seek Sequence: {seek_sequence}")

        self.draw_graph(seek_sequence, cylinders)

    def draw_graph(self, sequence, total_cylinders):
        self.canvas.delete("all")
        if not sequence: return

        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()

        if c_width < 10: c_width = 800
        if c_height < 10: c_height = 400

        pad_x = 40
        pad_y = 30

        # draw axis line
        self.canvas.create_line(pad_x, pad_y, c_width - pad_x, pad_y, width=3, fill="#2b1f47")
        self.canvas.create_text(pad_x, pad_y - 15, text="0", font=("Courier", 10, "bold"))
        self.canvas.create_text(c_width - pad_x, pad_y - 15, text=str(total_cylinders - 1),
                                font=("Courier", 10, "bold"))

        max_cyl = total_cylinders - 1 if total_cylinders > 1 else 1
        scale_x = (c_width - 2 * pad_x) / max_cyl

        steps = len(sequence)
        scale_y = (c_height - 2 * pad_y) / (steps if steps > 1 else 1)

        coords = []
        for i, cyl in enumerate(sequence):
            x = pad_x + (cyl * scale_x)
            y = pad_y + (i * scale_y)
            coords.append((x, y))

            # point
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#8a2be2", outline="white")

            # label offset to prevent text overlap
            offset_y = 12 if i % 2 == 0 else -12
            self.canvas.create_text(x, y + offset_y, text=str(cyl), font=("Courier", 9, "bold"), fill="#1a1a1a")

        # connecting lines
        for i in range(len(coords) - 1):
            self.canvas.create_line(coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1], fill="#2b1f47",
                                    width=2, dash=(4, 2))

    def clear_all(self):
        self.entry_head.delete(0, tk.END)
        self.entry_reqs.delete(0, tk.END)
        self.canvas.delete("all")
        self.lbl_stats.config(text="Total Head Movement: 0 Cylinders")
        self.lbl_sequence.config(text="Seek Sequence: []")
        self.algo_var.set("FCFS")  # reset selected button