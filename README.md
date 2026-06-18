# 🎯 Knidos zkVerify Challenge — Tutorial

Tutorial step-by-step buat selesaikan Knidos **"Verify a ZK Proof Manually"** challenge di testnet dengan score **5/5 perfect + 250 points + ZK Verifier badge**.

🔗 Challenge: https://testnet.knidos.xyz/zkverify-task

---

## 💰 Yang Lo Dapet

| Hasil | Poin | Badge |
|---|---|---|
| 5/5 correct | **250 pts** | ✅ ZK Verifier |
| 4/5 correct | 200 pts | ❌ |
| ≤3/5 correct | < 150 pts | ❌ |

**Bonus**: bisa pake banyak wallet — tiap wallet baru = +250 pts + badge baru. Ga ada cap jumlah wallet.

---

## 🛠 Yang Dibutuhin

1. **PC / laptop** (Windows / macOS / Linux)
2. **Docker Desktop** — https://docs.docker.com/get-docker/
3. **Browser** (Chrome / Firefox)
4. **Crypto wallet** (MetaMask / Rabby) — udah ada signature
5. **±10 menit** waktu per wallet

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

## ⚙️ Setup Multi-Wallet

Lo bisa pake banyak wallet — tiap wallet = +250 pts. Tiap wallet:
1. Pake wallet address beda di MetaMask/Rabby
2. Sign di browser
3. Selesai challenge → dapet 250 pts + badge

**Strategi:** bikin 3-5 wallet di MetaMask, kerjain semuanya.

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
├── scripts/
│   ├── start-challenge.sh       # Bash one-liner buat start container
│   └── verify-console.js        # Browser console helper buat verify
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
