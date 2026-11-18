import psutil
import os
import ctypes

def get_ram_info():
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total / (1024**3):.2f} GB")
    print(f"Used RAM:  {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    print(f"Free RAM:  {mem.available / (1024**3):.2f} GB")
    
    print("\nTop 15 Memory-Consuming Processes:")
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            info = p.info
            if info and info['memory_info']:
                procs.append((info['name'], info['pid'], info['memory_info'].rss))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    procs.sort(key=lambda x: x[2], reverse=True)
    for name, pid, rss in procs[:15]:
        print(f"  {name:25} (PID {pid:6}): {rss / (1024**2):8.2f} MB")

def empty_working_sets():
    """Empty working set for processes where permitted (Windows SetProcessWorkingSetSize)."""
    count = 0
    freed_approx = 0
    for p in psutil.process_iter(['pid', 'name']):
        try:
            # Try to empty working set
            handle = ctypes.windll.kernel32.OpenProcess(0x001F0FFF, False, p.pid)
            if handle:
                ctypes.windll.psapi.EmptyWorkingSet(handle)
                ctypes.windll.kernel32.CloseHandle(handle)
                count += 1
        except Exception:
            pass
    print(f"\nFlushed working sets for {count} accessible processes.")

if __name__ == "__main__":
    print("=== BEFORE OPTIMIZATION ===")
    get_ram_info()
    empty_working_sets()
    print("\n=== AFTER OPTIMIZATION ===")
    get_ram_info()
