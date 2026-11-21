# 🍪 03 Lab: User Role Controlled by Request Parameter

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab has an admin panel at `/admin`, which is meant to be reachable only by administrators. The application decides whether a user is an admin using a **user-controllable cookie** named `Admin` (`Admin=false` for normal users, `Admin=true` for admins).

Because the role is stored in a value the client fully controls, and the server trusts it without checking it against anything server-side, any user can promote themselves to administrator just by editing the cookie.

To solve the lab, access the admin panel and use it to delete the user `carlos`. A valid low-privileged account is provided: `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Log in as the low-privileged user

Log in with the credentials provided by the lab (`wiener:peter`). The **My Account** page confirms the session is for the normal user `wiener`.


### Step 2: Try to access `/admin`

Browse directly to `/admin` as `wiener`:

```
GET /admin
```

The application blocks the request and responds with:

```
Admin interface only available if logged in as an administrator
```

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_35_47" src="https://github.com/user-attachments/assets/f649f293-fd75-4d61-9b4c-8789f1462e63" />


### Step 3: Inspect the cookies

Open the browser developer tools (**F12 → Storage → Cookies**). Besides the `session` cookie, there is a suspicious second cookie:

```
Admin=false
```

The server is using this client-side value to decide whether the user is an administrator.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_35_58" src="https://github.com/user-attachments/assets/28035375-814b-4292-9f63-cbac2408d509" />


---

##  Exploitation

### Step 4: Tamper with the `Admin` cookie

Double-click the cookie value in the Storage tab and change it from `false` to `true`:

```
Admin=true
```

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_36_59" src="https://github.com/user-attachments/assets/f9fe3aec-abc7-4b77-ac1f-ac8c8fe64573" />


### Step 5: Access the admin panel

Reload the site and browse to `/admin` again. This time the server trusts the modified cookie and shows the admin panel with a list of users (`wiener`, `carlos`), each with a **Delete** link.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_41_28" src="https://github.com/user-attachments/assets/9b4dd323-7f2a-49c4-a297-ebbeb0ae00db" />


### Step 6: Delete the `carlos` user

Click **Delete** next to `carlos`. The page confirms `User deleted successfully!`, `carlos` is removed from the Users list, and the lab banner flips to **Solved**.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_41_40" src="https://github.com/user-attachments/assets/c161a95a-1c74-442c-9899-3edde5a27b85" />


---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Log in as `wiener:peter` | Logged in as a normal user |
| 2 | Browse to `/admin` | Access denied: "Admin interface only available if logged in as an administrator" |
| 3 | Inspect cookies in dev tools | Finds `Admin=false` |
| 4 | Change the cookie to `Admin=true` | Server now treats the session as an administrator |
| 5 | Reload and browse to `/admin` | Admin panel loads with the user list |
| 6 | Click **Delete** next to `carlos` | "User deleted successfully!" and lab marked as solved |

---

## 🧠 Key Takeaways

### 1. Root cause

The application stores the user's privilege level in a cookie (`Admin=true/false`) and trusts it on every request. Anything stored client-side (cookies, hidden form fields, URL parameters, headers) can be freely modified by the user, so it must never be the source of truth for authorization decisions.

### 2. Impact

Any authenticated (or even unauthenticated) user can escalate to administrator with a one-second edit in the browser, gaining full admin functionality. This is **vertical privilege escalation**: here it allows deleting any user, and in a real application it could expose user management, configuration, and sensitive data.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Keep roles server-side** | Store the user's role/permissions in the server-side session or database, never in a client-controlled value. |
| **Enforce access control on every request** | Verify the user's role on the server each time an admin endpoint is called. |
| **Never trust client-supplied data for authorization** | Treat cookies, parameters, and hidden fields as untrusted input. |
| **Sign or encrypt any client-side state** | If state must live in a cookie, use a signed/encrypted token (e.g. a properly validated JWT) so tampering is detected. |
| **Deny by default** | Require an explicit, positive authorization check before granting access to sensitive functionality. |
| **Test for privilege escalation** | Include tests that access privileged endpoints as a low-privileged user and expect a denial. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — User role controlled by request parameter (lab)](https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---


> 📝 **Author:** Hasan Abu Saber

