# 07 Lab: User ID Controlled by Request Parameter, with Data Leakage in Redirect

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-data-leakage-in-redirect)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab looks, at first, like it has fixed the IDOR from the earlier labs: browsing to `/my-account?id=carlos` as another user no longer shows carlos's account page in the browser — instead it redirects back to the user's own account.

The flaw is in **how** the redirect happens. The server starts building the response for `carlos`'s account (including his API key) and only **then** issues the redirect. The sensitive data is already present in the body of that redirect response — the browser just never renders it because it follows the redirect immediately. Reading the raw HTTP response (instead of letting the browser follow the redirect) reveals the leaked data.

To solve the lab, obtain the API key of the user `carlos` and submit it as the solution. A valid low-privileged account is provided: `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Log in and look at the account page

Log in with the credentials provided by the lab (`wiener:peter`) and open **My Account**. The page shows wiener's username, email and API key, with `id=wiener` in the URL.

<img width="2559" height="1251" alt="Screenshot_2026-11-27_12_45_36" src="https://github.com/user-attachments/assets/09b407be-9d30-437b-82f5-8744398ef6d4" />


### Step 2: Try changing the `id` parameter in the browser

Edit the URL to `/my-account?id=carlos`. This time the lab is **Not solved** and the page redirects back to wiener's own account instead of showing carlos's data — it looks like the IDOR has been fixed.


---

## 🚀 Exploitation

### Step 3: Replay the request in Burp Repeater and inspect the raw response

Send the request to **Burp Repeater**:

```
GET /my-account?id=carlos HTTP/2
```

Instead of letting Burp follow the redirect, inspect the response body directly. Even though the server intends to redirect the request away, the response body was already generated for `carlos` and contains his username and API key before the redirect takes effect.

<img width="2559" height="1251" alt="Screenshot_2026-11-27_12_45_58" src="https://github.com/user-attachments/assets/f7835056-6292-43ab-88d8-6f6ceab30853" />

### Step 4: Submit the API key

Copy carlos's API key from the leaked response body, click **Submit solution** on the lab page, and paste the key in. The lab banner flips to **Solved** with the message "Congratulations, you solved the lab!".
<img width="2559" height="1251" alt="Screenshot_2026-11-27_12_47_08" src="https://github.com/user-attachments/assets/ba7fd7be-1fa6-4d38-9cf5-ec67c917f490" />

---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Log in as `wiener:peter` and open My Account | URL contains `?id=wiener`, shows wiener's data |
| 2 | Change the URL to `/my-account?id=carlos` in the browser | Browser redirects back to wiener's account; looks protected |
| 3 | Replay `GET /my-account?id=carlos` in Burp Repeater | Raw response body contains carlos's username and API key before the redirect |
| 4 | Submit carlos's API key | "Congratulations, you solved the lab!" |

---

## 🧠 Key Takeaways

### 1. Root cause

The access-control check runs **after** the response for the requested account has already been built, and only a redirect is used to hide it from a normal browser. The data itself is still sent to the client in the HTTP response body; only the browser's automatic redirect-following stops it from being displayed. An attacker using a proxy like Burp Suite can simply read the raw response and bypass the "protection" entirely.

### 2. Impact

Any logged-in user can read another user's account data, including their API key, by inspecting the raw HTTP response instead of relying on the browser to follow the redirect. This is still **horizontal privilege escalation / IDOR**, just with a redirect giving a false sense of security.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Check access control before building the response** | Verify the user's ownership of the resource before any sensitive data is loaded or rendered, not after. |
| **Never rely on redirects as a security control** | A redirect only changes what the browser displays; it does not remove data already sent in the response body. |
| **Fail closed, early** | If the authorization check fails, return an error/redirect immediately, with no sensitive data in the body at all. |
| **Check object ownership on every request** | Verify on the server that the logged-in user is allowed to access the requested record. |
| **Test with raw HTTP, not just the browser** | Security testing should inspect actual responses (e.g. with Burp) rather than trusting what the browser renders. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — User ID controlled by request parameter, with data leakage in redirect (lab)](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-data-leakage-in-redirect)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

## 📸 Screenshots

All screenshots :

1. `01-my-account-wiener.png` — My Account page as `wiener`, with `id=wiener` in the URL
2. `02-id-carlos-redirect-not-solved.png` — browsing to `id=carlos` redirects back to wiener's account
3. `03-burp-response-carlos-api-key-leak.png` — Burp Repeater showing carlos's API key leaked in the raw response before the redirect

> 📝 **Author:** Hasan Abu Saber
> 📅 **Date solved:** 2026-11-28
