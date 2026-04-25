import matplotlib.pyplot as plt


def draw_gantt_chart(gantt):
    if not gantt:
        return

    # Extract unique PIDs in the order they appear
    unique_pids = []
    for task in gantt:
        if task["pid"] not in unique_pids:
            unique_pids.append(task["pid"])
            
    # Reverse so the first process is at the top of the chart
    unique_pids.reverse()

    fig, gnt = plt.subplots(figsize=(10, 5))
    gnt.set_title("Gantt Chart")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Processes")

    # Set y-ticks based on unique processes
    y_ticks = [10 * (i + 1) for i in range(len(unique_pids))]
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels(unique_pids)
    gnt.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Map PID to Y-coordinate
    pid_to_y = {pid: 10 * (i + 1) for i, pid in enumerate(unique_pids)}

    # Distinct colors for processes
    colors = plt.cm.tab10.colors
    pid_to_color = {pid: colors[i % len(colors)] for i, pid in enumerate(unique_pids)}

    for task in gantt:
        pid = task["pid"]
        start = task["start"]
        end = task["end"]
        duration = end - start
        
        y_center = pid_to_y[pid]
        
        gnt.broken_barh(
            [(start, duration)],
            (y_center - 3, 6),
            facecolors=pid_to_color[pid],
            edgecolor='black'
        )
        # Add text annotation inside the bar
        if duration > 0:
            gnt.text(start + duration / 2, y_center, f"{pid}", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
            
    # Improve x-axis limits
    max_time = max(task["end"] for task in gantt)
    gnt.set_xlim(0, max_time + max(1, max_time * 0.05))

    fig.tight_layout()
    plt.show()


def calculate_averages(processes):
    if not processes:
        return 0.0, 0.0

    total_wt = sum(p["waiting"] for p in processes)
    total_tat = sum(p["turnaround"] for p in processes)
    n = len(processes)
    return total_wt / n, total_tat / n

