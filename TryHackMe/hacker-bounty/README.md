# 💰 TryHackMe Bounty Hacker - Complete Walkthrough

> **Beginner Friendly Guide** 🌟
>
> I just completed the Bounty Hacker room on TryHackMe! This guide shows everything I did step-by-step.

---

## 📋 Room Info

| 🏷️ Detail | 📋 Value |
|:----------:|:---------|
| **Room Name** | Bounty Hacker 💰 |
| **Platform** | [TryHackMe](https://tryhackme.com) |
| **Difficulty** | 🟢 Easy |
| **Category** | FTP / SSH / Sudo Exploitation |
| **Status** | ✅ Completed |

---

## 🗺️ What I Did (Step by Step)

```
🎯 Step 1: Scan ports with Nmap
    ↓
📁 Step 2: Enumerate FTP (port 21)
    ↓
🔐 Step 3: Enumerate SSH (port 22)
    ↓
💥 Step 4: Exploit and get shell
    ↓
👑 Step 5: Privilege escalation with sudo
    ↓
🏆 Step 6: Find all flags!
```

---

## 📁 What's Inside This Repo

```
📂 tryhackme-bounty-hacker/
│
├── 📄 README.md              ← You are here!
├── 📄 LICENSE
│
├── 📁 01-reconnaissance/     ← Port scanning
├── 📁 02-enumeration/        ← FTP & SSH enumeration
├── 📁 03-exploitation/       ← Getting shell access
├── 📁 04-post-exploitation/  ← Finding user flag
├── 📁 05-privilege-escalation/ ← Becoming root
├── 📁 06-flags/              ← All flags captured
│
├── 📁 scripts/               ← Useful scripts
└── 📁 screenshots/           ← Where to add screenshots
```

---

## 🛠️ Tools I Used

| Tool | What It Does |
|------|-------------|
| **Nmap** | Finds open ports and services |
| **FTP** | Connects to FTP service |
| **SSH** | Secure remote login |
| **Hydra** | Brute forces passwords |
| **LinPEAS** | Linux privilege escalation checker |

---

## 🚀 Quick Commands

```bash
# 1. Scan the target
nmap -sV -sC <TARGET_IP>

# 2. Connect to FTP
ftp <TARGET_IP>

# 3. Download files from FTP
get locks.txt
get task.txt

# 4. Brute force SSH
hydra -l <username> -P locks.txt ssh://<TARGET_IP>

# 5. SSH login
ssh <username>@<TARGET_IP>

# 6. Check sudo privileges
sudo -l
```

---

## 📖 Full Walkthrough

| Step | What I Did | Link |
|:----:|:-----------|:----:|
| 1 | 🔍 Scanning | [01-reconnaissance](01-reconnaissance/) |
| 2 | 📁 Enumeration | [02-enumeration](02-enumeration/) |
| 3 | 💥 Exploitation | [03-exploitation](03-exploitation/) |
| 4 | 🏴 Post-Exploitation | [04-post-exploitation](04-post-exploitation/) |
| 5 | 👑 Privilege Escalation | [05-privilege-escalation](05-privilege-escalation/) |
| 6 | 🏆 Flags | [06-flags](06-flags/) |

---

## ⚠️ Important Note

> This is for **learning only**!
>
> Only test systems you **own** or have **permission** to test!

---


This is my walkthrough of the Bounty Hacker room. I hope it helps other beginners!

**Made with 💜 by Swoyon** 
