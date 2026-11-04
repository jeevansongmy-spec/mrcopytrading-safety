// PROOF OF COPYING: does MrCopyTrading's engine only copy?
// GitHub's own servers run this once a day (.github/workflows/proof-of-copy.yml). It reads ONLY Hyperliquid's public record
// (api.hyperliquid.xyz/info, no key, no MrCopyTrading server), so you don't have to trust us. Anyone can run it:
//   node proof-of-copy.mjs
// What it checks, for our own test copy wallets (never a customer):
//   every trade our engine OPENED or ADDED in a copy wallet must follow the copied trader, on the same coin and side:
//   either the trader traded it first (≤ 15 minutes before), or the trader HELD that position at that moment (a copy
//   takes the trader's open positions when it starts, and catches up if a trade was missed). The trader's position at
//   any moment comes from Hyperliquid's own fills ("startPosition") or, with no fill, from the trader's position now.
//   Closes are listed too; a close is always allowed (stop, stop-loss, or the trader closing).
// Result: PROOF-OF-COPY.md (matched X of Y, every trade with its Hyperliquid link).
import { writeFileSync } from "node:fs";

// our test copy wallets and the traders each one copies (public addresses; no customer data)
const WALLETS = [
  { wallet: "0xde7d52dd47181dd1e89fdda11d1159994f1a67f7", traders: ["0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1", "0x1e5cf44f64a66dae56104ed91bf15f6147200ac1"] },
  { wallet: "0xc81278752474a68355f1835e5d1fb015368f65f4", traders: ["0x720c933b5eb30fc37461789ef3264e51f2a7f4af"] },
];
const DAYS = 7, BEFORE_MS = 15 * 60_000, AFTER_MS = 5_000;
const INFO = "https://api.hyperliquid.xyz/info";
const post = async (body) => { const r = await fetch(INFO, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }); if (!r.ok) throw new Error(`Hyperliquid ${r.status}`); return r.json(); };

/** Every fill of one address since `since` (Hyperliquid pages at 2,000 fills). */
async function fills(user, since) {
  const out = [];
  let start = since;
  for (let i = 0; i < 20; i++) {
    const page = await post({ type: "userFillsByTime", user, startTime: start, aggregateByTime: true });
    if (!Array.isArray(page) || !page.length) break;
    out.push(...page);
    if (page.length < 2000) break;
    start = page[page.length - 1].time + 1;
  }
  return out;
}

const since = Date.now() - DAYS * 86_400_000;
/** The trader's position size on `coin` at time `t` (+ long, − short), from Hyperliquid's public fills and position. */
async function posAt(trader, coin, t, tf, nowPos) {
  const f = tf.filter((x) => x.coin === coin).sort((a, b) => a.time - b.time);
  const before = f.filter((x) => x.time <= t).pop();
  if (before) return +before.startPosition + (before.side === "B" ? +before.sz : -before.sz);
  const after = f.find((x) => x.time > t);
  if (after) return +after.startPosition;
  return nowPos(trader, coin);
}
const posCache = new Map();
async function nowPos(trader, coin) {
  const dex = coin.includes(":") ? coin.split(":")[0] : "";
  const k = trader + "|" + dex;
  if (!posCache.has(k)) posCache.set(k, await post({ type: "clearinghouseState", user: trader, ...(dex ? { dex } : {}) }));
  const p = (posCache.get(k)?.assetPositions ?? []).find((x) => x.position?.coin === coin);
  return p ? +p.position.szi : 0;
}
const link = (h) => (h && !/^0x0+$/.test(h) ? `[tx](https://app.hyperliquid.xyz/explorer/tx/${h})` : "");
const short = (a) => `${a.slice(0, 6)}…${a.slice(-4)}`;
const when = (t) => new Date(t).toISOString().slice(0, 16).replace("T", " ");
const isOpen = (f) => /^Open|Buy$|^Long > |^Short > /.test(f.dir || "") && !/^Close/.test(f.dir || "");
let opens = 0, matched = 0;
const sections = [];
for (const w of WALLETS) {
  const mine = (await fills(w.wallet, since)).sort((a, b) => a.time - b.time);
  const theirs = (await Promise.all(w.traders.map(async (t) => (await fills(t, since - BEFORE_MS)).map((f) => ({ ...f, trader: t }))))).flat();
  const rows = [];
  for (const f of mine) {
    const open = isOpen(f);
    // the trader's trade this one follows: same coin, same side, the trader first (≤ 15 min before, ≤ 5 s after)
    const lead = theirs.filter((x) => x.coin === f.coin && x.side === f.side && x.time <= f.time + AFTER_MS && x.time >= f.time - BEFORE_MS)
      .sort((a, b) => Math.abs(f.time - a.time) - Math.abs(f.time - b.time))[0];
    // no fresh trade: did the trader HOLD this coin on the same side at that moment (copy start / catch-up)?
    let held = null;
    if (open && !lead) for (const t of w.traders) {
      const p = await posAt(t, f.coin, f.time, theirs.filter((x) => x.trader === t), nowPos);
      if ((f.side === "B" && p > 0) || (f.side === "A" && p < 0)) { held = { trader: t, p }; break; }
    }
    if (open) { opens++; if (lead || held) matched++; }
    const why = lead ? `${short(lead.trader)} ${lead.dir} ${Math.round((f.time - lead.time) / 1000)} s before ${link(lead.hash)}`
      : held ? `${short(held.trader)} held ${held.p > 0 ? "long" : "short"} ${Math.abs(held.p)} ${f.coin} at that moment (copy start / catch-up)`
      : open ? "**the trader did not hold or trade it**" : "close (the trader closed, a stop, or a stop-loss: always allowed)";
    rows.push(`| ${when(f.time)} | ${f.coin} | ${f.dir} | ${f.sz} @ ${f.px} | ${link(f.hash)} | ${why} |`);
  }
  sections.push(`## Copy wallet ${short(w.wallet)} · copies ${w.traders.map(short).join(", ")}

${rows.length ? `| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
${rows.join("\n")}` : "No trades in this window."}`);
}

const d = new Date(), date = `${d.toLocaleString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }).replace(",", "")}, ${d.toISOString().slice(11, 16)} UTC`;
const run = process.env.GITHUB_RUN_ID ? `${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID}` : "run by hand";
const pass = opens === matched;
writeFileSync("PROOF-OF-COPY.md", `# Proof of copying: ${opens ? `${matched} of ${opens} opens follow the trader ${pass ? "✅" : "⚠️"}` : "no opens in this window"}

Checked **${date}** by GitHub Actions (${run}), from Hyperliquid's public record only (no MrCopyTrading server).
Last ${DAYS} days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

${sections.join("\n\n")}

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
`);
console.log(`${matched}/${opens} opens matched`);
