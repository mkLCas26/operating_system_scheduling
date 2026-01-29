import tkinter as tk
from tkinter import messagebox
import json
import re
from collections import deque

class QueueParkingDashboard:
    def __init__(self, root):
        self.root =  root
        self.root.title("Queue Parking Slot: FIFO format")
        self.root.state("zoomed")

        self.main_queue = deque()
        self.temp_queue = deque()
        self.max_capacity =  10
        self.total_arrivals = 0
        self.total_departures = 0
        self.dark = True

        self.theme = {
            "bg": "#0F172A",
            "card": "#1E293B",
            "sidebar": "#020617",
            "muted": "#94A3B8",
            "accent":"#38BDF8",
            "entry":"#020617",
            "error":"#EF4444",
            "text":"#F8FAFC"
        }

        self.vehicle_colors = {
            "Car": "#9fe5f5",
            "Motorcycle":"#c383eb",
            "Truck":"#fab143",
            "Van":"#de3a3a"
        }
        self.setup_ui()
        self.update_ui()


    def setup_ui(self):
        self.root.configure(bg=self.theme["bg"])
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

#SIDEBAR

        self.sidebar = tk.Frame(self.root, width=280, bg=self.theme["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar, text="QUEUE", fg=self.theme["accent"],
            bg=self.theme["sidebar"], font=("Segoe UI", 36,"bold") 
        ).pack(pady=(60,0))

        tk.Label(
            self.sidebar, text="FIFO SYSTEM",
            fg=self.theme["muted"], bg=self.theme["sidebar"],
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(0,60))

        self.stats = {}
        for text in ["Arrivals", "Departures", "Current Load"]:
            lbl = tk.Label(
                self.sidebar, font=("Segoe UI", 14),
                fg=self.theme["text"], bg=self.theme["sidebar"]
            )
            lbl.pack(pady=15)
            self.stats[text] = lbl

#MAIN
        self.main = tk.Frame(self.root, bg=self.theme["bg"])
        self.main.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main.columnconfigure(0, weight=3)
        self.main.columnconfigure(1, weight=2)
        self.main.columnconfigure(2, weight=3)
        
        self.main_card = self.card(self.main, "MAIN QUEUE (FRONT -> REAR)", 0)
        self.canvas_main = tk.Canvas(self.main_card, bg=self.theme["card"], highlightthickness=0)
        self.canvas_main.pack(expand=True, fill="both")

        self.ctrl_card = self.card(self.main, "CONTROL PANEL", 1)
        self.controls()

        self.temp_card = self.card(self.main, "TEMPORARY QUEUE", 2)
        self.canvas_temp = tk.Canvas(self.temp_card, bg=self.theme["card"], highlightthickness=0)
        self.canvas_temp.pack(expand= True, fill="both")

    def card(self, parent, title, col):
        frame = tk.Frame(parent, bg=self.theme["card"], padx=25, pady=25)
        frame.grid(row=0, column=col, sticky="nsew", padx=15)

        tk.Label(
            frame, text=title, bg=self.theme["card"],
            fg=self.theme["muted"], font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 20))

        return frame
    
    def controls(self):
        f= tk.Frame(self.ctrl_card, bg=self.theme["card"])
        f.pack(expand=True)

        tk.Label(
            f, text="TYPE OF VEHICLE",
            bg=self.theme["card"], fg=self.theme["muted"],
            font=("Segoe UI", 12, "bold")
        ).pack(pady=10)

        self.vtype = tk.StringVar(value="Car")
        for t in self.vehicle_colors:
            tk.Radiobutton(
                f, text=t, value=t, variable=self.vtype,
                indicatoron=0, width=20, pady=10,
                font=("Segoe UI", 12, "bold"),
                bg=self.theme["bg"], fg="white",
                selectcolor=self.vehicle_colors[t]
            ).pack(pady=4)

#INPUT
        tk.Label(
            f, text="PLATE NUMBER",
            bg=self.theme["card"], fg=self.theme['muted'],
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(30,10))

        self.plate = tk.Entry(
            f, font=("Consolas", 16, "bold"),
            justify="center", relief="solid", bd=3,
            bg=self.theme["entry"], fg = "white",
            insertbackground="white", highlightthickness=3,
            highlightbackground=self.theme["accent"],
            highlightcolor=self.theme["accent"]
        )
        self.plate.pack(ipady=12, fill="x")
        self.plate.insert(0, "ABC-1234")

        self.button(f, "PROCESS ARRIVAL", self.arrival)
        self.button(f, "PROCESS DEPARTURE", self.departure)

    def button(self, parent, text, cmd):
        tk.Button(
            parent, text=text, command=cmd,
            font=("Segoe UI", 13, "bold"),
            bg=self.theme["accent"], fg="black",
            relief="flat", pady=14
        ).pack(fill="x", pady=12)

#QUEUE LOGIC
    def arrival(self):
        plate = self.plate.get().strip().upper()

        if not re.match(r"^[A-Z]{3}-\d{4}$", plate):
            messagebox.showerror("Invalid Input","Follow the format ABC-1234")
            return
        
        if len(self.main_queue) + len(self.temp_queue) < self.max_capacity:
            messagebox.showwarning("Queue Full", "Parking queue is full")
            return
        
        self.total_arrivals += 1
        self.temp_queue.append({
            "plate": plate,
            "type": self.vtype.get(),
            "a": self.total_arrivals
        })
        
        self.balance()
        self.update_ui()
        self.plate.delete(0, tk.END) 

    def departure(self):
        if not self.main_queue:
            messagebox.showinfo("Empty", " No vehicles to depart")
            return
        
        self.total_departures += 1
        car = self.main_queue.popleft()
        self.balance()
        self.update_ui()

        messagebox.showinfo(
            "Departed",
            f"{car['plate']} departed\nArrival #{car['a']}"
        )
    def balance(self):
        while self.temp_queue and len(self.main_queue) < self.max_capacity:
            self.main_queue.append(self.temp_queue.popleft())

#DRAWING
    def draw(self, canvas, queue):
        canvas.delete("all")
        w, h= canvas.winfo_width(), canvas.winfo_height()
        slot = (h- 60)/ self.max_capacity

        for i in range(self.max_capacity):
            y= 30 + i * slot
            canvas.create_rectangle(40, y, w - 40, y + slot - 10, outline="#334155", width=2)

            if i < len(queue):
                car = queue[i]
                canvas.create_rectangle( 45, y + 5, w - 45, y + slot - 15, fill=self.vehicle_colors[car['type']], outline="")
                canvas.create_text(w / 2, y + slot / 2 - 5,
                                text=f"{car['plate']} ({car['type']})",
                                fill="black", font=("Segoe UI", 18, "bold"))
            
    def update_ui(self):
        self.stats["Arrivals"].config(text=f"Arrivals: {self.total_arrivals}")
        self.stats["Departures"].config(text=f"Departures: {self.total_departures}")
        self.stats["Current Load"].config(
            text=f"Current Load: {len(self.main_queue)}/ {self.max_capacity}"
        )
        self.draw(self.canvas_main, self.main_queue)
        self.draw(self.canvas_temp, self.temp_queue)

#RUN

if __name__ == "__main__":
    root = tk.Tk()
    app = QueueParkingDashboard(root)
    root.mainloop()
