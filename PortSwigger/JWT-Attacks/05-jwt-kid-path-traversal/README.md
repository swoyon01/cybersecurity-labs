# 🗂️ Lab 18: JWT Attacks — Authentication Bypass via `kid` Header Path Traversal

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-kid-header-path-traversal)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved

---

## 📋 Lab Description

> *"This lab uses a JWT-based mechanism for handling sessions. In order to verify the signature, the server uses the kid parameter in the JWT header to fetch the relevant key from its filesystem. To solve the lab, forge a JWT that grants you access to the admin panel at /admin, then delete the user carlos. You can log in to your own account using the following credentials: wiener:peter."*

---

## 🔍 Reconnaissance

### Step 1: Identify the Vulnerable Mechanism
Logged in with the provided credentials `wiener:peter`, loaded `/my-account`, and sent the request to Burp Repeater. Inspected the `session` cookie JWT using Burp's **JSON Web Token** tab.

**Decoded JWT Header:**

```json
{
  "kid": "b2c3f5a1-8d4e-4f2a-9c1b-3e6a8d2f1b4c",
  "alg": "HS256"
}
```

The `kid` (Key ID) header parameter tells the server **which file on its filesystem** contains the verification key. This is the critical flaw: the server trusts a value from inside the token to locate its own secret.

<img width="1280" height="684" alt="Screenshot 2026-10-31 230825" src="https://github.com/user-attachments/assets/94c7f5b5-4e17-444c-94be-8e7557787734" />


> **Note:** The decoded header shows the `kid` parameter — the server uses this value to build a file path and read the key from its filesystem.

---

## 🚀 Exploitation

### Goal: Forge a JWT Using a Key File We Control

Since the `kid` value is used as a file path, we can use **path traversal** to point it at a file whose contents we know — `/dev/null` (which is **empty**). Then we simply sign the token with an **empty key**, and the server's verification will succeed.

---

### Step 2: Confirm /admin Access is Denied (Before Attack)
Sent `GET /admin` with the original token (`sub: wiener`).

**Result:** ❌ `HTTP/2 401 Unauthorized` — *"Admin interface only available if logged in as an administrator"*


---

### Step 3: Inject Path Traversal into `kid`
Changed the `kid` header to a path traversal pointing to `/dev/null`:

```json
{
  "kid": "....//....//....//....//....//....//dev/null",
  "alg": "HS256"
}
```

> **Tip:** The lab filters `../`, so we use `....//` — the filter strips the middle `../` leaving a valid `../../` behind. A classic filter-evasion trick!



---

### Step 4: Sign the Forged Token with an Empty Key ✅
`/dev/null` is an **empty file**, so the server will verify the signature against an **empty key**. Using Burp's JWT Editor extension, generated a new symmetric key and set its value to empty, then signed the token.

**Forged JWT:**
```json
// Header
{
  "kid": "....//....//....//....//....//....//dev/null",
  "alg": "HS256"
}

// Payload
{
  "iss": "portswigger",
  "exp": 1790689207,
  "sub": "administrator"   // <-- forged claim
}
```

Sent `GET /admin` with the forged token → **✅ `HTTP/2 200 OK`** — full admin panel access! 🎯

<img width="1280" height="684" alt="Screenshot 2026-10-31 232201" src="https://github.com/user-attachments/assets/8d768000-6a04-40a1-9c70-6b89cbcc68fc" />


---

### Step 5: Delete the User carlos
The admin panel listed the users with delete links:

```text
/admin/delete?username=carlos
```

Sent the delete request with the same forged token → **✅ `HTTP/2 302 Found`** (redirect back to `/admin`).

<img width="1280" height="684" alt="Screenshot 2026-10-31 232230" src="https://github.com/user-attachments/assets/3d3cfe2c-fe74-4a50-9bcb-5fd25a3e7412" />


---

### Step 6: Lab Solved! 🎉
**"Congratulations, you solved the lab!"** — `carlos` deleted successfully.

<img width="1280" height="684" alt="Screenshot 2026-10-31 232457" src="https://github.com/user-attachments/assets/5a473dcc-fadc-4672-afd4-6f15f4275ad6" />


---

### What Happens?

**Server-side key lookup (normal flow):**
```python
kid = jwt.header["kid"]                    # attacker-controlled!
key = open(f"/app/keys/{kid}").read()     # path traversal happens HERE
jwt.verify(key)                             # uses file contents as key
```

**Original request:**
```json
"kid": "b2c3f5a1-8d4e-4f2a-9c1b-3e6a8d2f1b4c"
```
→ ❌ Access denied — normal user, `sub: wiener`

**Forged request:**
```json
"kid": "....//....//....//....//....//....//dev/null"
```
→ Server reads `/dev/null` (empty) → signature verified with **empty key** → ✅ **admin access**

---

## 🛠️ Burp Suite Intercept

I used **Burp Suite Community Edition** with the **JWT Editor** extension to forge the token.

### Steps:
1. Logged in with `wiener:peter` and sent the request to **Repeater**
2. Opened the **JSON Web Token** tab and decoded the session cookie
3. Injected the path traversal payload into the `kid` header (`....//` filter bypass)
4. Changed the payload `sub` → `administrator`
5. Created a **new symmetric key with an empty value** in JWT Editor (matching `/dev/null`'s contents)
6. **Signed** the token with the empty key and forwarded the request
7. Sent `/admin/delete?username=carlos` with the same forged token

### Attack Flow Summary
| Step | Action | Result |
|------|--------|--------|
| 1 | Decode baseline JWT | `kid` parameter discovered — key from filesystem |
| 2 | Request `/admin` as `wiener` | 401 Unauthorized — boundary confirmed |
| 3 | Inject `kid` path traversal to `/dev/null` | Token structure forged |
| 4 | Sign with empty key (`/dev/null` = empty) | **200 OK — admin access granted** |
| 5 | Delete `carlos` | 302 Found — deletion successful |
| 6 | Verify success | Lab solved |

---

## 📸 Proof of Concept


As seen in the screenshot:
- The `kid` header was hijacked with a path traversal to `/dev/null`
- The token was **forged with an empty key** and accepted by the server
- `carlos` was deleted via `/admin/delete?username=carlos`
- Lab shows **"Congratulations, you solved the lab!"**

---

## 🧠 Key Takeaways

### 1. Vulnerability Root Cause
The server uses the **attacker-controlled `kid` header** to build a filesystem path and read the verification key. Any input that influences file paths or key selection must be strictly validated — never trusted from inside the token.

### 2. Why `/dev/null` + Empty Key Works
- `/dev/null` is a **special device file that is always empty**
- The server reads it as the verification key → key = `""` (empty string)
- If we sign the JWT with the same empty key, verification **succeeds** — we control both sides

### 3. The `....//` Filter Bypass
| Payload | After Filter | Result |
|---------|-------------|--------|
| `../../../../dev/null` | stripped/blocked | ❌ Filtered |
| `....//....//dev/null` | `../../dev/null` | ✅ Bypassed |

The filter removes `../` and leaves `....` + `/` → `...` + `../` — classic recursive-filter bypass.

### 4. Enumeration Strategy
| Attempt | `kid` value | Signing Key | Response | Meaning |
|---------|-------------|-------------|----------|---------|
| 1st | Original UUID | Original key | 401 Unauthorized | Normal user — boundary confirmed |
| 2nd | Traversal → `/dev/null` | Empty string | 200 OK | ✅ **Empty key accepted** |
| 3rd | Traversal → `/dev/null` + `sub: administrator` | Empty string | 200 OK | ✅ **Full admin access** |

### 5. Impact
- **Arbitrary Key Selection:** Point `kid` at any readable file (e.g., a public static file) and sign with its known contents
- **Full Account Takeover:** Forge tokens for any identity, including administrators
- **Filesystem Exposure:** Path traversal can also be used to probe/read server files

### 6. Mitigation Strategies
| Defense | Implementation |
|---------|---------------|
| **Don't Trust `kid` from Tokens** | Map `kid` to keys via a strict server-side lookup table (allowlist) |
| **Block Path Traversal** | Reject any `kid` containing `/`, `\`, `..`, or URL-encoded variants |
| **Use a Database for Keys** | Store keys in a DB indexed by ID — never construct filesystem paths |
| **Fail Closed** | Unknown or malformed `kid` → reject the token, never fall back |
| **Parameterize File Access** | If files must be used, resolve and canonicalize the path, then verify it's inside an allowed directory |

### 7. Why This Matters for AppSec
- The `kid` parameter is **commonly used** in multi-key JWT setups (key rotation) — this mistake appears in real-world apps
- It combines two bug classes: **path traversal** + **JWT key confusion**
- It chains directly into **privilege escalation** and **full application compromise**
- The filter bypass (`....//`) is a reusable technique across many input-validation flaws

---

## 📚 References

- [PortSwigger — JWT Attacks](https://portswigger.net/web-security/jwt)
- [PortSwigger — JWT Authentication Bypass via kid Header Path Traversal (Lab)](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-kid-header-path-traversal)
- [PortSwigger — JWT Header Parameter Injections](https://portswigger.net/web-security/jwt#jwt-header-parameter-injections)
- [RFC 7515 — JSON Web Signature (JWS)](https://datatracker.ietf.org/doc/html/rfc7515)
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)

---

> 📝 **Author:** Saber Hasan Swoyon  
> 🎓 **Status:** Student | Aspiring AppSec Engineer  
> 📅 **Date Solved:** 2026-11-01
