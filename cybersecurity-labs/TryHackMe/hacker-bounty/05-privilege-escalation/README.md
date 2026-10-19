# 👑 Step 5: Privilege Escalation (Becoming Root)

## 🎯 What I Did

I escalated privileges to become root and get the final flag.

---

## 🛠️ Commands I Used

### Check Sudo Privileges

```bash
sudo -l
```

**What I found:**
```
User <username> may run the following commands on <hostname>:
    (root) NOPASSWD: /usr/bin/<binary>
```

**This means:** I can run a specific binary as root without password!

---

## 🛠️ Exploit Sudo

### Method 1: Use GTFOBins

Visit: https://gtfobins.github.io/

Search for the binary name and find the sudo exploit.

### Method 2: Run the Binary

```bash
sudo /usr/bin/<binary>
```

**Or with GTFOBins payload:**
```bash
sudo <binary> <payload>
```

### Result

```bash
root@<hostname>:~# 
```

🎉 **I'm root!**

---

## 📊 Results

| Before | After |
|--------|-------|
| Regular User | **ROOT** ✅ |
| Limited Access | Full Access |

---

## 🚀 Next Step

Get root flag! → [06-flags](../06-flags/)

---

**Made with 💜 by Swoyon**
