# 🧬 04 Lab: User Role Can Be Modified in User Profile

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile)
> **Category:** Access control vulnerabilities
> **Difficulty:** 🟢 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab has an admin panel at `/admin`, which is only accessible to logged-in users with a `roleid` of `2`. The application lets users update their email address through a JSON request, and the server's response includes the user's `roleid`.

The server also accepts a `roleid` field in the incoming update request and applies it to the user's profile without checking whether the user is allowed to change it. This is a form of **mass assignment**: the client can set fields it should never control.

To solve the lab, access the admin panel and use it to delete the user `carlos`. A valid low-privileged account is provided: `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Log in as the low-privileged user

Log in with the credentials provided by the lab (`wiener:peter`). The **My Account** page shows an email update form.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_52_05" src="https://github.com/user-attachments/assets/b096b6ad-ac7f-4fb2-ad41-c1a406bfd9f7" />


### Step 2: Try to access `/admin`

Browse directly to `/admin` as `wiener`:

```
GET /admin
```

The application denies access because the user does not have the admin role.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_17_54_59" src="https://github.com/user-attachments/assets/0af7fb8c-bc27-40ac-9c32-f7643c9472c9" />


### Step 3: Intercept the email update request

With Burp Suite running, submit the **Update email** form and look at the request and response in the HTTP history:

```
POST /my-account/change-email
Content-Type: application/json

{"email":"test@test.com"}
```

The response includes the user's role, which tells us how the application tracks privileges:

```
{"username":"wiener","email":"test@test.com","roleid":1}
```

<img width="2559" height="1251" alt="Screenshot_2026-11-18_18_31_15" src="https://github.com/user-attachments/assets/3bbd5555-c010-4f77-a5c5-b1d313921a8f" />


---

## 🚀 Exploitation

### Step 4: Inject `roleid` into the request

Send the request to **Burp Repeater** and add a `roleid` field with the value `2` to the JSON body:

```
POST /my-account/change-email
Content-Type: application/json

{"email":"admin@example.com","roleid":2}
```

The server accepts the extra field, and the response now shows `"roleid":2`. The account has been promoted to administrator.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_18_35_00" src="https://github.com/user-attachments/assets/17e424a5-e2cb-44e3-a886-ce6d72b2c78a" />


### Step 5: Access the admin panel

Browse to `/admin` again. The panel now loads and shows a list of users (`wiener`, `carlos`), each with a **Delete** link.

<img width="2559" height="1251" alt="Screenshot_2026-11-18_18_45_03" src="https://github.com/user-attachments/assets/44b13b86-41a0-427b-b3c0-02dac5c3c67f" />


### Step 6: Delete the `carlos` user

Click **Delete** next to `carlos`. The page confirms `User deleted successfully!`, `carlos` is removed from the Users list, and the lab banner flips to **Solved**

<img width="2559" height="1251" alt="Screenshot_2026-11-18_18_45_13" src="https://github.com/user-attachments/assets/0d36e574-e451-48cc-b187-7bcb194c0199" />


---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Log in as `wiener:peter` | Logged in as a normal user |
| 2 | Browse to `/admin` | Access denied |
| 3 | Intercept the email update request | Response reveals `"roleid":1` |
| 4 | Resend the request with `"roleid":2` added | Response shows `"roleid":2`, the user is now an admin |
| 5 | Browse to `/admin` | Admin panel loads with the user list |
| 6 | Click **Delete** next to `carlos` | "User deleted successfully!" and lab marked as solved |

---

## 🧠 Key Takeaways

### 1. Root cause

The server binds incoming request data directly onto the user object, including sensitive fields like `roleid` that the client should never be able to set (mass assignment). The role is changed with no check that the requester is authorized to change it.

### 2. Impact

Any logged-in user can escalate to administrator by adding one extra field to a normal request. This is **vertical privilege escalation**: here it allows deleting any user, and in a real application it could expose user management, configuration, and sensitive data.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Allowlist the fields a user can update** | Only accept explicitly permitted fields (e.g. `email`) and ignore everything else. |
| **Never bind request data directly to sensitive attributes** | Use DTOs or explicit mapping instead of automatic binding of all request fields. |
| **Protect role changes with a separate authorization check** | Only an administrator should be able to change a user's role, enforced server-side. |
| **Enforce access control on every request** | Verify the user's role on the server each time an admin endpoint is called. |
| **Don't expose internal fields unnecessarily** | Avoid returning fields like `roleid` in responses, which hints at what can be tampered with. |
| **Test for privilege escalation** | Include tests that try to set privileged fields as a low-privileged user and expect a denial. |

---

## 📚 References

- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
- [PortSwigger — User role can be modified in user profile (lab)](https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

## 📸 Screenshots

All screenshots :

1. `01-logged-in-as-wiener.png` — logged in as `wiener` on the My Account page
2. `02-admin-access-denied.png` — `/admin` denies access to a normal user
3. `03-burp-change-email-roleid-1.png` — the change-email request and the `roleid: 1` response in Burp
4. `04-burp-repeater-roleid-2.png` — Repeater with `roleid` set to `2` and the response confirming it
5. `05-admin-panel-users-list.png` — the admin panel reached after the role change
6. `06-lab-solved-carlos-deleted.png` — `carlos` deleted and the lab marked as solved

> 📝 **Author:** Saber Hasan Swoyon.

