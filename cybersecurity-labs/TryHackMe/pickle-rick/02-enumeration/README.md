<div align="center">

# 🕵️ Step 2: Enumeration

<img src="https://img.shields.io/badge/Phase-Enumeration-9b59b6?style=for-the-badge" />
<img src="https://img.shields.io/badge/Tool-Gobuster-9b59b6?style=for-the-badge" />

</div>

---

## 🎯 Objective

Discover hidden pages, files, and credentials on the web server.

---

## 🛠️ Commands Used

### 🌐 Visit the Website

```
http://<target-ip>
```

**What to look for:**
- 🖼️ Images and messages
- 📝 Any hints or notes
- 🔗 Links to other pages

---

### 🔍 Check Page Source Code

Press `Ctrl+U` or right-click → **View Page Source**

> 💡 **Hint:** Look for HTML comments (`<!-- ... -->`) — developers often leave notes, usernames, or hints here!

---

### 🤖 Check robots.txt

```bash
# 🔎 Check for hidden directories or clues
curl http://<target-ip>/robots.txt
```

> 💡 **Hint:** `robots.txt` can contain more than just URLs — sometimes passwords or hidden paths are stored here!

---

### 📁 Directory Brute-Force

```bash
# 🔎 Find hidden directories
gobuster dir -u http://<target-ip> -w /usr/share/wordlists/dirb/common.txt
```

**Expected findings:**
- `/assets/` — Static files
- `/login.php` — Login portal
- `/portal.php` — Command panel (after login)
- `/robots.txt` — Hidden information

---

### 🏠 Explore /assets Directory

```bash
# 🔎 Check for hidden files
curl http://<target-ip>/assets/
```

**Look for:**
- Images (check for steganography)
- Text files
- JavaScript files with hardcoded credentials

---

## 📊 Results Summary

<div align="center">

| 🔑 Credential | 📍 Where to Find |
|:-------------:|:----------------|
| **Username** | Homepage source code (HTML comments) |
| **Password** | `robots.txt` |

| 📂 Directory | 🔗 URL | 📝 Purpose |
|:------------:|:-------|:----------|
| `/assets/` | `http://<target-ip>/assets/` | Static files |
| `/login.php` | `http://<target-ip>/login.php` | 🔐 Login portal |
| `/portal.php` | `http://<target-ip>/portal.php` | 💥 Command panel |

</div>

---

## 🧠 Analysis

> 💡 **Key Insight:**
> 
> Developers often leave sensitive information in **plain sight** — source code comments and `robots.txt` are classic examples of **information disclosure** vulnerabilities. Always check these first!

---

## 🚀 Next Step

➡️ **Exploitation** → [03-exploitation/](../03-exploitation/)

---

<div align="center">

**Made with 💜 by Swoyon**

</div>
