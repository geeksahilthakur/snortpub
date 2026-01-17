<div align="center">

<img src="https://via.placeholder.com/1200x260/f8fafc/111827?text=SnortSheet" width="100%" alt="SnortSheet"/>

<h1>SnortSheet</h1>

<p>
A Serverless SIEM & Agentic SOC Framework<br/>
Snort → Python Middleware → Google Sheets → AI Automation
</p>

</div>

---

## License Status

<table>
<tr>
<td width="8%" align="center">🔒</td>
<td>
<strong>Proprietary Software</strong><br/>
This project is <strong>not open source</strong>. All rights are reserved by the author.
</td>
</tr>
</table>

---

## Usage Permissions

<table>
<thead>
<tr>
<th align="left">Action</th>
<th align="center">Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>View source code</td>
<td align="center">✅ Allowed</td>
</tr>
<tr>
<td>Copy or reuse code</td>
<td align="center">❌ Not allowed</td>
</tr>
<tr>
<td>Modify or fork</td>
<td align="center">❌ Not allowed</td>
</tr>
<tr>
<td>Commercial or non-commercial use</td>
<td align="center">❌ Not allowed</td>
</tr>
<tr>
<td>Reverse engineering</td>
<td align="center">❌ Not allowed</td>
</tr>
</tbody>
</table>

---

## About SnortSheet

SnortSheet is a **proprietary security middleware** designed to bridge  
**Snort IDS** with **cloud-native monitoring and automation workflows**.

Instead of relying on heavy infrastructure such as ELK or commercial SIEMs,
SnortSheet uses **Google Sheets as a lightweight SOC dashboard**, enabling:

- real-time visibility  
- low operational overhead  
- rapid alert access  
- AI-ready data pipelines  

This project focuses on **practical security engineering**, not vendor lock-in.

---

## Core Capabilities

<table>
<tr>
<td width="50%">

- Snort CSV alert ingestion  
- Intelligent deduplication  
- Rate-limited forwarding  
- HTML email alerts  

</td>
<td width="50%">

- Google Sheets SOC dashboard  
- Cloud-native visibility  
- Agentic AI compatibility  
- Automation-ready structure  

</td>
</tr>
</table>

---

## Architecture Overview

Attacker
↓
Snort IDS
↓
alert.csv
↓
Python Bridge
(deduplication & throttling)
↓
Google Apps Script
↓
Google Sheets (SOC) + Email Alerts


---

## Security Design Principles

- One-way outbound data flow only  
- No inbound ports required  
- TLS-encrypted transport  
- No Google credentials stored locally  
- Webhook-based backend isolation  
- Strict payload validation  

The sensor node remains isolated and hardened by design.

---

## Repository Structure

snortsheet/
├── snort_bridge.py # Core proprietary middleware
├── code.gs # Google Apps Script backend
├── requirements.txt # Python dependencies
├── README.md # Documentation
└── LICENSE # Proprietary license


---

## Licensing & Permissions

Any use of this software **requires explicit written permission**.

For licensing, research access, or commercial discussions:

**Email:** dev.sahilthakur@gmail.com  

Unauthorized usage constitutes **copyright infringement**.

---

## Author

**Sahil Thakur**  
Security Researcher & Developer  

Focus:  
Building lean, intelligent security systems without enterprise bloat.

---

## License (Full Text)

<details>
<summary>Click to expand license</summary>

Copyright (c) 2026 Sahil Thakur.
All Rights Reserved.

This software and the associated source code are proprietary.
No copying, modification, distribution, reverse engineering,
or use is permitted without explicit written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.


</details>

---

<div align="center">
<sub>Security is a process — not a product.</sub>
</div>
