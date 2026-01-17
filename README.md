# 🛡️ SnortSheet  
### *The “Serverless” SIEM & Agentic SOC Framework*

> **Turn Google Sheets into a Real-Time Security Dashboard**  
> An advanced Python middleware bridging **Snort IDS** with **Agentic AI workflows** (n8n, LLMs).

---

<p align="center">
  <img src="https://img.shields.io/badge/IDS-Snort-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/SIEM-Serverless-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Agentic-AI-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge">
</p>

---

## 📖 Table of Contents

- [🧐 About the Project](#-about-the-project)
- [💎 Why SnortSheet?](#-why-snortsheet)
- [🚀 The Agentic SOC Vision](#-the-agentic-soc-vision)
- [⚙️ Technical Architecture](#️-technical-architecture)
- [🔒 Security Considerations](#-security-considerations)
- [🛠️ Installation Guide](#️-installation-guide)
- [🏃‍♂️ Usage & Testing](#️-usage--testing)
- [🔧 Advanced Configuration](#-advanced-configuration)
- [❓ Troubleshooting & FAQ](#-troubleshooting--faq)
- [🗺️ Roadmap](#️-roadmap)
- [👨‍💻 Developer](#-developer)
- [📄 License](#-license)

---

## 🧐 About the Project

**SnortSheet** is a lightweight, security-first middleware that connects **Snort IDS** with the cloud-native power of **Google Sheets**, transforming raw packet alerts into a **real-time, collaborative SOC dashboard**.

Traditional SIEM stacks (ELK, Splunk, Graylog) are powerful—but expensive, heavy, and complex.  
SnortSheet removes that barrier by **eliminating databases entirely** and streaming alerts directly to the cloud.

🎯 **Mission:**  
Democratize intrusion detection, visualization, and *agentic security automation* for everyone.

---

## 📂 Repository Structure

```
snortsheet/
├── snort_bridge.py
├── code.gs
├── requirements.txt
└── README.md
```

---

## 💎 Why SnortSheet?

| Feature | Traditional SIEM | SnortSheet |
|------|------------------|-----------|
| Infrastructure Cost | 💸 High | 🟢 Free |
| Hardware Required | 🖥️ Heavy | 🍓 Raspberry Pi |
| Setup Complexity | 🔥 Complex | ⚡ Simple |
| Mobile Access | ❌ Rare | ✅ Native |
| AI Integration | ⚙️ Hard | 🤖 Ready |

---

## 🚀 The Agentic SOC Vision

SnortSheet acts as the **trigger layer** for autonomous SOC workflows using AI agents.

- False Positive Analysis via LLMs  
- Auto-block attackers via firewall automation  
- Threat intelligence enrichment  
- Automated SOC reporting  

---

## ⚙️ Technical Architecture

```
Attacker → Snort IDS → alert.csv → Python Bridge → Google Apps Script → Google Sheets / Email
```

---

## 🔒 Security Considerations

- One-way outbound data flow  
- TLS-encrypted communication  
- No Google credentials stored  
- Strict JSON validation  

---

## 🛠️ Installation Guide

### Prerequisites
- Ubuntu / Debian / Kali Linux  
- Python 3.8+  
- Internet access  

### Phase 1 — Google Apps Script
1. Create Google Sheet  
2. Extensions → Apps Script  
3. Paste `code.gs`  
4. Deploy as Web App (Access: Anyone)  
5. Copy Webhook URL  

### Phase 2 — Snort Setup
```
sudo apt update && sudo apt install snort -y
```

Add to `/etc/snort/snort.conf`:
```
output alert_csv: /var/log/snort/alert.csv timestamp,msg,proto,src,srcport,dst,dstport
```

### Phase 3 — Python Bridge
```
git clone https://github.com/geeksahil/snortsheet.git
cd snortsheet
pip3 install -r requirements.txt
```
Edit:
```
WEBHOOK_URL = "YOUR_GOOGLE_SCRIPT_URL"
```

Run:
```
sudo python3 snort_bridge.py
```

---

## 🏃‍♂️ Usage & Testing

| Test | Command |
|----|--------|
| ICMP | `ping <sensor-ip>` |
| DNS | `nslookup google.com` |
| HTTP | `curl http://example.com` |

---

## 🗺️ Roadmap

- Docker support  
- Slack / Discord alerts  
- GeoIP dashboards  
- One-click installer  

---

## 👨‍💻 Developer

**Sahil Thakur** (geeksahil)  
Lead Developer & Security Researcher  

---

## 📄 License

Copyright (c) 2026 Sahil Thakur.  
All Rights Reserved.

### PROPRIETARY LICENSE

This software and source code are the exclusive property of Sahil Thakur.

**Restrictions**
- No copying, modification, or distribution  
- No reverse engineering  
- No use without written permission  

**Contact:** dev.sahilthakur@gmail.com  

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
