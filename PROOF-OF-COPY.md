# Proof of copying: 1 of 1 opens follow the trader ✅

Checked **Nov 27 2026, 13:01 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/46003572133), from Hyperliquid's public record only (no MrCopyTrading server).
Last 7 days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

## Copy wallet 0xde7d…67f7 · copies 0xf97a…ddd1, 0x1e5c…0ac1

No trades in this window.

## Copy wallet 0xc812…65f4 · copies 0x720c…f4af

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-11-20 14:32 | xyz:CRCL | Close Long | 0.26 @ 52.135 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x34c24c5ee19aa4d0363c044936c8540205b500447c9dc3a2d88af7b1a09e7eba) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x98040d6dea21afd7997d044936c83e02091400538524cea93bccb8c0a92589c2) |
| 2026-11-20 19:53 | xyz:NVDA | Open Long | 0.107 @ 127.96 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x4d14f9a01d288bb14e8e04493ae66302044b0085b82baa83f0dda4f2dc2c659b) | 0x720c…f4af Open Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xc96963b3d3a43a4fcae304493ae62902029500996ea759216d320f0692a8143a) |

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
