# 🛡️ SentinelGate v2.0
**API Security Gateway & Real-Time Traffic Intelligence**

SentinelGate is a high-performance middleware layer designed to protect backend infrastructure from DDoS, brute-force attacks, and SQL Injection. Unlike traditional firewalls, it uses **Statistical Anomaly Detection** to identify system degradation in real-time.

## 🚀 Key Features
* **Token Bucket Rate Limiter:** Custom implementation for high-concurrency request management.
* **Z-Score Anomaly Detection:** Uses Pandas to calculate $Z = (x - \mu) / \sigma$ to detect behavioral deviations.
* **p99 Latency Monitoring:** Real-time tail latency analysis to ensure high-quality UX.
* **Regex Firewall:** Signature-based filtering to block OWASP Top 10 threats like SQLi.
* **Cyber-Ops Dashboard:** Interactive SOC interface built with Plotly.js and Tailwind CSS.

## 🏗️ Architecture
The system intercepts every request, logs metrics to a SQLite store, and uses a Pandas-driven analytics engine to update system health status every 2 seconds.

## 🛠️ Tech Stack
Python (Flask, Pandas), SQLite3, Plotly.js, Tailwind CSS, Git.
