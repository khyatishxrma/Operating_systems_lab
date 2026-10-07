from multiprocessing import Process, Value
from threading import Thread, current_thread

# --- Part A: Data and Metrics ---
processes = [
    {"pid": "P1", "arrival": 0, "burst": 7},
    {"pid": "P2", "arrival": 2, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 1},
    {"pid": "P4", "arrival": 5, "burst": 4},
]

intervals = [
    ("P1", 0, 2),
    ("P2", 2, 4),
    ("P1", 4, 6),
    ("P3", 6, 7),
    ("P2", 7, 9),
    ("P4", 9, 11),
    ("P1", 11, 13),
    ("P4", 13, 15),
    ("P1", 15, 16),
]


def calculate_metrics():
    print("\n--- SCHEDULING METRICS ---")
    print(f"{'PID':<4} {'AT':<3} {'BT':<3} {'CT':<3} {'TAT':<4} {'WT':<3} {'RT':<3}")
    tat_total = wt_total = rt_total = 0

    for p in processes:
        runs = [x for x in intervals if x[0] == p["pid"]]
        first_start = runs[0][1]
        completion = runs[-1][2]

        tat = completion - p["arrival"]
        wt = tat - p["burst"]
        rt = first_start - p["arrival"]

        tat_total += tat
        wt_total += wt
        rt_total += rt

        print(
            f"{p['pid']:<4} {p['arrival']:<3} {p['burst']:<3} "
            f"{completion:<3} {tat:<4} {wt:<3} {rt:<3}"
        )

    n = len(processes)
    print("Average TAT =", round(tat_total / n, 2))
    print("Average WT =", round(wt_total / n, 2))
    print("Average RT =", round(rt_total / n, 2))


def show_gantt_chart():
    print("\n--- ROUND ROBIN GANTT CHART ---")
    # Join process names separated by dividers
    chart_bar = " | ".join(pid for pid, _, _ in intervals)
    print(f"| {chart_bar} |")

    # Collect timeline timestamps: start of first + end of all intervals
    times = [intervals[0][1]] + [end for _, _, end in intervals]
    print("   ".join(f"{t:>2}" for t in times))


def thread_task(name):
    print(name, "running | Thread ID:", current_thread().ident)


def thread_demo():
    print("\n--- THREAD DEMO ---")
    t1 = Thread(target=thread_task, args=("Thread 1",))
    t2 = Thread(target=thread_task, args=("Thread 2",))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Both threads completed.")


def update_shared(value):
    value.value += 10


def shared_memory_demo():
    print("\n--- SHARED MEMORY DEMO ---")
    shared_value = Value("i", 5)
    print("Before child process:", shared_value.value)
    child = Process(target=update_shared, args=(shared_value,))
    child.start()
    child.join()
    print("After child process:", shared_value.value)


if __name__ == "__main__":
    calculate_metrics()
    show_gantt_chart()
    thread_demo()
    shared_memory_demo()
