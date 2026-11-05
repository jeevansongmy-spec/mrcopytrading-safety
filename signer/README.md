# Copy-only signer

The rules our copy engine's trade-only key must pass. Full rules: [api/index.py](api/index.py) (the docstring at the top).

- **Live:** https://mrcopytrading-signer.vercel.app/version shows the mode and the exact commit of this repo that runs.
- **Phase now: SHADOW.** The engine still signs as before and asks the signer about every action in the background; the
  signer answers allowed / refused and logs it. It holds no keys. After the shadow days, 100% of real copies must be
  allowed before it takes over the signing (switch), after a code review.
- **The promise:** opens and adds only when a copy that our website signed is live and a copied trader holds that coin on
  the same side right now, within the account's own money × min(20, 1.5 × the trader's leverage). Closes always, sent
  reduce-only. Withdraw and send are impossible for a trade-only key: Hyperliquid's own rule.
