import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/traffic.db')

def get_system_intelligence():
    conn = sqlite3.connect(DB_PATH)
    # Check the last 50 requests for a more reactive window
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50", conn)
    conn.close()
    
    if df.empty or len(df) < 5:
        return {"status": "COLLECTING", "p99": 0, "anomalies": 0, "avg": 0, "total_requests": len(df)}

    # Statistical Intelligence
    df['latency'] = pd.to_numeric(df['latency'])
    mean_lat = df['latency'].mean()
    std_lat = df['latency'].std()
    
    # Calculate Z-scores for the whole window
    # If std_lat is 0, z_score is 0
    df['z'] = (df['latency'] - mean_lat) / std_lat if std_lat > 0 else 0
    anomalies = df[df['z'].abs() > 1.5] # Tightened threshold to 1.5 for easier triggering
    
    p99 = df['latency'].quantile(0.99)
    
    # Trigger DANGER if anomalies exist or rate blocks are high
    block_count = len(df[df['status'] == 'BLOCKED'])
    is_danger = len(anomalies) > 0 or block_count > 10

    return {
        "status": "DANGER" if is_danger else "OPTIMAL",
        "p99": round(p99, 4),
        "avg": round(mean_lat, 4),
        "anomalies": len(anomalies),
        "total_requests": len(df)
    }
