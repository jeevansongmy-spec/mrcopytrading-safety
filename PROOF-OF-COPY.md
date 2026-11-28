# Proof of copying: no opens in this window

Checked **Nov 28 2026, 12:15 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/46143759030), from Hyperliquid's public record only (no MrCopyTrading server).
Last 7 days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

## Copy wallet 0xde7d…67f7 · copies 0xf97a…ddd1, 0x1e5c…0ac1

No trades in this window.

## Copy wallet 0xc812…65f4 · copies 0x720c…f4af

No trades in this window.

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
