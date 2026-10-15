import argparse
import ctypes
import json
import os
import time
from collections.abc import Callable

import cpmpy as cp


def peak_memory_mb() -> float:
    """Return the process's peak resident memory in MiB."""
    if os.name == "nt":
        class ProcessMemoryCounters(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.c_ulong),
                ("PageFaultCount", ctypes.c_ulong),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        get_current_process = kernel32.GetCurrentProcess
        get_current_process.restype = ctypes.c_void_p
        get_process_memory_info = psapi.GetProcessMemoryInfo
        get_process_memory_info.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ProcessMemoryCounters),
            ctypes.c_ulong,
        ]
        get_process_memory_info.restype = ctypes.c_int

        counters = ProcessMemoryCounters()
        counters.cb = ctypes.sizeof(counters)
        if not get_process_memory_info(
            get_current_process(), ctypes.byref(counters), counters.cb
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        peak_bytes = counters.PeakWorkingSetSize
    else:
        import resource

        peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_bytes = peak_rss if os.uname().sysname == "Darwin" else peak_rss * 1024

    return peak_bytes / (1024 * 1024)


def run_cli(model_name: str, build_model: Callable[[int], cp.Model]) -> None:
    parser = argparse.ArgumentParser(
        description=f"Résout le problème des N reines avec le modèle {model_name}."
    )
    parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Taille de l'échiquier (entier positif).",
    )
    parser.add_argument(
        "--solver",
        default="ortools",
        help="Solveur CPMpy à utiliser (par défaut : ortools).",
    )
    args = parser.parse_args()
    if args.n < 1:
        parser.error("--n doit être un entier positif.")

    model = build_model(args.n)
    start_time = time.perf_counter()
    solution_count = model.solveAll(solver=args.solver)
    elapsed_seconds = time.perf_counter() - start_time

    print(
        json.dumps(
            {
                "model": model_name,
                "n": args.n,
                "solutions": solution_count,
                "elapsed_seconds": elapsed_seconds,
                "peak_memory_mb": peak_memory_mb(),
            }
        )
    )
