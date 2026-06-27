import os
import tkinter as tk
from tkinter import messagebox

# Import GUI modules with local-first fallbacks for direct script execution and package execution
try:
    from mft_first_fit_gui import TransparentMFTFirstFitSimulator
    from mft_best_fit_gui import TransparentMFTBestFitSimulator
    from mft_worst_fit_gui import TransparentMFTWorstFitSimulator
    from mvt_gui import MVTSimulatorGUI
except Exception:
    from operating_system_scheduling.memory_management.mft_first_fit_gui import TransparentMFTFirstFitSimulator
    from operating_system_scheduling.memory_management.mft_best_fit_gui import TransparentMFTBestFitSimulator
    from operating_system_scheduling.memory_management.mft_worst_fit_gui import TransparentMFTWorstFitSimulator
    from operating_system_scheduling.memory_management.mvt_gui import MVTSimulatorGUI

class MemoryManagementMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎯 OS Memory Management & Scheduling Suite")
        
        self.geometry("1920x1080")
        self.minsize(1200, 780)
        self.resizable(True, True)

        self.colors = {
            "bg_fallback": "#1d1233",
            "btn_mft": "#c084fc",
            "btn_mvt": "#38bdf8",
            "btn_sub": "#4c2d82"
        }
        self.configure(bg=self.colors["bg_fallback"])

        self.mvt_configs = {"scheduling": None, "allocation": None, "compaction": None}

        self.setup_background()
        self.show_root_menu()

    def setup_background(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            asset_candidates = [
                os.path.join(base_dir, "..", "..", "assets", "mm_bg_main.png"),
                os.path.join(base_dir, "..", "assets", "temp_bg.png"),
                os.path.join(base_dir, "assets", "temp_bg.png"),
                os.path.join(base_dir, "..", "..", "assets", "temp_bg.png"),
            ]

            for asset_path in asset_candidates:
                if os.path.exists(asset_path):
                    self.bg_image = tk.PhotoImage(file=r"C:\Users\Precious Nicole\Documents\assets\mm_bg_main.png")
                    self.bg_label = tk.Label(self, image=self.bg_image, bd=0)
                    self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                    return

            print("No background image found; using fallback color.")
        except Exception as e:
            print(f"Error loading background asset: {e}")

    def clear_container(self):
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        
        self.content_frame = tk.Frame(self, bg=self.colors["bg_fallback"], bd=0, highlightthickness=0)
        self.content_frame.place(relx=0.508, rely=0.65, anchor="center", width=750, height=445)


    def show_root_menu(self):
        self.clear_container()

        tk.Label(self.content_frame, text="🎛️ MEMORY MANAGEMENT MENU", font=("Comic Sans MS", 24, "bold"),
                 fg="#ffffff", bg=self.colors["bg_fallback"]).pack(pady=(20, 30))

        btn_mft = tk.Button(self.content_frame, text="📟 Fixed Partitioning (MFT)",
                            font=("Comic Sans MS", 16, "bold"), bg=self.colors["btn_mft"], fg="#ffffff",
                            activebackground="#a855f7", activeforeground="white", bd=0, cursor="hand2", width=34, pady=12,
                            command=self.show_mft_strategies)
        btn_mft.pack(pady=10)

        btn_mvt = tk.Button(self.content_frame, text="🚀 Variable Partitioning (MVT)",
                            font=("Comic Sans MS", 16, "bold"), bg=self.colors["btn_mvt"], fg="#ffffff",
                            activebackground="#0284c7", activeforeground="white", bd=0, cursor="hand2", width=34, pady=12,
                            command=self.show_mvt_scheduling_step)
        btn_mvt.pack(pady=12)

        tk.Button(self.content_frame, text="❌ Close Suite", font=("Comic Sans MS", 12, "bold"),
                  bg=self.colors["bg_fallback"], fg="#ef4444", bd=0, cursor="hand2", command=self.quit).pack(pady=(25, 0))

    def show_mft_strategies(self):
        self.clear_container()

        tk.Label(self.content_frame, text="📌 MFT STRATEGIES", font=("Comic Sans MS", 22, "bold"),
                 fg="#ffffff", bg=self.colors["bg_fallback"]).pack(pady=(20, 30))

        for label, strategy in [
            ("Best Fit", "best"),
            ("Worst Fit", "worst"),
            ("First Fit", "first")
        ]:
            tk.Button(
                self.content_frame,
                text=label,
                font=("Comic Sans MS", 16, "bold"),
                bg=self.colors["btn_sub"],
                fg="#ffffff",
                activebackground="#7c3aed",
                activeforeground="white",
                bd=0,
                cursor="hand2",
                width=32,
                pady=12,
                command=lambda s=strategy: self.show_mft_execution(s)
            ).pack(pady=10)

        tk.Button(self.content_frame, text="⬅️ Back", font=("Comic Sans MS", 12, "bold"),
                  bg=self.colors["bg_fallback"], fg="#f8fafc", bd=0, cursor="hand2",
                  command=self.show_root_menu).pack(pady=(20, 0))

    def show_mft_execution(self, strategy):
        names = {
            "best": "Best Fit",
            "worst": "Worst Fit",
            "first": "First Fit"
        }
        
       
        try:
            if strategy == "first":
                mft_gui = TransparentMFTFirstFitSimulator()
            elif strategy == "best":
                mft_gui = TransparentMFTBestFitSimulator()
            elif strategy == "worst":
                mft_gui = TransparentMFTWorstFitSimulator()
            else:
                messagebox.showerror("Error", f"Unknown strategy: {strategy}")
                self.show_mft_strategies()
                return
            
            mft_gui.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch MFT GUI: {str(e)}")
            self.show_mft_strategies()

    def show_mvt_scheduling_step(self):
        self.clear_container()

        tk.Label(self.content_frame, text="📌 MVT CPU SCHEDULING", font=("Comic Sans MS", 22, "bold"),
                 fg="#ffffff", bg=self.colors["bg_fallback"]).pack(pady=(20, 30))

        for label, algorithm in [
            ("FCFS", "fcfs"),
            ("SJF", "sjf"),
            ("Priority", "priority"),
            ("Round Robin", "round_robin")
        ]:
            tk.Button(
                self.content_frame,
                text=label,
                font=("Comic Sans MS", 16, "bold"),
                bg=self.colors["btn_sub"],
                fg="#ffffff",
                activebackground="#0ea5e9",
                activeforeground="white",
                bd=0,
                cursor="hand2",
                width=32,
                pady=12,
                command=lambda alg=algorithm: self.show_mvt_allocation_step(alg)
            ).pack(pady=10)

        tk.Button(self.content_frame, text="⬅️ Back", font=("Comic Sans MS", 12, "bold"),
                  bg=self.colors["bg_fallback"], fg="#f8fafc", bd=0, cursor="hand2",
                  command=self.show_root_menu).pack(pady=(20, 0))

    def show_mvt_allocation_step(self, scheduling):
        self.mvt_configs["scheduling"] = scheduling
        self.clear_container()

        scheduling_names = {
            "fcfs": "FCFS",
            "sjf": "SJF",
            "priority": "Priority",
            "round_robin": "Round Robin"
        }

        tk.Label(self.content_frame, text="📌 MVT MEMORY ALLOCATION", font=("Comic Sans MS", 22, "bold"),
                 fg="#ffffff", bg=self.colors["bg_fallback"]).pack(pady=(20, 30))

        tk.Label(self.content_frame,
                 text=f"Napili: {scheduling_names.get(scheduling, scheduling)} CPU Scheduling",
                 font=("Comic Sans MS", 16), fg="#e5e7eb", bg=self.colors["bg_fallback"]).pack(pady=(0, 20))

        for label, strategy in [
            ("Best Fit", "best"),
            ("First Fit", "first"),
            ("Worst Fit", "worst")
        ]:
            tk.Button(
                self.content_frame,
                text=label,
                font=("Comic Sans MS", 16, "bold"),
                bg=self.colors["btn_sub"],
                fg="#ffffff",
                activebackground="#7c3aed",
                activeforeground="white",
                bd=0,
                cursor="hand2",
                width=32,
                pady=12,
                command=lambda alloc=strategy: self.show_mvt_compaction_step(alloc)
            ).pack(pady=10)

        tk.Button(self.content_frame, text="⬅️ Back", font=("Comic Sans MS", 12, "bold"),
                  bg=self.colors["bg_fallback"], fg="#f8fafc", bd=0, cursor="hand2",
                  command=self.show_mvt_scheduling_step).pack(pady=(20, 0))

    def show_mvt_compaction_step(self, allocation):
        self.mvt_configs["allocation"] = allocation
        self.clear_container()

        aggregation_names = {
            "best": "Best Fit",
            "first": "First Fit",
            "worst": "Worst Fit"
        }

        tk.Label(self.content_frame, text="📌 MVT COMPACTION", font=("Comic Sans MS", 22, "bold"),
                 fg="#ffffff", bg=self.colors["bg_fallback"]).pack(pady=(20, 30))

        tk.Label(self.content_frame,
                 text=("Choose compaction after allocation. "
                       "Even if there's no actual memory move logic, this is the final flow step."),
                 font=("Comic Sans MS", 14), fg="#e5e7eb", bg=self.colors["bg_fallback"], justify="center",
                 wraplength=680).pack(pady=(0, 20))

        for label, value in [("With Compaction", True), ("Without Compaction", False)]:
            tk.Button(
                self.content_frame,
                text=label,
                font=("Comic Sans MS", 16, "bold"),
                bg=self.colors["btn_sub"],
                fg="#ffffff",
                activebackground="#0ea5e9" if value else "#f97316",
                activeforeground="white",
                bd=0,
                cursor="hand2",
                width=32,
                pady=12,
                command=lambda comp=value: self.show_mvt_summary(comp)
            ).pack(pady=10)

        tk.Button(self.content_frame, text="⬅️ Back", font=("Comic Sans MS", 12, "bold"),
                  bg=self.colors["bg_fallback"], fg="#f8fafc", bd=0, cursor="hand2",
                  command=lambda: self.show_mvt_allocation_step(self.mvt_configs["scheduling"]) ).pack(pady=(20, 0))

    def show_mvt_summary(self, compaction):
        self.mvt_configs["compaction"] = compaction
        schedule_names = {
            "fcfs": "FCFS",
            "sjf": "SJF",
            "priority": "Priority",
            "round_robin": "Round Robin"
        }
        allocation_names = {
            "best": "Best Fit",
            "first": "First Fit",
            "worst": "Worst Fit"
        }

        self.clear_container()
        tk.Label(self.content_frame, text="✅ MVT CONFIGURATION SUMMARY", font=("Comic Sans MS", 22, "bold"),
                 fg="#ffffff", bg=self.colors["bg_fallback"]).pack(pady=(20, 25))

        tk.Label(self.content_frame,
                 text=(f"CPU Scheduling: {schedule_names.get(self.mvt_configs['scheduling'], 'Unknown')}\n"
                       f"Memory Allocation: {allocation_names.get(self.mvt_configs['allocation'], 'Unknown')}\n"
                       f"Compaction: {'Yes' if compaction else 'No'}"),
                 font=("Comic Sans MS", 16), fg="#e5e7eb", bg=self.colors["bg_fallback"], justify="center",
                 wraplength=680).pack(pady=(0, 25))

        tk.Button(self.content_frame, text="Run MVT Simulation", font=("Comic Sans MS", 14, "bold"),
                  bg="#34d399", fg="#0f172a", activebackground="#059669", activeforeground="#ffffff",
                  bd=0, cursor="hand2", width=24, pady=10,
                  command=lambda: self._launch_mvt_simulator()
                 ).pack(pady=12)

        tk.Button(self.content_frame, text="⬅️ Start Over", font=("Comic Sans MS", 12, "bold"),
                  bg=self.colors["bg_fallback"], fg="#f8fafc", bd=0, cursor="hand2",
                  command=self.show_root_menu).pack(pady=(15, 0))
    
    def _launch_mvt_simulator(self):
        """Launch the MVT simulator with configured options"""
        try:
            mvt_gui = MVTSimulatorGUI(
                scheduling=self.mvt_configs['scheduling'],
                allocation=self.mvt_configs['allocation'],
                compaction=self.mvt_configs['compaction']
            )
            mvt_gui.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch MVT simulator: {str(e)}")
        
if __name__ == "__main__":
    app = MemoryManagementMenu()
    app.mainloop()
