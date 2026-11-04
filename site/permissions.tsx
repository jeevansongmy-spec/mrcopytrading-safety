// The 2 permissions you give MrCopyTrading. You sign both in YOUR wallet (EIP-712); the signature goes straight to
// Hyperliquid's own API (api.hyperliquid.xyz/exchange), not to us.
//   1. ApproveAgent: our copy engine's API wallet may place trades on your account. It can't withdraw.
//   2. ApproveBuilderFee: our fee, at most 0.04% of each copied trade.
// From the live MrCopyTrading site: components/deposit/web3.tsx, lines 680–681, commit b17d446. Internal notes removed; code unchanged.
const HL_EX = "https://api.hyperliquid.xyz/exchange", HL_INFO = "https://api.hyperliquid.xyz/info";
const HL_DOMAIN = { name: "HyperliquidSignTransaction", version: "1", chainId: arbitrum.id, verifyingContract: "0x0000000000000000000000000000000000000000" as Address };

// From the live MrCopyTrading site: components/deposit/web3.tsx, lines 934–1007, commit b17d446. Internal notes removed; code unchanged.
const sigOf = (sig: Hex) => ({ r: sig.slice(0, 66), s: "0x" + sig.slice(66, 130), v: parseInt(sig.slice(130, 132), 16) });
const AGENT_NAME = "MrCopyTrading";
function TurnOn({ fee, onDone, cta: cta0, cs, onLeave }: { fee: string; onDone: () => void; cta?: string; cs?: CardSigner; onLeave?: () => void }) {
  const tt = useT();
  const cta = cta0 ?? tt("Enable trading");
  const wa = useAccount(), address = cs?.address ?? wa.address, status = cs ? "connected" : wa.status, chainId = cs ? arbitrum.id : wa.chainId;
  const acct = useAcct();
  const ws = useSignTypedData(), wm = useSignMessage(), sw = useSwitchChain();
  const signTypedDataAsync = cs ? cs.signTypedData : ws.signTypedDataAsync, signMessageAsync = cs ? cs.signMessage : wm.signMessageAsync;
  const switchChainAsync = sw.switchChainAsync;
  const gate = useTradeGate();
  const [v, setV] = useState<EngineView | null>(null), [busy, setBusy] = useState<"" | "proof" | "key" | "fee" | "all" | "check">(""), [err, setErr] = useState("");
  useEffect(() => { engineApi().then(setV).catch(() => setV(null)); }, []);
  const [act, setAct] = useState<boolean | null | undefined>(undefined);
  useEffect(() => { if (address) hlActive(address).then(setAct); }, [address]);
  if (status === "reconnecting" || !v) return <i className="dm-sk" style={{ height: 160 }} />;
  if (!address) return <ConnectCta why={v.account ?? acct ? tt("Connect your trading account {wallet}.", { wallet: short((v.account ?? acct)!) }) : tt("Connect the wallet that owns your trading account.")} />;
  const own = v.account ?? acct;
  if (own && address.toLowerCase() !== own) return <WrongWallet addr={address} own={own} doing="turnon" />;
  const done = v.approved && v.builderOk && v.unified;
  if (done) return <div className="dm-arrived" role="status">{CHECK}<div><b>{tt("Trading is enabled")}</b><span>{tt("Your copies go live by themselves when your money covers them.")}</span></div></div>;
  if (act === undefined) return <i className="dm-sk" style={{ height: 160 }} />;
  if (act === false) return <>
    <div className="dm-guide"><b className="dm-guide-h">{tt("Deposit first")}</b><p>{tt("These 3 free signatures work only after your first deposit. Deposit, then enable trading.")}</p></div>
    <button className="dm-cta big" onClick={() => { onLeave?.(); openDeposit(); }}>{tt("Deposit")}</button>
  </>;
  const post = async (action: Record<string, unknown>, nonce: number, sig: Hex) => {
    const r = await fetch(HL_EX, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ action, nonce, signature: sigOf(sig) }) }).then((x) => x.json());
    if (r?.status !== "ok") throw new Error(typeof r?.response === "string" ? r.response : tt("It did not go through. Please try again."));
  };
  const go = async () => {
    if (gate.blocked) return gate.open();
    setErr("");
    try {
      if (chainId !== arbitrum.id) await switchChainAsync({ chainId: arbitrum.id }).catch(() => undefined);
      let cur = v;
      if (!cur.approved) {
        let a = cur;
        if (!cur.agent || !cur.mine) {
          setBusy("proof");
          const ch = await engineApi("challenge");
          if (!ch.message) throw new Error(ch.error || tt("Please try again."));
          const proof = await signMessageAsync({ message: ch.message });
          a = await engineApi("agent", { message: ch.message, signature: proof });
        }
        if (a.error || !a.agent) throw new Error(a.error || tt("Please try again."));
        setBusy("key");
        const t = Date.now(), agent = a.agent.toLowerCase();
        const sig = await signTypedDataAsync({ domain: HL_DOMAIN, primaryType: "HyperliquidTransaction:ApproveAgent",
          types: { "HyperliquidTransaction:ApproveAgent": [{ name: "hyperliquidChain", type: "string" }, { name: "agentAddress", type: "address" }, { name: "agentName", type: "string" }, { name: "nonce", type: "uint64" }] },
          message: { hyperliquidChain: "Mainnet", agentAddress: agent as Address, agentName: AGENT_NAME, nonce: BigInt(t) } } as never);
        await post({ type: "approveAgent", hyperliquidChain: "Mainnet", signatureChainId: "0xa4b1", agentAddress: agent, agentName: AGENT_NAME, nonce: t }, t, sig);
        cur = { ...a, approved: true };
        setV(cur);
      }
      if (!cur.builderOk) {
        if (!cur.builder) throw new Error(tt("Please try again in a minute."));
        setBusy("fee");
        const t = Date.now(), builder = cur.builder.toLowerCase();
        const sig = await signTypedDataAsync({ domain: HL_DOMAIN, primaryType: "HyperliquidTransaction:ApproveBuilderFee",
          types: { "HyperliquidTransaction:ApproveBuilderFee": [{ name: "hyperliquidChain", type: "string" }, { name: "maxFeeRate", type: "string" }, { name: "builder", type: "address" }, { name: "nonce", type: "uint64" }] },
          message: { hyperliquidChain: "Mainnet", maxFeeRate: cur.maxFeeRate, builder: builder as Address, nonce: BigInt(t) } } as never);
        await post({ type: "approveBuilderFee", hyperliquidChain: "Mainnet", signatureChainId: "0xa4b1", maxFeeRate: cur.maxFeeRate, builder, nonce: t }, t, sig);
      }
