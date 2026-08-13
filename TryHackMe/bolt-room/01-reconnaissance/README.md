# 🔍 Step 1: Reconnaissance (Scanning)

## 🎯 What I Did

I scanned the target to find open ports and services.

---

## 🛠️ Commands I Used

### Basic Scan

```bash
nmap -sV -sC <TARGET_IP>
```

**What this does:**
- `-sV` = Find what services are running
- `-sC` = Run basic scripts to get more info
- `<TARGET_IP>` = The IP TryHackMe gives you

### What I Found

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.6p1
80/tcp   open  http    Apache httpd 2.4.29
8000/tcp open  http    Bolt CMS
```

**Important findings:**
- Port 22: SSH (remote login)
- Port 80: Website (Apache)
- Port 8000: **Bolt CMS** (this is important!)

---

## 🤔 What is Bolt CMS?

Bolt CMS is a content management system (like WordPress). 
The version I found had a known vulnerability!

---

## 🚀 Next Step

Let's look at the website → [02-enumeration](../02-enumeration/)

---

**Made with 💜 by Swoyon**
