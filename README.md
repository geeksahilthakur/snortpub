<div align="center">

<!-- PLACEHOLDER FOR LOGO - You can generate this later with Nano Banana -->

<img src="https://www.google.com/search?q=https://via.placeholder.com/800x200/1e1e2e/ffffff%3Ftext%3DSnortPub" alt="SnortPub Logo" width="100%" />

🛡️ SnortPub

The "Serverless" SIEM & Agentic SOC Starter Kit

Turn Google Sheets into a Real-Time Security Dashboard. An Open-Source Python Middleware bridging Snort IDS and Agentic AI (n8n, LLMs).

View Demo • Report Bug • Request Feature

</div>

📖 Table of Contents

About the Project

Why SnortPub? (Feasibility & Value)

🚀 The Agentic SOC Vision (Use Cases)

⚙️ Architecture

🛠️ Installation Guide

Step 1: Google Sheets Setup

Step 2: Snort Configuration

Step 3: Python Bridge Setup

🏃‍♂️ Usage & Testing

👨‍💻 Developer

🧐 About the Project

SnortPub serves as a vital bridge in the modern cybersecurity stack, acting as lightweight, open-source middleware. It seamlessly connects the industry-standard deep packet inspection capabilities of Snort IDS with the ubiquitous accessibility and collaborative power of Google Sheets. By marrying a battle-tested security engine with a cloud-native spreadsheet, it democratizes network monitoring and incident response.

In the traditional cybersecurity landscape, effectively managing and visualizing Snort logs is a significant hurdle. It typically necessitates deploying and maintaining resource-intensive infrastructure like MySQL databases, the ELK Stack (Elasticsearch, Logstash, Kibana), or expensive proprietary solutions like Splunk. These setups often require dedicated hardware, complex configuration, and significant maintenance overhead, which can be a barrier for students, hobbyists, and small teams trying to learn security concepts.

SnortPub radically simplifies this architecture. It bypasses the need for local databases entirely by piping alert data directly to the cloud via a custom, secure Python bridge. Key features include intelligent Anti-Flood logic that intelligently groups repetitive alerts to prevent API throttling and inbox spam, Real-time Email Alerts that deliver actionable intelligence immediately to your device, and a Live Dashboard that leverages Google Sheets' native charting tools for instant visualization of attack vectors and trends.

More than just a logging tool, SnortPub represents the foundational layer for a democratized Agentic SOC (Security Operations Center). It enables users to construct a sophisticated security monitoring environment without incurring enterprise software costs. By moving data to the cloud, it opens the door for integration with automation platforms (like n8n) and Large Language Models, allowing for automated threat analysis and response workflows that were previously accessible only to large organizations.

📂 Repository Structure

snortpub/
├── snort_bridge.py    # The Python Connector (Smart Logic & Anti-Flood)
├── code.gs            # Google Apps Script (The Backend Receiver)
├── README.md          # Documentation
└── requirements.txt   # Dependencies



💎 Why SnortPub? (Feasibility & Value)

Why should you use SnortPub over standard logging?

Zero Cost Infrastructure: No need to pay for cloud databases or host a heavy ELK stack. Google Sheets is your free, cloud-native database.

Accessibility: Monitor your network threats from anywhere in the world using the Google Sheets mobile app.

Low Latency: Alerts are pushed in near real-time (with smart throttling to prevent API bans).

Feasibility: Runs on anything from a Raspberry Pi to a high-end Linux server.

Data Portability: Once data is in Sheets, it is unlocked. Connect it to Looker Studio, Tableau, or AI agents easily.

🚀 The Agentic SOC Vision: Integrate with n8n & LLMs

This is where SnortPub shines. By getting data out of a text file and into the Cloud/API ecosystem, you unlock Agentic Workflows.

🔗 Possible Integrations (The "What Ifs")

SnortPub ➡️ Google Sheets ➡️ n8n ➡️ OpenAI/Gemini

Scenario: Snort detects a "Possible SQL Injection".

Agentic Action: An n8n workflow reads the new row, sends the payload to GPT-4 for analysis, and asks: "Is this a false positive?"

Result: The AI updates the sheet with "Confirmed Threat" or "False Alarm."

Automated Firewall Response

Scenario: Snort detects a "Brute Force Attack" from IP 192.168.x.x.

Agentic Action: A script watches the Sheet. When 10 alerts appear from one IP, it automatically SSHs into your router and blocks the IP.

Contextual Enrichment

Automatically enrich IP addresses using VirusTotal API or AbuseIPDB the moment they hit your spreadsheet.

SnortPub is not just a logger; it is the trigger for your autonomous security system.

⚙️ Architecture

graph LR
    A[Attacker] -- Packet --> B(Snort Sensor)
    B -- Writes Alert --> C[alert.csv]
    C -- Watches File --> D{Python Bridge}
    D -- HTTP POST --> E[Google Apps Script]
    E -- Appends Row --> F((Google Sheets))
    E -- Sends Email --> G[Admin Email]



🛠️ Installation Guide

Follow these steps exactly to build your own SnortPub system.

📋 Prerequisites

Before you begin, ensure you have:

A Linux Machine (Ubuntu/Debian/Kali recommended).

Python 3.x installed.

Snort installed (sudo apt install snort).

A Google Account.

Step 1: Google Sheets Setup (The Backend)

Create a new Google Sheet.

Go to Extensions > Apps Script.

Delete any existing code.

Copy the code from code.gs (provided in this repo) and paste it into the editor.

Save the project.

Deploy the Web App:

Click Deploy > New deployment.

Select type: Web app.

Description: SnortPub Receiver.

Execute as: Me.

Who has access: Anyone (Crucial step!).

Click Deploy and Copy the Web App URL. You will need this for the Python script.

Step 2: Snort Configuration (The Sensor)

Open your Snort configuration file:

sudo nano /etc/snort/snort.conf




Scroll to the Output Plugins section.

Add or Modify the alert_csv line to match this Safe Mode format:

output alert_csv: /var/log/snort/alert.csv timestamp,msg,proto,src,srcport,dst,dstport




(Note: We use this specific 7-column format to ensure compatibility with all Snort versions).

Save and exit (Ctrl+O, Enter, Ctrl+X).

Step 3: Python Bridge Setup (The Connector)

Clone this repository or download snort_bridge.py.

Open snort_bridge.py and find the configuration section:

# CONFIGURATION
WEBHOOK_URL = 'PASTE_YOUR_GOOGLE_APPS_SCRIPT_URL_HERE'




Paste the URL you copied in Step 1.

Install the required Python library:

pip install requests




🏃‍♂️ Usage & Testing

1. Start the Bridge

Run the Python script first. It will wait for alerts.

sudo python3 snort_bridge.py




2. Start Snort

Open a new terminal window. Start Snort using your network interface (check using ip addr, e.g., wlo1 or eth0).

sudo snort -c /etc/snort/snort.conf -i wlo1




3. Trigger an Attack

Open a third terminal and simulate an attack (like a Ping flood or DNS lookup).

# Test 1: Ping
ping 8.8.8.8

# Test 2: DNS Lookup (Force external)
nslookup google.com 8.8.8.8




4. Verify

Terminal: You should see colorful logs in the Python window ([EMAIL SENT], [LOG ONLY]).

Email: Check your inbox for a formatted alert.

Sheets: Watch the rows appear instantly in your Google Sheet.

❓ Troubleshooting

Q: 'No such device exists' error?
A: Check your network interface name using ip addr. Replace wlo1 or eth0 with your actual interface.

Q: Python script is not showing alerts?
A: Ensure Snort is writing to the file. Try deleting the old log: sudo rm /var/log/snort/alert.csv and restart the bridge.

Q: Emails are not sending?
A: Check if you deployed the Apps Script as 'New Version' and set access to 'Anyone'. Also, check the cooldown timer in Python.

👨‍💻 Developer

Sahil Thakur (aka geeksahil)

Network Security Enthusiast & Automation Developer.

Building tools to make Cyber Security accessible and "Agentic."

<div align="center">
<sub>Built with ❤️ using Python, Google Cloud, and Snort.</sub>
</div>
