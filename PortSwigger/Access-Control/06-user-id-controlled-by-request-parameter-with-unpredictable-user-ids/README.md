# 🔢 Lab: User ID Controlled by Request Parameter, with Unpredictable User IDs

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab has a horizontal privilege escalation vulnerability on the user account page, but this time user accounts are identified by **GUIDs** instead of usernames (for example `/my-account?id=3ae446d1-4a39-4047-8c19-945db5075a64`).

The developers assumed that a long, random identifier can't be guessed, so they skipped the ownership check. The flaw is that the GUIDs are **disclosed elsewhere in the application**: user IDs appear in the links on blog posts that point to each author's profile. An attacker can read carlos's GUID from there and use it to open his account page.

To solve the lab, find the GUID for the user `carlos`, use it to access his account page, and submit his API key as the solution. A valid low-privileged account is provided: `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Log in and look at the account page

Log in with the credentials provided by the lab (`wiener:peter`) and open **My Account**. The URL shows that the application identifies accounts by an unpredictable GUID instead of a username, so simply changing the `id` to `carlos` won't work:

```
GET /my-account?id=<wiener's GUID>
```

<img width="2560" height="1252" alt="Screenshot_2026-11-22_14_13_33" src="https://github.com/user-attachments/assets/adfc6843-9065-4836-b121-c92f7c818f3e" />


### Step 2: Find a blog post written by carlos

Browse the blog posts on the home page until you find one written by `carlos`. Each post shows its author's name as a link.


### Step 3: Read carlos's GUID from the author link

Click on the author name `carlos`. The URL of the page that opens contains his user ID:

```
GET /blogs?userId=<carlos's GUID>
```

Copy the GUID from the URL.

<img width="2560" height="1252" alt="Screenshot_2026-11-22_14_17_12" src="https://github.com/user-attachments/assets/4c9fe20b-37fa-42ef-b525-b93deb706fd4" />


---

## 🚀 Exploitation

### Step 4: Use carlos's GUID to open his account page

Go back to the account page and replace the `id` value with carlos's GUID:

```
GET /my-account?id=<carlos's GUID>
```

The application does not check that the session belongs to this user, so it returns carlos's account page, including his API key.

### Step 5: Submit the API key

Copy carlos's API key, click **Submit solution** on the lab page, and paste the key in. The lab banner flips to **Solved** with the message "Congratulations, you solved the lab!".

<img width="2560" height="1252" alt="Screenshot_2026-11-22_14_17_56" src="https://github.com/user-attachments/assets/b74114de-923a-47ad-9e6c-94c5707ced0a" />


---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Log in as `wiener:peter` and open My Account | URL contains wiener's GUID, not a guessable name |
| 2 | Browse blog posts and find one written by `carlos` | Author name is shown as a link |
| 3 | Click carlos's name and read the URL | carlos's GUID is disclosed in `?userId=` |
| 4 | Use the GUID in `/my-account?id=<GUID>` | carlos's account page and API key are displayed |
| 5 | Submit carlos's API key | "Congratulations, you solved the lab!" |

---

## 🧠 Key Takeaways

### 1. Root cause

The application still has the same flaw as the previous lab: it uses a client-supplied identifier to decide whose account to show and never checks that it belongs to the logged-in user. Switching to GUIDs only made the IDs harder to guess; it did not add an access control check. The GUIDs were also exposed in other parts of the app (the blog author links), so an attacker could simply look them up.

### 2. Impact

Any logged-in user can read another user's account data once they obtain that user's identifier. This is **horizontal privilege escalation** (IDOR): here it exposes other users' API keys, and in a real application it could expose personal data, private messages, or let an attacker take over accounts.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Check object ownership on every request** | Verify on the server that the logged-in user is allowed to access the requested record, no matter how the ID looks. |
| **Use the session, not a request parameter** | Take the user's identity from the server-side session instead of an `id` supplied by the client. |
| **Don't treat unpredictable IDs as security** | GUIDs make guessing hard, but they must never replace a real authorization check. |
| **Avoid leaking internal identifiers** | Don't expose user IDs in public pages and links unless it is necessary. |
| **Centralize access-control logic** | Enforce authorization in one consistent place (e.g. middleware) instead of ad hoc checks per page. |
| **Test for IDOR** | Include tests that log in as one user and try to access another user's resources, expecting a denial. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — User ID controlled by request parameter, with unpredictable user IDs (lab)](https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

## 📸 Screenshots

All screenshots :

1. `01-my-account-wiener-guid.png` — My Account page as `wiener`, with a GUID in the URL
2. `02-blog-post-by-carlos.png` — a blog post written by `carlos`
3. `03-carlos-guid-in-url.png` — carlos's GUID disclosed in the `userId` parameter
4. `04-lab-solved-carlos-api-key.png` — carlos's account page with his API key and the lab marked as solved

> 📝 **Author:** Hasan Abu Saber
> 📅 **Date solved:** 2026-11-23
