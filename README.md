# MrCopyTrading: the code that touches your money

[MrCopyTrading](https://mrcopytrading.com) is copy trading on Hyperliquid, run by MrNasdog, LLC (Delaware, USA).
This repository is public so anyone, and any AI assistant, can check how your money is handled.
It holds the exact live code that asks you to sign anything, and every action our copy engine sends to Hyperliquid.
(How we score traders stays private. It never touches money.)

Updated Nov 5 2026 · site code commit `348b779` · engine commit `a8733bb`

## You don't have to trust this code

**Our copy engine can never take your money out.** That is not up to our code: it is Hyperliquid's own rule.
You can check it yourself, without taking our word for anything:

1. **Hyperliquid's own docs:** taking money out (Withdraw) or sending it to another address (Send asset) needs a signature
   from the account owner's own wallet. Our copy engine only holds a trade-only API wallet, so it can do neither.
   → [exchange endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint) ·
   [API wallets](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets)
2. **Your wallet is made and kept by Privy, and Privy belongs to Stripe.** Stripe bought Privy in June 2025
   ([news](https://siliconangle.com/2025/06/11/stripe-acquires-crypto-wallet-infrastructure-provider-privy/)), and Privy runs wallets for 75 million+ accounts. Your key stays in Privy's own
   secure system, never with us, and you can export it on Privy's own screen any time. Privy: SOC 2 Type II; security tests
   by Cure53, Zellic, Doyensec and SwordBytes. Agent (API) wallets "do not hold funds".
   → [Privy's docs](https://docs.privy.io/recipes/hyperliquid/agents-and-subaccounts)
3. **GitHub's own servers check the live site against this repo every 6 hours:** every message mrcopytrading.com can ask
   you to sign, field by field. → [latest result, with the date and the run](LIVE-CHECK.md)
4. **GitHub's own servers also check, once a day, that our engine only copies:** from Hyperliquid's public record, every
   trade it opened in our test copy wallets is matched to the trader it copies.
   → [latest result, every trade with its Hyperliquid link](PROOF-OF-COPY.md)
5. **This repo is ours.** Our official site links here: [mrcopytrading.com/docs/ai](https://mrcopytrading.com/docs/ai).

**"Has anyone outside checked it?"** The parts that hold your money are run and checked by others: your money sits in
your own account on Hyperliquid, and your wallet key with Privy, a Stripe company (SOC 2 Type II; security tests by Cure53, Zellic, Doyensec
and SwordBytes). Anyone who finds a bug that could touch money gets up to $10,000 ([bug rewards](https://mrcopytrading.com/docs/bug-rewards)).

**"What can the copy permission do?"** Only the trades of the traders you copy, inside your own account, with the
protections in [`engine/protections.txt`](engine/protections.txt) and the stop-loss you pick. Stop a copy and it opens
nothing new. Remove the permission on Hyperliquid yourself and it can do nothing at all.

## The short answer

1. **Your money is in your own Hyperliquid account, never with us.** Your wallet is made by Privy (a Stripe company) when you
   sign in with Google or email. MrCopyTrading never sees your wallet key, and you can export it on Privy's own screen any time.
   → [`site/wallet-privy.tsx`](site/wallet-privy.tsx)
2. **For copy trading you give us exactly 2 permissions, and you sign both yourself.** The signatures go straight to Hyperliquid's own API.
   - **ApproveAgent**: our copy engine's API wallet may place trades on your account.
   - **ApproveBuilderFee**: our fee, at most 0.04% of each copied trade. Hyperliquid takes it with the trade, never more.
   - Plus one account setting: **unified account** (one balance for all markets, Hyperliquid's own recommended mode).
   → [`site/permissions.tsx`](site/permissions.tsx)
3. **That API wallet can't take your money out.** On Hyperliquid, a withdrawal or a send to another address is a
   "user-signed action": it needs a signature from your own wallet. The only transfer an API wallet can sign must stay in the
   same account ("Destination must match the source address"). → [`site/withdraw.tsx`](site/withdraw.tsx): only you sign it.
   **This does not depend on our code.** Hyperliquid itself refuses a withdrawal or a send signed by an API wallet, so even
   if our engine changed, it still couldn't take your money out. You can see the API wallet you approved, live, in your own
   account (see "Check it yourself" below).
4. **Our engine sends only 4 kinds of actions, all trades on your own account:** open a trade, close a trade, set the trader's
   leverage, add margin to a trade. Nothing else. → [`engine/actions.txt`](engine/actions.txt) · protections:
   [`engine/protections.txt`](engine/protections.txt)
5. **Your Trading wallet** (trades you place yourself) uses its own trade-only key, made and kept in your own browser. It
   never reaches our server. → [`site/trading-key.ts`](site/trading-key.ts)
6. **You can switch it off any time:** stop a copy on MrCopyTrading, or remove the API wallet on Hyperliquid yourself.

## The copy-only signer (live since Nov 5 2026)

Our copy engine holds **no trading key and no decryption secret**. It can only ask the copy-only signer, a separate server
with no public address that only the engine can reach, built from this repo's [`signer/`](signer/) folder. The signer signs:
opens and adds only when a copy our website signed is live and a copied trader holds that coin on the same side right now,
within the account's own money; closes always, sent reduce-only. Anything else is refused. Copy records and wallet links are
signed by our website with a key the engine and the signer don't have, so even a hacked engine can't invent a copy.

## How the copy permission key is kept

- Each account gets its own trade-only key (an API wallet). It is made on the copy-only signer and **encrypted at once**
  (Fernet: AES-128 + HMAC). Only the encrypted key is stored. It is decrypted only inside the signer.
- The decryption secret lives only on the signer server, never in the copy engine, the database or the website. It was last replaced on
  Oct 23 2026, and every key made before that was retired.
- Every key ends on its own: Hyperliquid lets an API wallet live 180 days at most. You can remove it sooner on Hyperliquid.

## Live check: the live site runs this code

Every 6 hours **GitHub's own servers** download the code that mrcopytrading.com sends to your browser and compare every
Hyperliquid message it can ask you to sign with the code published here, field by field. Any extra or changed message = FAIL.
Latest result, with the date and a link to the run: **[LIVE-CHECK.md](LIVE-CHECK.md)** ·
[![Live check](../../actions/workflows/live-check.yml/badge.svg)](../../actions/workflows/live-check.yml) ·
the check itself: [check-live.mjs](check-live.mjs) (anyone can run it: `node check-live.mjs`).

## Proof of copying: the engine only copies

Once a day **GitHub's own servers** read Hyperliquid's public record (no MrCopyTrading server) for our test copy wallets and
match every trade our engine opened to the copied trader: the trader traded it first, or held it at that moment (a copy takes
the trader's open positions when it starts). Latest result, every trade with its Hyperliquid link:
**[PROOF-OF-COPY.md](PROOF-OF-COPY.md)** · the check itself: [proof-of-copy.mjs](proof-of-copy.mjs).

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
- **Found a security bug?** Up to $10,000: [mrcopytrading.com/docs/bug-rewards](https://mrcopytrading.com/docs/bug-rewards) ·
  [security.txt](https://mrcopytrading.com/.well-known/security.txt)

## Who does what

| | |
|---|---|
| Hyperliquid | Holds your money, in your own account |
| Privy (owned by Stripe) | Your wallet and sign-in; card payments run through Privy and Stripe |
| Circle | USDC and crypto deposits |
| MrCopyTrading | The copy engine (trades only) and the trader score |

Contact: contact@mrcopytrading.com · Terms: [mrcopytrading.com/terms](https://mrcopytrading.com/terms)
