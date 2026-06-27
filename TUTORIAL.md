# Tutorial: Auto-Verify Knidos zkVerify Challenge

> 🌐 **Bahasa:** 🇮🇩 [Bahasa Indonesia](TUTORIAL.md) · 🇬🇧 [English](TUTORIAL.en.md)

Verifikasi 5 record ZK proof di [testnet.knidos.xyz/zkverify-task](https://testnet.knidos.xyz/zkverify-task) secara otomatis pakai **GitHub Codespaces**. Total ~5 menit setup + ~5 menit run. Bisa dapet sampe **250 pts + badge ZK Verifier** per wallet.

## Yang Lo Butuhin

| Kebutuhan | Detail |
|---|---|
| Akun GitHub | Buat Codespace (gratis 60 jam/bulan) |
| Browser | Chrome/Edge/Brave + extension MetaMask atau Rabby |
| Wallet address | Yang punya extension. Bisa wallet baru, gak perlu ada dana |

## Step 1 — Buka Codespace

1. Buka repo ini: **https://github.com/fauzidashine/knidos-zkverify-tutorial**
2. Klik tombol hijau **`<> Code`** (di atas file list, kanan)
3. Klik tab **Codespaces**
4. Klik **"+ Create codespace on main"**
5. Browser bakal nge-load VS Code di tab baru. Tunggu ~60 detik sampe terminal di bawah keliatan.

Codespace otomatis setup Docker + forward port 7878. Lo gak perlu install apa-apa.

## Step 2 — Pre-pull Docker Image

**Copy-paste ini ke terminal Codespace, terus Enter:**

```bash
docker pull ghcr.io/node101-io/knidos-challenge:latest
```

First pull butuh **5-15 menit** (image 225MB). Sabar, jangan Ctrl+C. Kalo udah pernah pull, jadi instant.

**Verify udah cached:**
```bash
docker images | grep knidos
```

Kalo keluar baris dengan `225MB`, lanjut Step 3. Kalo gak ada, tunggu pull sampe kelar.

## Step 3 — Install Python Deps

```bash
pip3 install --user pexpect requests
```

Output harusnya `Successfully installed ...` atau `Requirement already satisfied`. Kalo error, coba:
```bash
pip3 install --user --break-system-packages pexpect requests
```

## Step 4 — Run Auto-Verify

```bash
python3 scripts/auto-verify.py
```

**Output yang normal (~1-2 menit pertama):**

```
════════════════════════════════════════════════════════
  🧪  Knidos zkVerify Auto-Verify (Codespace Edition)
════════════════════════════════════════════════════════

▶ Phase 1: Spawning Docker challenge...
▶ Phase 2: Compiling circuit + deriving VK (~60-90s)...
✓ Circuit + VK ready.

────────────────────────────────────────────────────────
  ⚡  SIGN WALLET DI BROWSER (port 7878)
  1. Buka tab PORTS → klik globe di samping 7878
  2. Connect wallet + sign message
  3. Balik ke terminal ini, tekan Enter
────────────────────────────────────────────────────────
```

## Step 5 — Sign Wallet

1. Di Codespace, klik tab **PORTS** (di panel bawah, sebelah tab "Terminal")
2. Cari port **7878** → klik **icon globe** 🌐 di kolom "Forwarded Address"
3. Tab browser baru kebuka
4. MetaMask/Rabby popup minta **Sign message** → klik **Sign**
5. Tunggu 5-10 detik
6. Balik ke Codespace tab → **klik di area terminal** → tekan **Enter**

## Step 6 — Tunggu Auto-Verify Selesai

**Sekarang tinggal tunggu.** Jangan klik/sentuh apa-apa. Script bakal loop 5 records:

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
  ... (lanjut otomatis)
```

Tiap record butuh **20-60 detik** (Subscan API kadang rate-limited, script auto-retry). Total 5 records ≈ **3-5 menit**.

## Step 7 — Cek Hasil

Setelah 5 records selesai, terminal print:

```
════════════════════════════════════════════════════════
  FINAL SCORE
════════════════════════════════════════════════════════
  ✅ Correct: 5/5
  Total points: 250
```

Skor sync ke leaderboard **per jam** (bukan instant). Cek di:
**https://testnet.knidos.xyz/leaderboard**

5/5 correct = badge **ZK Verifier** ke-unlock.

---

## Troubleshooting

### Codespace gak muncul port 7878

Tunggu 30 detik setelah Codespace ready. Kalo masih gak ada, klik tab PORTS → "Add Port" → ketik `7878` → Enter.

### `docker: command not found`

Codespace butuh waktu start Docker daemon. Tunggu 1 menit, retry command.

### Stuck di "Compiling circuit" > 5 menit

Internet Codespace lambat. Cancel (Ctrl+C), terus retry:
```bash
python3 scripts/auto-verify.py
```

### Stuck di "Waiting for TUI prompt"

TUI Clack ke-blok. Cara fix:
1. Buka tab PORTS 7878 di browser → **refresh page**
2. Sign ulang kalo diminta
3. Balik terminal → tekan Enter
4. Kalo masih stuck, Ctrl+C → run ulang dari Step 4

### `Subscan rate-limit (403)` spam di output

Normal. Script auto-retry dengan jeda 45s → 90s → 135s. Sabar, jangan cancel.

### Wallet sign-in gak ke-detect

1. Pastikan MetaMask/Rabby udah unlock
2. Refresh tab PORTS 7878 → sign ulang
3. Klik di terminal → tekan Enter sekali lagi

### 5 records selesai tapi leaderboard gak update

Tunggu sampe **1 jam** (sync period). Kalo 24 jam masih 0:
- Kemungkinan judge script salah baca data
- Run ulang script (Step 4) — retry masih dapet poin

### Mau pake wallet beda

Hapus Codespace lama dulu (supaya container fresh):
1. Codespace tab → klik nama Codespace → **Stop** → confirm
2. Balik ke repo → klik **Code → Codespaces → "+"** → bikin baru
3. Ulangi dari Step 2

---

## Cara Kerja (baca kalo penasaran)

```
┌─────────────────────────────────────────────────────────────┐
│  scripts/auto-verify.py                                     │
│                                                             │
│  1. Spawn Docker container (Knidos challenge app)           │
│  2. Tunggu circuit compile + VK ready (~60-90s)             │
│  3. Buka web UI di port 7878 → user sign wallet             │
│  4. Loop 5 records:                                         │
│     a. Parse terminal output (fillsCommitment, timestamps)  │
│     b. Query Subscan API buat on-chain data                 │
│     c. 5 boolean checks (VK, time, fills, timestamps, tx)   │
│     d. Kirim ↑↓+Enter ke TUI Clack otomatis                │
│  5. Print final score + decline "Try again"                 │
└─────────────────────────────────────────────────────────────┘
```

Yang script lakuin per record:
- **VK check**: cocokin VK hash di TUI vs on-chain
- **Time check**: pastikan `startTime < endTime`
- **Timestamps check**: cocokin sama `pubs[2]`/`pubs[3]` on-chain
- **Fills check**: cocokin `fillsCommitment[0]`/`[1]` head+tail (tengah truncated)
- **Tx check**: settlement tx beneran exist di zkVerify

5 check pass → VALID. Ada 1 gagal → INVALID. Mayoritas record emang INVALID by design — tantangannya deteksi korup, bukan validate valid records.

---

## File-file di Repo Ini

| File | Fungsi |
|---|---|
| `scripts/auto-verify.py` | Full auto (ini yang dipake di tutorial) |
| `scripts/verify-console.js` | Semi-manual: paste di browser console Subscan |
| `scripts/start-challenge.sh` | Bash helper buat jalanin container manual |
| `.devcontainer/devcontainer.json` | Codespace auto-setup (Docker + Python) |
| `README.md` | Gambaran umum challenge |

---

## Credits

Repo ini bagian dari kontribusi komunitas Knidos. Docker image dari `ghcr.io/node101-io/knidos-challenge`. Script `auto-verify.py` ditulis pakai `pexpect` + `requests`, inspired dari pattern testing ZK proof verification di production.
