import sqlite3
import os
import time
import re
from collections import defaultdict

# 1. Database Initialization
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/traffic.db')

def init_db():
    if not os.path.exists(os.path.dirname(DB_PATH)): os.makedirs(os.path.dirname(DB_PATH))
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT, latency REAL, status TEXT, reason TEXT, 
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# 2. Token Bucket Algorithm (The SDE Flex)
class Guardian:
    def __init__(self, rate=2, capacity=5):
        self.tokens = defaultdict(lambda: float(capacity))
        self.last_check = defaultdict(time.time)
        self.rate = rate # Tokens per second
        self.capacity = capacity
        self.sqli_patterns = [r"SELECT", r"UNION", r"DROP", r"OR 1=1", r"--"]

    def allow_request(self, ip):
        now = time.time()
        # Refill tokens based on time passed
        lapse = now - self.last_check[ip]
        self.tokens[ip] = min(self.capacity, self.tokens[ip] + (lapse * self.rate))
        self.last_check[ip] = now
        
        if self.tokens[ip] >= 1:
            self.tokens[ip] -= 1
            return True, "ALLOWED"
        return False, "RATE_LIMIT_EXCEEDED"

    def check_security(self, text):
        for p in self.sqli_patterns:
            if re.search(p, str(text), re.IGNORECASE):
                return False, "SQL_INJECTION_ATTACK"
        return True, "SAFE"

guardian = Guardian()
