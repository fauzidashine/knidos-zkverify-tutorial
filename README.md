# 🎯 Knidos zkVerify Challenge — Tutorial

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=fauzidashine/knidos-zkverify-tutorial)

> 🌐 **Bahasa:** 🇮🇩 [Bahasa Indonesia](README.md) · 🇬🇧 [English](README.en.md)

Tutorial step-by-step buat selesaikan Knidos **"Verify a ZK Proof Manually"** challenge di testnet dengan score **5/5 perfect + 250 points + ZK Verifier badge**.

🔗 Challenge: https://testnet.knidos.xyz/zkverify-task

---

## 💰 Yang Lo Dapet

| Hasil | Poin | Badge |
|---|---|---|
| 5/5 correct | **250 pts** | ✅ ZK Verifier |
| 4/5 correct | 200 pts | ❌ |
| ≤3/5 correct | < 150 pts | ❌ |

---

## 🛠 Yang Dibutuhin

1. **Device apapun** yang bisa install Docker (PC / laptop / cloud VM / Chromebook via Linux)
2. **Docker** (Desktop atau Engine — lihat [Alternatif Docker](#-alternatif-docker) di bawah kalo bukan Windows/Mac)
3. **Browser** (Chrome / Firefox)
4. **Crypto wallet** (MetaMask / Rabby) — udah ada signature
5. **±10 menit** waktu per wallet

---

## 💻 Alternatif Docker

Ga punya Windows/Mac Desktop? Tenang, banyak opsi:

### 1. **Linux Native** (paling simple buat Linux user)

Install Docker Engine langsung — ga perlu Desktop:

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Logout & login lagi, atau:
newgrp docker

# Verify
docker --version
```

**Cocok untuk:** Ubuntu, Debian, Fedora, Arch, Mint, dll.

### 2. **WSL2** (Windows 10/11 tanpa Hyper-V)

1. Enable WSL: `wsl --install` (di PowerShell admin)
2. Install Ubuntu dari Microsoft Store
3. Di dalam Ubuntu, install Docker Engine (sama kayak Linux native di atas)
4. **WAJIB** enable Docker Desktop WSL2 integration, ATAU jalankan Docker di WSL2 langsung tanpa Desktop

```powershell
# PowerShell (admin)
wsl --install
wsl --set-default-version 2
```

Lalu di dalam WSL2 Ubuntu:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Cocok untuk:** Windows Home edition (ga punya Hyper-V), atau user yang lebih suka Linux env.

### 3. **Cloud VM Gratis** (ga punya PC sama sekali)

Spin up Linux VM di cloud — Docker pre-installed atau tinggal install:

| Provider | Free Tier | Setup |
|---|---|---|
| **Oracle Cloud** | 2 VM永久免费 (ARM, 4 CPU / 24GB RAM) | Sign up, bikin VM, SSH, install Docker |
| **Google Cloud** | $300 credit / 90 hari | `gcloud compute ssh`, install Docker |
| **AWS** | t2.micro / 12 bulan | `ssh -i key.pem ubuntu@vm`, install Docker |
| **Hetzner** | Cloud VM murah (~€4/mo) | Paling cepet, ga perlu credit card banyak |

**Paling recommended: Oracle Cloud** — kalo qualify, dapet 2 VM永久免费 yang bisa dipake selamanya.

Quick setup (Oracle Cloud):
```bash
# SSH ke VM
ssh ubuntu@<public-ip>

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# SSH tunnel supaya localhost:7878 ke-expose ke PC lo
# (Karena browser lo di PC, VM di cloud)
ssh -L 7878:localhost:7878 ubuntu@<public-ip>
```

Lalu buka `http://localhost:7878` di browser PC lo.

### 4. **GitHub Codespaces** (ga install apa-apa) ⭐ **PALING GAMPANG**

Paling cepet kalo cuma mau coba-coba — **langsung jalan dari browser HP/laptop manapun**:

1. Klik badge **"Open in GitHub Codespaces"** di atas README ini, **ATAU** buka repo → tombol hijau **"Code"** → tab **"Codespaces"** → **"Create codespace on main"**
2. Tunggu ~60 detik, dapet **VS Code di browser + Ubuntu container + Docker pre-installed** (auto-install via `.devcontainer/devcontainer.json`)
3. Di terminal Codespace, jalanin:
   ```bash
   docker run --pull=always -it -p 7878:7878 ghcr.io/node101-io/knidos-challenge:latest
   ```
4. Codespace otomatis **deteksi port 7878** dan kasih notifikasi "Open in Browser" — klik
5. Atau buka tab **"Ports"** di VS Code → klik ikon globe di sebelah port 7878 (visibility auto set ke public via devcontainer config)
6. URL format: `https://xxx-7878.app.github.dev`

**Free tier:** 60 jam/bulan untuk akun personal. Cukup buat kerjain banyak wallet.

**Auto-forward:** Port 7878 udah ke-config di `.devcontainer/devcontainer.json` jadi langsung auto-forward tanpa setting manual.

**Stop codespace** kalo udah selesai biar ga ke-bill: klik `Ctrl+Shift+P` → "Codespaces: Stop Current Codespace"

### 5. **Android (Termux + QEMU)** (advanced)

Bisa, tapi ribet:
1. Install Termux dari F-Droid
2. Install proot-distro: `pkg install proot-distro && proot-distro install ubuntu`
3. Masuk Ubuntu: `proot-distro login ubuntu`
4. Install Docker (limited — perlu qemu-user untuk emulate)
5. Forward port via SSH tunnel ke HP lain atau pakai `termux-wake-lock`

**Tidak direkomendasikan** — lebih banyak masalah daripada solusi.

### 6. **iOS** (sangat terbatas)

iOS ga support Docker natively. Harus pakai opsi cloud VM (nomor 3) atau GitHub Codespaces (nomor 4).

---

## 🚀 Step-by-Step

### Step 1: Install Docker

1. Download Docker Desktop di https://docs.docker.com/get-docker/
2. Install & **buka aplikasinya** (jangan di-close)
3. Verifikasi dengan buka terminal:
   ```bash
   docker --version
   ```

### Step 2: Jalanin Container

Buka **terminal / command prompt** (jangan di dalam Docker app):

- **Windows**: `Win+R` → ketik `cmd` → Enter
- **macOS**: buka "Terminal"
- **Linux**: langsung buka terminal

Copy-paste command ini:

```bash
docker run --pull=always -it -p 7878:7878 ghcr.io/node101-io/knidos-challenge:latest
```

**Yang terjadi:**
- Docker download image (~100MB, first time only)
- Container jalan di background
- Terminal nampilin URL `http://127.0.0.1:7878` + sign-in prompt

### Step 3: Sign Wallet

1. Buka browser
2. Pergi ke **http://localhost:7878**
3. Pastikan wallet lo udah ke-connect (MetaMask/Rabby)
4. **Sign** pesan yang muncul
5. **Balik ke terminal SEBELUM 10 menit** (signature expire)

Setelah sign:
- Container compile circuit (~30 detik)
- Container derive verification key (~10-30 detik)
- Muncul **Record 1/5** dengan data settlement tx

### Step 4: Verifikasi 5 Records

Tiap record, terminal nampilin:

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

### 5 Cek Wajib

Buat tiap record, cek **5 hal ini** ke Subscan:

| # | Check | Lihat di Subscan | Mark INVALID kalau |
|---|---|---|---|
| 1 | **Tx exists** | Page normal, bukan error | "Extrinsic not found on the zkVerify network" |
| 2 | **VK hash match** | `Parameters` → `vk_or_hash.Hash` | ≠ `0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b` |
| 3 | **Time forward** | startTime vs endTime di terminal | startTime > endTime |
| 4 | **Timestamps exact** | Lihat [Verifikasi Cepat](#-verifikasi-cepat) di bawah | Ada diff (bahkan 1 detik) |
| 5 | **fillsCommitment match** | Lihat [Verifikasi Cepat](#-verifikasi-cepat) di bawah | Tail hex beda |

#### Cek #4 & #5 — Verifikasi Cepat

1. Di halaman Subscan, tekan **F12** (DevTools)
2. Klik tab **Console**
3. Paste code dari [`scripts/verify-console.js`](./scripts/verify-console.js) → Enter
4. Lo bakal diminta paste data terminal — copy baris `fillsCommitment[0]`, `fillsCommitment[1]`, `startTime`, `endTime` ke prompt
5. Output nampilin 5 check results + rekomendasi (VALID atau INVALID)

#### Cek #2 — VK Hash

Di halaman Subscan, lihat **Parameters** section:
- Expand `0.vk_or_hash.value.Hash`
- Harus = `0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b`
- **Kalo beda (kayak `0x3f450a7e...de30`)** → INVALID

### Step 5: Submit Jawaban

Setelah cek 5 hal:
- **Semua pass** → `Valid` (Enter)
- **Ada 1 yg fail** → `↓` (arrow down) → `Invalid` (Enter)

Ulangi untuk 5 records. Habis submit ke-5:

```
5/5 correct — your answers have been recorded.
🎉 A perfect run — every record correct.
```

🎉 **Done!** 250 pts + ZK Verifier badge masuk.

---

## 🤖 Auto-Verify Mode (Codespace Edition)

Males klik Valid/Invalid 5 kali? Pake auto-verify:

```bash
python3 scripts/auto-verify.py
```

Script ini ngegantiin semua step manual:
1. Spawn Docker container otomatis
2. Wait circuit compile + VK derivation
3. Prompt: "sign wallet di browser, tekan Enter"
4. Loop 5 records:
   - Parse data record dari terminal output
   - Verify via Subscan API (5 checks: VK, time, timestamps, fillsCommitment)
   - Auto-select Valid/Invalid di TUI prompt
5. Show final score + per-record verdict

**Total interaction:** Sign wallet di browser + 1 Enter. Sisanya auto.

### Output Contoh

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

### Kapan Pakai Yang Mana

| Mode | Use case |
|---|---|
| **Manual** (Step 1-5 di atas) | First time, mau belajar pattern-nya |
| **verify-console.js** | Anti-fatal error Subscan, semi-auto per record |
| **auto-verify.py** | Push ke wallet kedua/ketiga, udah ngerti polanya |

### Catatan Penting

- **Subscan rate-limit (HTTP 403)**: Script auto-retry dengan exponential backoff (45s, 90s, 135s). Kalo kena, jangan panik.
- **Manual fallback**: Kalo parsing gagal atau API error, script prompt manual input verdict.
- **Dependencies**: `pexpect` + `requests`. Auto-install di first run. Atau pre-install: `pip3 install -r requirements.txt`
- **Works di Codespace**: devcontainer udah pre-install Python 3.11 + run `pip install` di post-create.

---

## 🚨 Jebakan Paling Sering

### 1. Time Backwards (paling sering!)
```
startTime: 1779802200000  →  13:30
endTime:   1779801840000  →  13:24  ← backward!
```
→ **INVALID** (impossible)

### 2. VK Hash Mismatch
On-chain VK = `0x3f450a7e...de30` ≠ circuit = `0xb3fe9116...0ac5b`
→ **INVALID** (proof pake circuit beda)

### 3. Timestamp Off By Seconds
```
startTime: 1779572520000  (terminal)
pubs[2]:   1779572518400  (on-chain) ← off 1.6 detik
```
→ **INVALID** (even 1 second off)

### 4. fillsCommitment Tail Mismatch
```
fillsCommitment[0]: 0x000...a7cc26 (terminal)
pubs[0] tail:        0x000...ecbe5 (on-chain) ← tail beda
```
→ **INVALID**

### 5. Tx Not Found
```
Extrinsic 0x903ef71d...2eb0 was not found on the zkVerify network
```
→ **INVALID** (settlement tx ga exist)

---

## 📋 Cheat Sheet — INVALID Markers

Transaksi yang **konsisten INVALID** across multiple wallets:

| Tx | Alasan |
|---|---|
| `0x8de15631…70c6` | VK hash selalu beda |
| `0x18796cf9…4660` | VK hash selalu beda |
| `0xbccc2e93…7fd9` | Terminal random forward/backwards |
| `0x2a165875…d005` | Terminal random forward/backwards |

Transaksi yang bisa VALID atau INVALID tergantung session:
- `0x4b5144a8…cb6c` — VALID kalo terminal forward, INVALID kalo backwards
- `0x42953c8f…7edb` — biasanya VALID
- `0x64e7611a…9c49` — biasanya VALID

---

## 🐛 Troubleshooting

### "docker: command not found"
→ Install Docker Desktop dulu, atau buka terminal app yang baru (bukan terminal lama).

### "Port 7878 already in use"
→ Stop container lama: `docker stop $(docker ps -q)` atau restart Docker.

### "Signature expired"
→ Lo kelamaan di step 3 (sign di browser). Restart dari step 2.

### "Already completed this challenge"
→ Wallet ini udah pernah 5/5. Pake wallet lain.

### Subscan return 403
→ Refresh browser, atau tunggu 5 menit. Cloudflare bisa rate-limit IP lo kalo kebanyakan query.

---

## 📦 Isi Repo Ini

```
.
├── README.md                    # Tutorial utama (file ini)
├── LICENSE                      # MIT License
├── requirements.txt             # Python deps buat auto-verify
├── scripts/
│   ├── start-challenge.sh       # Bash one-liner buat start container
│   ├── verify-console.js        # Browser console helper (semi-auto per record)
│   └── auto-verify.py           # Full-auto: spawn Docker + verify + select
├── .devcontainer/
│   └── devcontainer.json        # Auto-config Codespaces (Docker + Python 3.11)
└── .github/
    └── ISSUE_TEMPLATE/
        └── new-pattern.md       # Template buat report pola baru
```

---

## 📚 Resources

- Challenge page: https://testnet.knidos.xyz/zkverify-task
- Subscan zkVerify: https://zkverify.subscan.io
- Docker docs: https://docs.docker.com/get-docker/
- zkVerify docs: https://docs.zkverify.io/

---

## 📜 License

MIT — bebas dipake, diedit, di-share. Credit appreciated tapi ga wajib.

---

## 🙋 Kontribusi

Lo nemu pola baru atau tx marker lain? Buka PR atau issue — semua welcome.
