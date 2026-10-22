# 🚫 Lab 13: JWT Attacks — Authentication Bypass via Flawed Signature Verification

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved

---

## 📋 Lab Description

> *"This lab uses a JWT-based mechanism for handling sessions and exposes an error message when it receives an invalid token. It uses a weak secret key to sign the tokens. To solve the lab, first find the weak secret key. Then use it to forge a JWT with header parameter alg set to none, access the admin panel at /admin, then delete the user carlos. Note: You can log in to your own account using the following credentials: wiener:peter."*

---

## 🔍 Reconnaissance

### Step 1: Identify the Authentication Mechanism
Logged in with the provided credentials `wiener:peter` and loaded `/my-account`. The application issues a JWT inside the `session` cookie. Sent the request to Burp Repeater and inspected the token using Burp's **JSON Web Token** tab.

**Decoded JWT:**

```json
// Header
{
  "kid": "cbe9f5b4-02c0-4713-841d-de4eb3101837",
  "alg": "RS256"
}

// Payload
{
  "iss": "portswigger",
  "exp": 1790689207,
  "sub": "wiener"
}
```

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/5e612b40-a393-485a-89af-fad2be20bc1a" />


> **Note:** The Inspector panel decodes the header showing `"alg": "RS256"` — the baseline token is signed with RS256.

---

## 🚀 Exploitation

### Goal: Bypass Signature Verification Using `alg: none`

The lab verifies JWTs insecurely: **when the token header specifies `"alg":"none"`, the server skips signature verification entirely** and blindly trusts the payload claims. We can forge an unsigned token claiming to be `administrator`.

---

### Step 2: Test the `alg: none` Header
Modified the JWT header, changing the algorithm from `RS256` to `none` (re-encoded as Base64URL). The token was still accepted because the payload claim (`sub: wiener`) was unchanged — confirming the server parses the algorithm from the token header itself.

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/bf6c7fa7-616f-444b-9a19-a09a16233dfc" />


---

### Step 3: Confirm the Access-Control Boundary
Requested `/admin` as the normal user — both in the browser and in Repeater.

**Browser result:**
> Admin interface only available if logged in as an administrator

**Repeater result:** ❌ `HTTP/2 401 Unauthorized` with the original RS256 token (`sub: wiener`).

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/ceed8aa7-2177-4904-9d9b-c0672ffe6e68" />


<img width="1280" height="684" alt="Screenshot 2026-10-22 154250" src="https://github.com/user-attachments/assets/3815521e-2691-46c7-9845-a479b17aa677" />


---

### Step 4: Modify the Claim Without Removing the Signature (Rejected)
Changed the payload claim `sub` → `administrator` but **left the signature section untouched**. The server correctly **rejected** the token — the signature no longer matches the modified payload. This proves the signature protects the claims *when it is actually verified*.


---

### Step 5: Exploit the Flawed Verifier (`alg: none` + Empty Signature) ✅
Now the actual bypass. Forged the token:

1. **Header** → `"alg":"none"`
2. **Payload** → `"sub":"administrator"`
3. **Signature removed entirely** — token ends with a trailing `.`

Compact form: `base64url(header).base64url(payload).`

Sent `GET /admin` with the forged token in the `session` cookie → **✅ `HTTP/2 200 OK`** — the admin panel HTML is returned in the response body! 🎯

<img width="1280" height="720" alt="Screenshot 2026-10-22 154813" src="https://github.com/user-attachments/assets/58ffccd9-8896-4934-a7f1-652248c60a90" />


---

### Step 6: Delete the User carlos
Scrolled the response body — the **Users** section lists both `wiener` and `carlos`, each with a delete link:

```text
/admin/delete?username=carlos
```

Sent the delete request with the same forged admin token → **✅ `HTTP/2 302 Found`** (redirect back to `/admin`).


<img width="1280" height="684" alt="Screenshot 2026-10-07 025117" src="https://github.com/user-attachments/assets/f50d880f-6c3f-4ce7-b4b3-1260214e9a94" />


---

### Step 7: Lab Solved! 🎉
Following the redirect, the response confirms: **"Congratulations, you solved the lab!"** — and the browser shows `User deleted successfully!` with `carlos` removed from the user list.

<img width="1280" height="684" alt="Screenshot 2026-10-07 025246" src="https://github.com/user-attachments/assets/a0300196-582f-4f86-b86c-17a37d12b37c" />


<img width="1280" height="684" alt="Screenshot 2026-10-22 154657" src="https://github.com/user-attachments/assets/183ea8ce-42d6-4a50-8330-78e4fb376b33" />


---

### What Happens?

**Original JWT (RS256, valid signature):**
```json
Header:  { "kid": "cbe9f5b4-...", "alg": "RS256" }
Payload: { "iss": "portswigger", "exp": 1790689207, "sub": "wiener" }
```
→ ❌ Access denied — normal user, no admin rights

**Tampered claim, signature untouched:**
```json
Payload: { "sub": "administrator" }
```
→ ❌ **401 Unauthorized** — signature mismatch, server correctly rejects

**Forged token with `alg: none` + empty signature:**
```json
Header:  { "alg": "none" }
Payload: { "sub": "administrator" }
Signature: (empty — token ends with ".")
```
→ ✅ **200 OK** — server skips verification for `alg: none` and trusts the forged claim

---

## 🛠️ Burp Suite Intercept

I used **Burp Suite Community Edition** with the **JSON Web Token Editor** extension to intercept, decode, and modify the session token.

### Steps:
1. Logged in with `wiener:peter` and sent the `/my-account` request to **Repeater**
2. Opened the **JSON Web Token** tab to decode the token
3. Changed the header `alg` → `none` (Base64URL re-encoded automatically)
4. Changed the payload `sub` → `administrator`
5. **Removed the signature section entirely** so the token ends with a trailing `.`
6. Forwarded requests to `/admin` and `/admin/delete?username=carlos`

### Attack Flow Summary
| Step | Action | Result |
|------|--------|--------|
| 1 | Capture `/my-account` request | Baseline RS256 JWT obtained |
| 2 | Change header `alg` → `none` | Token still accepted |
| 3 | Request `/admin` as `wiener` | 401 Unauthorized — boundary confirmed |
| 4 | Change `sub` only, keep signature | 401 rejected — signature protects claims |
| 5 | `alg: none` + `sub: administrator` + empty signature | **200 OK — admin access granted** |
| 6 | Delete `carlos` | 302 Found — deletion successful |
| 7 | Verify success | Lab solved |

---

## 📸 Proof of Concept

![Lab Solved](./screenshots/13-lab-solved-browser.png)

As seen in the screenshot:
- The payload `"sub":"administrator"` was injected into the session JWT **with `alg: none` and an empty signature**
- The `/admin` panel loaded successfully and `carlos` was deleted via `/admin/delete?username=carlos`
- Lab shows **"Congratulations, you solved the lab!"**

---

## 🧠 Key Takeaways

### 1. Vulnerability Root Cause
The application **trusts the `alg` header from the token itself**. When it sees `"alg":"none"`, it skips signature verification entirely and blindly accepts the payload claims — a classic fail-open behavior.

### 2. Why `alg: none` is Catastrophic
- The token header must **never** dictate server-side security policy
- Servers should enforce a **strict algorithm allowlist** and ignore the token's own `alg` value
- `decode()` ≠ `verify()` — decoding is not verification; always use the library's `verify()` API

### 3. Encoding ≠ Encryption
JWT payloads are only **Base64URL encoded** — trivially reversible by anyone. The signature is the only thing protecting integrity, and it only works when actually checked.

### 4. Enumeration Strategy
| Attempt | Header `alg` | Payload `sub` | Signature | Response | Meaning |
|---------|-------------|---------------|-----------|----------|---------|
| 1st | `RS256` | `wiener` | Valid | 401 Unauthorized | Normal user, boundary confirmed |
| 2nd | `RS256` | `administrator` | Invalid (untouched) | 401 Unauthorized | ✅ Signature IS checked for RS256 |
| 3rd | `none` | `wiener` | Removed (trailing `.`) | 200 OK | `alg: none` accepted — **flaw confirmed** |
| 4th | `none` | `administrator` | Removed (trailing `.`) | 200 OK | ✅ **Full admin access** |

### 5. Impact
- **Full Account Takeover:** Forge tokens for any identity, including administrators
- **Privilege Escalation:** One header change turns a normal user into admin
- **Complete Application Compromise:** Admin functions, user deletion, data manipulation

### 6. Mitigation Strategies
| Defense | Implementation |
|---------|---------------|
| **Algorithm Allowlist** | Enforce server-side; never trust the token's `alg` header |
| **Reject Unsigned Tokens** | Fail closed on any verification error on all authenticated routes |
| **Use `verify()`, Never Just `decode()`** | Use a maintained JWT library's verification API |
| **Validate Standard Claims** | Enforce `iss`, `aud`, `exp`, `nbf` — not just the signature |
| **Regression Tests** | Altered claims, missing signatures, unexpected `alg` must all be rejected |

### 7. Why This Matters for AppSec
- JWTs power modern APIs, SPAs, and microservices — this flaw class is **extremely common**
- A single algorithm-confusion bug creates a **complete authentication bypass**
- It chains directly into **privilege escalation**, **data breaches**, and **compliance violations**

---

## 📚 References

- [PortSwigger — JWT Attacks](https://portswigger.net/web-security/jwt)
- [PortSwigger — JWT Authentication Bypass via Flawed Signature Verification (Lab)](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [jwt.io — JWT Debugger](https://jwt.io/)
- [Burp JWT Editor Extension](https://portswigger.net/bappstore)

---

## 🔗 Related Labs

| Lab | Topic | Status |
|-----|-------|--------|
| [Lab 12](../12-jwt-unverified-signature) | JWT — Authentication Bypass via Unverified Signature | ✅ Solved |
| [Lab 13](./13-jwt-flawed-signature) | JWT — Authentication Bypass via Flawed Signature Verification | ✅ Solved |
| [Lab 14](../14-jwt-weak-secret) | JWT — Brute-Forcing Weak Secret Keys | ⏳ Pending |

---

> 📝 **Author:** Saber Hasan Swoyon  
> 🎓 **Status:** Student | Aspiring AppSec Engineer  
> 📅 **Date Solved:** 2026-10-22
