# Copy-only signer

The rules our copy engine's trade-only key must pass. Full rules: [signer_core.py](signer_core.py).

- **Live since Nov 5 2026: the signer signs every trade.** [server.py](server.py) runs as one server with no public address,
  next to our copy engine, deployed from this folder. The engine holds no trading key and no decryption secret: it can only
  ask. A refused action is answered in Hyperliquid's own format and nothing is sent.
- **The promise:** opens and adds only when a copy that our website signed is live and a copied trader holds that coin on
  the same side right now, within the account's own money × min(20, 1.5 × the trader's leverage). Closes always, sent
  reduce-only. Withdraw and send are impossible for a trade-only key: Hyperliquid's own rule.
