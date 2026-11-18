# 2 🔓 Lab: Unprotected Admin Functionality with Unpredictable URL

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality-with-unpredictable-url)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab also has an unprotected admin panel, but this time the URL isn't guessable (e.g. `/admin`) and isn't disclosed in `robots.txt` either — it's randomized per lab instance (e.g. `/admin-ubtpr5`). The developers assumed that because the path can't be guessed or found in `robots.txt`, it's effectively hidden.

However, the page still ships client-side JavaScript that references the admin panel's URL directly — it's just wrapped in a client-side `isAdmin` check that controls whether a link to it is rendered in the UI. The URL itself is still present in the HTML/JS source sent to **every** visitor, logged in or not, because the check only decides whether to *display* a link — it does nothing to protect the endpoint itself.

To solve the lab, find the admin panel's unpredictable URL and use it to delete the user `carlos`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Rule out the obvious paths

Checking `robots.txt` and the page UI for an admin link, like in the previous lab, turns up nothing this time — there's no disclosed path and no visible link anywhere.

### Step 2: View the page source

Since the server must somehow decide whether to show an admin link, the logic for that decision has to live somewhere the browser can read it — the page's own HTML/JS. Viewing the page source (`view-source:`) reveals an inline `<script>` block:

```js
var isAdmin = false;
if (isAdmin) {
    var topLinksTag = document.getElementsByClassName("top-links")[0];
    var adminPanelTag = document.createElement('a');
    adminPanelTag.setAttribute('href', '/admin-ubtpr5');
    adminPanelTag.innerText = 'Admin panel';
    topLinksTag.append(adminPanelTag);
    var pTag = document.createElement('p');
    pTag.innerText = '|';
    topLinksTag.appendChild(pTag);
}
```

Even though `isAdmin` is `false` for this session (so the link never actually renders), the literal admin panel URL — `/admin-ubtpr5` — is sent in plain text to every visitor regardless of role. Access control implemented only on the client side like this leaks the "secret" it's meant to protect.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_05_17" src="https://github.com/user-attachments/assets/3f3e5c1b-7a32-48e5-8404-9d039481ae6d" />


---

## 🚀 Exploitation

### Step 3: Browse directly to the disclosed admin panel

Navigate straight to the URL found in the source, as the current (unauthenticated/low-privileged) session:

```
GET /admin-ubtpr5
```

The panel loads with no login prompt and no server-side access-control check, exposing the full user list (`wiener`, `carlos`) each with a **Delete** action — identical to the previous lab, the only difference was how the URL had to be found.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_04_53" src="https://github.com/user-attachments/assets/6ca1b310-b5f9-4857-93ba-b4a98113fb42" />


### Step 4: Delete the `carlos` user

Click **Delete** next to `carlos`. The server carries out the action with no authorization check.

### Step 5: Confirm the lab is solved

The page confirms `User deleted successfully!`, `carlos` is removed from the Users list, and the lab banner flips to **Solved**.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_05_06" src="https://github.com/user-attachments/assets/978ce6f4-1bf8-4ef2-a98b-4d95f7cf7d4c" />


---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Check `robots.txt` and the UI for an admin link | Nothing disclosed — URL is randomized and unlinked |
| 2 | View the page source (`view-source:`) | Inline JS reveals the hardcoded admin URL (`/admin-ubtpr5`), gated only by a client-side `isAdmin` flag |
| 3 | Browse directly to the leaked URL | Admin panel loads with no authentication or authorization check |
| 4 | Click **Delete** next to `carlos` | Action is carried out with no access-control check |
| 5 | Observe confirmation | "User deleted successfully!" and lab marked as solved |

---

## 🧠 Key Takeaways

### 1. Root cause

Access control was enforced **client-side only** — a JavaScript `isAdmin` flag decides whether to *display* a link, but the server performs no equivalent check when the admin endpoint itself is actually requested. Worse, the "hidden" URL is embedded directly in source sent to every visitor, so even an unguessable path provides no real protection once any client receives the page.

### 2. Impact

Any unauthenticated visitor who reads the page source can recover the admin panel's URL and gain full administrative capability — here, deleting any user account. This is a more realistic variant of the previous lab: even when a path resists blind guessing or isn't listed in `robots.txt`, if it's referenced anywhere in client-delivered code, it is not secret.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Enforce access control server-side, on every request** | Check authentication and role/permission on the admin endpoint itself — never rely on a flag or branch that only runs in the browser. |
| **Never leak sensitive URLs in client-side code** | Don't embed paths, feature flags, or logic for privileged functionality in JS delivered to all users; render links (and define routes) only for authorized users, decided server-side. |
| **Treat all client-side checks as advisory, not security boundaries** | Anything evaluated in the browser (`isAdmin`, feature flags, hidden form fields) can be read or bypassed by the client; it must be re-verified on the server. |
| **Centralize access-control logic** | Use a consistent, centrally enforced authorization mechanism (e.g. middleware/framework guard) rather than per-page, ad hoc checks. |
| **Principle of least privilege + deny by default** | Require an explicit, positive server-side authorization check before granting access to any sensitive functionality. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — Unprotected admin functionality with unpredictable URL (lab)](https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality-with-unpredictable-url)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

## 📸 Screenshots

All screenshots :

1. `01-view-source-admin-url.png` — page source revealing the hardcoded admin panel URL (`/admin-ubtpr5`) in client-side JS
2. `02-admin-panel-not-solved.png` — the admin panel reached directly via the leaked URL, listing `wiener` and `carlos`
3. `03-lab-solved-carlos-deleted.png` — `carlos` deleted and the lab marked as solved

> 📝 **Author:** Hasan Abu Saber
> 📅 **Date solved:** 2026-11-18
