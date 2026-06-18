/**
 * Knidos zkVerify — Browser Console Verification Helper
 * 
 * Cara pake:
 *   1. Buka halaman Subscan settlement tx di browser
 *   2. Tekan F12 (DevTools) → tab Console
 *   3. Copy-paste semua kode ini → Enter
 *   4. Liat output: PASS atau FAIL per check
 * 
 * Output format:
 *   ✓ Tx exists
 *   ✓ VK hash match
 *   ✓ Time forward
 *   ✓ Timestamp match
 *   ✓ fillsCommitment match
 * 
 * Atau kalau ada yang fail:
 *   ✗ Timestamp match
 *     pubs[2] on-chain = 1779572518400
 *     startTime from app = 1779572520000
 *     diff = 1600ms
 */

(async function() {
  const EXPECTED_VK = '0xb3fe911644c664fb0b3b7c72879d7a366e0df1a740888cca034934210630ac5b';
  
  // Get terminal data from URL (user must paste manually, see prompt)
  const url = window.location.href;
  if (!url.includes('zkverify.subscan.io/extrinsic/')) {
    return '❌ Bukan halaman Subscan settlement tx. Buka link Subscan dari terminal dulu.';
  }
  
  const tx = url.split('/extrinsic/')[1];
  
  // Read app data from terminal paste (user must run prompt() to enter)
  const appData = prompt(
    'Paste data dari terminal di sini (copy baris fillsCommitment/startTime/endTime):\n\n' +
    'Contoh:\n' +
    '0x000000000000…a7cc26\n' +
    '0x000000000000…554a1f\n' +
    '1779685200000\n' +
    '1779685560000'
  );
  
  if (!appData) return '❌ Dibatalkan';
  
  const lines = appData.trim().split('\n').map(l => l.trim());
  if (lines.length !== 4) return `❌ Expected 4 lines, got ${lines.length}`;
  
  const [appFills0, appFills1, appStart, appEnd] = lines;
  const startTime = parseInt(appStart);
  const endTime = parseInt(appEnd);
  
  const results = [];
  
  // Check 1: Tx exists (we're here so it does)
  results.push('✓ Tx exists');
  
  // Get page content
  const html = document.body.innerText;
  
  // Check 2: VK hash
  const vkMatch = html.match(/"Hash":"(0x[a-f0-9]{64})"/);
  if (!vkMatch) {
    results.push('✗ VK hash — not found in page (JS might not have loaded)');
  } else if (vkMatch[1].toLowerCase() !== EXPECTED_VK.toLowerCase()) {
    results.push(`✗ VK hash mismatch\n   on-chain: ${vkMatch[1]}\n   expected: ${EXPECTED_VK}`);
  } else {
    results.push('✓ VK hash match');
  }
  
  // Check 3: Time forward
  if (startTime >= endTime) {
    results.push(`✗ Time backwards\n   startTime: ${startTime}\n   endTime:   ${endTime}`);
  } else {
    results.push(`✓ Time forward (${endTime - startTime}ms window)`);
  }
  
  // Get pubs
  const pubsMatch = html.match(/"pubs".*?\]/s);
  if (!pubsMatch) {
    results.push('✗ pubs not found in page');
    return results.join('\n');
  }
  
  const pubs = [...pubsMatch[0].matchAll(/"0x[0-9a-f]{64}"/g)].map(m => m[0].slice(1, -1));
  
  if (pubs.length < 4) {
    results.push(`✗ Expected 4 pubs, got ${pubs.length}`);
    return results.join('\n');
  }
  
  // Check 4: Timestamps exact match
  const onStart = parseInt(pubs[2].slice(-13), 16);
  const onEnd = parseInt(pubs[3].slice(-13), 16);
  
  if (onStart !== startTime) {
    results.push(`✗ Timestamp mismatch (startTime)\n   pubs[2]:    ${onStart}\n   app:        ${startTime}\n   diff:       ${Math.abs(onStart - startTime)}ms`);
  } else if (onEnd !== endTime) {
    results.push(`✗ Timestamp mismatch (endTime)\n   pubs[3]:    ${onEnd}\n   app:        ${endTime}\n   diff:       ${Math.abs(onEnd - endTime)}ms`);
  } else {
    results.push('✓ Timestamps exact match');
  }
  
  // Check 5: fillsCommitment tail match
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
      results.push(`✗ fillsCommitment[${i}] tail mismatch\n   app: ...${appTail}\n   on:  ...${onStrip.slice(-6)}`);
      fillsOk = false;
    }
  }
  if (fillsOk) results.push('✓ fillsCommitment match');
  
  // Summary
  const failCount = results.filter(r => r.startsWith('✗')).length;
  const summary = failCount === 0
    ? `\n🎉 ALL CHECKS PASS → Mark VALID`
    : `\n❌ ${failCount} check(s) fail → Mark INVALID`;
  
  return results.join('\n') + summary;
})();
