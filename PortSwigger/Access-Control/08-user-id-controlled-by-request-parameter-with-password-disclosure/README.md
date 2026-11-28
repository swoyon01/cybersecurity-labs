# 08 Lab: User ID Controlled by Request Parameter, with Password Disclosure

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-password-disclosure)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab has the same `/my-account?id=` pattern as the earlier labs, but this time the account page includes a **password change form** whose hidden fields leak the current value of other users' passwords.

Requesting another user's account page (`/my-account?id=administrator`) returns a page that includes a password `<input>` field with the user's actual password pre-filled as its `value`. The front end hides this by rendering it as a password field (dots), but the raw HTTP response contains the plaintext password.

To solve the lab, leak the administrator's password, log in as `administrator`, and use the admin panel to delete the user `carlos`. A valid low-privileged account is provided: `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Log in and request the administrator's account page

Log in with the credentials provided by the lab (`wiener:peter`). With Burp Suite running, send a request for the administrator's account:

```
GET /my-account?id=administrator
```
<img width="2559" height="1251" alt="Screenshot_2026-11-28_14_30_51" src="https://github.com/user-attachments/assets/6e7a3153-e9bb-4745-92a8-9a43ca1b81c0" />

### Step 2: Read the leaked password from the raw response

In Burp, inspect the raw HTML response rather than the rendered page. The `change-password` form contains a hidden/password `<input>` whose `value` attribute holds the administrator's real password in plaintext:

```html
<input required type="password" name="password" value="0hkqwv26clldnr59po01">
```
<img width="2559" height="1251" alt="Screenshot_2026-11-28_14_31_43" src="https://github.com/user-attachments/assets/5516c18a-0c6a-4626-9016-f9a844873507" />


---

## 🚀 Exploitation

### Step 3: Log out and log back in as administrator

Log out of `wiener`'s session, then log in using:

```
Username: administrator
Password: <the leaked password>
```

The **My Account** page now shows the logged-in user as `administrator`, and an **Admin panel** link appears in the navigation bar — confirming the login succeeded with administrator privileges.

<img width="2559" height="1251" alt="Screenshot_2026-11-28_14_35_43" src="https://github.com/user-attachments/assets/aa0cd075-fd0b-4757-a5eb-1e24b5a5d480" />


### Step 4: Open the admin panel and delete `carlos`

Click **Admin panel**. The page lists all users (`wiener`, `carlos`), each with a **Delete** link.

<img width="2559" height="1251" alt="Screenshot_2026-11-28_14_36_03" src="https://github.com/user-attachments/assets/c73c0160-7af1-4f75-a5c4-4ea36c2d4aee" />


Click **Delete** next to `carlos`. The page confirms `User deleted successfully!`, `carlos` is removed from the Users list, and the lab banner flips to **Solved**.

---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Log in as `wiener:peter` and request `/my-account?id=administrator` via Burp | Server returns administrator's account page |
| 2 | Inspect the raw response | The password input's `value` leaks the administrator's plaintext password |
| 3 | Log out and log back in as `administrator` with the leaked password | Logged in with admin privileges; Admin panel link appears |
| 4 | Open the admin panel and delete `carlos` | "User deleted successfully!" and lab marked as solved |

---

## 🧠 Key Takeaways

### 1. Root cause

Two access-control failures combine here: first, the same IDOR as the earlier labs lets any user load another user's account page via `id=`. Second, the password change form pre-fills the password field with the user's **actual current password** instead of leaving it blank, leaking sensitive credentials to anyone who can view the response — even if the browser masks it visually.

### 2. Impact

An attacker can escalate from a low-privileged account directly to full administrator access by reading the admin's password out of a leaked form field, then logging in normally. This is a severe escalation: full account takeover, not just data exposure.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Never pre-fill password fields with the real password** | Leave password fields blank, or use a placeholder, and only update the password if the user submits a new value. |
| **Check object ownership on every request** | Verify on the server that the logged-in user is allowed to view the requested account. |
| **Use the session, not a request parameter** | Take the user's identity from the server-side session instead of an `id` supplied by the client. |
| **Never return secrets in HTML attributes** | Sensitive values should never be embedded in markup just because the front end can visually hide them. |
| **Hash and never display passwords** | Store passwords hashed, and never send the plaintext value back to the client after the initial submission. |
| **Test for IDOR and data leakage** | Include tests that inspect raw HTTP responses, not just the rendered page, for sensitive fields. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — User ID controlled by request parameter, with password disclosure (lab)](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-password-disclosure)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---


> 📝 **Author:** Saber Hasan Swoyon
> 📅 **Date solved:** 2026-11-28
