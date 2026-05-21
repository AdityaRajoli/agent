import subprocess
import time
import psutil
import os
import sys

def calculate_rma(tasks):
    """
    RMA Formula:
    U = Σ(Ci/Ti) ≤ n(2^(1/n) - 1)
    """
    n             = len(tasks)
    utilization   = sum(c / t for c, t in tasks)
    threshold     = n * (2 ** (1/n) - 1) * 100
    utilization_percent = utilization * 100
    return utilization_percent, threshold

def run_rma_analysis():
    print("\n--- RMA CPU Analysis ---")
    print("-" * 40)

    sys.path.insert(0, os.path.abspath("app"))

    if "test" in sys.modules:
        del sys.modules["test"]

    from test import find_max

    # Measure 3 tasks
    tasks  = []
    period = 1.0
    inputs = [(10, 5, 3), (3, 9, 1), (2, 4, 7)]

    for inp in inputs:
        start = time.time()
        find_max(*inp)
        end   = time.time()
        tasks.append((end - start, period))

    utilization, threshold = calculate_rma(tasks)

    print(f"  Number of Tasks : {len(tasks)}")
    print(f"  RMA Threshold   : {threshold:.2f}%")
    print(f"  CPU Utilization : {utilization:.4f}%")

    if utilization <= threshold:
        print(f"  RMA Status : ✅ CPU within limit")
        print(f"  ({utilization:.4f}% ≤ {threshold:.2f}%)")
    else:
        print(f"  RMA Status : ❌ CPU overloaded!")
        print(f"  ({utilization:.4f}% > {threshold:.2f}%)")

    return utilization, threshold

def run_adaptive_tests(test_files):
    metrics = {
        "tests_passed"      : False,
        "coverage"          : 0.0,
        "complexity"        : 0.0,
        "execution_time_sec": 0.0,
        "cpu_percent"       : 0.0,
        "ram_percent"       : 0.0,
        "rma_utilization"   : 0.0,
        "rma_threshold"     : 0.0
    }

    start_time = time.time()

    # ── Run pytest for Python ──────────────────────────
    python_tests = [f for f in test_files if f.endswith('.py')]
    if python_tests:
        print("Running pytest...")
        result = subprocess.run(
            ["python3", "-m", "coverage", "run",
             "-m", "pytest"] + python_tests + ["-v"],
            capture_output=False
        )
        metrics['tests_passed'] = (result.returncode == 0)

        # Get coverage
        cov = subprocess.run(
            ["python3", "-m", "coverage", "report"],
            capture_output=True, text=True
        )
        for line in cov.stdout.split('\n'):
            if 'TOTAL' in line:
                parts = line.split()
                try:
                    metrics['coverage'] = float(parts[-1].replace('%', ''))
                except:
                    metrics['coverage'] = 0.0

    # ── Run GTest for C ───────────────────────────────
    cpp_tests = [f for f in test_files if f.endswith('.cpp')]
    if cpp_tests:
        print("Running GTest...")
        result = subprocess.run(
            ["make", "-C", "build"],
            capture_output=False
        )
        if result.returncode == 0:
            test_run = subprocess.run(
                ["./build/runTests"],
                capture_output=False
            )
            if not metrics['tests_passed']:
                metrics['tests_passed'] = (test_run.returncode == 0)

    # ── Complexity with Lizard ────────────────────────
    print("Checking complexity with Lizard...")
    lizard_result = subprocess.run(
        ["lizard", "app/", "--warnings_only", "-C", "10"],
        capture_output=True, text=True
    )
    if lizard_result.stdout.strip():
        metrics['complexity'] = 15.0
    else:
        metrics['complexity'] = 5.0

    # ── Performance Metrics ───────────────────────────
    metrics['cpu_percent']        = psutil.cpu_percent(interval=1)
    metrics['ram_percent']        = psutil.virtual_memory().percent
    metrics['execution_time_sec'] = round(time.time() - start_time, 2)

    # ── RMA Analysis ──────────────────────────────────
    rma_util, rma_thresh          = run_rma_analysis()
    metrics['rma_utilization']    = round(rma_util,   4)
    metrics['rma_threshold']      = round(rma_thresh, 2)

    print(f"\nCoverage : {metrics['coverage']}%")
    print(f"CPU      : {metrics['cpu_percent']}% | RAM: {metrics['ram_percent']}% | Time: {metrics['execution_time_sec']}s")

    return metrics
