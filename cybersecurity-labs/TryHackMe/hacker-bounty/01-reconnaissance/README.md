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
- `-sC` = Run basic scripts for more info
- `<TARGET_IP>` = The IP TryHackMe gives you

### What I Found

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

**Important findings:**
- Port 21: FTP (File Transfer)
- Port 22: SSH (Secure Shell)
- Port 80: HTTP (Website)

---

## 🤔 What Are These Services?

| Service | Port | What It Does |
|---------|------|-------------|
| **FTP** | 21 | Transfer files |
| **SSH** | 22 | Secure remote login |
| **HTTP** | 80 | Website |

---

## 🚀 Next Step

Let's enumerate FTP → [02-enumeration](../02-enumeration/)

---

**Made with 💜 by Swoyon**
