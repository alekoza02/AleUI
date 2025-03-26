import ctypes
import ctypes.wintypes
import psutil
import time

ntdll = ctypes.WinDLL("ntdll")
SystemProcessorPerformanceInformation = 8

class SYSTEM_PROCESSOR_PERFORMANCE_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("IdleTime", ctypes.wintypes.LARGE_INTEGER),
        ("KernelTime", ctypes.wintypes.LARGE_INTEGER),
        ("UserTime", ctypes.wintypes.LARGE_INTEGER),
        ("Reserved1", ctypes.wintypes.LARGE_INTEGER * 2),
        ("Reserved2", ctypes.c_ulong),
    ]

class CPU_performance:
    def __init__(self):
        # Store previous times to calculate delta
        self.previous_idle_times = [0] * psutil.cpu_count()
        self.previous_total_times = [0] * psutil.cpu_count()

    def get_usage(self):
        # Query the performance information
        info_array = (SYSTEM_PROCESSOR_PERFORMANCE_INFORMATION * psutil.cpu_count())()
        result = ntdll.NtQuerySystemInformation(SystemProcessorPerformanceInformation, ctypes.byref(info_array), ctypes.sizeof(info_array), None)

        # Initialize total and idle times for this iteration
        idle_time = 0
        total_time = 0
        for i, core in enumerate(info_array):
            # Calculate deltas (current value - previous value)
            delta_idle = core.IdleTime - self.previous_idle_times[i]
            delta_total = (core.KernelTime + core.UserTime) - self.previous_total_times[i]
            
            idle_time += delta_idle
            total_time += delta_total
            
            # Save current values for next iteration
            self.previous_idle_times[i] = core.IdleTime
            self.previous_total_times[i] = core.KernelTime + core.UserTime

        # Compute CPU usage based on delta times
        if total_time > 0:
            cpu_usage = min(100 * (1 - (idle_time / total_time)), 100)
            return cpu_usage
