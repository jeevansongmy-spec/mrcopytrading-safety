"""MrCopyTrading COPY-ONLY SIGNER (Safety 6 -> 9, change 1). Public code: github.com/jeevansongmy-spec/mrcopytrading-safety
(folder signer/), deployed from that repo; GET /version shows the exact commit that runs.

WHAT IT IS FOR
  Our copy engine places trades on a user's Hyperliquid account with a trade-only key (an API wallet). Hyperliquid itself
  already refuses any withdrawal or send by that key. This signer adds the second promise: the key may only place trades
  that FOLLOW the copied trader. It checks every action against Hyperliquid's own public data and against copy records
  that only our website can sign, never against what the engine says.

PHASE NOW: SHADOW (SIGNER_MODE=shadow)
  The engine still signs its own trades exactly as before. For every action it also asks this signer (in the background,
  never waiting) "would you allow this?". The signer answers and logs it. After the shadow days the log must show 100%
  allowed for real copies before the signer takes over the signing (switch), reviewed first by our engine reviewer.
  In shadow mode this service holds NO keys.

THE RULES (each action the engine wants to send)
  close / cut ........ always allowed. When the signer signs (switch), it sends them reduce-only, so they can only shrink a
                        position (Hyperliquid enforces reduce-only).
  add isolated margin  allowed only when the amount is above 0 (moves the user's own money into their own position).
  set leverage ....... allowed (Hyperliquid caps it at the coin's maximum). Exposure is limited by the size rule below.
  open / add ......... allowed only when ALL of these hold:
     1. the account has a LIVE copy whose record carries a valid website signature, and the same login has a wallet link to
        this account that the website signed after the wallet's own signature (the engine can't make either);
     2. one of those copied traders holds this coin NOW, on the SAME side (read from Hyperliquid; a 2-second cache may
        allow, but before refusing it reads again);
     3. after the order, the account's total positions stay within its own money on Hyperliquid x min(20, 1.5 x the
        highest leverage among ALL the traders it copies), plus 10% and $25 of room. Money and positions come from
        Hyperliquid, never from our database; before refusing, everything is read again.
  Anything else is refused.
"""
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler

INFO = "https://api.hyperliquid.xyz/info"
STABLES = {"USDC", "USDT0", "USDT", "USDH", "USDE", "USDHL"}
_cache: dict = {}
_weight = {"min": 0, "used": 0}
_pool = ThreadPoolExecutor(max_workers=16)          # reads go out together (speed for the switch)
READ_BUDGET = 400                      # Hyperliquid read weight per minute for this instance (its own IP, not the engine's)


def _env(k: str, default: str = "") -> str:
    return os.environ.get(k, default)


def _mac(text: str) -> str:
    return hmac.new(_env("COPY_SIGN_KEY").encode(), text.encode(), hashlib.sha256).hexdigest()


def _eq(a: str | None, b: str) -> bool:
    return bool(a) and hmac.compare_digest(a, b)


# ---------------------------------------------------------------------------------------------- Hyperliquid (public)
def _hl(body: dict, ttl: float, weight: int = 2):
    k = json.dumps(body, sort_keys=True)
    hit = _cache.get(k)
    if hit and ttl > 0 and time.time() - hit[0] < ttl:
        return hit[1]
    m = int(time.time() // 60)
    if _weight["min"] != m:
        _weight.update(min=m, used=0)
    if _weight["used"] + weight > READ_BUDGET:
        raise RuntimeError("read budget")
    _weight["used"] += weight
    req = urllib.request.Request(INFO, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=6) as r:
        val = json.loads(r.read())
    _cache[k] = (time.time(), val)
    return val


def _dexes() -> list[str]:
    return [""] + [d["name"] for d in (_hl({"type": "perpDexs"}, 6 * 3600) or []) if d]


def _dex_of(coin: str) -> str:
    return coin.split(":", 1)[0] if ":" in coin else ""


def _state(addr: str, dex: str, ttl: float) -> dict:
    return _hl({"type": "clearinghouseState", "user": addr, **({"dex": dex} if dex else {})}, ttl) or {}


def _pos(addr: str, coin: str, ttl: float) -> float:
    for p in _state(addr, _dex_of(coin), ttl).get("assetPositions", []):
        if (p.get("position") or {}).get("coin") == coin:
            return float(p["position"].get("szi") or 0)
    return 0.0


def _book(addr: str, ttl: float) -> dict:
    """The account's own money and positions on Hyperliquid: every perp dex + spot stablecoins."""
    eq = ntl = 0.0
    dx = _dexes()
    futs = [_pool.submit(_state, addr, d, ttl) for d in dx]
    spot_f = _pool.submit(_hl, {"type": "spotClearinghouseState", "user": addr}, ttl)
    for f in futs:
        s = f.result()
        eq += float((s.get("marginSummary") or {}).get("accountValue") or 0)
        ntl += sum(abs(float((p.get("position") or {}).get("positionValue") or 0)) for p in s.get("assetPositions", []))
    spot = spot_f.result() or {}
    eq += sum(float(b.get("total") or 0) for b in spot.get("balances", []) if b.get("coin") in STABLES)
    return {"equity": eq, "ntl": ntl}


def _mid(coin: str) -> float:
    mids = _hl({"type": "allMids", **({"dex": _dex_of(coin)} if _dex_of(coin) else {})}, 2) or {}
    return float(mids.get(coin) or 0)


# ---------------------------------------------------------------------------------------------- signed records (F1)
def _sb(path: str):
    url = _env("SUPABASE_URL").rstrip("/") + "/rest/v1/" + path
    key = _env("SUPABASE_KEY")
    req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=6) as r:
        return json.loads(r.read())


def _sb_insert(table: str, row: dict) -> None:
    url = _env("SUPABASE_URL").rstrip("/") + "/rest/v1/" + table
    key = _env("SUPABASE_KEY")
    req = urllib.request.Request(url, data=json.dumps(row).encode(), method="POST",
                                 headers={"apikey": key, "Authorization": "Bearer " + key, "Content-Type": "application/json", "Prefer": "return=minimal"})
    urllib.request.urlopen(req, timeout=6).read()


def copy_sig_text(c: dict, account: str) -> str:
    return f"copy|{c['id']}|{c['user_id']}|{(c.get('trader') or '').lower()}|{(account or '').lower()}"


def agent_sig_text(a: dict) -> str:
    return f"agent|{(a.get('agent_address') or '').lower()}|{(a.get('account') or '').lower()}|{a.get('user_id') or ''}"


def signed_traders(account: str) -> tuple[list[str], dict]:
    """The traders this account may follow: LIVE copies the website signed, AND, for every one of them, the same login has a
    wallet link to THIS account that the website signed right after the wallet itself signed the wallet check (Walter S1:
    the copy's wallet address comes from the database, so the copy signature alone can't prove the wallet is that login's)."""
    acct = account.lower()
    ag_f = _pool.submit(_sb, f"mi_agents?select=agent_address,account,user_id,claim_sig&account=eq.{acct}&revoked_at=is.null")
    rows = _sb(f"mi_copies?select=id,user_id,trader,account,status,sig&account=eq.{acct}&status=eq.live")
    agents = ag_f.result()
    bound = {a["user_id"] for a in agents if a.get("user_id") and _eq(a.get("claim_sig"), _mac(agent_sig_text(a)))}
    ok, bad, unlinked = [], 0, 0
    for c in rows:
        if c["user_id"] not in bound:
            unlinked += 1
        elif _eq(c.get("sig"), _mac(copy_sig_text(c, acct))) or _eq(c.get("sig"), _mac(copy_sig_text(c, ""))):
            ok.append(c["trader"].lower())
        else:
            bad += 1
    return sorted(set(ok)), {"live_copies": len(rows), "unsigned": bad, "no_signed_wallet_link": unlinked}


# ---------------------------------------------------------------------------------------------- the rules
def decide(b: dict) -> tuple[bool | None, str, dict]:
    kind, acct, coin = b.get("kind"), (b.get("account") or "").lower(), b.get("coin") or ""
    if kind == "close":
        return True, "close: always allowed (sent reduce-only when the signer signs)", {}
    if kind == "iso":
        add = float(b.get("add") or 0)
        return (add > 0), ("isolated margin add" if add > 0 else "isolated margin can only be added"), {"add": add}
    if kind == "lev":
        return True, "leverage: allowed; exposure is limited by the size rule", {"lev": b.get("lev"), "cross": b.get("is_cross")}
    if kind != "open":
        return False, f"unknown action {kind!r}", {}
    if not acct or not coin:
        return False, "missing account or coin", {}
    me_f, mid_f = _pool.submit(_book, acct, 15), _pool.submit(_mid, coin)    # the account + price, while records load
    traders, rec = signed_traders(acct)
    if not traders:
        return False, "no LIVE copy with a valid website signature for this account", rec
    side = 1 if b.get("is_buy") else -1
    pos = dict(zip(traders, _pool.map(lambda t: _pos(t, coin, 2), traders)))
    holders = [t for t in traders if pos[t] * side > 0]
    if not holders:                                        # F4: never refuse on a cached read
        pos = dict(zip(traders, _pool.map(lambda t: _pos(t, coin, 0), traders)))
        holders = [t for t in traders if pos[t] * side > 0]
    if not holders:
        return False, f"no copied trader holds {coin} {'long' if side > 0 else 'short'} now", {**rec, "traders": traders}
    def lev_of(ttl: float) -> float:                       # Walter S2: the whole account → ALL its signed traders count
        return max([bk["ntl"] / bk["equity"] if bk["equity"] > 0 else 0.0 for bk in _pool.map(lambda t: _book(t, ttl), traders)] or [0.0])
    lev = lev_of(60)
    cap = min(20.0, 1.5 * lev)
    px = mid_f.result() or float(b.get("px") or 0)
    sz = abs(float(b.get("sz") or 0))
    me = me_f.result()
    limit = me["equity"] * cap * 1.10 + 25
    after = me["ntl"] + sz * px
    if after > limit:                                      # F4 + Walter S3: fresh reads (account AND traders) before refusing
        me_f2 = _pool.submit(_book, acct, 0)
        lev = lev_of(0)
        cap = min(20.0, 1.5 * lev)
        me = me_f2.result()
        limit, after = me["equity"] * cap * 1.10 + 25, me["ntl"] + sz * px
    d = {**rec, "holders": holders, "trader_lev": round(lev, 3), "cap_x": round(cap, 3), "equity": round(me["equity"], 2),
         "after_ntl": round(after, 2), "limit": round(limit, 2)}
    if after > limit:
        return False, f"size: positions after the order ${after:,.0f} > ${limit:,.0f} (money x {cap:.2f})", d
    return True, "open: follows the copied trader, within the size rule", d


# ---------------------------------------------------------------------------------------------- HTTP
class handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        p = self.path.split("?")[0].rstrip("/")
        if p.endswith("/version") or p in ("", "/api/index"):
            self._send(200, {"service": "mrcopytrading copy-only signer", "mode": _env("SIGNER_MODE", "shadow"),
                             "commit": _env("VERCEL_GIT_COMMIT_SHA")[:12],
                             "repo": f"github.com/{_env('VERCEL_GIT_REPO_OWNER')}/{_env('VERCEL_GIT_REPO_SLUG')}",
                             "code": "https://github.com/jeevansongmy-spec/mrcopytrading-safety/tree/main/signer"})
        elif p.endswith("/health"):
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        if not self.path.split("?")[0].rstrip("/").endswith("/check"):
            return self._send(404, {"error": "not found"})
        tok = (self.headers.get("Authorization") or "").removeprefix("Bearer ").strip()
        if not _env("SIGNER_TOKEN") or not _eq(tok, _env("SIGNER_TOKEN")):
            return self._send(401, {"error": "unauthorized"})
        try:
            b = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0) or 0) or b"{}")
        except Exception:  # noqa: BLE001
            return self._send(400, {"error": "bad json"})
        t0 = time.time()
        try:
            ok, why, det = decide(b)
        except Exception as e:  # noqa: BLE001 — no answer is never a refusal in shadow; it is logged as unknown
            ok, why, det = None, f"could not check: {str(e)[:140]}", {}
        ms = int((time.time() - t0) * 1000)
        det = {**det, "rtt_prev_ms": b.get("rtt_prev_ms"), "check_ms": ms, "lev_req": b.get("lev"), "add": b.get("add")}
        try:
            _sb_insert("mi_signer_checks", {"mode": _env("SIGNER_MODE", "shadow"), "account": (b.get("account") or "").lower(),
                                            "kind": b.get("kind"), "coin": b.get("coin"), "is_buy": b.get("is_buy"),
                                            "sz": b.get("sz"), "detail": det, "allowed": ok, "reason": why, "ms": ms})
        except Exception:  # noqa: BLE001
            pass
        self._send(200, {"allowed": ok, "reason": why, "ms": ms})
