# Live check: PASS ✅

Checked **Nov 5 2026, 06:57 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/41983834342).
Downloaded 328 JavaScript files (14.6 MB) from the live https://mrcopytrading.com
and compared every Hyperliquid message it can ask you to sign with the code published in [site/](site/).

The live site asks users to sign only the messages published here, with the same fields. None of them lets MrCopyTrading withdraw or send your money: Withdraw and Send are signed by you, to the address you choose, and Hyperliquid refuses a withdrawal signed by our copy permission (API wallet).

| Message you may sign | Fields on the live site | Published here | Result |
|---|---|---|---|
| ApproveAgent | hyperliquidChain,agentAddress,agentName,nonce | yes | ✅ same |
| ApproveBuilderFee | hyperliquidChain,maxFeeRate,builder,nonce | yes | ✅ same |
| SendAsset | hyperliquidChain,destination,sourceDex,destinationDex,token,amount,fromSubAccount,nonce | yes | ✅ same |
| UsdClassTransfer | hyperliquidChain,amount,toPerp,nonce | yes | ✅ same |
| UserSetAbstraction | hyperliquidChain,user,abstraction,nonce | yes | ✅ same |
| Withdraw | hyperliquidChain,destination,amount,time | yes | ✅ same |

The check itself: [check-live.mjs](check-live.mjs) · schedule: [.github/workflows/live-check.yml](.github/workflows/live-check.yml)
