# Proof of copying: 4 of 4 opens follow the trader ✅

Checked **Nov 19 2026, 12:04 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/44520434547), from Hyperliquid's public record only (no MrCopyTrading server).
Last 7 days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

## Copy wallet 0xde7d…67f7 · copies 0xf97a…ddd1, 0x1e5c…0ac1

No trades in this window.

## Copy wallet 0xc812…65f4 · copies 0x720c…f4af

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-11-14 22:12 | xyz:MSTR | Open Long | 0.558 @ 96.8696003584 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xb3fbdf163c54a202b5750448cde6520209cb00fbd757c0d457c48a68fb587bed) | 0x720c…f4af Open Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xdeb85d08e3078883e0320448cde61802071000ee7e0aa7558281085ba20b626e) |
| 2026-11-14 22:39 | xyz:MSTR | Close Long | 0.116 @ 96.999 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x4d0407c5e6a4d8f24e7d0448ce3f6502041900ab81a7f7c4f0ccb318a5a8b2dc) | 0x720c…f4af Close Long 0 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xbb890607731fe16dbd020448ce3f6102048c00ed0e13003f5f51b15a3213bb58) |
| 2026-11-14 23:44 | xyz:MSTR | Close Long | 0.12 @ 97.104 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x7a2207a07e41de857b9b0448cf19bf02086100861944fd571deab2f33d45b870) | 0x720c…f4af Close Long 0 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xfc7fe8e06086f2e5fdf90448cf19c102029b00c5fb8a11b8a04894331f8accd0) |
| 2026-11-14 23:45 | xyz:MSTR | Close Long | 0.144 @ 97.525 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x8669aad43ba6e0e687e30448cf1c80020d2200b9d6a9ffb82a325626faaabad1) | 0x720c…f4af Close Long 1 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xdd880565157465dedf010448cf1c74020903004ab07784b08150b0b7d4783fc9) |
| 2026-11-14 23:54 | xyz:MSTR | Close Long | 0.136 @ 98.9958676471 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x76cd449bcb48ea0278470448cf3acc0201b00081664c08d41a95efee8a4cc3ed) | 0x720c…f4af Close Long 1 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xcbd0b94658425ddacd4a0448cf3abd02058b002bf3457cac6f996499174637c5) |
| 2026-11-15 00:27 | xyz:MSTR | Close Long | 0.042 @ 97.55 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x49cb846f5dd032b14b450448cfa69b0202760054f8d35183ed942fc21cd40c9b) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x6e8dc89dfa13a7cd70070448cfa67d0201f000839516c69f125673f0b91781b8) |
| 2026-11-15 01:23 | xyz:PURRDAT | Open Long | 4.0 @ 7.175 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x250b03984b7b4e5826840448d06193020b88007de67e6d2ac8d3aeeb0a7f2842) | 0x720c…f4af Open Long 16 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x823ba09128e6636583b50448d060b502054d0076c3e9823726044be3e7ea3d50) |
| 2026-11-15 02:17 | xyz:PURRDAT | Close Long | 2.0 @ 7.5759 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x615e49ec9cb2f72462d80448d114a10205f600d237b615f60526f53f5bb6d10f) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x470b96dce897d41f48850448d114850214f000c2839af2f1ead4422fa79bae09) |
| 2026-11-15 03:24 | xyz:PURRDAT | Close Long | 2.0 @ 7.7051 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xa98040ec766739c7aaf90448d1f0f702031b00d2116a58994d48ec3f356b13b2) | 0x720c…f4af Close Long 29 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xfa11e2060d1cea81fb8b0448d1ef520201b700eba81009549dda8d58cc10c46c) |
| 2026-11-16 15:42 | xyz:GOOGL | Open Long | 0.038 @ 287.87 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x571d7300ea408c8058970448ede32c02074000e68543ab52fae61e53a944666a) | 0x720c…f4af held long 1000 xyz:GOOGL at that moment (copy start / catch-up) |
| 2026-11-18 06:01 | xyz:COPPER | Open Long | 2.0 @ 5.9243 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x2c47d4319276f1de2dc104490b5750020a0700172d7a10b0d0107f84517acbc8) | 0x720c…f4af Open Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x2cf5da5437f9a6d12e6f04490b572002030f0039d2fcc5a3d0be85a6f6fd80bb) |
| 2026-11-18 06:21 | xyz:COPPER | Close Long | 2.0 @ 5.9151 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xfa5ac3ddef2f8eeefbd404490b9a5b02089300c38a22adc19e236f30ae2368d9) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x76b32787f14c0955782c04490b9a370202b9006d8c4f28271a7bd2dab04fe340) |

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
