# Lab 13: JWT Authentication Bypass via Flawed Signature Verification

> **Source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification)  
> **Track:** Authentication / JWT  
> **Difficulty:** Apprentice  
> **Status:** ✅ Solved

---

## 🎯 Objective

Exploit a flaw in the lab's JWT signature verification to access `/admin` as `administrator`, then delete the user `carlos` to complete the lab.

---

## 🛠️ Tools

- Burp Suite Community Edition (Repeater + Inspector)
- Firefox (Burp Browser)
- Kali Linux

---

## 🔍 Vulnerability Background

The lab verifies JWTs insecurely: **when the token header specifies `"alg":"none"`, the server skips signature verification entirely** and blindly trusts the payload claims.

JWT header and payload are only **Base64URL-encoded — not encrypted**. Anyone can decode, modify, and re-encode them. Because the server accepts an unsigned token, changing the `sub` claim to `administrator` grants full admin access — no secret key required.

⚠️ **Lesson:** Decoding a token is not verifying it. A JWT must be treated as a *bearer credential*.

---

## 🔍 Step-by-Step Methodology

### Step 1 — Capture the Baseline Authenticated Request

Logged in with the lab-supplied credentials (`wiener`), loaded `/my-account`, and sent the request to **Burp Repeater**. The `session` cookie contains a JWT. The Inspector panel decodes the header:

```json
{"kid":"cbe9f5b4-02c0-4713-841d-de4eb3101837","alg":"RS256"}
```

The baseline token is signed with **RS256**.

<img width="1280" alt="baseline-jwt-request" src="screenshots/01-baseline-jwt-request.png">

---

### Step 2 — Test the `alg: none` Header

Modified the JWT header, changing the algorithm to `none` (re-encoded as Base64URL). The token remains accepted because the payload claim (`sub: wiener`) is unchanged — confirming the server parses the header algorithm from the token itself.

<img width="1280" alt="alg-none-header-test" src="screenshots/02-alg-none-header-test.png">

---

### Step 3 — Confirm the Access-Control Boundary

Requested `/admin` as the normal user — both in the browser and in Repeater.

**Browser result:**
> Admin interface only available if logged in as an administrator

**Repeater result:** `HTTP/2 401 Unauthorized` with the original RS256 token (`sub: wiener`).

<img width="1280" alt="admin-denied-browser" src="screenshots/03-admin-denied-browser.png">

<img width="1280" alt="admin-denied-401" src="screenshots/04-admin-denied-401.png">

---

### Step 4 — Modify the Claim Without Removing the Signature (Rejected)

Changed the payload claim `sub` → `administrator` but **left the signature section untouched**. The server correctly **rejects** the token — the signature no longer matches the modified payload. This proves the signature protects the claims *when it is actually verified*.

<img width="1280" alt="admin-claim-rejected" src="screenshots/05-admin-claim-rejected.png">

---

### Step 5 — Exploit the Flawed Verifier (`alg: none` + empty signature)

Now the actual bypass. Forged the token:

1. Header → `"alg":"none"`
2. Payload → `"sub":"administrator"`
3. **Signature removed entirely** — token ends with a trailing `.`

Compact form: `base64url(header).base64url(payload).`

Sent `GET /admin` with the forged token in the `session` cookie → **`HTTP/2 200 OK`**. The admin panel HTML is returned in the response body.

<img width="1280" alt="alg-none-admin-accepted" src="screenshots/06-alg-none-admin-accepted.png">

<img width="1280" alt="admin-panel" src="screenshots/07-admin-panel.png">

---

### Step 6 — Delete `carlos` via the Admin Panel

Scrolled the response body — the **Users** section lists both `wiener` and `carlos`, each with a delete link:

```text
/admin/delete?username=carlos
```

Sent the delete request with the same forged admin token → **`HTTP/2 302 Found`** (redirect back to `/admin`).

<img width="1280" alt="admin-user-list" src="screenshots/08-admin-user-list.png">

<img width="1280" alt="delete-carlos-302" src="screenshots/09-delete-carlos-302.png">

---

### Step 7 — Lab Solved

Following the redirect, the response confirms: **"Congratulations, you solved the lab!"** — and the browser shows `User deleted successfully!` with `carlos` removed from the user list. 🎉

<img width="1280" alt="lab-solved-repeater" src="screenshots/10-lab-solved-repeater.png">

<img width="1280" alt="lab-solved-browser" src="screenshots/11-lab-solved-browser.png">

---

## 📝 Attack Flow Summary

| Step | Action | Tool | Result |
|------|--------|------|--------|
| 1 | Capture `/my-account` request | Burp Proxy / Repeater | Baseline RS256 JWT obtained |
| 2 | Change header `alg` → `none` | Inspector | Token still accepted |
| 3 | Request `/admin` as `wiener` | Browser / Repeater | 401 Unauthorized — boundary confirmed |
| 4 | Change `sub` only, keep signature | Inspector | 401 rejected — signature protects claims |
| 5 | `alg: none` + `sub: administrator` + empty signature | Repeater | **200 OK — admin access granted** |
| 6 | Delete `carlos` | Repeater | 302 Found — deletion successful |
| 7 | Verify success | Browser | Lab solved |

---

## 🎯 Key Takeaways

1. **`alg: none` is catastrophic** — Never let a token header dictate verification policy; enforce a strict server-side algorithm allowlist.
2. **Encoding ≠ Encryption** — Base64URL is trivially reversible. JWT payloads are readable and editable by anyone.
3. **A correct verifier fails closed** — Step 4 proved the signature protects claims *when verified*. The bug was skipping verification entirely for `alg: none`.
4. **The trailing `.` matters** — Removing the signature section means an empty third segment; some tools silently drop it.
5. **`decode()` ≠ `verify()`** — Use the library's verification API and fail closed on any error.
6. **Validate standard claims** — `iss`, `aud`, `exp`, `nbf` should all be enforced, not just the signature.

---

## 🛡️ How This Is Fixed (Defender View)

- Maintain an **explicit server-side algorithm allowlist** — ignore the token's `alg` header.
- **Reject unsigned tokens** on all authenticated routes; fail closed on any verification failure.
- Use a maintained JWT library's **`verify()`** method, never decode-only.
- Validate standard claims (`iss`, `aud`, `exp`, `nbf`) as appropriate.
- Add regression tests: altered claims, missing signatures, unexpected `alg`, and invalid signatures must all be rejected.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the PortSwigger Web Security Academy. Unauthorized testing on systems you do not own or have explicit permission to test is **illegal and unethical**.

> 🔒 Session tokens and lab hostnames should be redacted (blurred) in screenshots before publishing, as they are replayable bearer credentials.

---

## 🔗 References

- [PortSwigger JWT Labs](https://portswigger.net/web-security/jwt)
- [JWT Authentication Bypass via Flawed Signature Verification — Lab](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [Burp JWT Editor Extension](https://portswigger.net/bappstore)

---

*Happy Hacking! 🐱‍💻*
