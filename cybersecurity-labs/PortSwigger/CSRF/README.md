# 🎭 Cross-Site Request Forgery

> Forcing a logged-in victim's browser to send a state-changing request they never intended.

[![Category](https://img.shields.io/badge/PortSwigger-CSRF-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-9-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

CSRF converts any state-changing endpoint without a per-request token into an attack: change email → reset password → account takeover. Modern defences exist but partial implementations are routinely bypassed.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **No defences** | A plain HTML form auto-submitted to the target endpoint. |
| **Token validation depends on method** | Token checked on `POST` but not on `GET`; swap the method. |
| **Token validation when present** | Remove the `csrf` parameter entirely and the server skips validation. |
| **Token not tied to session** | Attacker's own valid token used against the victim. |
| **Token tied to non-session cookie** | Cookie injection via CRLF in a search field pairs the attacker's token. |
| **Token duplicated in cookie** | Double-submit bypassed when the cookie can be set by the attacker. |
| **SameSite bypass** | `SameSite=Lax` bypassed via `_method=POST` override or a `GET` endpoint. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | CSRF vulnerability with no defenses | Apprentice | ⏳ Planned | — |
| 02 | CSRF where token validation depends on request method | Practitioner | ⏳ Planned | — |
| 03 | CSRF where token validation depends on token being present | Practitioner | ⏳ Planned | — |
| 04 | CSRF where token is not tied to user session | Practitioner | ⏳ Planned | — |
| 05 | CSRF where token is tied to non-session cookie | Practitioner | ⏳ Planned | — |
| 06 | CSRF where token is duplicated in cookie | Practitioner | ⏳ Planned | — |
| 07 | SameSite Lax bypass via method override | Practitioner | ⏳ Planned | — |
| 08 | SameSite Strict bypass via client-side redirect | Practitioner | ⏳ Planned | — |
| 09 | SameSite Strict bypass via sibling domain | Practitioner | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Per-request tokens** | Unpredictable, session-bound, single-use CSRF tokens on every state-changing request. |
| **SameSite cookies** | `SameSite=Lax` or `Strict`, plus `Secure` and `HttpOnly`. |
| **Origin / Referer check** | Validate against the expected origin as defence in depth. |
| **Re-authentication** | Require the current password for sensitive actions (email/password change). |
| **Avoid GET for state changes** | All mutations must be `POST`/`PUT`/`DELETE`. |

## 📚 References

- [PortSwigger — CSRF](https://portswigger.net/web-security/csrf)
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
