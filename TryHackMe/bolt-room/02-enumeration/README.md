# 🕵️ Step 2: Enumeration (Looking Around)

## 🎯 What I Did

I visited the website and looked for clues.

---

## 🛠️ What I Did

### 1. Visit the Website

```
http://<TARGET_IP>:8000
```

I saw a Bolt CMS website.

### 2. Look for Login Page

I tried common URLs:
```
http://<TARGET_IP>:8000/login
http://<TARGET_IP>:8000/admin
http://<TARGET_IP>:8000/bolt
```

**Found it!** The login page was at:
```
http://<TARGET_IP>:8000/bolt/login
```

### 3. Try Default Credentials

I tried common username/password combinations:
- admin / admin
- admin / password
- bolt / bolt

**One of them worked!** 

> 💡 **Tip:** Always try default credentials first!

---

## 📊 What I Found

| Finding | Value |
|---------|-------|
| CMS | Bolt |
| Login URL | `/bolt/login` |
| Username | [Found by trying defaults] |
| Password | [Found by trying defaults] |

---

## 🚀 Next Step

Let's hack in with Metasploit → [03-exploitation](../03-exploitation/)

---

**Made with 💜 by Swoyon**
