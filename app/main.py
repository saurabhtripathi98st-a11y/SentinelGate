from flask import Flask, request, jsonify, render_template
import sqlite3
import time
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logic.core import guardian, init_db, DB_PATH
from logic.analyst import get_system_intelligence

app = Flask(__name__)
init_db()

def log_request(ip, latency, status, reason):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO logs (ip, latency, status, reason) VALUES (?, ?, ?, ?)",
                 (ip, latency, status, reason))
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/access')
def access_resource():
    start = time.time()
    ip = request.remote_addr
    
    # Check Security
    is_safe, msg = guardian.check_security(request.args.get('input', ''))
    if not is_safe:
        log_request(ip, 0, "BLOCKED", msg)
        return jsonify({"error": msg}), 403
    
    # Check Rate Limit
    is_allowed, msg = guardian.allow_request(ip)
    if not is_allowed:
        log_request(ip, 0, "BLOCKED", msg)
        return jsonify({"error": msg}), 429

    # --- SIMULATE CHAOS JITTER ---
    # If the request has 'chaos=true', we add random high latency
    delay = 0.05
    if request.args.get('chaos') == 'true':
        delay = random.uniform(0.1, 0.5) # Randomly very slow!
    
    time.sleep(delay) 
    latency = time.time() - start
    log_request(ip, latency, "ALLOWED", "SUCCESS")
    return jsonify({"status": "Success", "latency": round(latency, 4)})

@app.route('/api/intelligence')
def intelligence():
    return jsonify(get_system_intelligence())

@app.route('/api/logs')
def logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, status, reason, timestamp FROM logs ORDER BY timestamp DESC LIMIT 10")
    data = [{"ip": r[0], "status": r[1], "reason": r[2], "time": r[3]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5005, debug=True)
