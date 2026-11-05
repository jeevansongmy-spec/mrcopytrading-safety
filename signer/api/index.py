"""Vercel entry of the copy-only signer (shadow checks only, no keys). The rules live in ../signer_core.py."""
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from signer_core import _env, _eq, _sb_insert, decide  # noqa: E402

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
