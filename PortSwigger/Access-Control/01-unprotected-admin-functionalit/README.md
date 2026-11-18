# 01 🔓 Lab: Unprotected Admin Functionality

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab has an unprotected admin panel. The application assumes that because the admin page's URL isn't linked from anywhere in the UI, nobody will find it — a classic case of **"security through obscurity."** The URL is, however, disclosed in the site's `robots.txt` file, which is meant to tell search engine crawlers what *not* to index, but ends up handing an attacker the exact path to look for.

Because the admin panel itself performs no authentication or access-control check, simply knowing (or guessing) the URL is enough to reach it as an anonymous, unauthenticated user.

To solve the lab, find the admin panel and use it to delete the user `carlos`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Look at the lab in its starting state

The lab loads as an ordinary shop front end. There is no visible link to any admin or management area anywhere in the UI.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_16_54_34" src="https://github.com/user-attachments/assets/66ab2433-c9a8-4b1f-9b48-7edaebc6cc6b" />


### Step 2: Check `robots.txt` for hidden paths

`robots.txt` is a public file that any visitor (not just search engines) can request. Developers sometimes use it to tell crawlers to skip sensitive-looking paths, which has the side effect of listing exactly those paths for anyone who checks.

```
GET /robots.txt
```

```
User-agent: *
Disallow: /administrator-panel
```

This discloses a hidden path, `/administrator-panel`, that isn't linked from anywhere else on the site.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_16_55_00" src="https://github.com/user-attachments/assets/dc8318b7-24fa-4e9f-8ffd-a4e8f3b89e3c" />


---

## 🚀 Exploitation

### Step 3: Browse directly to the disclosed admin panel

Navigate straight to the disclosed path as the current (unauthenticated/low-privileged) session:

```
GET /administrator-panel
```

The panel loads with no login prompt and no access-control check at all, exposing a full user list (`wiener`, `carlos`) each with a **Delete** action.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_16_55_36" src="https://github.com/user-attachments/assets/a01ccd56-aca8-4a8e-b13b-9dce51179966" />


### Step 4: Delete the `carlos` user

Click **Delete** next to `carlos`. The application performs no authorization check on this action either — it simply carries it out.

### Step 5: Confirm the lab is solved

The page confirms `User deleted successfully!`, `carlos` is removed from the Users list, and the lab banner flips to **Solved**.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_16_55_47" src="https://github.com/user-attachments/assets/62d060ce-4084-48be-a01f-7cce299d15f8" />

---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Load the site normally | No link to any admin area in the UI |
| 2 | Request `/robots.txt` | `Disallow: /administrator-panel` — the hidden path is disclosed |
| 3 | Browse directly to `/administrator-panel` | Admin panel loads with no authentication or authorization check |
| 4 | Click **Delete** next to `carlos` | Action is carried out with no access-control check |
| 5 | Observe confirmation | "User deleted successfully!" and lab marked as solved |

---

## 🧠 Key Takeaways

### 1. Root cause

The admin functionality relies entirely on the obscurity of its URL rather than an actual access-control check (e.g. verifying the requester is logged in and holds an admin role). Not linking a page in the UI is not a security control — any path that is reachable at all, even indirectly disclosed via `robots.txt`, directory listings, JS bundles, sitemap files, or simple guessing, will eventually be found.

### 2. Impact

Any unauthenticated visitor who discovers the URL gets full administrative capability — here, the ability to delete any user account. In a real application, admin panels typically expose far more sensitive actions (user management, configuration, financial data), so this class of bug can lead to full compromise of the application.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Enforce access control server-side, on every request** | Check authentication and role/permission on the admin endpoint itself, not just by hiding its link in the UI. |
| **Never rely on security through obscurity** | An unlinked or "secret" URL is not a security boundary — assume any path can be discovered. |
| **Be careful what `robots.txt` discloses** | Don't use `robots.txt` to "hide" sensitive paths; it is publicly readable and often the first thing an attacker checks. |
| **Centralize access-control logic** | Use a consistent, centrally enforced authorization mechanism (e.g. middleware/framework guard) rather than per-page, ad hoc checks that are easy to forget. |
| **Principle of least privilege + deny by default** | Require an explicit, positive authorization check before granting access to any sensitive functionality. |
| **Monitor and test for forced browsing** | Include automated checks/tests that attempt to access privileged endpoints without authentication as part of the test suite. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — Unprotected admin functionality (lab)](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

## 📸 Screenshots

All screenshots live in [`./screenshots`](./screenshots), in the order referenced above:

1. `01-lab-start-shop-page.png` — the lab in its starting, unsolved state
2. `02-robots-txt-disclosure.png` — `robots.txt` disclosing the `/administrator-panel` path
3. `03-admin-panel-accessed.png` — the admin panel reached directly, with no access-control check
4. `04-lab-solved-carlos-deleted.png` — `carlos` deleted and the lab marked as solved

> 📝 **Author:** Hasan Abu Saber
> 📅 **Date solved:** 2026-11-18
