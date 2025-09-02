from flask import Flask, request, jsonify
import secrets, time, os

app = Flask(__name__)

# TTL = 24 jam
TTL = 24 * 60 * 60
db = {}  # pakai dictionary sederhana (reset tiap restart server)

def generate_key():
    return "FREE-" + secrets.token_hex(6).upper()

@app.route("/")
def home():
    return """
    <h2>Key Generator</h2>
    <button onclick="getKey()">Generate Key</button>
    <p id="out"></p>
    <script>
    async function getKey(){
        const res = await fetch('/gen').then(r=>r.json());
        document.getElementById('out').innerText = 
            "KEY: " + res.key + "\\n(Berlaku 24 jam)";
    }
    </script>
    """

@app.route("/gen")
def gen():
    key = generate_key()
    db[key] = time.time() + TTL
    return jsonify({"key": key, "exp": int(time.time()) + TTL})

@app.route("/validate")
def validate():
    key = request.args.get("key")
    if not key or key not in db:
        return jsonify({"ok": False, "err": "invalid"})
    if time.time() > db[key]:
        return jsonify({"ok": False, "err": "expired"})
    return jsonify({"ok": True, "msg": "valid"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
