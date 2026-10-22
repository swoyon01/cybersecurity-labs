# 🔐 Lab 14: JWT Attacks — Authentication Bypass via Weak Signing Key

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-weak-signing-key)  
> **Difficulty:** 🟠 Practitioner  
> **Status:** ⏳ In progress — the screenshot supplied so far shows **Not solved**

---

## 📋 Lab Description

This lab uses a JWT-based session mechanism with an extremely weak secret key. The key can be recovered with a wordlist. To complete the lab, use the recovered key to sign a modified session token, access `/admin`, and delete the user `carlos`.

The lab-provided credentials are `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these steps against systems unless you have explicit authorization.

---

## 🔍 Reconnaissance

### Step 1: Capture and inspect the session JWT

1. Start the lab and log in using `wiener:peter`.
2. In Burp Suite, send the post-login `GET /my-account` request to **Repeater**.
3. Inspect the `session` cookie with Burp's **JSON Web Token** editor. The token uses a symmetric HMAC signing algorithm (the lab token uses `HS256`). Save a copy of the JWT locally for the cracking step; do not add the token or cookie to this README.
4. Change the request path to `/admin` and send it. As the normal user, access should be denied.
<img width="1280" height="684" alt="Screenshot 2026-10-18 014931" src="https://github.com/user-attachments/assets/d5d27a09-35df-48f3-9578-8ec4d5d8f4c9" />

<img width="1280" height="684" alt="Screenshot 2026-10-22 220656" src="https://github.com/user-attachments/assets/ed4d054d-c39c-4c4d-8b77-6e58d50887e8" />

<img width="1280" height="684" alt="image" src="https://github.com/user-attachments/assets/aa42ef71-ee41-4dc5-8353-f3b1d7493151" />


---

## 🚀 Exploitation

### Step 2: Brute-force the weak signing secret

Use Hashcat's JWT HMAC-SHA256 mode (`16500`) with a JWT secrets wordlist. Replace `<YOUR-JWT>` with the captured token and the wordlist path with the location on your machine:

```bash
hashcat -a 0 -m 16500 '<YOUR-JWT>' /usr/share/wordlist.........
```
<img width="1280" height="684" alt="Screenshot 2026-10-17 181257" src="https://github.com/user-attachments/assets/6d84ced2-29a2-4abe-989f-3359d8dda1bc" />

The lab's weak signing secret is:

```text
secret1
```

If Hashcat has already cracked the token and you need to display the saved result again, use `--show`:

```bash
hashcat -m 16500 --show '<YOUR-JWT>'
```
<img width="1280" height="684" alt="Screenshot 2026-10-17 181554" src="https://github.com/user-attachments/assets/bbb1b406-1f60-4471-9492-b9139746863c" />

---

### Step 3: Create a symmetric signing key in Burp

Burp's JWT Editor expects the JWK `k` value to contain the Base64-encoded secret. Encode the lab secret:

```bash
printf 'secret1' | base64
# c2VjcmV0MQ==
```

Then in Burp Suite:

1. Open **JWT Editor Keys** and select **New Symmetric Key**.
2. Click **Generate** to create a JWK.
3. Replace the generated `k` value with the Base64 value above, then save the key.

Base64 is only an encoding; it does not make a secret safe. The value shown here is the known secret for this practice lab, not a production credential.

<img width="1280" height="684" alt="Screenshot 2026-10-18 015230" src="https://github.com/user-attachments/assets/82a65da2-9b4b-4718-81ff-5ab6c56bdbaa" />

---

### Step 4: Modify and sign the JWT

1. Return to the `GET /admin` request in Repeater and open the **JSON Web Token** editor tab.
2. Change the payload claim `sub` from `wiener` to `administrator`.
3. Select **Sign**, choose the symmetric key you created, and leave **Don't modify header** selected. This preserves the token's existing signing algorithm while producing a valid signature with the recovered secret.
4. Send the request. The lab should now return the admin page.

Unlike the previous “flawed signature verification” lab, this attack does **not** remove the signature or set `alg` to `none`. The application verifies the signature, but the weak signing key allows us to create a valid one for the modified claims.

<img width="1280" height="684" alt="Screenshot 2026-10-18 015319" src="https://github.com/user-attachments/assets/46d479b0-e4e6-4793-94dc-fb2fcaa877df" />

<img width="1280" height="684" alt="Screenshot 2026-10-17 183407" src="https://github.com/user-attachments/assets/9521f7e2-ff00-45fe-9ab7-0a67e47c58c0" />


---

### Step 5: Delete `carlos` and verify completion

From the admin page, find the delete link for `carlos`. Send the lab's delete request:

```http
GET /admin/delete?username=carlos
```

The lab typically responds with `302 Found` and redirects back to `/admin`. Follow the redirect; the page should show **“Congratulations, you solved the lab!”**

<img width="1280" height="684" alt="Screenshot 2026-10-17 183751" src="https://github.com/user-attachments/assets/f424616e-90e2-421f-81a0-c0817d86a3bc" />


<img width="1280" height="684" alt="Screenshot 2026-10-18 015450" src="https://github.com/user-attachments/assets/696c6b37-0af1-43b6-82d9-923217a3fe16" />


---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Capture the normal user's JWT | Baseline signed session token |
| 2 | Request `/admin` as `wiener` | Access denied |
| 3 | Crack the JWT with Hashcat mode `16500` | Weak secret recovered: `secret1` |
| 4 | Create a Burp symmetric JWK using the Base64-encoded secret | Key ready to sign |
| 5 | Change `sub` to `administrator` and sign without modifying the header | Valid modified JWT |
| 6 | Request `/admin` with the newly signed token | Admin panel returned |
| 7 | Delete `carlos` and follow the redirect | Lab solved |

---

## 🧠 Key Takeaways

### 1. Root cause

The JWT is signed with a weak, guessable symmetric secret. Because the same secret is used to create and verify the HMAC signature, recovering it lets an attacker produce valid signatures for modified claims.

### 2. Impact

A valid forged token can impersonate another user, including an administrator, and reach actions protected by that identity. In this lab, that permits access to `/admin` and deletion of `carlos`.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Use a high-entropy signing secret** | Generate a cryptographically random key appropriate for the algorithm; never use dictionary words or sample values. |
| **Protect and rotate keys** | Store signing keys in a secrets manager, restrict access, and rotate them if exposure is suspected. |
| **Pin allowed algorithms** | Configure the server to accept only the expected algorithm; do not let an untrusted token header set security policy. |
| **Verify all security-relevant claims** | Validate the signature and applicable claims such as `iss`, `aud`, `exp`, and `nbf`. |
| **Add negative tests** | Ensure weak/incorrect keys, altered claims, invalid signatures, and unexpected algorithms are rejected. |

---

## 📚 References

- [PortSwigger — JWT attacks](https://portswigger.net/web-security/jwt)
- [PortSwigger — JWT authentication bypass via weak signing key (lab)](https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-weak-signing-key)
- [PortSwigger — Brute-forcing secret keys using Hashcat](https://portswigger.net/web-security/jwt#brute-forcing-secret-keys-using-hashcat)
- [Wallarm — JWT secrets wordlist](https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list)
- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)

---


> 📝 **Author:** Swoyon  
> 📅 **Date solved:** 22-10-2026
