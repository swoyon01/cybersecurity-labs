<div align="center">

# 🏆 Step 6: All 3 Ingredients (Flags)

<img src="https://img.shields.io/badge/Phase-Flags%20Captured-8e44ad?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-Completed-00b894?style=for-the-badge" />

</div>

---

## 🎯 Objective

Collect all 3 ingredients to complete the room!

---

## 🥇 Ingredient 1: Mr. Meeseeks

<div align="center">

| 🏷️ Property | 📋 Value |
|:-----------:|:---------|
| **Name** | Mr. Meeseeks |
| **Location** | Web directory / Homepage source code |
| **Method** | Source code inspection (`Ctrl+U`) |

</div>

### 🛠️ Commands Used

```bash
# 🔎 Check web directory
ls -la /var/www/html/
```

```bash
# 🔎 Find text files
find /var/www/ -type f -name "*.txt" 2>/dev/null
```

> 💡 **Hint:** Check the homepage source code carefully. The first ingredient is hidden in plain sight!

---

## 🥈 Ingredient 2: 1 Jerry Tear

<div align="center">

| 🏷️ Property | 📋 Value |
|:-----------:|:---------|
| **Name** | 1 Jerry Tear |
| **Location** | `/home/rick/second ingredients` |
| **Method** | Filter bypass (`less` instead of `cat`) |

</div>

### 🛠️ Commands Used

```bash
# 🔎 Find ingredient files
find / -name "*ingredient*" 2>/dev/null
```

```bash
# 📖 Read with less (cat is blocked)
less "/home/rick/second ingredients"
```

**Alternative methods:**
```bash
# Method 2: head
head "/home/rick/second ingredients"
```

```bash
# Method 3: python3
python3 -c 'print(open("/home/rick/second ingredients").read())'
```

> 💡 **Hint:** When `cat` is blocked, always try `less`, `head`, `tail`, or Python!

---

## 🥉 Ingredient 3: Fleeb Juice

<div align="center">

| 🏷️ Property | 📋 Value |
|:-----------:|:---------|
| **Name** | Fleeb Juice |
| **Location** | `/root/` |
| **Method** | Privilege escalation (`sudo bash`) |

</div>

### 🛠️ Commands Used

```bash
# 👑 Become root first
sudo bash
```

```bash
# 📂 List root directory
ls -la /root/
```

```bash
# 📖 Read the flag
cat /root/3rd.txt
```

**Alternative:**
```bash
cat /root/third\ ingredients
```

> 💡 **Hint:** The third ingredient requires root privileges. Check `sudo -l` first!

---

## 📊 Final Summary

<div align="center">

| 🏅 # | 📝 Ingredient | 📍 Location | 🔧 Method | ✅ Status |
|:----:|:-------------|:------------|:----------|:---------:|
| 🥇 | **Mr. Meeseeks** | Web directory | Source code inspection | ✅ |
| 🥈 | **1 Jerry Tear** | `/home/rick/second ingredients` | Filter bypass (`less`) | ✅ |
| 🥉 | **Fleeb Juice** | `/root/` | Privilege escalation (`sudo`) | ✅ |

</div>

---

## 🎉 Room Complete!

<div align="center">

### *"Wubbalubbadubdub!"* 🥒

**Rick is saved! All 3 ingredients collected!**

<img src="https://img.shields.io/badge/Rick-Saved-00b894?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-ROOTED-00b894?style=for-the-badge" />

</div>

---

## 🏆 What I Learned

> 🧠 **Key Takeaways:**
> 
> 1. 🔍 **Always check source code** — credentials hide in HTML comments
> 2. 🤖 **`robots.txt` is gold** — can contain sensitive information
> 3. 🛡️ **Filter bypass is essential** — `cat` blocked? Use `less`, `python3`, etc.
> 4. 👑 **`sudo -l` first** — always check sudo privileges immediately
> 5. 🐚 **Reverse shells are powerful** — full control over the target

---

<div align="center">

**Made with 💜 by Swoyon**

⭐ **If this helped you, give it a star!** ⭐

</div>
