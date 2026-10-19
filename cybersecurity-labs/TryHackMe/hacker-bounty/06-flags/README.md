# 🏆 Step 6: Flags (The Rewards!)

## 🎯 What I Did

I collected all the flags to complete the room!

---

## 🏅 Flags I Found

### 🥇 User Flag

**Location:** `/home/<username>/user.txt`

**Command:**
```bash
cat /home/<username>/user.txt
```

**What it looks like:**
```
THM{...}
```

---

### 🥈 Root Flag

**Location:** `/root/root.txt`

**Command:**
```bash
cat /root/root.txt
```

**What it looks like:**
```
THM{...}
```

---

## 📊 Summary

| Flag | Location | How I Got It |
|------|----------|-------------|
| User Flag | `/home/<username>/user.txt` | SSH login |
| Root Flag | `/root/root.txt` | Sudo exploitation |

---

## 🎉 Room Complete!

```
╔═══════════════════════════════════════╗
║         🎉 CONGRATULATIONS! 🎉        ║
║                                       ║
║   You completed Bounty Hacker!        ║
║                                       ║
╚═══════════════════════════════════════╝
```

---

## 🧠 What I Learned

1. 🔍 **Always check FTP** — anonymous login can leak files
2. 📁 **Download everything** — files can contain passwords
3. 🔐 **Hydra is powerful** — brute force with found wordlists
4. 👑 **Check `sudo -l`** — easy privilege escalation
5. 🌐 **GTFOBins** — great resource for sudo exploits

---

**Made with 💜 by Swoyon**

⭐ Star this repo if it helped you!
