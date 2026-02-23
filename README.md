# 🚀 Authorized DDoS Pentest Tool GUI

A professional **GUI-based DDoS simulation tool** for **authorized penetration testing** and security assessments. This tool helps cybersecurity professionals test target resilience under controlled DDoS conditions.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/yourusername/ddos-pentest-gui/actions)

## ✨ Features

- **6 Attack Vectors**: TCP Flood, UDP Flood, HTTP GET/POST Flood, Slowloris, Multi-vector
- **Modern GUI**: Intuitive tkinter interface with real-time logging
- **Thread Control**: 50-2000 configurable threads
- **Duration Control**: 10-300 second attack windows
- **Input Validation**: Prevents invalid configurations
- **Live Monitoring**: Real-time status and progress indicators
- **Thread-Safe**: Proper async logging and GUI updates

## 🎯 Use Cases (Authorized Only)

- **Red Team Engagements** - Simulate DDoS during authorized pentests
- **DoS Resilience Testing** - Validate WAF/IPS configurations
- **Load Testing** - Stress test web applications under controlled conditions
- **Security Training** - Educational demonstrations (lab environments only)

## 📋 Prerequisites

- Python 3.8+
- `requests` library (`pip install requests`)

## 🚀 Quick Start


# Clone the repo
git clone https://github.com/yourusername/ddos-pentest-gui.git
cd ddos-pentest-gui

# Install dependencies
pip install -r requirements.txt

# Run the GUI
python ddos_pentest_gui.py
📊 Usage
Enter Target: IP/hostname and port (80 default)
Configure: Threads (50-2000), Duration (10-300s)
Select Attack: Choose from 6 attack types
Execute: Click START ATTACK
Monitor: Real-time logs and status
Stop: Use STOP ATTACK button anytime
Attack Types


Type	Protocol	Purpose
1	TCP Flood	SYN flood simulation
2	UDP Flood	UDP packet storm
3	HTTP GET	Layer 7 GET flood
4	HTTP POST	Layer 7 POST flood
5	Slowloris	Slow HTTP DoS
6	Multi-vector	Random attack combination
🛡️ Legal & Ethical Use
⚠️ AUTHORIZED USE ONLY ⚠️




✅ Allowed:
• Owned infrastructure testing
• Client-authorized pentests
• Red team engagements with RoE
• Lab/research environments
• Security training (isolated networks)

❌ NEVER:
• Production systems without permission
• Third-party infrastructure
• Competitors or rivals
• Any unauthorized network activity
Always obtain written authorization before testing.

🐛 Troubleshooting


Issue	Solution
"Connection refused"	Verify target/port accessible
"Too many threads"	Reduce thread count (start with 100)
GUI freezes	Normal during heavy attacks
No requests library	pip install requests
Firewall blocks	Test from authorized network
🔧 Development
bash



# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Lint code
flake8 src/
📄 License
This project is MIT licensed [blocked]. See the LICENSE [blocked] file for details.

🤝 Contributing
Fork the project
Create feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open Pull Request
🙏 Acknowledgments
Built for cybersecurity professionals conducting authorized assessments
Follows OWASP testing guidelines for DoS testing
GUI powered by tkinter (Python standard library)
Use Responsibly • Test Ethically • Stay Authorized

Pentest
