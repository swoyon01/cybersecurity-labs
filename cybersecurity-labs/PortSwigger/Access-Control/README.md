# 🚪 Access Control & IDOR

> Broken authorization — vertical (role) and horizontal (object-level) privilege escalation.

[![Category](https://img.shields.io/badge/PortSwigger-Access-Control-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-14-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

Access control is the #1 category in the OWASP Top 10 (A01: Broken Access Control). Most real-world bug-bounty payouts come from IDOR: a user changing `id=123` to `id=124` and reading someone else's data.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Vertical escalation** | Reaching admin functionality as a normal user — hidden paths, role params, header trust. |
| **Horizontal escalation / IDOR** | Accessing another user's objects by changing an identifier. |
| **Parameter-based** | `role=admin`, `isAdmin=true`, `X-Original-URL` headers trusted by the front-end. |
| **Method & path tricks** | `POST` vs `GET`, `/admin` vs `/ADMIN`, trailing slash, `..;/`. |
| **Referer-based checks** | Control relies on the `Referer` header, which is attacker-controlled. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | Unprotected admin functionality | Apprentice | ⏳ Planned | — |
| 02 | Unprotected admin functionality with unpredictable URL | Apprentice | ⏳ Planned | — |
| 03 | User role controlled by request parameter | Apprentice | ⏳ Planned | — |
| 04 | User role can be modified in user profile | Apprentice | ⏳ Planned | — |
| 05 | User ID controlled by request parameter | Apprentice | ⏳ Planned | — |
| 06 | User ID controlled by request parameter, with unpredictable user IDs | Apprentice | ⏳ Planned | — |
| 07 | User ID controlled by request parameter with password disclosure | Apprentice | ⏳ Planned | — |
| 08 | Insecure direct object references | Apprentice | ⏳ Planned | — |
| 09 | URL-based access control can be circumvented | Practitioner | ⏳ Planned | — |
| 10 | Method-based access control can be circumvented | Practitioner | ⏳ Planned | — |
| 11 | User ID controlled by request parameter with data leakage in redirect | Practitioner | ⏳ Planned | — |
| 12 | Multi-step process with no access control on one step | Practitioner | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Deny by default** | Every endpoint requires an explicit authorization decision. |
| **Server-side ownership checks** | Query objects scoped to the session user: `WHERE id=? AND owner_id=?`. |
| **Centralised policy** | Enforce in one middleware/policy layer, not per-view ad hoc checks. |
| **Never trust the client** | Role, user id and hidden URL come from the session, not the request. |
| **Test with two accounts** | A second low-privileged account is the core IDOR test. |

## 📚 References

- [PortSwigger — Access control](https://portswigger.net/web-security/access-control)
- [OWASP A01:2021 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
