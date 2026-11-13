# Proof of copying: 1 of 1 opens follow the trader ✅

Checked **Nov 13 2026, 11:28 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/43417359334), from Hyperliquid's public record only (no MrCopyTrading server).
Last 7 days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

## Copy wallet 0xde7d…67f7 · copies 0xf97a…ddd1, 0x1e5c…0ac1

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-11-07 23:15 | HYPE | Close Long | 0.15 @ 77.407 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x03ebc40628ad8ac4056504484d9ad001e200dbebc3a0a996a7b46f58e7a164ae) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | HYPE | Open Short | 0.21 @ 77.407 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x09072858a0de9eaf0a8004484d9adb01e600403e3bd1bd81accfd3ab5fd27899) | 0x1e5c…0ac1 held short 1557.11 HYPE at that moment (copy start / catch-up) |
| 2026-11-07 23:15 | xyz:INTC | Close Long | 0.35 @ 56.066 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xeac7116c5fbd075cec4004484d9ae602018d0051fab0262e8e8fbcbf1eb0e147) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | xyz:LITE | Close Long | 0.018 @ 537.09 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x2fa4c8d7441a1c14311e04484d9aef0201d600bcdf1d3ae6d36d742a031df5fe) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | xyz:MRVL | Close Long | 0.06 @ 141.28 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xaa79354549041353abf204484d9af902024b002ae40732254e41e0980807ed3e) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | HYPE | Close Short | 0.21 @ 77.38 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x6cf678d20713edcc6e7004484d9c5f02025600b7a2170c9e10bf2424c617c7b7) | close (the trader closed, a stop, or a stop-loss: always allowed) |

## Copy wallet 0xc812…65f4 · copies 0x720c…f4af

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-11-09 13:13 | xyz:SOXL | Close Long | 0.26 @ 47.173 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x948d1dec12b24962960604486b061302059c00d1adb568343855c93ed1b6234d) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x2990d6801db9a5ea2b0a04486b05f80201930065b8bcc4bccd5981d2dcbd7fd4) |
| 2026-11-09 14:55 | xyz:SOXL | Close Long | 0.27 @ 52.15 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x2e5598368646bd342fcf04486c57630209ad001c2149dc06d21e4389454a971e) | 0x720c…f4af Close Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x8ef87aceb9742803907204486c572702068400b4547746d532c12621787801ee) |
| 2026-11-11 15:29 | io:NBIS | Close Long | 0.07 @ 155.99 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xe504db96d42c637ae67e0448918c540205c6007c6f2f824c88cd86e993203d65) | close (the trader closed, a stop, or a stop-loss: always allowed) |

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
