// LIVE CHECK: does the live site run the money code published in this repo?
// GitHub's own servers run this every 6 hours (.github/workflows/live-check.yml). Anyone can read it and run it:
//   node check-live.mjs
// What it does:
//   1. Downloads the live mrcopytrading.com pages and every JavaScript file they load (the code your browser runs).
//   2. Finds every Hyperliquid message the live site can ask you to sign ("HyperliquidTransaction:…", EIP-712).
//   3. Compares them, field by field, with the code published in site/. Any extra or changed message = FAIL.
// Why it matters: these signed messages are the ONLY way the site can act on your Hyperliquid account. Withdraw and Send
// are signed by you, for you. Hyperliquid itself refuses a withdrawal signed by our copy permission (API wallet).
// Results: LIVE-CHECK.md (written by each run, with a link to the run on GitHub).
import { readFileSync, readdirSync, writeFileSync } from "node:fs";

const SITE = "https://mrcopytrading.com";
const PAGES = ["/", "/app", "/deposit", "/wallet", "/copies", "/trade", "/account", "/ai", "/go?copy=0x0000000000000000000000000000000000000000:1"];
const get = async (u) => { try { const r = await fetch(u, { headers: { "User-Agent": "mrcopytrading-live-check" } }); return r.ok ? await r.text() : ""; } catch { return ""; } };
const fieldsIn = (body) => [...body.matchAll(/name:\s*"(\w+)"/g)].map((m) => m[1]).join(",");

// 1. the live code
const seen = new Set(), queue = [];
for (const p of PAGES) for (const m of (await get(SITE + p)).matchAll(/\/_next\/static\/[^"'\s<>]+?\.js/g)) queue.push(m[0]);
const js = [];
while (queue.length && seen.size < 2000) {
  const u = queue.pop();
  if (seen.has(u)) continue;
  seen.add(u);
  const t = await get(SITE + u);
  js.push(t);
  for (const m of t.matchAll(/(?:\/_next\/)?static\/[A-Za-z0-9_\-]+\/[A-Za-z0-9_\-/.~]+?\.js/g)) {
    const p = m[0].startsWith("/_next/") ? m[0] : "/_next/" + m[0];
    if (!seen.has(p)) queue.push(p);
  }
}
const live = new Map();   // type → set of field lists found
for (const t of js) for (const m of t.matchAll(/"HyperliquidTransaction:(\w+)":\s*\[([^\]]*)\]/g)) {
  if (!live.has(m[1])) live.set(m[1], new Set());
  live.get(m[1]).add(fieldsIn(m[2]));
}
const liveDomain = js.some((t) => /name:\s*"HyperliquidSignTransaction"/.test(t));

// 2. the published code
const pub = new Map();
for (const f of readdirSync("site")) for (const m of readFileSync(`site/${f}`, "utf8").matchAll(/"HyperliquidTransaction:(\w+)":\s*\[([^\]]*)\]/g)) pub.set(m[1], fieldsIn(m[2]));

// 3. compare
const rows = [], bad = [];
for (const [type, lists] of [...live].sort()) {
  const want = pub.get(type), ok = !!want && [...lists].every((l) => l === want);
  rows.push(`| ${type} | ${[...lists].join(" / ")} | ${want ? "yes" : "NO"} | ${ok ? "✅ same" : "❌ different"} |`);
  if (!ok) bad.push(type);
}
for (const type of pub.keys()) if (!live.has(type)) { rows.push(`| ${type} | (not on the live site) | yes | ❌ missing |`); bad.push(type); }
if (js.length < 20) bad.push("could not read the live site");
if (!liveDomain) bad.push("signing domain not found");

const d = new Date(), pass = bad.length === 0;
const now = `${d.toLocaleString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }).replace(",", "")}, ${d.toISOString().slice(11, 16)} UTC`;
const run = process.env.GITHUB_RUN_ID ? `${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID}` : "run by hand";
writeFileSync("LIVE-CHECK.md", `# Live check: ${pass ? "PASS ✅" : "FAIL ❌"}

Checked **${now}** by GitHub Actions (${run}).
Downloaded ${js.length} JavaScript files (${(js.reduce((a, t) => a + t.length, 0) / 1e6).toFixed(1)} MB) from the live ${SITE}
and compared every Hyperliquid message it can ask you to sign with the code published in [site/](site/).

${pass ? "The live site asks users to sign only the messages published here, with the same fields. None of them lets MrCopyTrading withdraw or send your money: Withdraw and Send are signed by you, to the address you choose, and Hyperliquid refuses a withdrawal signed by our copy permission (API wallet)." : "Something on the live site differs from the published code: " + bad.join(", ") + "."}

| Message you may sign | Fields on the live site | Published here | Result |
|---|---|---|---|
${rows.join("\n")}

The check itself: [check-live.mjs](check-live.mjs) · schedule: [.github/workflows/live-check.yml](.github/workflows/live-check.yml)
`);
console.log(pass ? "PASS" : "FAIL: " + bad.join(", "), "·", js.length, "files ·", [...live.keys()].join(" "));
process.exit(pass ? 0 : 1);
