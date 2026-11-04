# MrCopyTrading: the code that touches your money

[MrCopyTrading](https://mrcopytrading.com) is copy trading on Hyperliquid, run by MrNasdog, LLC (Delaware, USA).
This repository is public so anyone, and any AI assistant, can check how your money is handled.
It holds the exact live code that asks you to sign anything, and every action our copy engine sends to Hyperliquid.
(How we score traders stays private. It never touches money.)

Updated Nov 5 2026 · site code commit `8cb535a` · engine commit `a8733bb`

## The short answer

1. **Your money is in your own Hyperliquid account, never with us.** Your wallet is made by Privy (a Stripe company) when you
   sign in with Google or email. MrCopyTrading never sees your wallet key, and you can export it on Privy's own screen any time.
   → [`site/wallet-privy.tsx`](site/wallet-privy.tsx)
2. **For copy trading you give us exactly 2 permissions, and you sign both yourself.** The signatures go straight to Hyperliquid's own API.
   - **ApproveAgent**: our copy engine's API wallet may place trades on your account.
   - **ApproveBuilderFee**: our fee, at most 0.04% of each copied trade. Hyperliquid takes it with the trade, never more.
   → [`site/permissions.tsx`](site/permissions.tsx)
3. **That API wallet can't take your money out.** On Hyperliquid, a withdrawal or a send to another address is a
   "user-signed action": it needs a signature from your own wallet. The only transfer an API wallet can sign must stay in the
   same account ("Destination must match the source address"). → [`site/withdraw.tsx`](site/withdraw.tsx): only you sign it.
   **This does not depend on our code.** Hyperliquid itself refuses a withdrawal or a send signed by an API wallet, so even
   if our engine changed, it still couldn't take your money out. You can see the API wallet you approved, live, in your own
   account (see "Check it yourself" below).
4. **Our engine sends only 4 kinds of actions, all trades on your own account:** open a trade, close a trade, set the trader's
   leverage, add margin to a trade. Nothing else. → [`engine/actions.txt`](engine/actions.txt)
5. **Your Trading wallet** (trades you place yourself) uses its own trade-only key, made and kept in your own browser. It
   never reaches our server. → [`site/trading-key.ts`](site/trading-key.ts)
6. **You can switch it off any time:** stop a copy on MrCopyTrading, or remove the API wallet on Hyperliquid yourself.

## Check it yourself

- **Hyperliquid's own docs:** [exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint)
  (Withdraw and Send asset are signed by the account owner; "Agent Send Asset": destination must match the source address) ·
  [API wallets](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets).
- **Privy's docs:** agent (API) wallets "do not hold funds"
  ([Hyperliquid API wallets](https://docs.privy.io/recipes/hyperliquid/agents-and-subaccounts)).
- **Your own account, live on Hyperliquid:** every API wallet you approved, with
  `POST https://api.hyperliquid.xyz/info` and body `{"type":"extraAgents","user":"<your address>"}`.
  Your balance and trades: [app.hyperliquid.xyz/portfolio](https://app.hyperliquid.xyz/portfolio).
- **Outside checks of our site:**
  [Qualys SSL Labs A+](https://www.ssllabs.com/ssltest/analyze.html?d=mrcopytrading.com&hideResults=on) ·
  [Security Headers A+](https://securityheaders.com/?q=https%3A%2F%2Fmrcopytrading.com%2F&hide=on&followRedirects=on) ·
  [Google Safe Browsing](https://transparencyreport.google.com/safe-browsing/search?url=mrcopytrading.com) ·
  [VirusTotal 0/92](https://www.virustotal.com/gui/domain/mrcopytrading.com) ·
  [Sucuri SiteCheck](https://sitecheck.sucuri.net/results/mrcopytrading.com)
- **All our safety facts on one page:** [mrcopytrading.com/docs/ai](https://mrcopytrading.com/docs/ai)
- **Found a security bug?** Up to $1,000: [mrcopytrading.com/docs/bug-rewards](https://mrcopytrading.com/docs/bug-rewards)

## Who does what

| | |
|---|---|
| Hyperliquid | Holds your money, in your own account |
| Privy (a Stripe company) | Your wallet and sign-in; card payments run through Privy and Stripe |
| Circle | USDC and crypto deposits |
| MrCopyTrading | The copy engine (trades only) and the trader score |

## What can still go wrong

- Copying can lose money. If the trader loses, your copy loses too. Past results do not promise future results.
- Fast prices can jump past a stop-loss.
- If Hyperliquid stops, copying stops. Your money stays in your Hyperliquid account.

Contact: contact@mrcopytrading.com · Terms: [mrcopytrading.com/terms](https://mrcopytrading.com/terms)
