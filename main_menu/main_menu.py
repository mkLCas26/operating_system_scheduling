import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def open_cpu_scheduling():
    messagebox.showinfo("CPU Scheduling", "CPU Scheduling module opened.")

def open_disk_management():
    messagebox.showinfo("Disk Management", "Disk Management module opened.")

def open_memory_management():
    messagebox.showinfo("Memory Management", "Memory Management module opened.")

def open_virtual_memory():
    messagebox.showinfo("Virtual Memory", "Virtual Memory module opened.")

root = tk.Tk()
root.title("Operating System Scheduling")  
root.geometry("1024x576")
root.resizable(False, False)

try:
    bg_image = Image.open(r"C:\Users\Precious Nicole\Documents\OS\operating_system_scheduling\main_menu\purple.jpg")
    bg_image = bg_image.resize((1024, 576), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=1024, height=576)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

except FileNotFoundError:
   print("Background image not found. Continuing without background.")

   canvas = tk.Canvas(root, width=1024, height=576, bg="lightblue")
   canvas.pack(fill="both", expand=True)

canvas.create_rectangle(390, 220, 634, 450, fill="#b5c4ba", outline="#ffffff", width=2) 
canvas.create_rectangle(390, 220, 634, 245, fill="#8ba094", outline="#ffffff", width=2)

canvas.create_rectangle(396, 226, 406, 236, fill="#b5c4ba", outline="#ffffff")
canvas.create_rectangle(618, 226, 628, 236, fill="#b5c4ba", outline="#ffffff")

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

btn_cpu = tk.Button(root, text="💻 CPU SCHEDULING", command=open_cpu_scheduling, **button_config)
btn_disk = tk.Button(root, text="💾 DISK MANAGEMENT", command=open_disk_management, **button_config)
btn_mem = tk.Button(root, text="📟 MEMORY MANAGEMENT", command=open_memory_management, **button_config)
btn_vmem = tk.Button(root, text="📁 VIRTUAL MEMORY", command=open_virtual_memory, **button_config)

canvas.create_window(512, 275, window=btn_cpu)
canvas.create_window(512, 320, window=btn_disk)
canvas.create_window(512, 365, window=btn_mem)
canvas.create_window(512, 410, window=btn_vmem)

canvas.create_rectangle(390, 490, 634, 530, fill="#1c1135", outline="#9c84cf", width=1)
canvas.create_text(
    512, 510, 
    text="SIMULATOR ACTIVE\nSelect an Option to Begin", 
    font=("Courier New", 9), 
    fill="#ebd15b", 
    justify="center"
)
root.mainloop()