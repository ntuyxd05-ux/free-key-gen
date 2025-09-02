from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import secrets, time, os

# ---- penyimpanan sederhana in-memory (reset saat restart)
KEYS = {}  # key -> expired_at (epoch)

TTL = 24 * 60 * 60  # 24 jam
app = Flask(__name__)

def generate_key():
    return "FREE-" + secrets.token_hex(6).upper()

@app.route("/")
def home():
    return """
    <h2>Key Generator (Free)</h2>
    <button onclick="getKey()">Generate Key</button>
    <p id="out"></p>
    <script>
      async function getKey(){
        const r = await fetch('/gen');
        const j = await r.json();
        document.getElementById('out').innerText =
          "KEY: " + j.key + "\\n(berlaku 24 jam)";
      }
    </script>
    """

@app.route("/gen")
def gen():
    key = generate_key()
    KEYS[key] = int(time.time()) + TTL
    return jsonify({"key": key, "exp": KEYS[key]})

@app.route("/validate")
def validate():
    key = request.args.get("key", "")
    now = int(time.time())
    if (not key) or (key not in KEYS):
        return jsonify({"ok": False, "err": "invalid"})
    if now > KEYS[key]:
        del KEYS[key]
        return jsonify({"ok": False, "err": "expired"})
    return jsonify({"ok": True})
    
if __name__ == "__main__":
    # Render akan set PORT; lokal default 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
