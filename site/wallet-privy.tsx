// Your wallet: made by Privy (a Stripe company) when you sign in with Google or email. MrCopyTrading never sees the key.
// You can export it any time: the export runs on Privy's own screen (useExportWallet), not ours.
// From the live MrCopyTrading site: components/deposit/privy.tsx, lines 36–45, commit 8cb535a. Internal notes removed; code unchanged.
const cfg = () => {
  const dark = typeof document !== "undefined" && document.documentElement.dataset.theme === "dark";
  return {
    loginMethods: ["google", "email"] as ("google" | "email")[],
    appearance: { theme: dark ? "dark" as const : "light" as const, accentColor: "#fcd535" as const, logo: "https://mrcopytrading.com/logo.png", walletChainType: "ethereum-only" as const },
    embeddedWallets: { ethereum: { createOnLogin: "off" as const }, showWalletUIs: false },
    defaultChain: arbitrum, supportedChains: [arbitrum],
  };

// From the live MrCopyTrading site: components/deposit/privy.tsx, lines 458–476, commit 8cb535a. Internal notes removed; code unchanged.
function Backup({ addr, className }: { addr: string; className?: string }) {
  const tt = useT();
  const { ready, authenticated, user } = usePrivy();
  const { exportWallet } = useExportWallet();
  const BK = "mct-backup", asked = () => { try { return sessionStorage.getItem(BK) === addr; } catch { return false; } };
  const [ask, setAsk] = useState(asked);
  const mine = authenticated && !!user?.linkedAccounts.some((a) => a.type === "wallet" && "walletClientType" in a && a.walletClientType === "privy" && a.address.toLowerCase() === addr.toLowerCase());
  useEffect(() => {
    if (!mine || !asked()) return;
    try { sessionStorage.removeItem(BK); sessionStorage.removeItem("mct-privy-login"); } catch {}
    setAsk(false);
    exportWallet({ address: addr }).catch(() => undefined);
  }, [mine]);
  const close = () => { try { sessionStorage.removeItem(BK); } catch {} setAsk(false); };
  if (!ready) return null;
  const go = () => {
    if (mine) { exportWallet({ address: addr }).catch(() => undefined); return; }
