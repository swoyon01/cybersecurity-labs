# 🔑 Lab 12: JWT Attacks — Authentication Bypass via Unverified Signature

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved

---

## 📋 Lab Description

> *"This lab uses a JWT-based mechanism for handling sessions. Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives. To solve the lab, modify your session token to gain access to the admin panel at /admin, then delete the user carlos. You can log in to your own account using the following credentials: wiener:peter."*

---

## 🔍 Reconnaissance

### Step 1: Identify the Authentication Mechanism
<img width="1280" height="684" alt="Screenshot 2026-09-29 204151" src="https://github.com/user-attachments/assets/30416e19-743e-4a70-9d16-6fb12af6e68a" />

Logged in with the provided credentials `wiener:peter` and inspected the session handling. The application issues a JWT inside the `session` cookie after login.

### Step 2: Test the Session Token
Visited `/admin` with the valid session — the response was:
<img width="1280" height="684" alt="Screenshot 2026-09-29 205119" src="https://github.com/user-attachments/assets/d652997d-eba6-4b90-a3cd-4a8ef072d0f1" />


```
"Admin interface only available if logged in as an administrator"
```
<img width="1280" height="684" alt="Screenshot 2026-09-29 205411" src="https://github.com/user-attachments/assets/1ce62c0c-6b79-48bc-883e-8db584e0579f" />

**Result:** `401 Unauthorized` — the application checks the `sub` (subject) claim of the JWT to decide access, but the question is: **does it verify the signature?**

---

## 🚀 Exploitation

### Goal: Modify the JWT Payload Without a Valid Signature

A JWT has three parts:

```
HEADER.PAYLOAD.SIGNATURE
```

The **payload** is only **Base64URL encoded — NOT encrypted**. Anyone can read and modify it. Normally, the **signature** protects the payload from tampering. In this lab, the server **never verifies the signature**, so we can modify the payload freely.

---

### Step 1: Capture & Decode the JWT
Intercepted the `POST /login` request in Burp Suite and examined the `Set-Cookie: session=` header using Burp's **JSON Web Token** tab.

**Decoded JWT:**

```json
// Header
{
  "kid": "7230234b-8b3e-460b-a569-c44aaf74d9d2",
  "alg": "RS256"
}

// Payload
{
  "iss": "portswigger",
  "exp": 1790689207,
  "sub": "wiener"
}
```
<img width="1280" height="684" alt="Screenshot 2026-09-29 204437" src="https://github.com/user-attachments/assets/ea9eb045-2bcc-4a63-b8d8-6b87f0e46032" />


> **Note:** The JSON Web Token tab shows the full decoded token — Header (`kid`, `alg: RS256`), Payload (`iss`, `exp`, `sub`), and the raw signature bytes.

---

### Step 2: Confirm /admin Access is Denied (Before Attack)
Sent the request to `/admin` using the original token in Burp Repeater.

**Result:** ❌ **401 Unauthorized**

<img width="1280" height="684" alt="Screenshot 2026-09-29 205411" src="https://github.com/user-attachments/assets/678eb028-a8fe-4010-9923-60c1faf5d054" />


> **Note:** The Repeater response shows `HTTP/2 401 Unauthorized` with the "Admin interface only available if logged in as an administrator" message. The original `sub: wiener` token is rejected.

---

### Step 3: Modify the JWT Payload (The Attack!) ✅
Since the signature is **not verified**, simply changed the `sub` claim from `"wiener"` to `"administrator"` in Burp's JSON Web Token editor and forwarded the request — **no re-signing needed**.

**Modified Payload:**
```json
{
  "iss": "portswigger",
  "exp": 1790703141,
  "sub": "administrator"   // <-- changed from "wiener"
}
```

<img width="1280" height="684" alt="Screenshot 2026-09-30 004025" src="https://github.com/user-attachments/assets/2575b722-36fa-4d70-8b34-cdd0487c8979" />


> **Note:** The payload section shows `"sub":"administrator"`. The JWT was tampered with directly in the editor and sent to `/admin` without a valid signature — the server accepted it.

---

### Step 4: Access the Admin Panel
Sent the request to `/admin` with the tampered JWT.

**Result:** ✅ **200 OK** — full admin panel access granted! 🎯



The admin panel revealed the user list with delete options:

```
Users
  wiener  -  Delete
  carlos  -  Delete
```

<img width="1280" height="684" alt="Screenshot 2026-09-30 004242" src="https://github.com/user-attachments/assets/318867ab-24e1-4890-9e8e-66671386f8c8" />


---

### Step 5: Delete the User carlos
Sent the final request:

```
GET /admin/delete?username=carlos
```

**Result:** ✅ **302 Found** — carlos was successfully deleted!
<img width="1280" height="684" alt="Screenshot 2026-09-30 004333" src="https://github.com/user-attachments/assets/eb27a8ac-c158-4d0b-9e8c-701a0bdf77fc" />

<img width="1280" height="684" alt="Screenshot 2026-09-30 010013" src="https://github.com/user-attachments/assets/2691f947-14b4-460f-bdd1-d7c28e9dcb71" />


---

### What Happens?

**Original JWT Payload:**
```json
{ "iss": "portswigger", "exp": 1790689207, "sub": "wiener" }
```
→ ❌ Access denied — not an administrator

**Tampered JWT Payload (signature left invalid):**
```json
{ "iss": "portswigger", "exp": 1790703141, "sub": "administrator" }
```
→ ✅ Access granted — full admin privileges, because the server **never checked the signature**

---

## 🛠️ Burp Suite Intercept

I used **Burp Suite Community Edition** with the **JSON Web Token Editor** extension to intercept, decode, and modify the session token.

### Steps:
1. Configured Firefox proxy to route through Burp Suite (127.0.0.1:8080)
2. Logged in with `wiener:peter` and intercepted the `POST /login` request
3. Observed the `Set-Cookie: session=<JWT>` header in the response
4. Sent requests to **Repeater** for repeated testing
5. Opened the **JSON Web Token** tab to decode and edit the payload
6. Changed `sub: wiener` → `sub: administrator` and forwarded the request


> **Note:** Burp's JSON Web Token editor shows the deserialized JWT with editable Header, Payload, and Signature sections — making tampering trivial when verification is missing.

---

## Concept

As seen in the screenshot:
- The payload `"sub":"administrator"` was injected into the session JWT **without a valid signature**
- The `/admin` panel loaded successfully and `carlos` was deleted via `/admin/delete?username=carlos`
- Lab shows **"Congratulations, you solved the lab!"**

---

## 🧠 Key Takeaways

### 1. Vulnerability Root Cause
The application **parses the JWT payload but never cryptographically verifies the signature**. This means an attacker can claim any identity simply by editing the Base64URL-encoded payload.

### 2. Why Base64URL is NOT Encryption
- JWT payloads are only **Base64URL encoded** — a reversible encoding, not a cipher
- Anyone can decode, read, and modify the contents (use `jwt.io` or Burp's JWT tab)
- **Only the signature protects integrity** — without verification, the token is just a signed-looking JSON object

### 3. Enumeration Strategy
| Attempt | Payload `sub` value | Signature | Response | Meaning |
|---------|--------------------:|-----------|--------|---------|
| 1st | `wiener` (original) | Valid | 401 Unauthorized | Normal user, no admin rights |
| 2nd | `administrator` | **Invalid (untouched)** | 200 OK | ✅ **Signature NOT verified** |

### 4. Impact
- **Full Account Takeover:** Claim any user's identity, including administrators
- **Privilege Escalation:** A normal user becomes admin by changing one string
- **Complete Application Compromise:** Admin panels, user deletion, data manipulation — everything an admin can do

### 5. Mitigation Strategies
| Defense | Implementation |
|---------|---------------|
| **Always Verify Signatures** | Reject any JWT whose signature fails validation — no exceptions |
| **Enforce Algorithm Allowlist** | Only accept expected algorithms (e.g., RS256); reject `none` |
| **Use Established Libraries** | Use actively maintained JWT libraries (`jsonwebtoken`, `PyJWT`, etc.) |
| **Server-Side Identity Checks** | Never trust token claims alone; verify roles against the database |
| **Short Expiry + Revocation** | Keep `exp` short and maintain a token denylist |

### 6. Why This Matters for AppSec
Understanding JWT verification flaws is critical because:
- JWTs are **everywhere** — modern APIs, SPAs, microservices all use them
- A single missing `verify()` call creates a **complete authentication bypass**
- It leads directly to **privilege escalation**, **data breaches**, and **compliance violations**
- It often chains into larger attacks (IDOR, admin function abuse, mass user deletion)

---

## 📚 References

- [PortSwigger — JWT Attacks](https://portswigger.net/web-security/jwt)
- [PortSwigger — Exploiting Flawed JWT Signature Verification](https://portswigger.net/web-security/jwt#flawed-jwt-signature-verification)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [jwt.io — JWT Debugger](https://jwt.io/)
- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

---

## 🔗 Related Labs

| Lab | Topic | Status |
|-----|-------|--------|
| [Lab 11](../11-xxe) | XXE — External Entity Exploitation | ✅ Solved |
| [Lab 12](./12-jwt-unverified-signature) | JWT — Authentication Bypass via Unverified Signature | ✅ Solved |
| [Lab 13](../13-jwt-wak-secret) | JWT — Brute-Forcing Weak Secret Keys | ⏳ Pending |

---

> 📝 **Author:** Saber Hasan Swoyon  
> 🎓 **Status:** Student | Aspiring AppSec Engineer  
> 📅 **Date Solved:** 2026-09-30
