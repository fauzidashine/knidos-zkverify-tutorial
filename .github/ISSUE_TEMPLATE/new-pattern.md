name: New INVALID/VALID Pattern
description: Report a new tx hash or invalid pattern you found
labels: enhancement, patterns

---

## Tx Hash
`0x...`

## Block
(block number)

## VK hash on-chain
`0x...`

## What was the verdict?
- [ ] VALID
- [ ] INVALID

## Why invalid? (if applicable)
- [ ] Time backwards (st > et)
- [ ] VK hash mismatch (different from circuit `0xb3fe9116...0ac5b`)
- [ ] Timestamp off (pubs[2/3] ≠ startTime/endTime)
- [ ] fillsCommitment tail mismatch
- [ ] Tx not found on zkVerify
- [ ] Other (explain)

## How often did you see this pattern?
- [ ] Once
- [ ] Every time (consistent marker)
- [ ] Sometimes (depends on session)

## Screenshot (optional)
[Attach if helpful]
