# Tutorial: Auto-Verify Knidos zkVerify Challenge

> 🌐 **Language:** 🇮🇩 [Bahasa Indonesia](TUTORIAL.md) · 🇬🇧 [English](TUTORIAL.en.md)

Verify 5 ZK proof records at [testnet.knidos.xyz/zkverify-task](https://testnet.knidos.xyz/zkverify-task) automatically using **GitHub Codespaces**. ~5 minutes setup + ~5 minutes run. Earn up to **250 pts + ZK Verifier badge** per wallet.

## What You Need

| Requirement | Details |
|---|---|
| GitHub account | For Codespaces (free 60 hours/month) |
| Browser | Chrome/Edge/Brave + MetaMask or Rabby extension |
| Wallet address | Any wallet with the extension. New wallets work — no funds needed |

## Step 1 — Open Codespace

1. Open this repo: **https://github.com/fauzidashine/knidos-zkverify-tutorial**
2. Click the green **`<> Code`** button (top of file list, right side)
3. Click the **Codespaces** tab
4. Click **"+ Create codespace on main"**
5. Your browser will load VS Code in a new tab. Wait ~60 seconds until you see the terminal at the bottom.

Codespace automatically sets up Docker + forwards port 7878. No installation needed.

## Step 2 — Pre-pull Docker Image

**Copy-paste this into the Codespace terminal, then press Enter:**

```bash
docker pull ghcr.io/node101-io/knidos-challenge:latest
```

First pull takes **5-15 minutes** (225MB image). Be patient, don't Ctrl+C. Already pulled once? It'll be instant.

**Verify it's cached:**
```bash
docker images | grep knidos
```

If you see a row with `225MB`, proceed to Step 3. Otherwise, wait for the pull to finish.

## Step 3 — Install Python Deps

```bash
pip3 install --user pexpect requests
```

Output should be `Successfully installed ...` or `Requirement already satisfied`. If it errors, try:
```bash
pip3 install --user --break-system-packages pexpect requests
```

## Step 4 — Run Auto-Verify

```bash
python3 scripts/auto-verify.py
```

**Expected output (first ~1-2 minutes):**

```
════════════════════════════════════════════════════════
  🧪  Knidos zkVerify Auto-Verify (Codespace Edition)
════════════════════════════════════════════════════════

▶ Phase 1: Spawning Docker challenge...
▶ Phase 2: Compiling circuit + deriving VK (~60-90s)...
✓ Circuit + VK ready.

────────────────────────────────────────────────────────
  ⚡  SIGN WALLET IN BROWSER (port 7878)
  1. Open PORTS tab → click globe next to 7878
  2. Connect wallet + sign message
  3. Come back to this terminal, press Enter
────────────────────────────────────────────────────────
```

## Step 5 — Sign Wallet

1. In the Codespace, click the **PORTS** tab (bottom panel, next to "Terminal" tab)
2. Find port **7878** → click the **globe icon** 🌐 in the "Forwarded Address" column
3. A new browser tab opens
4. MetaMask/Rabby popup asks for **Sign message** → click **Sign**
5. Wait 5-10 seconds
6. Switch back to the Codespace tab → **click in the terminal area** → press **Enter**

## Step 6 — Wait for Auto-Verify to Finish

**Now just wait.** Don't click/touch anything. The script will loop through 5 records:

```
✓ Resuming...

▶ Phase 4: Verifying 5 records...

─── Record 1/5 ───
  fill_0:       0x000000000000...a7cc26
  fill_1:       0x000000000000...b3ec51
  startTime:    1779685560000
  endTime:      1779685200000
  settlement:   0x4b5144a8...cbcb6c

  ▶ Verifying via Subscan API...
  ✗ VERDICT: INVALID — time backwards (st > et)
  → Sent: Invalid

─── Record 2/5 ───
  ... (continues automatically)
```

Each record takes **20-60 seconds** (Subscan API sometimes rate-limits, script auto-retries). Total 5 records ≈ **3-5 minutes**.

## Step 7 — Check Results

After 5 records finish, the terminal prints:

```
════════════════════════════════════════════════════════
  FINAL SCORE
════════════════════════════════════════════════════════
  ✅ Correct: 5/5
  Total points: 250
```

Score syncs to leaderboard **every hour** (not instant). Check at:
**https://testnet.knidos.xyz/leaderboard**

5/5 correct = **ZK Verifier** badge unlocked.

---

## Troubleshooting

### Codespace doesn't show port 7878

Wait 30 seconds after the Codespace is ready. If still missing, click the PORTS tab → "Add Port" → type `7878` → Enter.

### `docker: command not found`

Codespace needs time to start the Docker daemon. Wait 1 minute, retry the command.

### Stuck at "Compiling circuit" > 5 minutes

Codespace internet is slow. Cancel (Ctrl+C), then retry:
```bash
python3 scripts/auto-verify.py
```

### Stuck at "Waiting for TUI prompt"

Clack TUI is blocked. Fix:
1. Open the PORTS 7878 tab in browser → **refresh page**
2. Sign again if prompted
3. Back to terminal → press Enter
4. If still stuck, Ctrl+C → re-run from Step 4

### `Subscan rate-limit (403)` spam in output

Normal. Script auto-retries with delays 45s → 90s → 135s. Be patient, don't cancel.

### Wallet sign-in not detected

1. Make sure MetaMask/Rabby is unlocked
2. Refresh PORTS 7878 tab → sign again
3. Click in terminal → press Enter once more

### 5 records finished but leaderboard didn't update

Wait up to **1 hour** (sync period). If still 0 after 24 hours:
- Possible judge script misread the data
- Re-run the script (Step 4) — retries still earn points

### Want to use a different wallet

Delete the old Codespace first (so the container is fresh):
1. Codespace tab → click Codespace name → **Stop** → confirm
2. Back to repo → click **Code → Codespaces → "+"** → create new one
3. Repeat from Step 2

---

## How It Works (read if curious)

```
┌─────────────────────────────────────────────────────────────┐
│  scripts/auto-verify.py                                     │
│                                                             │
│  1. Spawn Docker container (Knidos challenge app)           │
│  2. Wait for circuit compile + VK ready (~60-90s)           │
│  3. Open web UI on port 7878 → user signs wallet            │
│  4. Loop 5 records:                                         │
│     a. Parse terminal output (fillsCommitment, timestamps)  │
│     b. Query Subscan API for on-chain data                  │
│     c. 5 boolean checks (VK, time, fills, timestamps, tx)   │
│     d. Send ↑↓+Enter to Clack TUI automatically            │
│  5. Print final score + decline "Try again"                 │
└─────────────────────────────────────────────────────────────┘
```

What the script does per record:
- **VK check**: match VK hash in TUI vs on-chain
- **Time check**: ensure `startTime < endTime`
- **Timestamps check**: match against `pubs[2]`/`pubs[3]` on-chain
- **Fills check**: match `fillsCommitment[0]`/`[1]` head+tail (middle is truncated)
- **Tx check**: settlement tx actually exists on zkVerify

5 checks pass → VALID. Any 1 fails → INVALID. Most records are INVALID by design — the challenge is to detect corruption, not to validate records.

---

## Files in This Repo

| File | Purpose |
|---|---|
| `scripts/auto-verify.py` | Full auto (used in this tutorial) |
| `scripts/verify-console.js` | Semi-manual: paste in Subscan browser console |
| `scripts/start-challenge.sh` | Bash helper to run the container manually |
| `.devcontainer/devcontainer.json` | Codespace auto-setup (Docker + Python) |
| `README.md` / `README.en.md` | Overview of the challenge (BI / EN) |
| `TUTORIAL.md` / `TUTORIAL.en.md` | Step-by-step walkthrough (BI / EN) |

---

## Credits

This repo is part of a community contribution to Knidos. Docker image from `ghcr.io/node101-io/knidos-challenge`. The `auto-verify.py` script is written with `pexpect` + `requests`, inspired by ZK proof verification testing patterns in production.
