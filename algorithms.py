from collections import deque


def _prepare_processes(processes):
    return sorted((process.copy() for process in processes), key=lambda item: item["arrival"])


def _finalize_process(process, end_time):
    process["turnaround"] = end_time - process["arrival"]
    process["waiting"] = process["turnaround"] - process["burst"]


def round_robin(processes, quantum):
    if quantum <= 0:
        raise ValueError("Quantum must be greater than 0.")

    processes_copy = _prepare_processes(processes)
    if not processes_copy:
        return [], []

    time = 0
    gantt = []
    ready_queue = deque()
    completed = []
    remaining_burst = {p["pid"]: p["burst"] for p in processes_copy}
    process_index = 0

    while len(completed) < len(processes_copy):
        while process_index < len(processes_copy) and processes_copy[process_index]["arrival"] <= time:
            ready_queue.append(processes_copy[process_index])
            process_index += 1

        if not ready_queue:
            if process_index >= len(processes_copy):
                break
            time = processes_copy[process_index]["arrival"]
            continue

        current_process = ready_queue.popleft()
        pid = current_process["pid"]
        start_time = time

        execution_time = min(quantum, remaining_burst[pid])
        time += execution_time
        remaining_burst[pid] -= execution_time

        gantt.append({"pid": pid, "start": start_time, "end": time})

        while process_index < len(processes_copy) and processes_copy[process_index]["arrival"] <= time:
            ready_queue.append(processes_copy[process_index])
            process_index += 1

        if remaining_burst[pid] == 0:
            _finalize_process(current_process, time)
            completed.append(current_process)
        else:
            ready_queue.append(current_process)

    return gantt, completed

# Test function to demonstrate all scheduling algorithms
def test_scheduling_algorithms():
    # Sample processes: [pid, arrival_time, burst_time, priority]
    test_processes = [
        {'pid': 'P1', 'arrival': 0, 'burst': 10, 'priority': 3},
        {'pid': 'P2', 'arrival': 0, 'burst': 1, 'priority': 1},
        {'pid': 'P3', 'arrival': 0, 'burst': 2, 'priority': 4},
        {'pid': 'P4', 'arrival': 0, 'burst': 1, 'priority': 5},
        {'pid': 'P5', 'arrival': 0, 'burst': 5, 'priority': 2}
    ]
    
    print("Original Processes:")
    for p in test_processes:
        print(f"PID: {p['pid']}, Arrival: {p['arrival']}, Burst: {p['burst']}, Priority: {p['priority']}")
    
    print("\n" + "="*50)
    print("ROUND ROBIN (Quantum = 2)")
    print("="*50)
    
    # Test Round Robin
    rr_processes = [p.copy() for p in test_processes]  # Create copy for testing
    gantt_rr, completed_rr = round_robin(rr_processes, 2)
    
    print("\nGantt Chart:")
    for entry in gantt_rr:
        print(f"PID: {entry['pid']}, Start: {entry['start']}, End: {entry['end']}")
    
    print("\nProcess Details:")
    total_waiting = 0
    total_turnaround = 0
    for p in completed_rr:
        print(f"PID: {p['pid']}, Waiting Time: {p['waiting']}, Turnaround Time: {p['turnaround']}")
        total_waiting += p['waiting']
        total_turnaround += p['turnaround']
    
    print(f"\nAverage Waiting Time: {total_waiting / len(completed_rr):.2f}")
    print(f"Average Turnaround Time: {total_turnaround / len(completed_rr):.2f}")

# Your other scheduling algorithms (fixed versions)
def fcfs(processes):
    processes_copy = _prepare_processes(processes)
    time = 0
    gantt = []

    for p in processes_copy:
        start = max(time, p["arrival"])
        end = start + p["burst"]
        gantt.append({"pid": p["pid"], "start": start, "end": end})
        _finalize_process(p, end)
        time = end

    return gantt, processes_copy


def sjf(processes):
    processes_copy = sorted(
        (process.copy() for process in processes),
        key=lambda item: (item["arrival"], item["burst"]),
    )
    time = 0
    gantt = []
    completed = []

    while processes_copy:
        available = [p for p in processes_copy if p["arrival"] <= time]
        if not available:
            time = min(processes_copy, key=lambda x: x["arrival"])["arrival"]
            continue

        shortest = min(available, key=lambda x: (x["burst"], x["arrival"]))
        start = time
        time += shortest["burst"]
        gantt.append({"pid": shortest["pid"], "start": start, "end": time})
        _finalize_process(shortest, time)
        completed.append(shortest)
        processes_copy.remove(shortest)

    return gantt, completed


def priority_scheduling(processes):
    processes_copy = sorted(
        (process.copy() for process in processes),
        key=lambda item: (item["arrival"], item["priority"]),
    )
    time = 0
    gantt = []
    completed = []

    while processes_copy:
        available = [p for p in processes_copy if p["arrival"] <= time]
        if not available:
            time = min(processes_copy, key=lambda x: x["arrival"])["arrival"]
            continue

        highest = min(available, key=lambda x: (x["priority"], x["arrival"]))  # Lower number = higher priority
        start = time
        time += highest["burst"]
        gantt.append({"pid": highest["pid"], "start": start, "end": time})
        _finalize_process(highest, time)
        completed.append(highest)
        processes_copy.remove(highest)

    return gantt, completed
