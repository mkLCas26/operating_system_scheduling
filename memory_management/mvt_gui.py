import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random

# Import MVTSimulator with local-first fallback for direct execution
try:
    from mvt_process import MVTSimulator
except Exception:
    from operating_system_scheduling.memory_management.mvt_process import MVTSimulator


class MVTSimulatorGUI(tk.Tk):
    def __init__(self, scheduling="fcfs", allocation="first", compaction=False):
        super().__init__()
        self.title("🚀 MVT (Multiple Variable Partitioning) Simulator")
        self.geometry("1920x1080")
        self.resizable(True, True)
        
        self.scheduling = scheduling
        self.allocation = allocation
        self.compaction = compaction
        self.simulator = None
        self.report = None
        
        # Color scheme
        self.colors = {
            "bg": "#0f172a",
            "secondary_bg": "#1e293b",
            "accent": "#0ea5e9",
            "success": "#34d399",
            "warning": "#fbbf24",
            "danger": "#f87171",
            "text": "#f1f5f9"
        }
        
        self.configure(bg=self.colors["bg"])
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self, bg=self.colors["bg"])
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(main_frame, bg=self.colors["secondary_bg"])
        header.pack(fill="x", pady=(0, 10))
        
        title_label = tk.Label(
            header,
            text="🚀 MVT Simulator - Multiple Variable Partitioning",
            font=("Arial", 20, "bold"),
            bg=self.colors["secondary_bg"],
            fg=self.colors["accent"]
        )
        title_label.pack(pady=10, padx=10)
        
        config_text = f"CPU: {self.scheduling.upper()} | Allocation: {self.allocation.upper()} | Compaction: {'ON' if self.compaction else 'OFF'}"
        config_label = tk.Label(
            header,
            text=config_text,
            font=("Arial", 12),
            bg=self.colors["secondary_bg"],
            fg=self.colors["text"]
        )
        config_label.pack(pady=(0, 10), padx=10)
        
        # Content area
        content = tk.Frame(main_frame, bg=self.colors["bg"])
        content.pack(fill="both", expand=True)
        
        # Left panel - Input/Control
        left_panel = tk.Frame(content, bg=self.colors["secondary_bg"], width=350)
        left_panel.pack(side="left", fill="both", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self._setup_input_panel(left_panel)
        
        # Right panel - Output/Results
        right_panel = tk.Frame(content, bg=self.colors["secondary_bg"])
        right_panel.pack(side="right", fill="both", expand=True)
        
        self._setup_output_panel(right_panel)
    
    def _setup_input_panel(self, parent):
        """Setup input configuration panel"""
        title = tk.Label(
            parent,
            text="📊 Configuration",
            font=("Arial", 14, "bold"),
            bg=self.colors["secondary_bg"],
            fg=self.colors["accent"]
        )
        title.pack(pady=10, padx=10)
        
        # Total Memory
        tk.Label(parent, text="Total Memory (KB):", bg=self.colors["secondary_bg"], fg=self.colors["text"]).pack(anchor="w", padx=10, pady=(10, 0))
        self.memory_var = tk.StringVar(value="1024")
        memory_entry = tk.Entry(parent, textvariable=self.memory_var, font=("Arial", 11))
        memory_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Number of Processes
        tk.Label(parent, text="Number of Processes:", bg=self.colors["secondary_bg"], fg=self.colors["text"]).pack(anchor="w", padx=10, pady=(10, 0))
        self.num_processes_var = tk.StringVar(value="5")
        num_entry = tk.Entry(parent, textvariable=self.num_processes_var, font=("Arial", 11))
        num_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Time Limit
        tk.Label(parent, text="Simulation Time Limit:", bg=self.colors["secondary_bg"], fg=self.colors["text"]).pack(anchor="w", padx=10, pady=(10, 0))
        self.time_limit_var = tk.StringVar(value="100")
        time_entry = tk.Entry(parent, textvariable=self.time_limit_var, font=("Arial", 11))
        time_entry.pack(fill="x", padx=10, pady=(0, 15))
        
        # Separator
        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10, pady=10)
        
        # Buttons
        btn_run = tk.Button(
            parent,
            text="▶️  Run Simulation",
            font=("Arial", 12, "bold"),
            bg=self.colors["success"],
            fg="#0f172a",
            command=self._run_simulation,
            cursor="hand2"
        )
        btn_run.pack(fill="x", padx=10, pady=5)
        
        btn_reset = tk.Button(
            parent,
            text="🔄 Reset",
            font=("Arial", 11),
            bg=self.colors["warning"],
            fg="#0f172a",
            command=self._reset,
            cursor="hand2"
        )
        btn_reset.pack(fill="x", padx=10, pady=5)
        
        btn_export = tk.Button(
            parent,
            text="💾 Export Report",
            font=("Arial", 11),
            bg=self.colors["accent"],
            fg="#0f172a",
            command=self._export_report,
            cursor="hand2"
        )
        btn_export.pack(fill="x", padx=10, pady=(5, 15))
        
        # Separator
        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10, pady=10)
        
        # Process Info
        info_label = tk.Label(
            parent,
            text="📋 Process Details",
            font=("Arial", 12, "bold"),
            bg=self.colors["secondary_bg"],
            fg=self.colors["accent"]
        )
        info_label.pack(pady=10, padx=10)
        
        self.process_info_text = scrolledtext.ScrolledText(
            parent,
            height=15,
            font=("Arial", 9),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"]
        )
        self.process_info_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def _setup_output_panel(self, parent):
        """Setup output/results panel"""
        # Tabs for different views
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)
        
        # Style tabs
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", padding=[20, 10], font=("Arial", 11))
        
        # Tab 1: Summary
        summary_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(summary_frame, text="📊 Summary")
        self._setup_summary_tab(summary_frame)
        
        # Tab 2: Memory Layout
        memory_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(memory_frame, text="💾 Memory Layout")
        self._setup_memory_tab(memory_frame)
        
        # Tab 3: Execution Log
        log_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(log_frame, text="📝 Execution Log")
        self._setup_log_tab(log_frame)
        
        # Tab 4: Statistics
        stats_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(stats_frame, text="📈 Statistics")
        self._setup_stats_tab(stats_frame)
    
    def _setup_summary_tab(self, parent):
        """Setup summary results tab"""
        self.summary_text = scrolledtext.ScrolledText(
            parent,
            font=("Courier New", 10),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"]
        )
        self.summary_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.summary_text.config(state="disabled")
    
    def _setup_memory_tab(self, parent):
        """Setup memory layout tab"""
        self.memory_canvas = tk.Canvas(
            parent,
            bg=self.colors["bg"],
            highlightthickness=0
        )
        self.memory_canvas.pack(fill="both", expand=True, padx=10, pady=10)
    
    def _setup_log_tab(self, parent):
        """Setup execution log tab"""
        self.log_text = scrolledtext.ScrolledText(
            parent,
            font=("Courier New", 9),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"]
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_text.config(state="disabled")
    
    def _setup_stats_tab(self, parent):
        """Setup statistics tab"""
        self.stats_text = scrolledtext.ScrolledText(
            parent,
            font=("Courier New", 10),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["accent"]
        )
        self.stats_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.stats_text.config(state="disabled")
    
    def _run_simulation(self):
        """Run the MVT simulation"""
        try:
            total_memory = int(self.memory_var.get())
            num_processes = int(self.num_processes_var.get())
            time_limit = int(self.time_limit_var.get())
            
            if total_memory <= 0 or num_processes <= 0 or time_limit <= 0:
                messagebox.showerror("Error", "All values must be positive")
                return
            
            # Create simulator
            self.simulator = MVTSimulator(
                total_memory=total_memory,
                cpu_scheduling=self.scheduling,
                allocation_strategy=self.allocation,
                enable_compaction=self.compaction
            )
            
            # Generate random processes
            process_info = "Generated Processes:\n" + "="*40 + "\n"
            for i in range(num_processes):
                pid = f"P{i+1}"
                arrival = random.randint(0, time_limit // 3)
                burst = random.randint(5, 20)
                memory = random.randint(50, 300)
                priority = random.randint(1, 5) if self.scheduling == "priority" else 0
                
                self.simulator.add_process(pid, arrival, burst, memory, priority)
                process_info += f"{pid}: Arrival={arrival}, Burst={burst}, Memory={memory}KB, Priority={priority}\n"
            
            self.process_info_text.config(state="normal")
            self.process_info_text.delete(1.0, tk.END)
            self.process_info_text.insert(tk.END, process_info)
            self.process_info_text.config(state="disabled")
            
            # Run simulation
            self.report = self.simulator.simulate(time_limit)
            
            # Display results
            self._display_results()
            
            messagebox.showinfo("Success", "Simulation completed successfully!")
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def _display_results(self):
        """Display simulation results"""
        if not self.report:
            return
        
        # Summary tab
        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║          MVT SIMULATION RESULTS - DETAILED SUMMARY             ║
╚════════════════════════════════════════════════════════════════╝

📋 CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CPU Scheduling Algorithm:    {self.report['scheduling_algorithm']}
  Memory Allocation Strategy:   {self.report['allocation_strategy']}
  Compaction Enabled:           {'✅ YES' if self.report['compaction_enabled'] else '❌ NO'}
  Total Memory:                 {self.report['total_memory']}KB

📊 PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Processes:              {self.report['processes_completed']}
  Average Turnaround Time:      {self.report['avg_turnaround_time']} units
  Average Waiting Time:         {self.report['avg_waiting_time']} units
  Context Switches:             {self.report['context_switches']}

💾 MEMORY STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Internal Fragmentation: {self.report['total_internal_fragmentation']}KB
  Total External Fragmentation: {self.report['total_external_fragmentation']}KB
  Memory Blocks:                {len(self.report['memory_blocks'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Process details
        summary += "\n✅ COMPLETED PROCESSES DETAILS\n" + "━"*70 + "\n"
        summary += f"{'PID':<6} {'Arrival':<8} {'Burst':<8} {'Start':<8} {'End':<8} {'TAT':<8} {'WT':<8}\n"
        summary += "━"*70 + "\n"
        
        for proc in self.report['completed_processes']:
            tat = proc['turnaround_time'] if proc['turnaround_time'] else "N/A"
            wt = proc['waiting_time'] if proc['waiting_time'] else "N/A"
            summary += f"{proc['pid']:<6} {proc['arrival_time']:<8} {proc['burst_time']:<8} {str(proc['start_time']):<8} {str(proc['end_time']):<8} {str(tat):<8} {str(wt):<8}\n"
        
        self.summary_text.config(state="normal")
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state="disabled")
        
        # Memory layout
        self._display_memory_layout()
        
        # Execution log
        log_text = "\n".join(self.report['execution_log'])
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, log_text)
        self.log_text.config(state="disabled")
        
        # Statistics
        self._display_statistics()
    
    def _display_memory_layout(self):
        """Display memory layout visualization"""
        self.memory_canvas.delete("all")
        
        if not self.report:
            return
        
        blocks = self.report['memory_blocks']
        total_memory = self.report['total_memory']
        
        canvas_width = 900
        canvas_height = 400
        margin = 50
        block_height = 60
        
        # Draw memory blocks
        colors = {
            "allocated": "#34d399",
            "free": "#94a3b8",
            "fragmented": "#f97316"
        }
        
        y_pos = margin
        for block in blocks:
            x_start = margin + (block['start'] / total_memory) * (canvas_width - 2*margin)
            x_end = margin + (block['end'] / total_memory) * (canvas_width - 2*margin)
            
            color = colors['allocated'] if not block['is_free'] else colors['free']
            
            # Draw block
            self.memory_canvas.create_rectangle(
                x_start, y_pos, x_end, y_pos + block_height,
                fill=color, outline="white", width=2
            )
            
            # Label
            label = f"{block['block_id']}\n{block['size']}KB"
            if block['allocated_process']:
                label += f"\n{block['allocated_process']}"
            
            self.memory_canvas.create_text(
                (x_start + x_end) / 2, y_pos + block_height / 2,
                text=label, fill="#0f172a", font=("Arial", 9, "bold")
            )
            
            y_pos += block_height + 10
        
        # Legend
        legend_y = y_pos + 20
        self.memory_canvas.create_rectangle(margin, legend_y, margin+30, legend_y+30, fill=colors['allocated'], outline="white")
        self.memory_canvas.create_text(margin+50, legend_y+15, text="Allocated", anchor="w", fill=self.colors["text"], font=("Arial", 10))
        
        self.memory_canvas.create_rectangle(margin+200, legend_y, margin+230, legend_y+30, fill=colors['free'], outline="white")
        self.memory_canvas.create_text(margin+250, legend_y+15, text="Free", anchor="w", fill=self.colors["text"], font=("Arial", 10))
    
    def _display_statistics(self):
        """Display detailed statistics"""
        stats = f"""
╔════════════════════════════════════════════════════════════════╗
║                    DETAILED STATISTICS                         ║
╚════════════════════════════════════════════════════════════════╝

🔄 CPU SCHEDULING ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Algorithm Used:               {self.report['scheduling_algorithm']}
  Context Switches:             {self.report['context_switches']}
  Average Turnaround Time:      {self.report['avg_turnaround_time']} units
  Average Waiting Time:         {self.report['avg_waiting_time']} units

💾 MEMORY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Allocation Strategy:          {self.report['allocation_strategy']}
  Compaction:                   {'ENABLED' if self.report['compaction_enabled'] else 'DISABLED'}
  Total Memory Available:       {self.report['total_memory']}KB
  Total Internal Fragmentation: {self.report['total_internal_fragmentation']}KB
  Total External Fragmentation: {self.report['total_external_fragmentation']}KB
  
  Fragmentation Ratio:
    Internal:                   {round(self.report['total_internal_fragmentation']/self.report['total_memory']*100, 2)}%
    External:                   {round(self.report['total_external_fragmentation']/self.report['total_memory']*100, 2)}%

📦 MEMORY BLOCKS FINAL STATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for block in self.report['memory_blocks']:
            stats += f"""
  Block ID:                     {block['block_id']}
    Start Address:              {block['start']}KB
    End Address:                {block['end']}KB
    Size:                       {block['size']}KB
    Status:                     {'FREE' if block['is_free'] else 'ALLOCATED'}
    Allocated Process:          {block['allocated_process'] if block['allocated_process'] else 'N/A'}
    Internal Fragmentation:     {block['internal_frag']}KB
"""
        
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)
        self.stats_text.config(state="disabled")
    
    def _reset(self):
        """Reset the simulator"""
        self.simulator = None
        self.report = None
        
        self.summary_text.config(state="normal")
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.config(state="disabled")
        
        self.memory_canvas.delete("all")
        
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.config(state="disabled")
        
        self.process_info_text.config(state="normal")
        self.process_info_text.delete(1.0, tk.END)
        self.process_info_text.config(state="disabled")
    
    def _export_report(self):
        """Export the report to a file"""
        if not self.report:
            messagebox.showwarning("Warning", "Run simulation first")
            return
        
        try:
            filename = f"mvt_report_{self.scheduling}_{self.allocation}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"MVT SIMULATION REPORT\n")
                f.write(f"{'='*70}\n\n")
                f.write(f"Configuration:\n")
                f.write(f"  CPU Scheduling: {self.report['scheduling_algorithm']}\n")
                f.write(f"  Memory Allocation: {self.report['allocation_strategy']}\n")
                f.write(f"  Compaction: {'YES' if self.report['compaction_enabled'] else 'NO'}\n\n")
                
                f.write(f"Performance Metrics:\n")
                f.write(f"  Avg Turnaround Time: {self.report['avg_turnaround_time']}\n")
                f.write(f"  Avg Waiting Time: {self.report['avg_waiting_time']}\n")
                f.write(f"  Context Switches: {self.report['context_switches']}\n\n")
                
                f.write(f"Memory Statistics:\n")
                f.write(f"  Internal Fragmentation: {self.report['total_internal_fragmentation']}KB\n")
                f.write(f"  External Fragmentation: {self.report['total_external_fragmentation']}KB\n\n")
                
                f.write(f"Execution Log:\n")
                for entry in self.report['execution_log']:
                    f.write(f"  {entry}\n")
            
            messagebox.showinfo("Success", f"Report exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")


if __name__ == "__main__":
    app = MVTSimulatorGUI(scheduling="fcfs", allocation="first", compaction=False)
    app.mainloop()
