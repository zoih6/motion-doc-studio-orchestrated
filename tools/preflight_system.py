#!/usr/bin/env python3
"""Safe preflight for small workspaces; emits human or JSON output."""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, time
from pathlib import Path


def mb(n: int) -> float:
    return round(n / 1024 / 1024, 1)


def mem_available() -> int:
    text = Path('/proc/meminfo').read_text()
    for line in text.splitlines():
        if line.startswith('MemAvailable:'):
            return int(line.split()[1]) * 1024
    return 0


def workspace_bytes(root: Path) -> int:
    total = 0
    for p in root.rglob('*'):
        try:
            if p.is_file() and not p.is_symlink():
                total += p.stat().st_size
        except OSError:
            pass
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    usage = shutil.disk_usage(root)
    available = mem_available()
    used_workspace = workspace_bytes(root)
    mem_warn = int(os.getenv('MOTION_MEM_WARN_MB', '600')) * 1024 * 1024
    mem_critical = int(os.getenv('MOTION_MEM_CRITICAL_MB', '250')) * 1024 * 1024
    work_warn = int(os.getenv('MOTION_WORK_WARN_MB', '55')) * 1024 * 1024
    work_critical = int(os.getenv('MOTION_WORK_CRITICAL_MB', '128')) * 1024 * 1024
    duplicate = subprocess.run("ps -eo comm= | sort | uniq -c | sort -nr | head -20", shell=True, text=True, capture_output=True).stdout.splitlines()
    status = 'ok'
    reasons = []
    if available < mem_critical:
        status = 'blocked'; reasons.append('MemAvailable below critical threshold')
    elif available < mem_warn:
        status = 'caution'; reasons.append('MemAvailable below comfortable threshold')
    if used_workspace > work_critical:
        status = 'blocked'; reasons.append('workspace exceeds critical threshold')
    elif used_workspace > work_warn and status == 'ok':
        status = 'caution'; reasons.append('workspace exceeds target threshold')
    result = {
        'timestamp_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'root': str(root), 'status': status, 'reasons': reasons,
        'memory': {'available_mb': mb(available), 'warn_mb': mb(mem_warn), 'critical_mb': mb(mem_critical)},
        'disk': {'free_mb': mb(usage.free), 'total_mb': mb(usage.total)},
        'workspace': {'bytes': used_workspace, 'size_mb': mb(used_workspace), 'warn_mb': mb(work_warn), 'critical_mb': mb(work_critical)},
        'process_snapshot': duplicate,
        'temp_work': os.getenv('TEMP_WORK', '/var/tmp/motion-doc-studio'),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else f"status={status} memory={mb(available)}MB disk_free={mb(usage.free)}MB workspace={mb(used_workspace)}MB")
    return 2 if status == 'blocked' else 0

if __name__ == '__main__':
    raise SystemExit(main())
