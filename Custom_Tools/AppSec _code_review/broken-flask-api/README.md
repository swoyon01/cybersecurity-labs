# 🛡️ AppSec Journey — Broken Flask API: Vulnerability Analysis

> A hands-on application security project where I took a deliberately vulnerable Flask REST API, identified every security flaw, and rebuilt it securely.
> Part of my Application Security learning journey.

![Status](https://img.shields.io/badge/Status-Completed-green)
![Stack](https://img.shields.io/badge/Flask-SQLite%20%2F%20JWT-blue)
![OWASP](https://img.shields.io/badge/OWASP%20Top%2010-2021-red)

---

## 📌 About

This repo documents a vulnerability assessment of a **Flask API** that handles users, authentication, and admin operations — and every single thing that is wrong with it. 🙃

Each finding maps to the **OWASP Top 10 (2021)** categories and includes a **before → after** fix.

## 📁 Structure

```
├── insecure-api/
│   └── vulnerable_api.py    # ❌ The vulnerable version (do not deploy!)
├── secure-api/
│   ├── secure_api.py        # ✅ The fixed version
│   └── requirements.txt
└── README.md                # This write-up
```

---

## 🔍 Findings

### 1. SQL Injection (SQLi) — `GET /api/user/<id>`, `GET /api/search`

**What's wrong:** User input is concatenated directly into SQL queries.

```python
query = f"SELECT id, username, email FROM users WHERE id = {user_id}"
```

**Impact — CWE-89 / OWASP A03:2021:**
```
GET /api/user/1 OR 1=1 --        → dumps every row in the users table
GET /api/user/1; DROP TABLE users --  → destroys data
GET /api/search?q=' UNION SELECT 1,password,3 FROM users --  → credential theft
```

**Fix:** Always use parameterized queries (prepared statements). Never concatenate user input.

```python
conn.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
```

---

### 2. Broken Access Control / IDOR — `DELETE /api/admin/delete/<id>`

**What's wrong:** "Authorization" is decided by a **client-controlled header**:

```python
if request.headers.get("X-Admin") != "true":
    return {"error": "Forbidden"}, 403
```

Anyone can send `X-Admin: true` and delete any user. This is **CWE-302 (Authentication Bypass by Assumed-Immutable Data)** — a classic **OWASP A01:2021 Broken Access Control** finding.

**Fix:** Authorization decisions must come from the **server-verified session/JWT**, never from anything the client sends as a hint. Require a valid JWT with `role == "admin"` signed by your secret.

---

### 3. Authentication Weaknesses — `POST /api/login`

**What's wrong:**

| Issue | Why it matters |
|-------|---------------|
| **Plaintext password comparison** `user[1] == password` | Passwords stored in plaintext (CWE-256). If the DB leaks, every account is compromised instantly. |
| **No password hashing** | Missing `bcrypt`/`argon2`/`werkzeug.security` hashing + per-user salt. |
| **No rate limiting** | Login endpoint can be brute-forced at unlimited speed (OWASP A07). |
| **Generic error handling missing** | Different behavior can leak whether a username exists. |

**Fix:**
```python
check_password_hash(user[1], password)   # bcrypt-style salted hash
@limiter.limit("5 per minute")            # brute-force protection
```

---

### 4. JWT Security Problems — `/api/login`, `/api/profile`

**What's wrong:**

| Issue | CWE / Risk |
|-------|-----------|
| **Hard-coded weak secret** `SECRET = "my-secret-key"` | CWE-798 — the secret is in the source code. Anyone who reads the repo (or guesses the obvious key) can **forge tokens for any user**. |
| **No expiry claim (`exp`)** | Stolen tokens are valid **forever** — no rotation, no revocation. |
| **No `iat`/`iss` validation** | Weak token validation depth. |
| **Unverified payload trust** | `user_id` is taken straight from the decoded token — combined with the known secret, an attacker forges `{"user_id": 1}` and reads **anyone's** profile. |

**Impact:** Full account takeover of every user via token forgery.

**Fix:**
- Load the secret from an **environment variable / secrets manager** (never the codebase).
- Add `exp`, `iat` claims and check `exp` on decode.
- Tie the token to a real server-side user lookup (see #5).

---

### 5. Broken Access Control / IDOR — `GET /api/profile`

**What's wrong:** The endpoint trusts the `user_id` claim from the token **without verifying that the requester actually owns the account**. Combined with the forgeable JWT, any authenticated (or forged) token can read **any other user's** profile — an **Insecure Direct Object Reference (IDOR)**, CWE-639.

**Fix:** Verify the token's identity against the requested resource server-side, and load the user record **from the database using the verified identity** — not a client-supplied identifier.

---

### 6. Sensitive Information Disclosure — `GET /api/search`

**What's wrong:** On error, the raw exception and internal filenames are returned to the client:

```python
return {"error": str(e), "database": "users.db"}, 500
```

This leaks stack traces, table structure, file paths — reconnaissance gold for an attacker (**CWE-209, OWASP A05**).

**Fix:** Catch exceptions, log them **server-side only**, and return a generic error:

```python
app.logger.exception("Search query failed")
return {"error": "Internal server error"}, 500
```

---

### 7. Credential / Password Handling Problems

- ❌ Plaintext passwords stored in the database (no hashing, no salt)
- ❌ JWT secret hard-coded in source (it IS a credential!)
- ❌ Credentials compared with `==` (timing side-channel, minor vs. plaintext storage)
- ✅ Fix: `werkzeug.security.generate_password_hash()` / `check_password_hash()`, secret in env vars

---

### 8. Debug & Error-Handling Risks

**What's wrong:** `app.run(debug=True)`

Flask's debug mode exposes the **Werkzeug interactive debugger** — if an exception is triggered, anyone who reaches the error page gets a Python console **inside the app**, typically full RCE.

**Fix:** `app.run(debug=False)` in production, error handlers return generic JSON, real errors logged internally.

---

### 9. Other API-Security Issues Noticed

| # | Issue | Category |
|---|-------|----------|
| 10 | **No input validation** — `user_id`, `q`, JSON body are never validated | Input validation (CWE-20) |
| 11 | **DB connections never closed** (`conn.close()` missing) → resource exhaustion | Availability / DoS |
| 12 | **Over-broad `except Exception`** swallows all errors, masks attacks | Error handling |
| 13 | **`SELECT *`** in search → leaks every column (incl. password) | Data exposure |
| 14 | **No HTTPS / TLS mentioned** — tokens & passwords travel in cleartext | Transport security |
| 15 | **No security headers, CORS policy, or auth middleware** | API hardening |
| 16 | **No audit logging** of admin/delete actions | Accountability |
| 17 | **`role` claim in JWT never checked** anywhere | Broken access control |

---

## 🛠️ How to Run (for learning only!)

```bash
# Vulnerable version — NEVER deploy
cd insecure-api
python vulnerable_api.py

# Test SQLi:
curl "http://localhost:5000/api/user/1%20OR%201=1--"

# Test admin bypass:
curl -X DELETE -H "X-Admin: true" http://localhost:5000/api/admin/delete/1
```

```bash
# Fixed version
cd secure-api
pip install -r requirements.txt
export JWT_SECRET="$(openssl rand -hex 32)"
python secure_api.py
```

---

## 📚 Key Takeaways

1. **Never trust client input** — headers, params, or claims — for security decisions.
2. **Parameterized queries** kill the entire SQLi class of bugs.
3. **Hash passwords** with salted, memory-hard algorithms.
4. **JWT secrets live in env vars**, tokens need expiry, and authorization must be server-side.
5. **Debug mode and verbose errors** are reconnaissance gifts to attackers.
6. Secure defaults beat secure intentions: validate input, close connections, log errors internally.

---

## 🔗 References

- [OWASP Top 10 — 2021](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [JWT.io — Token Debugger](https://jwt.io/)

---

## 🤝 Connect

**Swoyon** - [@swoyon01](https://github.com/swoyon01)

---

Made with for cybersecurity enthusiasts

---

*Part of my AppSec Journey 🛡️ | Broken by design, fixed by learning.*
