// Withdraw and send: signed ONLY by your own wallet (Hyperliquid 'user-signed actions'). Our engine has no part in it.
// From the live MrCopyTrading site: components/deposit/web3.tsx, lines 757–784, commit 8cb535a. Internal notes removed; code unchanged.
  const send = async (address: string) => {
    setErr(""); setBusy(true);
    try {
      if (chainId !== arbitrum.id) await switchChainAsync({ chainId: arbitrum.id }).catch(() => undefined);
      const t = Date.now(), base = { hyperliquidChain: "Mainnet", signatureChainId: "0xa4b1" };
      const dst0 = (to ?? "").toLowerCase(), USDC_TOKEN = "USDC:0x6d1e7cde53ba9467b783cb7c530ce054";
      const sd = b?.unified ? "spot" : "", dd = !dst || dst.unified || dst.isNew ? "spot" : "";
      const [action, types, primaryType, message] = pair
        ? [{ type: "sendAsset", ...base, destination: dst0, sourceDex: sd, destinationDex: dd, token: USDC_TOKEN, amount: amtStr(amt), fromSubAccount: "", nonce: t },
           { "HyperliquidTransaction:SendAsset": [{ name: "hyperliquidChain", type: "string" }, { name: "destination", type: "string" }, { name: "sourceDex", type: "string" }, { name: "destinationDex", type: "string" }, { name: "token", type: "string" }, { name: "amount", type: "string" }, { name: "fromSubAccount", type: "string" }, { name: "nonce", type: "uint64" }] },
           "HyperliquidTransaction:SendAsset", { hyperliquidChain: "Mainnet", destination: dst0, sourceDex: sd, destinationDex: dd, token: USDC_TOKEN, amount: amtStr(amt), fromSubAccount: "", nonce: BigInt(t) }]
        : mode === "withdraw"
        ? [{ type: "withdraw3", ...base, destination: (toAddr ? dest.trim() : address).toLowerCase(), amount: amtStr(amt), time: t },
           { "HyperliquidTransaction:Withdraw": [{ name: "hyperliquidChain", type: "string" }, { name: "destination", type: "string" }, { name: "amount", type: "string" }, { name: "time", type: "uint64" }] },
           "HyperliquidTransaction:Withdraw", { hyperliquidChain: "Mainnet", destination: (toAddr ? dest.trim() : address).toLowerCase(), amount: amtStr(amt), time: BigInt(t) }]
        : [{ type: "usdClassTransfer", ...base, amount: amtStr(amt), toPerp, nonce: t },
           { "HyperliquidTransaction:UsdClassTransfer": [{ name: "hyperliquidChain", type: "string" }, { name: "amount", type: "string" }, { name: "toPerp", type: "bool" }, { name: "nonce", type: "uint64" }] },
           "HyperliquidTransaction:UsdClassTransfer", { hyperliquidChain: "Mainnet", amount: amtStr(amt), toPerp, nonce: BigInt(t) }];
      const sig = await signTypedDataAsync({ domain: HL_DOMAIN, types, primaryType, message } as never);
      const signature = { r: sig.slice(0, 66), s: "0x" + sig.slice(66, 130), v: parseInt(sig.slice(130, 132), 16) };
      const r = await fetch(HL_EX, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ action, nonce: t, signature }) }).then((x) => x.json());
      if (r?.status !== "ok") throw new Error(typeof r?.response === "string" ? r.response : tt("It did not go through. Nothing moved. Please try again."));
      setWant(false);
      setOk(mode === "withdraw" ? tt("{amount} is on its way", { amount: usd(amt - W_FEE) }) : pair ? tt("{amount} moved", { amount: usd(amt) }) : toPerp ? tt("{amount} moved to Perps", { amount: usd(amt) }) : tt("{amount} moved to Spot", { amount: usd(amt) }));
      onDone();
