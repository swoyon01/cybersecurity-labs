# 🔐 Authentication

> Breaking login, session and account-recovery mechanisms — from username enumeration to full account takeover.

[![Category](https://img.shields.io/badge/PortSwigger-Authentication-FF6633?style=flat)](https://portswigger.net/web-security/authentication)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-4-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-14-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

Authentication decides who you are. Every flaw here is a direct path to account takeover: an enumeration oracle that hands over valid usernames, a rate-limit-free login form, a reset token that is not bound to its user, or a 2FA step that can simply be skipped.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Username enumeration** | Response body, status code, or timing reveals whether an account exists. |
| **Credential brute force** | No lockout / no rate limit — especially with a known username and a small password list. |
| **Broken brute-force protection** | IP-based lockout bypassed with `X-Forwarded-For`, or reset by a successful login. |
| **Logic flaws** | Reset token not tied to user, reusable, predictable, or validated client-side. |
| **2FA bypass** | Verification step skippable, brute-forceable, or the account is fully logged in before 2FA. |
| **Session flaws** | Session stays valid after password change; cookie not rotated on login (fixation). |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|-----|------------|--------|----------|
| 01 | Username enumeration via different responses | 🟢 Apprentice | ✅ Solved | [View](./01-username-enum-different-responses/README.md) |
| 02 | Username enumeration via subtly different responses | 🟢 Apprentice | ✅ Solved | [View](./02-username-enum-subtly-different-responses/README.md) |
| 03 | Password reset broken logic | 🟢 Apprentice | ✅ Solved | [View](./03-password-reset-broken-logic/README.md) |
| 04 | Username enumeration via response timing | 🟠 Practitioner | ✅ Solved | [View](./04-username-enum-response-timing/README.md) |
| 05 | 2FA simple bypass | 🟢 Apprentice | ⏳ Planned | — |
| 06 | Password reset poisoning via middleware | 🟠 Practitioner | ⏳ Planned | — |
| 07 | Password brute-force via password change | 🟠 Practitioner | ⏳ Planned | — |
| 08 | Broken brute-force protection, multiple credentials per request | 🟠 Practitioner | ⏳ Planned | — |
| 09 | Broken brute-force protection, IP block | 🟠 Practitioner | ✅ Solved | [View](./05-broken-bruteforce-ip-block/README.md)  |
| 10 | 2FA broken logic | 🟠 Practitioner | ⏳ Planned | — |
| 11 | 2FA bypass using a brute-force attack | 🔴 Expert | ⏳ Planned | — |
| 12 | Brute-forcing a stay-logged-in cookie | 🟠 Practitioner | ⏳ Planned | — |
| 13 | Offline password cracking | 🟠 Practitioner | ⏳ Planned | — |
| 14 | Authentication bypass via encryption oracle | 🔴 Expert | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

## 🔬 Techniques used in these write-ups

```http
POST /login HTTP/2
Host: TARGET

username=wiener&password=peter          # baseline
username=alice&password=peter           # "Invalid username"  -> alice does not exist
username=carlos&password=peter          # "Incorrect password" -> carlos exists
```

| Technique | How it shows up |
|---|---|
| **Status code oracle** | `200` for valid user, `401` for invalid — trivially enumerable. |
| **Subtle body oracle** | One character of difference, or a trailing typo — needs a diffing proxy. |
| **Timing oracle** | Valid username triggers a slow password hash (~1s) even when the password is wrong. |
| **Rate-limit bypass** | Rotate `X-Forwarded-For`, or keep the counter at zero by interleaving a valid login. |

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Uniform responses** | Identical body, status code and timing for unknown user vs wrong password. |
| **Dummy hash** | Always run a password hash (Argon2id/bcrypt) even when the user does not exist. |
| **Rate limiting + lockout** | Per-account **and** per-IP, server-side, with exponential backoff. |
| **Bound, single-use reset tokens** | Token tied to the user, short TTL, invalidated on use, delivered out-of-band. |
| **2FA enforcement server-side** | The session must stay in a "pre-2FA" state until verification succeeds. |
| **MFA + passkeys** | Phishing-resistant factors where possible; never treat 2FA as optional per-request. |
| **Rotate session on login** | New session ID on privilege change; invalidate all sessions on password change. |

## 📚 References

- [PortSwigger — Authentication](https://portswigger.net/web-security/authentication)
- [PortSwigger — Password-based authentication labs](https://portswigger.net/web-security/authentication/password-based)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP A07:2021 Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
