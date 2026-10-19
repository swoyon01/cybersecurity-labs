<div align="center">

# 🔍 Step 1: Reconnaissance

<img src="https://img.shields.io/badge/Phase-Reconnaissance-3498db?style=for-the-badge" />
<img src="https://img.shields.io/badge/Tool-Nmap-3498db?style=for-the-badge&logo=nmap" />

</div>

---

## 🎯 Objective

Discover open ports and running services on the target machine.

---

## 🛠️ Commands Used

### 📡 Basic Port Scan

```bash
# 🔎 Scan top 1000 ports with service detection
nmap -sV -sC 10.10.10.10
```

<details>
<summary>🖥️ Click to see output</summary>

```
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for 10.10.10.10
Host is up (0.15s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 34:45:... (RSA)
|   256 78:90:... (ECDSA)
|_  256 12:34:... (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Rick is sup4r cool
|_http-server-header: Apache/2.4.18 (Ubuntu)

Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed.
Nmap done: 1 IP address (1 host up) scanned in 12.34 seconds
```

</details>

---

### 🔬 Full Port Scan

```bash
# 🔎 Scan ALL 65535 ports
nmap -p- -sV 10.10.10.10
```

**Result:** Only ports **22** and **80** are open.

---

### 🎯 Aggressive Scan

```bash
# 🔎 Aggressive scan with OS detection
nmap -A -p 22,80 10.10.10.10
```

---

## 📊 Results Summary

<div align="center">

| 🚪 Port | 🏷️ Service | 📝 Version | 🎯 Priority |
|:-------:|:-----------|:-----------|:-----------:|
| **22** | 🔐 SSH | OpenSSH 7.2p2 Ubuntu | Medium |
| **80** | 🌐 HTTP | Apache 2.4.18 (Ubuntu) | **High** 🔥 |

</div>

---

## 🧠 Analysis

> 💡 **Key Insight:**
> 
> Port 80 (HTTP) is our **primary attack surface**. The web server is running Apache on Ubuntu, which suggests a Linux-based target with potential web vulnerabilities.

---

## 🚀 Next Step

➡️ **Enumeration** → [02-enumeration/](../02-enumeration/)

---

<div align="center">

**Made with 💜 by Swoyon**

</div>
