#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
for skill in sorted(root.glob('skills/*/SKILL.md')):
    text = skill.read_text(encoding='utf-8')
    if not text.startswith('---') or not re.search(r'^name:\s*\S+', text, re.M) or not re.search(r'^description:\s*', text, re.M):
        errors.append(f'{skill}: missing required frontmatter')
    if len(text.splitlines()) > 500:
        errors.append(f'{skill}: exceeds 500 lines')
for path in root.rglob('*'):
    if '.git' in path.parts or not path.is_file():
        continue
    try: text = path.read_text(encoding='utf-8', errors='ignore')
    except OSError: continue
    if re.search(r'(gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})', text):
        errors.append(f'{path}: possible secret token')
for required in ['AGENTS.md', 'workflow/00_system_intake.md', 'workflow/12_safe_execution.md', 'workflow/13_github_delivery.md', 'tools/preflight_system.py', 'tools/run_logged.sh', 'tools/checkpoint.sh']:
    if not (root / required).exists(): errors.append(f'missing {required}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('validation passed: skills, orchestrator docs, safety tools, and secret scan')
