# 🔐 Lab 15: JWT Attacks — Authentication Bypass via JWK Header Injection

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jwk-header-injection)  
> **Difficulty:** 🟠 Practitioner  
> **Status:** ✅ Solved


---

## 📋 Lab Description

This lab uses a JWT-based session mechanism that trusts the `jwk` (JSON Web Key) parameter in the token header to supply the key used to verify the signature. An attacker can generate their own RSA key pair, sign a modified token with the private key, and embed the matching public key directly in the `jwk` header. If the server does not restrict which keys it will accept, it verifies the forged token successfully.

To complete the lab, forge a valid admin session token and use it to access `/admin` and delete the user `carlos`.

The lab-provided credentials are `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these steps against systems unless you have explicit authorization.

---

## 🔍 Reconnaissance

### Step 1: Capture and inspect the session JWT

1. Start the lab and log in using `wiener:peter`.
2. In Burp Suite, send the post-login `GET /my-account` request to **Repeater**.
3. Inspect the `session` cookie with Burp's **JSON Web Token** editor. The token header uses an asymmetric signing algorithm (the lab token uses `RS256`). Save a copy of the JWT locally for later steps; do not add the token or cookie to this README.
4. Change the request path to `/admin` and send it. As the normal user, access should be denied.

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/b73216f9-b95a-421e-8ad4-0bd3ba473345" />

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/68002de0-4b3e-4e9e-bda5-b6bf42699f54" />


<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/75ac634f-6014-43e7-8ac2-59a0762e4ff6" />

---

## 🚀 Exploitation

### Step 2: Generate a new RSA key pair in Burp

1. In Burp's **JWT Editor Keys** tab, click **New RSA Key**.
2. Click **Generate** to create a new key pair, then save it. This key is entirely attacker-controlled and has nothing to do with the server's real signing key.

<img width="1280" height="684" alt="image" src="https://github.com/user-attachments/assets/5667a388-cb22-482f-9cd4-474bbe76d15e" />


---

### Step 3: Modify the claims and embed the JWK header

1. Return to the `GET /admin` request in Repeater and open the **JSON Web Token** editor tab.
2. Change the payload claim `sub` from `wiener` to `administrator`.
3. Select **Attack** → **Embedded JWK**, then choose the RSA key generated in Step 2.

Burp's JWT Editor does the equivalent of the following automatically:
- Signs the token with the new key's **private** key.
- Adds a `jwk` parameter to the token **header** containing the new key's **public** key, in JWK format.
- Sets `kid` in the header to match the `kid` of the embedded JWK.

If the server reads the key to verify the signature straight from the `jwk` header, instead of checking it against a trusted keystore, the forged token verifies as authentic even though it was never issued by the server.

4. Send the request.

<img width="1280" height="684" alt="image" src="https://github.com/user-attachments/assets/d362a306-a52a-4875-b252-478341c1df5b" />

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/c9bcac4b-cf5a-46c3-9baa-0e138c2ccb77" />

---

### Step 4: Delete `carlos` and verify completion

From the admin page, find the delete link for `carlos`. Send the lab's delete request:

```http
GET /admin/delete?username=carlos
```

The lab typically responds with `302 Found` and redirects back to `/admin`. Follow the redirect; the page should show **“Congratulations, you solved the lab!”**

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/f66b5094-86c7-4b19-a6cb-8611fc5b91ae" />

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/9c2cabaf-d8c1-4a6e-a23d-9dca79e1b4de" />

---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Capture the normal user's JWT | Baseline signed session token (RS256) |
| 2 | Request `/admin` as `wiener` | Access denied |
| 3 | Generate a new attacker-controlled RSA key pair | Private key for signing, public key for the `jwk` header |
| 4 | Change `sub` to `administrator` | Modified payload |
| 5 | Sign the token and embed the public key via the `jwk` header (Burp: Attack → Embedded JWK) | Server verifies the token against the attacker's own embedded key |
| 6 | Request `/admin` with the newly signed token | Admin panel returned |
| 7 | Delete `carlos` and follow the redirect | Lab solved |

---

## 🧠 Key Takeaways

### 1. Root cause

The server trusts the `jwk` header to supply the public key used for signature verification, instead of verifying against a fixed, pre-registered set of trusted keys. This lets an attacker supply their own key pair and have the server validate a token signed with it, defeating the point of signature verification entirely.

### 2. Impact

A valid forged token can impersonate another user, including an administrator, and reach actions protected by that identity. In this lab, that permits access to `/admin` and deletion of `carlos`.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Never derive trust from attacker-controlled header fields** | Do not accept `jwk` (or `jku`) values to determine the verification key; these are part of the untrusted token. |
| **Use a fixed, server-side keystore** | Verify signatures only against keys the server itself generated and stores, looked up by a trusted identifier. |
| **Pin allowed algorithms** | Configure the server to accept only the expected algorithm; do not let an untrusted token header set security policy. |
| **Verify all security-relevant claims** | Validate the signature and applicable claims such as `iss`, `aud`, `exp`, and `nbf`. |
| **Add negative tests** | Ensure tokens with injected or unexpected `jwk`/`jku`/`kid` headers are rejected. |

---

## 📚 References

- [PortSwigger — JWT attacks](https://portswigger.net/web-security/jwt)
- [PortSwigger — JWT authentication bypass via jwk header injection (lab)](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jwk-header-injection)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 7517 — JSON Web Key (JWK)](https://datatracker.ietf.org/doc/html/rfc7517)

---

## 📸 Screenshot placement

Save your screenshots in a `screenshots/` folder and use the filenames referenced above. The README already has a placeholder at each step. Before publishing, redact session cookies/JWTs and consider hiding the temporary lab hostname from screenshots.

> 📝 **Author:** Saber Hasan Swoyon  
> 📅 **Date solved:** 26-10-2026
