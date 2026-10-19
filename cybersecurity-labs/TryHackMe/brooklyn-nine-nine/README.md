# TryHackMe Commands Collection

> A personal collection of commands & methodology practiced on TryHackMe rooms.
> 

---

## 📁 Room: Brooklyn Nine Nine

**Difficulty:** Easy  
**Category:** Linux / SSH / Privilege Escalation  
**Status:** ✅ Completed

---

### 🔍 Step 1: Enumeration

#### Nmap - Basic Port Scan
```bash
nmap -sV -sC <target-ip>
```

#### Nmap - Full Port Scan
```bash
nmap -p- -sV -sC <target-ip>
```

#### Nmap - Quick Top Ports
```bash
nmap --top-ports 1000 -sV <target-ip>
```

#### Gobuster - Directory Enumeration
```bash
gobuster dir -u http://<target-ip> -w /usr/share/wordlists/dirb/common.txt
```

#### Cewl - Generate Wordlist from Website
```bash
cewl http://<target-ip> -m 3 -w custom-wordlist.txt
```

---

### 🔓 Step 2: Brute-Force (SSH)

#### Hydra - Basic SSH Attack
```bash
hydra -l <username> -P <wordlist> ssh://<target-ip>
```

#### Hydra - Stop on First Hit
```bash
hydra -l <username> -P <wordlist> ssh://<target-ip> -f
```

#### Hydra - With Thread Count
```bash
hydra -l <username> -P <wordlist> ssh://<target-ip> -f -t 32
```

#### Hydra - Alternative Syntax
```bash
hydra -l <username> -P <wordlist> <target-ip> ssh -f -t 64
```

#### Create Custom Wordlist
```bash
echo -e "password\n123456\nadmin\n<username>\n<username>123" > custom.txt
```

#### Extract RockYou (if compressed)
```bash
gunzip /usr/share/wordlists/rockyou.txt.gz
```

#### RockYou Top 1000 (faster)
```bash
head -n 1000 /usr/share/wordlists/rockyou.txt > top1000.txt
```

---

### 🖥️ Step 3: SSH Login

```bash
ssh <username>@<target-ip>
```

---

### 🎯 Step 4: Post-Exploitation

#### List Files
```bash
ls -la
```

#### Read User Flag
```bash
cat user.txt
```

#### Check Sudo Privileges
```bash
sudo -l
```

#### Check SUID Binaries
```bash
find / -perm -4000 2>/dev/null
```

#### Check Running Processes
```bash
ps aux
```

#### Check Cron Jobs
```bash
cat /etc/crontab
```

#### Check OS Version
```bash
cat /etc/os-release
```

#### Check Kernel Version
```bash
uname -a
```

---

### ⬆️ Step 5: Privilege Escalation

#### Sudo Abuse (check GTFOBins)
```bash
sudo <binary>
```

#### Search for Writable Directories
```bash
find / -writable -type d 2>/dev/null
```

#### Search for Password Files
```bash
find / -name "*.txt" -o -name "*.bak" -o -name "*.old" 2>/dev/null
```

#### Check Environment Variables
```bash
env
```

#### Check PATH
```bash
echo $PATH
```

---

### 🏁 Step 6: Root Flag

```bash
cat /root/root.txt
```

---

## 📚 Common Tools Cheatsheet

### Nmap
| Command | Description |
|---------|-------------|
| `nmap <ip>` | Basic scan |
| `nmap -sV <ip>` | Service version detection |
| `nmap -sC <ip>` | Default scripts |
| `nmap -p- <ip>` | All ports |
| `nmap -A <ip>` | Aggressive scan |

### Hydra
| Flag | Description |
|------|-------------|
| `-l <user>` | Single username |
| `-L <file>` | Username wordlist |
| `-P <file>` | Password wordlist |
| `-f` | Stop on first valid |
| `-t <n>` | Parallel threads |
| `-V` | Verbose mode |

### SSH
| Command | Description |
|---------|-------------|
| `ssh user@ip` | Connect to host |
| `ssh -p 2222 user@ip` | Custom port |
| `scp file user@ip:/path` | Copy file |

---

## 🛡️ Ethical Note

> All commands documented here are for **educational and authorized penetration testing purposes only**.  
> Never use these techniques on systems you do not own or have explicit permission to test.

---

**Prepared by Saber Hasan Swoyon** 🔥  
*Happy Hacking!*

