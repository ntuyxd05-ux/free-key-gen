from flask import Flask, request, jsonify
app = Flask(__name__)

@app.get("/")
def home():
    return "<h2>Key Generator</h2><button onclick=\"gen()\">Generate Key</button><pre id='out'></pre><script>async function gen(){let r=await fetch('/gen');let j=await r.json();document.getElementById('out').innerText=JSON.stringify(j,null,2)}</script>"

@app.get("/gen")
def gen():
    import secrets, time
    key = "FREE-" + secrets.token_hex(6).upper()
    exp = int(time.time()) + 24*60*60
    return jsonify({"key": key, "exp": exp})

@app.get("/validate")
def validate():
    key = request.args.get("key","")
    ok = key.startswith("FREE-") and len(key) > 10
    return jsonify({"ok": ok})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
