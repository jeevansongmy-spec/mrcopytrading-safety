# Proof of copying: 6 of 6 opens follow the trader ✅

Checked **Nov 11 2026, 11:25 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/43011742853), from Hyperliquid's public record only (no MrCopyTrading server).
Last 7 days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

## Copy wallet 0xde7d…67f7 · copies 0xf97a…ddd1, 0x1e5c…0ac1

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-11-04 20:12 | HYPE | Close Short | 0.14 @ 83.131 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x6b9ca17c51bf8ae26d16044812ee7e0201b50061ecb2a9b40f654ccf10b364cd) | 0xf97a…ddd1 Open Long 9 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x3f265a77ebf261c740a0044812ee0702018c005d86f58099e2ef05caaaf63bb1) |
| 2026-11-05 15:10 | HYPE | Open Long | 0.15 @ 79.153 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x0f07065fb62c63a81080044821d9870205a70045512f827ab2cfb1b275203d92) | 0xf97a…ddd1 Open Long 10 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x17ea289dc51af5761963044821d8ef021e660083601e1448bbb2d3f0841ecf60) |
| 2026-11-07 23:15 | HYPE | Close Long | 0.15 @ 77.407 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x03ebc40628ad8ac4056504484d9ad001e200dbebc3a0a996a7b46f58e7a164ae) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | HYPE | Open Short | 0.21 @ 77.407 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x09072858a0de9eaf0a8004484d9adb01e600403e3bd1bd81accfd3ab5fd27899) | 0x1e5c…0ac1 held short 1557.11 HYPE at that moment (copy start / catch-up) |
| 2026-11-07 23:15 | xyz:INTC | Close Long | 0.35 @ 56.066 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xeac7116c5fbd075cec4004484d9ae602018d0051fab0262e8e8fbcbf1eb0e147) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | xyz:LITE | Close Long | 0.018 @ 537.09 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x2fa4c8d7441a1c14311e04484d9aef0201d600bcdf1d3ae6d36d742a031df5fe) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | xyz:MRVL | Close Long | 0.06 @ 141.28 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xaa79354549041353abf204484d9af902024b002ae40732254e41e0980807ed3e) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-07 23:15 | HYPE | Close Short | 0.21 @ 77.38 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x6cf678d20713edcc6e7004484d9c5f02025600b7a2170c9e10bf2424c617c7b7) | close (the trader closed, a stop, or a stop-loss: always allowed) |

## Copy wallet 0xc812…65f4 · copies 0x720c…f4af

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-11-05 15:25 | io:NBIS | Open Long | 0.46 @ 118.65 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x1fdccb8b9a712d8721560448220a79020efa007135744c59c3a576de59750771) | 0x720c…f4af Open Long 9 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xeca6899513b7c26aee2004482209ef020be0007aaebae13c906f34e7d2bb9c55) |
| 2026-11-05 15:31 | xyz:SOXL | Open Long | 0.22 @ 48.448 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x29687d1c4e9afc4e2ae20448221fa3021e3a0001e99e1b20cd31286f0d9ed638) | 0x720c…f4af Open Long 259 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x983f552be73f384c99b904482210f3020bc400118232571e3c08007ea6331237) |
| 2026-11-05 15:33 | io:NBIS | Close Long | 0.15 @ 119.11 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xf6014f8b34cdece0f77b0448222583020e350070cfc10bb399c9faddf3c1c6cb) | 0x720c…f4af Close Long 3 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xcb6c7d0216e56fe1cce6044822255f02065b00e7b1e88eb36f352854d5e949cc) |
| 2026-11-05 16:06 | xyz:SOXL | Open Long | 0.31 @ 43.069 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x8b3efc8e52c99e9d8cb80448229377020a510073edccbd6f2f07a7e111cd7888) | 0x720c…f4af Open Long 3 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x199bed8e8ee9951f1b150448229353020917007429ecb3f1bd6498e14ded6f09) |
| 2026-11-05 19:09 | io:NBIS | Close Long | 0.1 @ 118.59 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xc96c9f1d27452668cae6044824fc890201ff0002c248453a6d354a6fe6490053) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-05 19:41 | io:NBIS | Close Long | 0.1 @ 122.11 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xa9e2c13611a3fae7ab5c0448256822020bd8001baca719b94dab6c88d0a7d4d2) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x473dc9676e7d278848b7044825680502157e004d0970465aeb0674ba2d710172) |
| 2026-11-05 20:55 | xyz:GOOGL | Close Long | 0.039 @ 283.21 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x840b27cf033f2acc8584044826600c02044700b49e32499e27d3d321c23304b7) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-06 03:29 | io:ANTH | Open Long | 0.008 @ 1636.0 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x107221c5c613126911eb04482b88300202f100ab6116313bb43acd188516ec53) | 0x720c…f4af Open Long 3 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x2728a36dd6fa2bf828a204482b87fd02036e005371fd4acacaf14ec095fe05e2) |
| 2026-11-06 03:47 | io:ANTH | Close Long | 0.008 @ 1702.2 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x5d14ba6d02b1e2865e8e04482bc4670201f800529db5015800dd65bfc1b5bc71) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x5884df29350dc1d859fe04482bc44b01f100f70ed000e0aafc4d8a7bf4019bc2) |
| 2026-11-09 13:13 | xyz:SOXL | Close Long | 0.26 @ 47.173 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x948d1dec12b24962960604486b061302059c00d1adb568343855c93ed1b6234d) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x2990d6801db9a5ea2b0a04486b05f80201930065b8bcc4bccd5981d2dcbd7fd4) |
| 2026-11-09 14:55 | xyz:SOXL | Close Long | 0.27 @ 52.15 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x2e5598368646bd342fcf04486c57630209ad001c2149dc06d21e4389454a971e) | 0x720c…f4af Close Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x8ef87aceb9742803907204486c572702068400b4547746d532c12621787801ee) |

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
