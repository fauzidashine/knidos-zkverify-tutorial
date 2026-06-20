/**
 * Knidos zkVerify — Browser Console Verification Helper v2.0
 *
 * Cara pake:
 *   1. Buka halaman Subscan settlement tx di browser
 *   2. Tekan F12 (DevTools) → tab Console
 *   3. Copy-paste semua kode ini → Enter
 *   4. Prompt弹窗 bakal minta 4 baris data app — paste
 *   5. Liat banner VALID/INVALID + otomatis ke-copy ke clipboard
 *
 * Yang baru di v2.0:
 *   ✓ Fix bug innerText → outerHTML (biar pubs ke-detect)
 *   ✓ Auto-pick verdict (VALID atau INVALID) dari 5 checks
 *   ✓ Auto-copy verdict ke clipboard
 *   ✓ Big ASCII banner biar gampang dibaca
 *   ✓ Color-coded output (hijau = pass, merah = fail)
 *   ✓ Robust regex (handle JSON di <script> tag)
 */

(async function() {
  const EXPECTED_VK = '0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b';

  const url = window.location.href;
  if (!url.includes('zkverify.subscan.io/extrinsic/')) {
    console.error('%c❌ Bukan halaman Subscan settlement tx', 'color: red; font-weight: bold; font-size: 14px');
    console.log('Buka link Subscan dari terminal dulu. URL harus berisi: zkverify.subscan.io/extrinsic/0x...');
    return;
  }

  const tx = url.split('/extrinsic/')[1].split('?')[0].split('#')[0];

  const appData = prompt(
    'Paste 4 baris data dari terminal (satu nilai per baris):\n\n' +
    'Format:\n' +
    '  0x000000000000…a7cc26     <- fillsCommitment[0]\n' +
    '  0x000000000000…554a1f     <- fillsCommitment[1]\n' +
    '  1779685200000             <- startTime\n' +
    '  1779685560000             <- endTime'
  );

  if (!appData) {
    console.log('%c❌ Dibatalkan', 'color: orange');
    return;
  }

  const lines = appData.trim().split('\n').map(l => l.trim()).filter(l => l);
  if (lines.length !== 4) {
    console.error(`%c❌ Expected 4 lines, got ${lines.length}`, 'color: red; font-weight: bold');
    console.log('Format harus PERSIS 4 baris: 2 fillsCommitment + 2 timestamp angka.');
    return;
  }

  const [appFills0, appFills1, appStart, appEnd] = lines;
  const startTime = parseInt(appStart);
  const endTime = parseInt(appEnd);

  if (isNaN(startTime) || isNaN(endTime)) {
    console.error('%c❌ Line 3 & 4 harus angka (timestamp)', 'color: red; font-weight: bold');
    return;
  }

  const results = [];
  let verdict = 'VALID';

  // FIX v2.0: outerHTML nge-capture <script> tag (data Subscan di JS, bukan visible text)
  const html = document.documentElement.outerHTML;

  // Check 1: Tx exists
  results.push({ check: 'Tx exists', pass: true });
  console.log('%c✓ Tx exists', 'color: green; font-weight: bold');

  // Check 2: VK hash — robust regex untuk outerHTML
  const vkMatch = html.match(/"Hash"\s*:\s*"(0x[a-f0-9]{64})"/);
  if (!vkMatch) {
    results.push({ check: 'VK hash', pass: false, detail: 'not found' });
    verdict = 'INVALID';
    console.log('%c✗ VK hash — not found in page', 'color: red; font-weight: bold');
    console.log('   Kemungkinan: Subscan ganti struktur, atau JS belum load. Refresh halaman.');
  } else if (vkMatch[1].toLowerCase() !== EXPECTED_VK.toLowerCase()) {
    results.push({ check: 'VK hash', pass: false, detail: 'mismatch' });
    verdict = 'INVALID';
    console.log('%c✗ VK hash mismatch', 'color: red; font-weight: bold');
    console.log(`   on-chain: ${vkMatch[1]}`);
    console.log(`   expected: ${EXPECTED_VK}`);
  } else {
    results.push({ check: 'VK hash', pass: true });
    console.log('%c✓ VK hash match', 'color: green; font-weight: bold');
  }

  // Check 3: Time forward (startTime < endTime)
  if (startTime >= endTime) {
    results.push({ check: 'Time forward', pass: false, detail: 'time backwards' });
    verdict = 'INVALID';
    console.log('%c✗ Time backwards', 'color: red; font-weight: bold');
    console.log(`   startTime: ${startTime}`);
    console.log(`   endTime:   ${endTime}`);
  } else {
    results.push({ check: 'Time forward', pass: true, detail: `${endTime - startTime}ms window` });
    console.log(`%c✓ Time forward (${endTime - startTime}ms window)`, 'color: green; font-weight: bold');
  }

  // Extract pubs — FIXED regex untuk outerHTML
  const pubsMatch = html.match(/"pubs"\s*:\s*\[([^\]]+)\]/);
  if (!pubsMatch) {
    results.push({ check: 'pubs extract', pass: false, detail: 'pubs not found' });
    verdict = 'INVALID';
    console.log('%c✗ pubs not found in page', 'color: red; font-weight: bold');
    console.log('   Fix: refresh Subscan page, tunggu 2-3 detik, re-run script ini.');
  } else {
    const pubs = [...pubsMatch[1].matchAll(/0x[0-9a-f]{64}/g)].map(m => m[0]);

    if (pubs.length < 4) {
      results.push({ check: 'pubs count', pass: false, detail: `got ${pubs.length}` });
      verdict = 'INVALID';
      console.log(`%c✗ Expected 4 pubs, got ${pubs.length}`, 'color: red; font-weight: bold');
      console.log('   Raw block:', pubsMatch[1].slice(0, 200));
    } else {
      console.log(`%c✓ pubs extracted (${pubs.length} values)`, 'color: gray');

      // Check 4: Timestamps exact match
      const onStart = parseInt(pubs[2].slice(-13), 16);
      const onEnd = parseInt(pubs[3].slice(-13), 16);

      if (onStart !== startTime) {
        results.push({ check: 'Timestamp start', pass: false, detail: `${Math.abs(onStart - startTime)}ms diff` });
        verdict = 'INVALID';
        console.log('%c✗ Timestamp mismatch (startTime)', 'color: red; font-weight: bold');
        console.log(`   pubs[2]:    ${onStart}`);
        console.log(`   app:        ${startTime}`);
        console.log(`   diff:       ${Math.abs(onStart - startTime)}ms`);
      } else if (onEnd !== endTime) {
        results.push({ check: 'Timestamp end', pass: false, detail: `${Math.abs(onEnd - endTime)}ms diff` });
        verdict = 'INVALID';
        console.log('%c✗ Timestamp mismatch (endTime)', 'color: red; font-weight: bold');
        console.log(`   pubs[3]:    ${onEnd}`);
        console.log(`   app:        ${endTime}`);
        console.log(`   diff:       ${Math.abs(onEnd - endTime)}ms`);
      } else {
        results.push({ check: 'Timestamps', pass: true });
        console.log('%c✓ Timestamps exact match', 'color: green; font-weight: bold');
      }

      // Check 5: fillsCommitment head/tail match
      function extractTail(s) {
        return s.includes('…') ? s.split('…')[1] : s.slice(-6);
      }
      function extractHead(s) {
        if (s.includes('…')) return s.split('…')[0].replace(/^0x/, '');
        return s.slice(2, -6);
      }

      let fillsOk = true;
      for (let i = 0; i < 2; i++) {
        const app = i === 0 ? appFills0 : appFills1;
        const on = pubs[i];
        const appHead = extractHead(app);
        const appTail = extractTail(app);
        const onStrip = on.slice(2);

        if (!onStrip.startsWith(appHead) || !onStrip.endsWith(appTail)) {
          results.push({ check: `fillsCommitment[${i}]`, pass: false, detail: 'head/tail mismatch' });
          fillsOk = false;
          verdict = 'INVALID';
          console.log(`%c✗ fillsCommitment[${i}] mismatch`, 'color: red; font-weight: bold');
          console.log(`   app head: ${appHead}`);
          console.log(`   app tail: ...${appTail}`);
          console.log(`   on head:  ${onStrip.slice(0, appHead.length)}`);
          console.log(`   on tail:  ...${onStrip.slice(-6)}`);
        }
      }
      if (fillsOk) {
        results.push({ check: 'fillsCommitment', pass: true });
        console.log('%c✓ fillsCommitment match', 'color: green; font-weight: bold');
      }
    }
  }

  // ============ FINAL VERDICT (auto-pick) ============
  const isValid = verdict === 'VALID';
  const banner = isValid
    ? '\n╔════════════════════════════════════════╗\n║                                        ║\n║      ✅  ANSWER: VALID                 ║\n║                                        ║\n║   📋 Copied to clipboard — paste di    ║\n║      TUI prompt buat auto-input.       ║\n║                                        ║\n╚════════════════════════════════════════╝\n'
    : '\n╔════════════════════════════════════════╗\n║                                        ║\n║      ❌  ANSWER: INVALID               ║\n║                                        ║\n║   📋 Copied to clipboard — paste di    ║\n║      TUI prompt buat auto-input.       ║\n║                                        ║\n╚════════════════════════════════════════╝\n';

  const bannerColor = isValid
    ? 'color: green; font-size: 14px; font-weight: bold; background: #f0fff0; padding: 8px'
    : 'color: red; font-size: 14px; font-weight: bold; background: #fff0f0; padding: 8px';
  console.log('%c' + banner, bannerColor);

  // Auto-copy verdict ke clipboard (HTTPS Subscan supports clipboard API)
  try {
    await navigator.clipboard.writeText(verdict);
    console.log(`%c📋 "${verdict}" copied! Tinggal paste (Ctrl+V / Cmd+V) di TUI challenge.`, 'color: blue; font-weight: bold');
  } catch (e) {
    console.log(`%c⚠️ Clipboard blocked (${e.name}). Manual: type "${verdict}" di TUI.`, 'color: orange; font-weight: bold');
  }

  // Summary table
  console.log('\n%c═══ Verification Summary ═══', 'font-weight: bold; font-size: 13px');
  console.log(`%cTx:           ${tx.slice(0, 10)}...${tx.slice(-6)}`, 'color: gray');
  results.forEach(r => {
    const sym = r.pass ? '✓' : '✗';
    const c = r.pass ? 'green' : 'red';
    console.log(`%c${sym} ${r.check.padEnd(22)} ${r.detail || ''}`, `color: ${c}`);
  });
  console.log(`%cFinal verdict: ${verdict}`, `color: ${isValid ? 'green' : 'red'}; font-weight: bold; font-size: 14px`);

  return verdict;
})();
