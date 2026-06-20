#!/usr/bin/env python3
"""
Knidos zkVerify - Auto Verify (Codespace Edition)
==================================================

Full-auto verification. Lo cuma perlu:
  1. Run script ini di Codespace terminal
  2. Sign wallet di browser (port 7878)
  3. Balik ke terminal, tekan Enter
  4. Script otomatis verify 5 records + auto-select Valid/Invalid

Usage:
  python3 scripts/auto-verify.py

Dependencies (auto-installed on first run):
  pexpect, requests
"""

import sys
import os
import re
import time
import json
import subprocess

# ---- Auto-install deps ----
def ensure_deps():
    """Ensure pexpect + requests are available. Try several install strategies."""
    missing = []
    for mod in ('pexpect', 'requests'):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if not missing:
        return

    print(f"Installing: {', '.join(missing)}...")

    # Try multiple strategies in order of preference
    strategies = [
        # 1. Normal pip (works in most environments)
        [sys.executable, '-m', 'pip', 'install', '--quiet'] + missing,
        # 2. With --break-system-packages (PEP 668, Python 3.11+)
        [sys.executable, '-m', 'pip', 'install', '--quiet', '--break-system-packages'] + missing,
        # 3. User install
        [sys.executable, '-m', 'pip', 'install', '--quiet', '--user'] + missing,
        # 4. Fallback: pip3 directly
        ['pip3', 'install', '--quiet'] + missing,
    ]

    last_err = None
    for cmd in strategies:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if r.returncode == 0:
                print(f"  ✓ Installed via: {' '.join(cmd[:4])}...")
                return
            last_err = r.stderr or r.stdout
        except Exception as e:
            last_err = str(e)

    print(f"✗ Auto-install failed.")
    print(f"  Run manually: pip3 install -r requirements.txt")
    print(f"  Last error: {last_err[:200] if last_err else 'unknown'}")
    sys.exit(1)

ensure_deps()

# Import after ensure_deps() so they're available module-wide
import pexpect
import requests

# ---- Config ----
EXPECTED_VK = '0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b'
SUBSCAN_API = 'https://zkverify.webapi.subscan.io/api/scan/extrinsic'
DOCKER_IMAGE = 'ghcr.io/node101-io/knidos-challenge:latest'

# ---- ANSI colors ----
class C:
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    B = '\033[94m'
    M = '\033[95m'
    X = '\033[0m'
    BOLD = '\033[1m'

# ---- Parse record from terminal output ----
def parse_records(log_text):
    """Parse all records from accumulated terminal output.

    Records are separated by blank lines. Each record has:
      fillsCommitment[0]: 0x...
      fillsCommitment[1]: 0x...
      startTime:           <ms timestamp>
      endTime:             <ms timestamp>
      Settlement tx:       0x...64 hex chars
    """
    out = []
    current = {}
    for line in log_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        m = re.match(r'fillsCommitment\[0\]:\s*(\S+)', line)
        if m:
            # New record starts — save previous if complete
            if len(current) == 5:
                out.append(current)
            current = {'fill_0': m.group(1)}
            continue

        m = re.match(r'fillsCommitment\[1\]:\s*(\S+)', line)
        if m:
            current['fill_1'] = m.group(1)
            continue

        m = re.match(r'startTime:\s*(\d+)', line)
        if m:
            current['start_time'] = m.group(1)
            continue

        m = re.match(r'endTime:\s*(\d+)', line)
        if m:
            current['end_time'] = m.group(1)
            continue

        m = re.search(r'(?:[Ss]ettlement\s+tx|Tx)[:\s]+(0x[a-f0-9]{64})', line)
        if m:
            current['tx_hash'] = m.group(1)
            if len(current) == 5:
                out.append(current)
                current = {}
            continue

    # Tail record (if file ended without trailing newline)
    if len(current) == 5:
        out.append(current)

    return out

# ---- Verify one record via Subscan API ----
def verify_record(record, retries=3):
    """Returns (verdict, reason)."""
    if not record.get('tx_hash'):
        return 'INVALID', 'no tx hash in record'

    for attempt in range(retries):
        try:
            r = requests.post(
                SUBSCAN_API,
                json={'hash': record['tx_hash']},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            if r.status_code == 403:
                wait = 45 * (attempt + 1)
                print(f'    {C.Y}⚠ Subscan rate-limit (403). Wait {wait}s, retry {attempt+1}/{retries}...{C.X}')
                time.sleep(wait)
                continue
            if r.status_code != 200:
                print(f'    {C.Y}⚠ HTTP {r.status_code}, retry {attempt+1}/{retries}...{C.X}')
                time.sleep(5)
                continue

            data = r.json()
            if data.get('code') != 0:
                return 'INVALID', f"Subscan error: {data.get('message', 'unknown')}"

            params = (data.get('data') or {}).get('params') or []

            # Find VK and pubs in params
            vk = None
            pubs_raw = None
            for p in params:
                pname = (p.get('name') or '').lower()
                val = p.get('value')
                if isinstance(val, dict) and 'Hash' in val:
                    vk = val['Hash']
                elif isinstance(val, dict) and 'Raw' in val:
                    raw = val['Raw']
                    if isinstance(raw, str) and len(raw) > 100:
                        pubs_raw = raw
                elif isinstance(val, str) and len(val) > 100 and '0x' in val:
                    if not pubs_raw:
                        pubs_raw = val
                elif 'pubs' in pname or 'public' in pname:
                    pubs_raw = str(val) if val else pubs_raw

            if not vk:
                return 'INVALID', 'no VK found in on-chain params'
            if not pubs_raw:
                return 'INVALID', 'no pubs found in on-chain params'

            # Extract 4 pubs (hex 64 chars)
            pubs = re.findall(r'0x[a-f0-9]{64}', pubs_raw)
            if len(pubs) < 4:
                return 'INVALID', f'only {len(pubs)} pubs (expected 4)'

            # Check 1: VK match
            if vk.lower() != EXPECTED_VK.lower():
                return 'INVALID', f'VK mismatch (on-chain: {vk[:10]}...)'

            # Check 2: Time forward
            try:
                start = int(record['start_time'])
                end = int(record['end_time'])
            except (ValueError, KeyError):
                return 'INVALID', 'invalid timestamps'
            if start >= end:
                return 'INVALID', f'time backwards ({start} >= {end})'

            # Check 3: Timestamp exact match
            # pubs[2] = startTime, pubs[3] = endTime (last 13 hex chars = ms timestamp)
            try:
                on_start = int(pubs[2][-13:], 16)
                on_end = int(pubs[3][-13:], 16)
            except (ValueError, IndexError):
                return 'INVALID', 'cannot parse on-chain timestamps'

            if on_start != start:
                return 'INVALID', f'startTime diff {abs(on_start - start)}ms'
            if on_end != end:
                return 'INVALID', f'endTime diff {abs(on_end - end)}ms'

            # Check 4: fillsCommitment head/tail match
            for i in range(2):
                app = record[f'fill_{i}']
                on = pubs[i][2:]  # strip 0x
                if '…' in app:
                    app_head = app.split('…')[0].replace('0x', '')
                    app_tail = app.split('…')[1]
                else:
                    app_head = app[2:-6]
                    app_tail = app[-6:]
                if not on.startswith(app_head) or not on.endswith(app_tail):
                    return 'INVALID', f'fillsCommitment[{i}] head/tail mismatch'

            return 'VALID', 'all 5 checks pass'

        except requests.exceptions.Timeout:
            print(f'    {C.Y}⚠ Timeout, retry {attempt+1}/{retries}...{C.X}')
            time.sleep(5)
        except Exception as e:
            print(f'    {C.Y}⚠ Error: {e}, retry {attempt+1}/{retries}...{C.X}')
            time.sleep(5)

    return 'INVALID', 'API failed after retries'

# ---- Wait for TUI to show Valid/Invalid prompt ----
def wait_for_tui_prompt(child, timeout=30):
    """Wait until the challenge TUI shows a Valid/Invalid selection prompt."""
    patterns = [
        r'Valid\s*\n\s*Invalid',   # box-style: "Valid" on top, "Invalid" below
        r'>+\s*Valid',              # arrow indicator before Valid
        r'\bValid\b.*\bInvalid\b', # both words visible
    ]
    try:
        idx = child.expect(patterns + [pexpect.TIMEOUT], timeout=timeout)
        return idx < len(patterns)
    except pexpect.TIMEOUT:
        return False
    except Exception:
        return False

# ---- Send TUI selection ----
def send_tui_selection(child, verdict):
    """Send key sequence to select Valid (default) or Invalid (Down+Enter)."""
    if verdict == 'VALID':
        child.send('\r')  # default = Valid
    else:
        child.send('\x1b[B')  # Down arrow
        time.sleep(0.2)
        child.send('\r')

# ---- Main ----
def main():
    print(f'\n{C.M}{C.BOLD}{"═" * 56}')
    print(f'  🧪  Knidos zkVerify Auto-Verify (Codespace Edition)')
    print(f'{"═" * 56}{C.X}\n')
    print(f'  EXPECTED_VK: {EXPECTED_VK[:10]}...{EXPECTED_VK[-6:]}')
    print(f'  Subscan API: {SUBSCAN_API}')

    # ---- Phase 1: Spawn Docker ----
    print(f'\n{C.B}▶ Phase 1: Spawning Docker challenge...{C.X}')
    print(f'  Image: {DOCKER_IMAGE}')
    print(f'  Port:  7878')

    log_path = '/tmp/knidos_run.log'
    logf = open(log_path, 'w')

    # File-like wrapper for pexpect.logfile_read (needs .write() + .flush())
    class LogMirror:
        def __init__(self, fh):
            self.fh = fh
        def write(self, data):
            self.fh.write(data)
            self.fh.flush()
        def flush(self):
            self.fh.flush()

    try:
        child = pexpect.spawn(
            f'docker run --pull=always -it --name knidos_run -p 7878:7878 {DOCKER_IMAGE}',
            encoding='utf-8',
            timeout=900,
            dimensions=(50, 200),
        )
    except pexpect.ExceptionPexpect as e:
        print(f'{C.R}✗ Failed to spawn Docker: {e}{C.X}')
        print(f'  Is Docker daemon running? Try: docker info')
        sys.exit(1)

    # Mirror child output to logfile (so we can parse later)
    child.logfile_read = LogMirror(logf)

    # ---- Phase 2: Wait for circuit ----
    print(f'\n{C.B}▶ Phase 2: Compiling circuit + deriving VK (~60-90s)...{C.X}')
    try:
        idx = child.expect([
            r'VK[:\s].*0x[a-f0-9]{64}',
            r'Verification\s+key',
            r'Wallet\s+signed',
            r'Pulling',
            pexpect.TIMEOUT,
        ], timeout=180)
        if idx == 4:
            print(f'{C.Y}⚠ Timeout. Last 30 lines of output:{C.X}')
            with open(log_path) as f:
                lines = f.readlines()
            for line in lines[-30:]:
                print('  ' + line.rstrip())
            return
    except Exception as e:
        print(f'{C.Y}⚠ Error: {e}{C.X}')
        return

    print(f'{C.G}✓ Circuit + VK ready.{C.X}')

    # ---- Phase 3: User signs wallet ----
    print(f'\n{C.BOLD}{C.Y}{"─" * 56}')
    print(f'  ⚡  SIGN WALLET DI BROWSER (port 7878)')
    print(f'  1. Buka tab PORTS → klik globe di samping 7878')
    print(f'  2. Connect wallet + sign message')
    print(f'  3. Balik ke terminal ini, tekan Enter')
    print(f'{"─" * 56}{C.X}')
    input()
    print(f'{C.G}✓ Resuming...{C.X}\n')

    # ---- Phase 4: Loop 5 records ----
    results = []
    print(f'{C.B}▶ Phase 4: Verifying 5 records...{C.X}')

    for i in range(5):
        print(f'\n{C.BOLD}─── Record {i+1}/5 ───{C.X}')

        # Wait for record to appear in log
        print(f'  {C.B}▶ Waiting for record data...{C.X}')
        record = None
        for attempt in range(30):  # up to 30s
            time.sleep(1)
            with open(log_path) as f:
                log_text = f.read()
            records = parse_records(log_text)
            # Get only NEW records since last check
            new_records = records[len(results):]
            if new_records:
                record = new_records[0]
                break

        if not record:
            print(f'  {C.R}✗ Timeout waiting for record data{C.X}')
            print(f'  Last 20 lines:')
            with open(log_path) as f:
                lines = f.readlines()
            for line in lines[-20:]:
                print(f'    {line.rstrip()}')
            print(f'\n  Full log: {log_path}')
            print(f'  Falling back to MANUAL mode.')
            print(f'  Verify yourself, then select Valid/Invalid di TUI.')
            verdict = input(f'  Type VALID or INVALID, then Enter: ').strip().upper()
            fallback_record = record or {'fill_0': '?', 'fill_1': '?', 'start_time': '?', 'end_time': '?', 'tx_hash': '?'}
            fallback_record['verdict'] = verdict
            fallback_record['reason'] = 'manual fallback'
            results.append(fallback_record)
            continue

        # Show parsed record
        print(f'  fill_0:       {record["fill_0"]}')
        print(f'  fill_1:       {record["fill_1"]}')
        print(f'  startTime:    {record["start_time"]}')
        print(f'  endTime:      {record["end_time"]}')
        print(f'  settlement:   {record["tx_hash"][:10]}...{record["tx_hash"][-6:]}')

        # Verify
        print(f'\n  {C.B}▶ Verifying via Subscan API...{C.X}')
        verdict, reason = verify_record(record)
        record['verdict'] = verdict
        record['reason'] = reason
        results.append(record)

        if verdict == 'VALID':
            print(f'  {C.G}{C.BOLD}✓ VERDICT: VALID{C.X} — {reason}')
        else:
            print(f'  {C.R}{C.BOLD}✗ VERDICT: INVALID{C.X} — {reason}')

        # Wait for TUI prompt + auto-select
        print(f'  {C.B}▶ Waiting for TUI prompt...{C.X}')
        if wait_for_tui_prompt(child, timeout=30):
            send_tui_selection(child, verdict)
            sel = 'Valid' if verdict == 'VALID' else 'Invalid'
            print(f'  {C.G}→ Sent: {sel}{C.X}')
        else:
            print(f'  {C.Y}⚠ TUI prompt not detected.{C.X}')
            print(f'  MANUAL: select {verdict} di TUI, then press Enter di sini.')
            input()

        time.sleep(1)

    # ---- Phase 5: Final summary ----
    print(f'\n{C.M}{C.BOLD}{"═" * 56}')
    print(f'  📊  Final Results')
    print(f'{"═" * 56}{C.X}')

    valid_count = sum(1 for r in results if r.get('verdict') == 'VALID')
    invalid_count = len(results) - valid_count
    score = valid_count * 50

    print(f'\n  Valid:   {C.G}{valid_count}/5{C.X}')
    print(f'  Invalid: {C.R}{invalid_count}/5{C.X}')
    print(f'  Score:   {C.BOLD}{score} pts{C.X}')

    if valid_count == 5:
        print(f'\n  {C.G}{C.BOLD}🏆 PERFECT! 5/5 correct.{C.X}')
        print(f'  {C.G}Badge "ZK Verifier" UNLOCKED! 🎉{C.X}')
    elif valid_count >= 4:
        print(f'\n  {C.Y}Almost! Need 5/5 for badge.{C.X}')
    else:
        print(f'\n  {C.R}Run ulang buat coba lagi (max 200 pts per wallet).{C.X}')

    print(f'\n  Per-record:')
    for idx, r in enumerate(results, 1):
        sym = f'{C.G}✓{C.X}' if r.get('verdict') == 'VALID' else f'{C.R}✗{C.X}'
        v = r.get('verdict', '?')
        reason = r.get('reason', '?')
        print(f'    {idx}. {sym} {v:7} — {reason}')

    # Save results
    results_path = '/tmp/knidos_results.json'
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\n  Full log:     {log_path}')
    print(f'  Results JSON: {results_path}')

    print(f'\n{C.B}Tekan Enter buat exit (Docker container auto-cleanup)...{C.X}')
    input()
    child.close(force=True)
    logf.close()
    # Cleanup container
    subprocess.run(['docker', 'rm', '-f', 'knidos_run'], capture_output=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{C.Y}Interrupted.{C.X}')
        subprocess.run(['docker', 'rm', '-f', 'knidos_run'], capture_output=True)
        sys.exit(1)
    except Exception as e:
        print(f'\n{C.R}Fatal: {e}{C.X}')
        import traceback
        traceback.print_exc()
        subprocess.run(['docker', 'rm', '-f', 'knidos_run'], capture_output=True)
        sys.exit(1)
