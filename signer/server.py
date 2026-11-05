"""MrCopyTrading COPY-ONLY SIGNER — the server that SIGNS (Railway, one copy only, private network next to the engine).
Public code: github.com/jeevansongmy-spec/mrcopytrading-safety (folder signer/); GET /version shows the commit that runs.

The rules are in signer_core.py (the same file the shadow checks used). This server adds the signing:
  POST /check  -> would the rules allow this action? (shadow; no signing)
  POST /act    -> check, then sign and send to Hyperliquid with the account's trade-only key, and answer with EXACTLY what
                  Hyperliquid answered. A refused action is answered in Hyperliquid's own format, so the engine treats it
                  like any refused order (Walter F4). Closes go out reduce-only (the SDK's market_close). The engine's order
                  fence (expiresAfter) and order id (cloid) are passed through unchanged (Walter F5).
  GET /version, /health

One request at a time (HTTPServer, not threaded): two signatures can never share a nonce (Walter F5).
Keys: the encrypted trade-only keys stay in the database; the unlock secret (COPYTRADE_KEY_SECRET) is a setting of THIS
service. With SIGNER_KEYPOOL=on it also keeps 3 spare keys ready for new users (so the engine needs no secret at all).
SIGNER_MODE: "shadow" = /act refuses to sign (checks only) · "enforce" = /act signs.
"""
import base64
import hashlib
import json
import os
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import signer_core as core
from signer_core import _env, _eq, _sb, _sb_insert, decide

SPARE_KEYS = 3
EXCHANGE_TIMEOUT_S = 10
_ex_cache: dict = {}


def _fernet():
    sec = _env("COPYTRADE_KEY_SECRET").strip()
    if not sec:
        return None
    from cryptography.fernet import Fernet
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(sec.encode()).digest()))   # = the engine's copytrade._fernet


_enc: dict = {}                                       # account -> its rows with ENCRYPTED keys (closes still work if the database is down)


def _key(acct: str, agent: str | None) -> tuple[str, str]:
    try:
        rows = _sb(f"mi_agents?select=agent_address,agent_key&account=eq.{acct}&revoked_at=is.null")
        _enc[acct] = rows
    except Exception:  # noqa: BLE001 — database down: the last rows read (encrypted) are enough to sign a close
        rows = _enc.get(acct) or []
    row = next((r for r in rows if not agent or r["agent_address"] == agent.lower()), None)
    if not row or not (row.get("agent_key") or "").startswith("enc:"):
        raise RuntimeError("no encrypted trade-only key for this account")
    f = _fernet()
    if not f:
        raise RuntimeError("COPYTRADE_KEY_SECRET is not set on the signer")
    return row["agent_address"], f.decrypt(row["agent_key"][4:].encode()).decode()


def _exchange(acct: str, agent: str | None):
    from eth_account import Account
    from hyperliquid.exchange import Exchange
    from hyperliquid.utils import constants
    agent_addr, key = _key(acct, agent)
    k = (agent_addr, acct)
    hit = _ex_cache.get(k)
    if hit and time.time() - hit[0] < 6 * 3600:
        return hit[1]
    ex = Exchange(Account.from_key(key), constants.MAINNET_API_URL, account_address=acct, perp_dexs=core._dexes(), timeout=EXCHANGE_TIMEOUT_S)
    _ex_cache[k] = (time.time(), ex)
    return ex


def _refused(kind: str, why: str):
    msg = "Copy-only signer refused: " + why
    if kind in ("open", "close"):                         # Hyperliquid's own order answer → the engine's "rejected" path
        return {"status": "ok", "response": {"type": "order", "data": {"statuses": [{"error": msg}]}}}
    return {"status": "err", "response": msg}             # leverage / margin: the engine's existing "not ok" path


def act(b: dict):
    kind, acct, coin = b.get("kind"), (b.get("account") or "").lower(), b.get("coin") or ""
    if _env("SIGNER_MODE", "shadow") != "enforce":
        raise PermissionError("the signer is in shadow mode: it does not sign")
    if kind == "close":
        ok, why, det = True, "close (reduce-only)", {}
    else:
        try:
            ok, why, det = decide(b)
        except Exception as e:  # noqa: BLE001 — could not read: one more try, then refuse (the engine retries next pass)
            try:
                ok, why, det = decide(b)
            except Exception as e2:  # noqa: BLE001
                ok, why, det = False, f"could not check ({str(e2)[:100]})", {}
    if not ok:
        _log(b, False, why, det)
        return _refused(kind, why)
    from hyperliquid.utils.types import Cloid
    ex = _exchange(acct, b.get("agent"))
    ex.set_expires_after(b.get("expires_after"))         # the engine's lease fence, unchanged (F5)
    cl = Cloid.from_str(b["cloid"]) if b.get("cloid") else None
    if kind == "open":
        res = ex.market_open(coin, bool(b.get("is_buy")), float(b["sz"]), None, float(b.get("slippage") or 0.01), cloid=cl, builder=b.get("builder"))
    elif kind == "close":
        res = ex.market_close(coin, sz=float(b["sz"]) if b.get("sz") is not None else None, slippage=float(b.get("slippage") or 0.01), cloid=cl, builder=b.get("builder"))
    elif kind == "lev":
        res = ex.update_leverage(int(b["lev"]), coin, is_cross=bool(b.get("is_cross")))
    elif kind == "iso":
        res = ex.update_isolated_margin(float(b["add"]), coin)
    else:
        return _refused(kind or "", f"unknown action {kind!r}")
    _log(b, True, why, {**det, "answer": json.dumps(res)[:300] if res is not None else None})
    return res


def _log(b: dict, ok, why: str, det: dict) -> None:
    try:
        _sb_insert("mi_signer_checks", {"mode": _env("SIGNER_MODE", "shadow"), "account": (b.get("account") or "").lower(), "kind": b.get("kind"),
                                        "coin": b.get("coin"), "is_buy": b.get("is_buy"), "sz": b.get("sz"), "detail": det, "allowed": ok, "reason": why,
                                        "ms": det.get("check_ms")})
    except Exception:  # noqa: BLE001
        pass


def _key_pool_loop() -> None:
    """Keep SPARE_KEYS unclaimed trade-only keys ready (the engine's _fill_key_pool, moved here for the Lock)."""
    from eth_account import Account
    while True:
        try:
            f = _fernet()
            if f and _env("SIGNER_KEYPOOL") == "on":
                spare = _sb("mi_agents?select=agent_address&account=is.null&revoked_at=is.null")
                for _ in range(max(0, SPARE_KEYS - len(spare))):
                    a = Account.create()
                    key = "0x" + a.key.hex().removeprefix("0x")
                    _sb_insert("mi_agents", {"agent_address": a.address.lower(), "agent_key": "enc:" + f.encrypt(key.encode()).decode()})
        except Exception:  # noqa: BLE001
            pass
        time.sleep(60)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):                           # no request lines in the logs (they carry account addresses)
        pass

    def _send(self, code: int, body) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        p = self.path.split("?")[0].rstrip("/")
        if p in ("", "/version"):
            self._send(200, {"service": "mrcopytrading copy-only signer", "host": "railway", "mode": _env("SIGNER_MODE", "shadow"),
                             "commit": _env("RAILWAY_GIT_COMMIT_SHA")[:12], "repo": f"github.com/{_env('RAILWAY_GIT_REPO_OWNER')}/{_env('RAILWAY_GIT_REPO_NAME')}",
                             "code": "https://github.com/jeevansongmy-spec/mrcopytrading-safety/tree/main/signer"})
        elif p == "/health":
            self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        p = self.path.split("?")[0].rstrip("/")
        tok = (self.headers.get("Authorization") or "").removeprefix("Bearer ").strip()
        if not _env("SIGNER_TOKEN") or not _eq(tok, _env("SIGNER_TOKEN")):
            return self._send(401, {"error": "unauthorized"})
        try:
            b = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0) or 0) or b"{}")
        except Exception:  # noqa: BLE001
            return self._send(400, {"error": "bad json"})
        t0 = time.time()
        if p == "/check":
            try:
                ok, why, det = decide(b)
            except Exception as e:  # noqa: BLE001
                ok, why, det = None, f"could not check: {str(e)[:140]}", {}
            det = {**det, "rtt_prev_ms": b.get("rtt_prev_ms"), "check_ms": int((time.time() - t0) * 1000)}
            _log(b, ok, why, det)
            return self._send(200, {"allowed": ok, "reason": why, "ms": det["check_ms"]})
        if p == "/act":
            try:
                return self._send(200, act(b))
            except PermissionError as e:
                return self._send(503, {"error": str(e)})
            except Exception as e:  # noqa: BLE001 — the engine reads an error as "no answer" (pending, settled by cloid)
                return self._send(502, {"error": str(e)[:200]})
        self._send(404, {"error": "not found"})


class Server6(HTTPServer):
    address_family = socket.AF_INET6                     # Railway's private network is IPv6 (dual-stack bind)

    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


if __name__ == "__main__":
    threading.Thread(target=_key_pool_loop, daemon=True, name="key-pool").start()
    Server6(("::", int(_env("PORT", "8080"))), Handler).serve_forever()
