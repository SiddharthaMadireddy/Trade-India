#!/usr/bin/env python3
"""Auto-run scanner commands locally without Claude sandbox network limits.
Uses local fixtures/fallback if external fetch fails."""
import subprocess, sys, os

commands = [
    ["python3", "trader-scanner/scan.py", "universe"],
    ["python3", "trader-scanner/scan.py", "daily"],
    ["python3", "trader-scanner/scan.py", "orb", "--at", "10:15"],
]
for cmd in commands:
    print(f"\n>>> Running: {' '.join(cmd)}")
    # Auto-run; don't fail on network error — print status
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout[-1200:] if len(result.stdout) > 1200 else result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
    print("Return:", result.returncode)
