# N8N-Automation
This projects are just PoC to learn, practice and experiment on both workflow automation (via code) and AI-integrated workflow automation.
<br>
I'm doing all of this by self-hosting both an N8N instance and an AI model (Ollama llama3) that works as a SOC analyst.
<br><br>
**🐧Linux Threat Hunter**
  <br>
This project is a SIEM-LLM system intended to monitor and protect Linux Systems via log extraction and analysis. 
<br>
This workflow automatically extracts Linux network logs based on a schedule trigger. The logs are parsed with Python to extract data and signatures that are then given to an AI agent, analysing every log and asigning a risk level to each one. The AI agent's output is then saved in a database via integration with PostgreSQL for audit purposes 
<br>
Highlights 💥
<br>
💻 Automatic data extraction.<br>
🤖 self-hosted AI that identifies anomalies that bypass conventional signature-based detection<br>
🛡️ 100% self-hosted (orchestraton and AI) to maximize privacy and data security.<br>
🐍 Noise reduction by smart parsing to recover key data.<br>
🐘 Pre and post-processing storage in PostgreSQL to perform audits and maintain integrity.
<br> <br>

**🍯Honeypot with LLM analysis** <br>
This project is SOAR infrastructure designed to capture intrusion attempts using an isolated Docker-based Flask honeypot and analyse the captured information with AI. <br>
A decoy simulating an administrative login is deployed on the system to attract threat actors who are already on the system. Key data like IP addresses and inputs are captured and sent to the automation platform for processing. The AI agent then generates an output specifying the detected attack type, the risk level to the system and suggests remediation. <br>
Both the attacker information and the AI analysis are stored in databases through PostgreSQL integration to audit the detected attacks and the AI's performance as a SOC analyst.
<br>
Furthermore, email notification to the SOC team are automated to provide real-time alerts and detailed attacker data, while also blocking the attacker's IP address.
<br>
Highlights 💥
<br>
🤖 self-hosted AI that helps contain the threat<br>
🛡️ 100% self-hosted (orchestraton and AI) to maximize privacy and data security.<br>
🐍 Noise reduction by smart parsing to recover key data.<br>
🐘 Persistent storage in PostgreSQL, allowing audit and threat hunting.
🏰 Persistent logs for every intrusion, alerts via Gmail API to notify the SOC team, and automated IP blocking to reduce Mean Time To Respond (MTTR) and enable real-time defense.

**💻Automated Static & Dinamic File Analysis ** <br>
This project is a DFIR systed designed to perform automated multi-layered file analysis using Python (integrating various INFOSEC-specific Python libraries), Docker Sandboxing and LLM orchestration. <br>
A Python-based watchdog service monitors specific system directories in real-time. Upon detection of a new file it executes a dual-stage analysis: Static (Calculating Shannon entropy, signature-based detection based on YARA rules and checking existing databases) and dynamic (executing the file in an isolated environment to capture behavioral logs). The intel is sent via webhook to N8N, where the AI agent evaluates the collected forensic data. The system determines the threat level and stores the results in SQL. If a threat is in fact detected, a secondary AI agent generates remediation steps to reduce MMTR 
<br>
Highlights 💥
<br>
🔬 Hybrid inspection for better security <br>
🤖 self-hosted AI to interpret complex sandbox logs and identify suspicious patterns <br>
🛡️ 100% self-hosted (orchestraton and AI) to maximize privacy and data security.<br>
🐍 Python-driven metadata extraction  ensures high-fidelity data input for the AI. <br>
🐘 Persistent storage in PostgreSQL for every analysis for audit and threat hunting purposes. <br>

