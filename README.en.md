# 🎯 Knidos zkVerify Challenge — Tutorial

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=fauzidashine/knidos-zkverify-tutorial)

> 🌐 **Language:** 🇮🇩 [Bahasa Indonesia](README.md) · 🇬🇧 [English](README.en.md)

Step-by-step tutorial for solving the Knidos **"Verify a ZK Proof Manually"** challenge on testnet with a **5/5 perfect score + 250 points + ZK Verifier badge**.

🔗 Challenge: https://testnet.knidos.xyz/zkverify-task

---

## 💰 What You Get

| Result | Points | Badge |
|---|---|---|
| 5/5 correct | **250 pts** | ✅ ZK Verifier |
| 4/5 correct | 200 pts | ❌ |
| ≤3/5 correct | < 150 pts | ❌ |

---

## 🛠 What You Need

1. **Any device** that can install Docker (PC / laptop / cloud VM / Chromebook via Linux)
2. **Docker** (Desktop or Engine — see [Docker Alternatives](#-docker-alternatives) below if you're not on Windows/Mac)
3. **Browser** (Chrome / Firefox)
4. **Crypto wallet** (MetaMask / Rabby) — already have a signature
5. **±10 minutes** per wallet

---

## 💻 Docker Alternatives

Don't have Windows/Mac Desktop? No worries, plenty of options:

### 1. **Linux Native** (simplest for Linux users)

Install Docker Engine directly — no Desktop needed:

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Logout & login again, or:
newgrp docker

# Verify
docker --version
```

**Best for:** Ubuntu, Debian, Fedora, Arch, Mint, etc.

### 2. **WSL2** (Windows 10/11 without Hyper-V)

1. Enable WSL: `wsl --install` (in PowerShell as admin)
2. Install Ubuntu from the Microsoft Store
3. Inside Ubuntu, install Docker Engine (same as Linux native above)
4. **MUST** enable Docker Desktop WSL2 integration, OR run Docker inside WSL2 directly without Desktop

```powershell
# PowerShell (admin)
wsl --install
wsl --set-default-version 2
```

Then inside WSL2 Ubuntu:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Best for:** Windows Home edition (no Hyper-V), or users who prefer a Linux environment.

### 3. **Free Cloud VM** (no PC at all)

Spin up a Linux VM in the cloud — Docker pre-installed or just install it:

| Provider | Free Tier | Setup |
|---|---|---|
| **Oracle Cloud** | 2 VMs always-free (ARM, 4 CPU / 24GB RAM) | Sign up, create VM, SSH, install Docker |
| **Google Cloud** | $300 credit / 90 days | `gcloud compute ssh`, install Docker |
| **AWS** | t2.micro / 12 months | `ssh -i key.pem ubuntu@vm`, install Docker |
| **Hetzner** | Cheap Cloud VM (~€4/mo) | Fastest, no big credit card needed |

**Most recommended: Oracle Cloud** — if you qualify, you get 2 always-free VMs you can use forever.

Quick setup (Oracle Cloud):
```bash
# SSH into VM
ssh ubuntu@<public-ip>

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# SSH tunnel to expose localhost:7878 to your PC
# (because your browser is on your PC, the VM is in the cloud)
ssh -L 7878:localhost:7878 ubuntu@<public-ip>
```

Then open `http://localhost:7878` in your PC browser.

### 4. **GitHub Codespaces** (install nothing) ⭐ **EASIEST**

Fastest if you just want to try it — **runs directly from any phone/laptop browser**:

1. Click the **"Open in GitHub Codespaces"** badge at the top of this README, **OR** open the repo → green **"Code"** button → **"Codespaces"** tab → **"Create codespace on main"**
2. Wait ~60 seconds, you'll get **VS Code in browser + Ubuntu container + Docker pre-installed** (auto-install via `.devcontainer/devcontainer.json`)
3. In the Codespace terminal, run:
   ```bash
   docker run --pull=always -it -p 7878:7878 ghcr.io/node101-io/knidos-challenge:latest
   ```
4. Codespace automatically **detects port 7878** and shows "Open in Browser" notification — click it
5. Or open the **"Ports"** tab in VS Code → click the globe icon next to port 7878 (visibility auto-set to public via devcontainer config)
6. URL format: `https://xxx-7878.app.github.dev`

**Free tier:** 60 hours/month for personal accounts. Plenty for many wallets.

**Auto-forward:** Port 7878 is pre-configured in `.devcontainer/devcontainer.json` so it auto-forwards without manual setup.

**Stop codespace** when done to avoid billing: press `Ctrl+Shift+P` → "Codespaces: Stop Current Codespace"

### 5. **Android (Termux + QEMU)** (advanced)

Yes it's possible, but messy:
1. Install Termux from F-Droid
2. Install proot-distro: `pkg install proot-distro && proot-distro install ubuntu`
3. Enter Ubuntu: `proot-distro login ubuntu`
4. Install Docker (limited — needs qemu-user to emulate)
5. Forward port via SSH tunnel to another device or use `termux-wake-lock`

**Not recommended** — more problems than solutions.

### 6. **iOS** (very limited)

iOS doesn't support Docker natively. Use a cloud VM option (option 3) or GitHub Codespaces (option 4).

---

## 🚀 Step-by-Step

### Step 1: Install Docker

1. Download Docker Desktop at https://docs.docker.com/get-docker/
2. Install & **open the app** (don't close it)
3. Verify by opening a terminal:
   ```bash
   docker --version
   ```

### Step 2: Run the Container

Open a **terminal / command prompt** (not inside the Docker app):

- **Windows**: `Win+R` → type `cmd` → Enter
- **macOS**: open "Terminal"
- **Linux**: open a terminal directly

Copy-paste this command:

```bash
docker run --pull=always -it -p 7878:7878 ghcr.io/node101-io/knidos-challenge:latest
```

**What happens:**
- Docker downloads the image (~100MB, first time only)
- Container runs in the background
- Terminal shows URL `http://127.0.0.1:7878` + sign-in prompt

### Step 3: Sign Wallet

1. Open a browser
2. Go to **http://localhost:7878**
3. Make sure your wallet is connected (MetaMask/Rabby)
4. **Sign** the message that appears
5. **Come back to the terminal WITHIN 10 minutes** (signature expires)

After signing:
- Container compiles circuit (~30 seconds)
- Container derives verification key (~10-30 seconds)
- **Record 1/5** appears with settlement tx data

### Step 4: Verify 5 Records

For each record, the terminal shows:

```
─── Record 1/5 ─────────────────────────────────────────
  Settlement tx:  https://zkverify.subscan.io/extrinsic/0x4b51...
  
  Public inputs (committed in the proof):
    fillsCommitment[0]: 0x000000000000…a7cc26
    fillsCommitment[1]: 0x000000000000…554a1f
    startTime:          1779685200000  →  2026-05-25T05:00:00.000Z
    endTime:            1779685560000  →  2026-05-25T05:06:00.000Z
    
  Verification key hash (compiled from circuit): 0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b
  
? Record 1/5: valid or invalid?
```

### 5 Mandatory Checks

For each record, check these **5 things** against Subscan:

| # | Check | Where to look on Subscan | Mark INVALID if |
|---|---|---|---|
| 1 | **Tx exists** | Page is normal, not an error | "Extrinsic not found on the zkVerify network" |
| 2 | **VK hash match** | `Parameters` → `vk_or_hash.Hash` | ≠ `0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b` |
| 3 | **Time forward** | startTime vs endTime in terminal | startTime > endTime |
| 4 | **Timestamps exact** | See [Quick Verification](#-quick-verification) below | There's a diff (even 1 second) |
| 5 | **fillsCommitment match** | See [Quick Verification](#-quick-verification) below | Tail hex differs |

#### Checks #4 & #5 — Quick Verification

1. On the Subscan page, press **F12** (DevTools)
2. Click the **Console** tab
3. Paste the code from [`scripts/verify-console.js`](./scripts/verify-console.js) → Enter
4. You'll be prompted to paste terminal data — copy the `fillsCommitment[0]`, `fillsCommitment[1]`, `startTime`, `endTime` lines into the prompt
5. Output shows 5 check results + recommendation (VALID or INVALID)

#### Check #2 — VK Hash

On the Subscan page, look at the **Parameters** section:
- Expand `0.vk_or_hash.value.Hash`
- Must equal `0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b`
- **If different (like `0x3f450a7e...de30`)** → INVALID

### Step 5: Submit Answer

After checking all 5 things:
- **All pass** → `Valid` (Enter)
- **Any 1 fails** → `↓` (arrow down) → `Invalid` (Enter)

Repeat for 5 records. After submitting the 5th:

```
5/5 correct — your answers have been recorded.
🎉 A perfect run — every record correct.
```

🎉 **Done!** 250 pts + ZK Verifier badge credited.

---

## 🤖 Auto-Verify Mode (Codespace Edition)

Don't want to click Valid/Invalid 5 times? Use auto-verify:

```bash
python3 scripts/auto-verify.py
```

This script replaces all manual steps:
1. Spawn Docker container automatically
2. Wait for circuit compile + VK derivation
3. Prompt: "sign wallet in browser, press Enter"
4. Loop 5 records:
   - Parse record data from terminal output
   - Verify via Subscan API (5 checks: VK, time, timestamps, fillsCommitment)
   - Auto-select Valid/Invalid in TUI prompt
5. Show final score + per-record verdict

**Total interaction:** Sign wallet in browser + 1 Enter. Rest is automatic.

### Sample Output

```
─── Record 1/5 ───
  fill_0:       0x000000000000…a7cc26
  fill_1:       0x000000000000…554a1f
  startTime:    1779685200000
  endTime:      1779685560000
  settlement:   0x4b5144a4…d28c6cb6c

  ▶ Verifying via Subscan API...
  ✓ VERDICT: VALID — all 5 checks pass
  → Sent: Valid

─── Record 2/5 ───
  ...
  ✗ VERDICT: INVALID — time backwards (1779685560000 >= 1779685200000)
  → Sent: Invalid

══════════════════════════════════════════════
  📊  Final Results
══════════════════════════════════════════════
  Valid:   2/5
  Invalid: 3/5
  Score:   100 pts
```

### When to Use Which

| Mode | Use case |
|---|---|
| **Manual** (Steps 1-5 above) | First time, want to learn the pattern |
| **verify-console.js** | Anti-fatal-error Subscan, semi-auto per record |
| **auto-verify.py** | Push to second/third wallet, already understand the pattern |

### Important Notes

- **Subscan rate-limit (HTTP 403)**: Script auto-retries with exponential backoff (45s, 90s, 135s). Don't panic if hit.
- **Manual fallback**: If parsing fails or API errors, script prompts for manual verdict input.
- **Dependencies**: `pexpect` + `requests`. Auto-install on first run. Or pre-install: `pip3 install -r requirements.txt`
- **Works in Codespace**: devcontainer pre-installs Python 3.11 + runs `pip install` in post-create.

---

## 🚨 Most Common Traps

### 1. Time Backwards (most common!)
```
startTime: 1779802200000  →  13:30
endTime:   1779801840000  →  13:24  ← backward!
```
→ **INVALID** (impossible)

### 2. VK Hash Mismatch
On-chain VK = `0x3f450a7e...de30` ≠ circuit = `0xb3fe9116...0ac5b`
→ **INVALID** (proof uses different circuit)

### 3. Timestamp Off By Seconds
```
startTime: 1779572520000  (terminal)
pubs[2]:   1779572518400  (on-chain) ← off by 1.6 seconds
```
→ **INVALID** (even 1 second off)

### 4. fillsCommitment Tail Mismatch
```
fillsCommitment[0]: 0x000...a7cc26 (terminal)
pubs[0] tail:        0x000...ecbe5 (on-chain) ← tail differs
```
→ **INVALID**

### 5. Tx Not Found
```
Extrinsic 0x903ef71d...2eb0 was not found on the zkVerify network
```
→ **INVALID** (settlement tx doesn't exist)

---

## 📋 Cheat Sheet — INVALID Markers

Transactions that are **consistently INVALID** across multiple wallets:

| Tx | Reason |
|---|---|
| `0x8de15631…70c6` | VK hash always different |
| `0x18796cf9…4660` | VK hash always different |
| `0xbccc2e93…7fd9` | Terminal randomizes forward/backwards |
| `0x2a165875…d005` | Terminal randomizes forward/backwards |

Transactions that can be VALID or INVALID depending on session:
- `0x4b5144a8…cb6c` — VALID if terminal forward, INVALID if backwards
- `0x42953c8f…7edb` — usually VALID
- `0x64e7611a…9c49` — usually VALID

---

## 🐛 Troubleshooting

### "docker: command not found"
→ Install Docker Desktop first, or open a new terminal app (not the old one).

### "Port 7878 already in use"
→ Stop old container: `docker stop $(docker ps -q)` or restart Docker.

### "Signature expired"
→ You took too long at step 3 (signing in browser). Restart from step 2.

### "Already completed this challenge"
→ This wallet has already scored 5/5. Use a different wallet.

### Subscan returns 403
→ Refresh the browser, or wait 5 minutes. Cloudflare may rate-limit your IP if you query too much.

---

## 📦 Contents of This Repo

```
.
├── README.md                    # Main tutorial (Bahasa Indonesia)
├── README.en.md                 # Main tutorial (English)
├── TUTORIAL.md                  # Codespace walkthrough (Bahasa Indonesia)
├── TUTORIAL.en.md               # Codespace walkthrough (English)
├── LICENSE                      # MIT License
├── requirements.txt             # Python deps for auto-verify
├── scripts/
│   ├── start-challenge.sh       # Bash one-liner to start the container
│   ├── verify-console.js        # Browser console helper (semi-auto per record)
│   └── auto-verify.py           # Full-auto: spawn Docker + verify + select
├── .devcontainer/
│   └── devcontainer.json        # Auto-config for Codespaces (Docker + Python 3.11)
└── .github/
    └── ISSUE_TEMPLATE/
        └── new-pattern.md       # Template for reporting new patterns
```

---

## 📚 Resources

- Challenge page: https://testnet.knidos.xyz/zkverify-task
- Subscan zkVerify: https://zkverify.subscan.io
- Docker docs: https://docs.docker.com/get-docker/
- zkVerify docs: https://docs.zkverify.io/

---

## 📜 License

MIT — free to use, modify, share. Credit appreciated but not required.

---

## 🙋 Contributing

Found a new pattern or another tx marker? Open a PR or issue — all welcome.
