# 05 Lab: User ID Controlled by Request Parameter

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab has a horizontal privilege escalation vulnerability on the user account page. The **My Account** page identifies which account to show using a `id` parameter in the URL (for example `/my-account?id=wiener`), and the application never checks that the logged-in user is actually the owner of that account.

Because the user ID is fully controlled by the client, any logged-in user can view another user's account page, including their API key, just by changing the value of `id`. This is an **IDOR** (Insecure Direct Object Reference).

To solve the lab, obtain the API key of the user `carlos` and submit it as the solution. A valid low-privileged account is provided: `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Log in and look at the account page

Log in with the credentials provided by the lab (`wiener:peter`) and open **My Account**. The URL shows that the application uses a request parameter to decide whose account to display:

```
GET /my-account?id=wiener
```

The page shows the username and the API key of the logged-in user.
<img width="2560" height="1252" alt="Screenshot_2026-11-22_13_53_30" src="https://github.com/user-attachments/assets/92bf43c2-cd67-45be-9cda-6d99ec7c66b6" />


<img width="2560" height="1252" alt="Screenshot_2026-11-22_13_52_21" src="https://github.com/user-attachments/assets/940420a6-2f27-4ac6-ab5c-b58c2ba0b83a" />


---

## 🚀 Exploitation

### Step 2: Change the `id` parameter to `carlos`

Edit the URL in the address bar and replace `wiener` with `carlos`:

```
GET /my-account?id=carlos
```

The application does not verify that the session belongs to `carlos`, so it returns carlos's account page, including his API key.

<img width="2560" height="1252" alt="Screenshot_2026-11-22_14_02_40" src="https://github.com/user-attachments/assets/0ecfec86-67a4-4a5e-90f8-6420cf7d7830" />


### Step 3: Submit the API key

Copy carlos's API key, click **Submit solution** on the lab page, and paste the key in.

### Step 4: Confirm the lab is solved

The lab banner flips to **Solved** with the message "Congratulations, you solved the lab!".

<img width="2560" height="1252" alt="Screenshot_2026-11-22_14_02_57" src="https://github.com/user-attachments/assets/8f646343-3502-4e65-8e0a-3bb672671255" />


---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Log in as `wiener:peter` and open My Account | URL contains `?id=wiener` and shows wiener's API key |
| 2 | Change the URL to `/my-account?id=carlos` | carlos's account page and API key are displayed |
| 3 | Submit carlos's API key | Solution accepted |
| 4 | Observe confirmation | "Congratulations, you solved the lab!" |

---

## 🧠 Key Takeaways

### 1. Root cause

The application uses a client-supplied identifier (`id`) to look up the account to display, but never checks that the identifier belongs to the logged-in user. Anything in a URL, parameter, cookie or header can be modified by the user, so it can't be trusted to decide whose data to return.

### 2. Impact

Any logged-in user can read the account data of any other user just by editing the URL. This is **horizontal privilege escalation**: here it exposes other users' API keys, and in a real application it could expose personal data, private messages, or let an attacker take over accounts.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Use the session, not a request parameter** | Take the user's identity from the server-side session instead of an `id` supplied by the client. |
| **Check object ownership on every request** | Verify on the server that the logged-in user is allowed to access the requested record. |
| **Use unpredictable identifiers** | Random IDs (such as GUIDs) make guessing harder, but they must never replace a real authorization check. |
| **Centralize access-control logic** | Enforce authorization in one consistent place (e.g. middleware) instead of ad hoc checks per page. |
| **Deny by default** | Require an explicit, positive authorization check before returning any user's data. |
| **Test for IDOR** | Include tests that log in as one user and try to access another user's resources, expecting a denial. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — User ID controlled by request parameter (lab)](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

## 📸 Screenshots

All screenshots :

1. `01-my-account-id-wiener.png` — My Account page as `wiener`, with `id=wiener` in the URL
2. `02-my-account-id-carlos-api-key.png` — the account page for `carlos` after changing the `id` parameter
3. `03-lab-solved.png` — the lab marked as solved

> 📝 **Author:** Hasan Abu Saber
> 📅 **Date solved:** 2026-11-23
