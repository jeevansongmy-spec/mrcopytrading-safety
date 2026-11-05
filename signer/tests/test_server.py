"""Signer tests — no real order is ever sent (a fake exchange records what would go out). Run: python tests/test_server.py"""
import json, os, sys, base64, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SUPABASE_URL", "http://x"); os.environ.setdefault("SUPABASE_KEY", "x"); os.environ["COPY_SIGN_KEY"] = "k"
import server, signer_core
ok = True
def check(name, cond):
    global ok; ok = ok and cond; print(("PASS " if cond else "FAIL ") + name)

class FakeEx:
    def __init__(self): self.calls = []; self.exp = "unset"
    def set_expires_after(self, v): self.exp = v
    def market_open(self, coin, is_buy, sz, px, slip, cloid=None, builder=None):
        self.calls.append(("open", coin, is_buy, sz, slip, cloid.to_raw() if cloid else None, builder)); return {"status": "ok", "response": {"type": "order", "data": {"statuses": [{"filled": {"avgPx": "1", "totalSz": str(sz), "oid": 1}}]}}}
    def market_close(self, coin, sz=None, slippage=0.01, cloid=None, builder=None):
        self.calls.append(("close", coin, sz, slippage, cloid.to_raw() if cloid else None)); return None
    def update_leverage(self, lev, coin, is_cross=True): self.calls.append(("lev", coin, lev, is_cross)); return {"status": "ok"}
    def update_isolated_margin(self, amt, coin): self.calls.append(("iso", coin, amt)); return {"status": "ok"}
orig_exchange, orig_log = server._exchange, server._log
fake = FakeEx(); server._exchange = lambda acct, agent: fake; server._log = lambda *a, **k: None
cl = "0x" + "ab" * 16
# 1 shadow mode never signs
os.environ["SIGNER_MODE"] = "shadow"
try: server.act({"kind": "open", "account": "0xa", "coin": "BTC", "is_buy": True, "sz": 1}); check("shadow mode refuses to sign", False)
except PermissionError: check("shadow mode refuses to sign", True)
os.environ["SIGNER_MODE"] = "enforce"
# 2 refused open → Hyperliquid's own order format, nothing sent
server.decide = lambda b: (False, "no copied trader holds DOGE long now", {})
r = server.act({"kind": "open", "account": "0xa", "coin": "DOGE", "is_buy": True, "sz": 1, "cloid": cl})
check("refusal in Hyperliquid order format", r["response"]["data"]["statuses"][0]["error"].startswith("Copy-only signer refused"))
check("refusal sends nothing", fake.calls == [])
r = server.act({"kind": "lev", "account": "0xa", "coin": "DOGE", "lev": 5, "is_cross": True})
check("refused leverage → status err", r["status"] == "err")
# 3 allowed open: cloid, builder, slippage, expiry passed through unchanged
server.decide = lambda b: (True, "ok", {})
r = server.act({"kind": "open", "account": "0xa", "coin": "HYPE", "is_buy": True, "sz": 0.5, "slippage": 0.01, "cloid": cl, "builder": {"b": "0xbb", "f": 40}, "expires_after": 123456})
check("open sent once with the engine's cloid/builder", fake.calls[-1] == ("open", "HYPE", True, 0.5, 0.01, cl, {"b": "0xbb", "f": 40}))
check("expiresAfter passed through", fake.exp == 123456)
check("Hyperliquid answer returned as-is", r["response"]["data"]["statuses"][0]["filled"]["totalSz"] == "0.5")
# 4 close never checked, always reduce-only market_close; None (no position) passed through
server.decide = lambda b: (_ for _ in ()).throw(AssertionError("close must not be checked"))
r = server.act({"kind": "close", "account": "0xa", "coin": "HYPE", "sz": 0.5, "cloid": cl})
check("close → market_close (reduce-only), answer None passed", fake.calls[-1][0] == "close" and r is None)
# 5 read error twice → refused, nothing sent
n = len(fake.calls); server.decide = lambda b: (_ for _ in ()).throw(RuntimeError("read budget"))
r = server.act({"kind": "open", "account": "0xa", "coin": "HYPE", "is_buy": True, "sz": 1, "cloid": cl})
check("unreadable → refused, not sent", "could not check" in r["response"]["data"]["statuses"][0]["error"] and len(fake.calls) == n)
# 6 key unlock = the engine's own derivation
os.environ["COPYTRADE_KEY_SECRET"] = "s3cret"
from cryptography.fernet import Fernet
eng = Fernet(base64.urlsafe_b64encode(hashlib.sha256(b"s3cret").digest()))
tok = eng.encrypt(b"0xdeadbeef")
check("decrypts what the engine encrypted", server._fernet().decrypt(tok) == b"0xdeadbeef")
# 7 speed: a ready connection is used without any database read; the log never delays the answer
import time
server._ex_cache[("0xagent", "0xacct")] = (time.time(), fake)
real_key = server._key
server._key = lambda acct, agent: (_ for _ in ()).throw(AssertionError("no database read when a connection is ready"))
check("ready connection: no database read", orig_exchange("0xacct", "0xAGENT") is fake)
server._ex_cache[("0xagent", "0xacct")] = (time.time() - 7 * 3600, fake)
try: orig_exchange("0xacct", "0xagent"); check("connection older than 6 h is not used", False)
except AssertionError: check("connection older than 6 h is not used", True)
server._key = real_key
slow = []
server._log_now = lambda *a: (time.sleep(1), slow.append(1))
t0 = time.time(); orig_log({"kind": "open"}, True, "ok", {}); dt = time.time() - t0
check("log written after the answer (no wait)", dt < 0.1)
server._bg.shutdown(wait=True); check("log still written", slow == [1])
print("ALL PASS" if ok else "FAILED"); sys.exit(0 if ok else 1)
