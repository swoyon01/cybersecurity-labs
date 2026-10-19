# 🏆 Step 6: Flags (The Rewards!)

## 🎯 What I Did

I collected all the flags to complete the room!

---

## 🏅 Flags I Found

### 🥇 Flag 1: User Flag

**Location:** `/home/<username>/`

**Command:**
```bash
cat /home/<username>/user.txt
```

**What it looks like:**
```
THM{...}
```

---

### 🥈 Flag 2: Root Flag

**Location:** `/root/`

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
| User Flag | `/home/<username>/` | After exploiting Bolt CMS |
| Root Flag | `/root/` | After becoming root with `sudo` |

---

## 🎉 Room Complete!

```
╔═══════════════════════════════════════╗
║         🎉 CONGRATULATIONS! 🎉        ║
║                                       ║
║      You completed the Bolt room!     ║
║                                       ║
║         🐕 Bolt would be proud!       ║
╚═══════════════════════════════════════╝
```

---

## 🧠 What I Learned

1. 🔍 **Always scan first** — Nmap shows what's open
2. 🕵️ **Look at the website** — Login pages are gold
3. 💥 **Metasploit is powerful** — Known exploits save time
4. 👑 **Check `sudo -l`** — Easy privilege escalation
5. 🏆 **Flags are the goal** — Always look for them!

---

**Made with 💜 by Swoyon**

⭐ Star this repo if it helped you!
