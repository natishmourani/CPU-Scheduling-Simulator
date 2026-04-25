import tkinter as tk
from tkinter import messagebox, ttk
from algorithms import fcfs, sjf, priority_scheduling, round_robin
from utils import draw_gantt_chart, calculate_averages

def launch_gui():
    def clear_inputs():
        for entry in (entry_pid, entry_arrival, entry_burst, entry_priority):
            entry.delete(0, tk.END)

    def add_process():
        pid = entry_pid.get().strip()
        if not pid:
            messagebox.showerror("Invalid input", "PID must be non-empty.")
            return
            
        if any(p["pid"] == pid for p in process_list):
            messagebox.showerror("Invalid input", f"Process with PID '{pid}' already exists.")
            return

        arrival_str = entry_arrival.get().strip()
        if not arrival_str:
            messagebox.showerror("Invalid input", "Arrival Time is missing.")
            return
        try:
            arrival = int(arrival_str)
            if arrival < 0:
                messagebox.showerror("Invalid input", "Arrival Time must be >= 0.")
                return
        except ValueError:
            messagebox.showerror("Invalid input", "Arrival Time must be an integer.")
            return

        burst_str = entry_burst.get().strip()
        if not burst_str:
            messagebox.showerror("Invalid input", "Burst Time is missing.")
            return
        try:
            burst = int(burst_str)
            if burst <= 0:
                messagebox.showerror("Invalid input", "Burst Time must be > 0.")
                return
        except ValueError:
            messagebox.showerror("Invalid input", "Burst Time must be an integer.")
            return

        priority = 0
        display_priority = "-"
        if algo_var.get() == "Priority":
            priority_str = entry_priority.get().strip()
            if not priority_str:
                messagebox.showerror("Invalid input", "Priority is missing.")
                return
            try:
                priority = int(priority_str)
                if priority < 0:
                    messagebox.showerror("Invalid input", "Priority must be >= 0.")
                    return
            except ValueError:
                messagebox.showerror("Invalid input", "Priority must be an integer.")
                return
            display_priority = priority

        process_list.append({"pid": pid, "arrival": arrival, "burst": burst, "priority": priority})
        tree.insert("", tk.END, values=(pid, arrival, burst, display_priority))
        clear_inputs()

    def remove_process():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a process to remove.")
            return
            
        for item in selected_items:
            values = tree.item(item, 'values')
            pid_to_remove = str(values[0])
            process_list[:] = [p for p in process_list if p["pid"] != pid_to_remove]
            tree.delete(item)

    def clear_all():
        if not process_list:
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all processes?"):
            process_list.clear()
            for item in tree.get_children():
                tree.delete(item)

    def on_algo_change(event=None):
        selected = algo_var.get()
        if selected == "Round Robin":
            entry_quantum.state(['!disabled'])
        else:
            entry_quantum.state(['disabled'])
            
        if selected == "Priority":
            entry_priority.state(['!disabled'])
            for i, item in enumerate(tree.get_children()):
                p = process_list[i]
                tree.item(item, values=(p["pid"], p["arrival"], p["burst"], p["priority"]))
        else:
            entry_priority.state(['disabled'])
            for i, item in enumerate(tree.get_children()):
                p = process_list[i]
                tree.item(item, values=(p["pid"], p["arrival"], p["burst"], "-"))

    def run_algorithm():
        selected = algo_var.get()
        if not process_list:
            messagebox.showerror("Error", "Please add at least one process.")
            return

        updated = []
        if selected == "FCFS":
            gantt, updated = fcfs(process_list.copy())
        elif selected == "SJF":
            gantt, updated = sjf(process_list.copy())
        elif selected == "Priority":
            gantt, updated = priority_scheduling(process_list.copy())
        elif selected == "Round Robin":
            try:
                q = int(quantum_var.get())
                if q <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid input", "Enter a positive integer for time quantum.")
                return
            gantt, updated = round_robin(process_list.copy(), q)
        else:
            messagebox.showerror("Error", "Please select a scheduling algorithm.")
            return

        draw_gantt_chart(gantt)
        avg_wt, avg_tat = calculate_averages(updated)
        
        # Display results in a new window
        result_window = tk.Toplevel(root)
        result_window.title("Scheduling Results")
        result_window.geometry("500x350")
        
        result_tree = ttk.Treeview(result_window, columns=("PID", "Waiting", "Turnaround"), show='headings')
        result_tree.heading("PID", text="PID")
        result_tree.heading("Waiting", text="Waiting Time")
        result_tree.heading("Turnaround", text="Turnaround Time")
        
        result_tree.column("PID", width=100, anchor=tk.CENTER)
        result_tree.column("Waiting", width=150, anchor=tk.CENTER)
        result_tree.column("Turnaround", width=150, anchor=tk.CENTER)
        
        for p in updated:
            result_tree.insert("", tk.END, values=(p['pid'], p['waiting'], p['turnaround']))
            
        result_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        avg_label = tk.Label(result_window, text=f"Average Waiting Time: {avg_wt:.2f}\nAverage Turnaround Time: {avg_tat:.2f}", font=('Arial', 12, 'bold'))
        avg_label.pack(pady=10)

    root = tk.Tk()
    root.title("Process Scheduler Simulator")
    root.geometry("650x550")
    
    # Apply a theme if available
    style = ttk.Style(root)
    if 'clam' in style.theme_names():
        style.theme_use('clam')

    process_list = []

    # --- Input Frame ---
    input_frame = ttk.LabelFrame(root, text="Add New Process", padding=(10, 10))
    input_frame.pack(fill=tk.X, padx=10, pady=10)

    ttk.Label(input_frame, text="PID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    entry_pid = ttk.Entry(input_frame, width=10)
    entry_pid.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    entry_arrival = ttk.Entry(input_frame, width=10)
    entry_arrival.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(input_frame, text="Burst Time:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
    entry_burst = ttk.Entry(input_frame, width=10)
    entry_burst.grid(row=0, column=5, padx=5, pady=5)

    ttk.Label(input_frame, text="Priority:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    entry_priority = ttk.Entry(input_frame, width=10)
    entry_priority.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Button(input_frame, text="Add Process", command=add_process).grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky=tk.EW)

    # --- Process List Frame ---
    list_frame = ttk.LabelFrame(root, text="Process List", padding=(10, 10))
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    columns = ("PID", "Arrival", "Burst", "Priority")
    tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    btn_frame = ttk.Frame(root)
    btn_frame.pack(fill=tk.X, padx=10, pady=5)
    ttk.Button(btn_frame, text="Remove Selected", command=remove_process).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Clear All", command=clear_all).pack(side=tk.LEFT, padx=5)

    # --- Control Frame ---
    control_frame = ttk.LabelFrame(root, text="Simulation Controls", padding=(10, 10))
    control_frame.pack(fill=tk.X, padx=10, pady=10)

    ttk.Label(control_frame, text="Select Algorithm:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    algo_var = tk.StringVar(value="FCFS")
    algo_menu = ttk.Combobox(control_frame, textvariable=algo_var, values=["FCFS", "SJF", "Priority", "Round Robin"], state="readonly")
    algo_menu.grid(row=0, column=1, padx=5, pady=5)
    algo_menu.bind("<<ComboboxSelected>>", on_algo_change)

    ttk.Label(control_frame, text="Time Quantum:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    quantum_var = tk.StringVar()
    entry_quantum = ttk.Entry(control_frame, textvariable=quantum_var, width=10)
    entry_quantum.grid(row=0, column=3, padx=5, pady=5)

    on_algo_change()

    ttk.Button(control_frame, text="Run Scheduler", command=run_algorithm).grid(row=0, column=4, padx=20, pady=5)

    root.mainloop()

