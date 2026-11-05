// Your Trading wallet (trades you place yourself): its trade-only key is made IN YOUR BROWSER and kept there
// (localStorage). It never reaches our server, and like every API wallet it can't withdraw or send money.
// From the live MrCopyTrading site: components/trading/exchange.ts, lines 17–22, commit a829e37. Internal notes removed; code unchanged.
export function tradeKey(tw: string): { pk: Hex; address: string } {
  let pk: Hex | null = null;
  try { pk = localStorage.getItem(KEY(tw)) as Hex | null; } catch { /* private mode: a new key each time */ }
  if (!pk || !/^0x[0-9a-f]{64}$/.test(pk)) { pk = generatePrivateKey(); try { localStorage.setItem(KEY(tw), pk); } catch {} }
  return { pk, address: privateKeyToAccount(pk).address.toLowerCase() };
}
