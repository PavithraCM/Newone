import ctypes
import os
import sys
import time

CPU_THRESHOLD = 80.0
MEMORY_THRESHOLD = 85.0
DISK_THRESHOLD = 90.0
LOG_FILE = "system_health.log"


def log_and_alert(message, is_alert=False):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{'ALERT' if is_alert else 'INFO'}] {message}"
    print(log_entry)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
    except IOError as e:
        print(f"Failed to write to log file: {e}", file=sys.stderr)


def get_cpu_usage():
    try:
        output = os.popen("wmic cpu get loadpercentage").read()
        lines = [line.strip() for line in output.split("\n") if line.strip()]
        if len(lines) > 1 and lines[1].isdigit():
            return float(lines[1])
        return 0.0
    except Exception:
        return 0.0


def get_memory_usage():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(stat)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    return float(stat.dwMemoryLoad)


def get_disk_usage():
    total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong()
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p("C:\\"), None, ctypes.byref(total), ctypes.byref(free)
    )
    if total.value == 0:
        return 0.0
    return ((total.value - free.value) / total.value) * 100.0


def check_system_health():
    print("=" * 60)
    print(f"--- Running System Health Check (Logging to {LOG_FILE}) ---")
    print("=" * 60)

    cpu = get_cpu_usage()
    if cpu > CPU_THRESHOLD:
        log_and_alert(
            f"High CPU usage: {cpu:.1f}% (Threshold: {CPU_THRESHOLD}%)",
            is_alert=True,
        )
    else:
        log_and_alert(f"CPU Usage: {cpu:.1f}%")

    memory = get_memory_usage()
    if memory > MEMORY_THRESHOLD:
        log_and_alert(
            f"High Memory usage: {memory:.1f}% (Threshold: {MEMORY_THRESHOLD}%)",
            is_alert=True,
        )
    else:
        log_and_alert(f"Memory Usage: {memory:.1f}%")

    disk = get_disk_usage()
    if disk > DISK_THRESHOLD:
        log_and_alert(
            f"High Disk usage on C:: {disk:.1f}% (Threshold: {DISK_THRESHOLD}%)",
            is_alert=True,
        )
    else:
        log_and_alert(f"Disk Usage on C: {disk:.1f}%")

    try:
        processes = len(os.popen("tasklist").read().strip().split("\n")) - 3
        log_and_alert(f"Total active running processes: {max(0, processes)}")
    except Exception:
        pass
    print("=" * 60)


if __name__ == "__main__":
    check_system_health()
