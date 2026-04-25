# Process Scheduler Simulator

A desktop GUI application that simulates classic CPU scheduling algorithms with real-time **Gantt Chart** visualization. Built with Python, Tkinter, and Matplotlib.

---

## Features

- **4 Scheduling Algorithms** — FCFS, SJF (Non-Preemptive), Priority (Non-Preemptive), and Round Robin
- **Interactive GUI** — Add, remove, and manage processes through a clean Tkinter interface
- **Gantt Chart Visualization** — Color-coded per-process chart rendered with Matplotlib
- **Performance Metrics** — Per-process Waiting Time and Turnaround Time with averages
- **Input Validation** — Graceful error handling for all fields (arrival, burst, priority, quantum)
- **Dynamic Controls** — Time Quantum field enables only for Round Robin; Priority field enables only for Priority scheduling

---

## Project Structure

```
process-scheduler/
│
├── main.py           # Entry point — launches the GUI
├── gui.py            # Tkinter GUI layout and event logic
├── algorithms.py     # Scheduling algorithm implementations (FCFS, SJF, Priority, RR)
└── utils.py          # Gantt chart drawing and average calculation helpers
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- `matplotlib` library

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/process-scheduler.git
cd process-scheduler

# Install dependencies
pip install matplotlib
```

### Running the App

```bash
python main.py
```

---

## Algorithms

| Algorithm | Description | Preemptive |
|-----------|-------------|------------|
| **FCFS** | First Come First Served — processes run in arrival order | ❌ |
| **SJF** | Shortest Job First — shortest burst time runs next | ❌ |
| **Priority** | Lower priority number = higher precedence | ❌ |
| **Round Robin** | Each process gets a fixed time quantum in a cyclic queue | ✅ |

> **Note:** In Priority Scheduling, a lower number means *higher* priority (e.g., Priority 1 runs before Priority 5).

---

## How to Use

1. **Add Processes** — Fill in PID, Arrival Time, and Burst Time. Priority is required only for Priority Scheduling.
2. **Select Algorithm** — Choose from the dropdown. For Round Robin, set a Time Quantum > 0.
3. **Run Scheduler** — Click *Run Scheduler* to view the Gantt chart and results window.
4. **View Results** — A results window shows per-process Waiting and Turnaround Times alongside averages.

---

## Metrics

- **Waiting Time** = Turnaround Time − Burst Time
- **Turnaround Time** = Completion Time − Arrival Time
- **Average Waiting Time** and **Average Turnaround Time** are displayed after each simulation run.

---

## Built With

- [Python](https://www.python.org/) — Core language
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework (standard library)
- [Matplotlib](https://matplotlib.org/) — Gantt chart rendering

---

## 📄 License

This project is free to use — anyone can download, run, and build on it.
  
