# Proof of copying: 4 of 4 opens follow the trader ✅

Checked **Nov 25 2026, 13:25 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/45623424671), from Hyperliquid's public record only (no MrCopyTrading server).
Last 7 days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

## Copy wallet 0xde7d…67f7 · copies 0xf97a…ddd1, 0x1e5c…0ac1

No trades in this window.

## Copy wallet 0xc812…65f4 · copies 0x720c…f4af

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-11-19 21:32 | xyz:CRCL | Open Long | 0.476 @ 50.882 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xf5be70334aa56943f738044929b6c6020db40018e5a8881699871b8609a9432e) | 0x720c…f4af Open Long 5 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xa1922161578f9fa3a30b044929b682020a060046f282be75455accb41683798e) |
| 2026-11-19 21:43 | xyz:NVDA | Open Long | 0.098 @ 144.93 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xad00f04169ff4fb5ae7a044929dbcf020184002704f26e8750c99b9428f329a0) | 0x720c…f4af Open Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x8e280fa982d736ad8fa1044929db9e0202f7008f1dda557f31f0bafc41db1098) |
| 2026-11-20 00:04 | xyz:CRCL | Close Long | 0.216 @ 51.755 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x53e7726573bdfa8f556104492baa72020211004b0eb11961f7b01db832b1d479) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xb7481af81d704074b8c104492baa570202d400ddb8735f465b10c64adc741a5f) |
| 2026-11-20 05:04 | io:NBIS | Open Long | 0.16 @ 92.84 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xe95c638259fc1c56ead604492f84ff0206940067f4ff3b288d250ed518fff641) | 0x720c…f4af Open Long 3 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xf3dec8f139b4fb27f55804492f84d30207cc00d6d4b819fa97a77443f8b8d512) |
| 2026-11-20 14:32 | xyz:CRCL | Close Long | 0.26 @ 52.135 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x34c24c5ee19aa4d0363c044936c8540205b500447c9dc3a2d88af7b1a09e7eba) | 0x720c…f4af Close Long 2 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x98040d6dea21afd7997d044936c83e02091400538524cea93bccb8c0a92589c2) |
| 2026-11-20 19:53 | xyz:NVDA | Open Long | 0.107 @ 127.96 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x4d14f9a01d288bb14e8e04493ae66302044b0085b82baa83f0dda4f2dc2c659b) | 0x720c…f4af Open Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xc96963b3d3a43a4fcae304493ae62902029500996ea759216d320f0692a8143a) |

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
