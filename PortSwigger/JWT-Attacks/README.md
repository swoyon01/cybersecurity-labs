# 🔑 JWT Attacks

> Attacking JSON Web Token implementations — broken signature verification, weak keys, and header injection.

[![Category](https://img.shields.io/badge/PortSwigger-JWT-Attacks-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-12-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

JWTs are the default session mechanism for APIs and SPAs. A single implementation mistake (unverified signature, `none` algorithm accepted, weak HMAC secret, injectable `jku`/`kid`) turns a signed token into an attacker-forgeable admin credential.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Unverified signature** | Server decodes the token but never calls `verify()` — any payload with the same `alg` is accepted. |
| **`none` algorithm** | Server trusts the header's `alg` and accepts an unsigned token when set to `none`. |
| **Weak HMAC secret** | HS256 secret crackable offline with a wordlist (`hashcat -m 16500`). |
| **Algorithm confusion** | RS256 public key abused as an HS256 secret. |
| **Header injection** | `jwk`, `jku`, `kid` are attacker-controllable — SSRF, path traversal, SQLi through `kid`. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | JWT authentication bypass via unverified signature | Apprentice | ✅ Solved | [View](./01-jwt-unverified-signature/README.md) |
| 02 | JWT authentication bypass via flawed signature verification | Apprentice | ✅ Solved | [View](./02-jwt-flawed-signature/README.md) |
| 03 | JWT authentication bypass via weak signing key | Practitioner | ✅ Solved | [View](./03-jwt-weak-signing-key/README.md) |
| 04 | JWT authentication bypass via `jwk` header injection | Practitioner | ⏳ Planned | — |
| 05 | JWT authentication bypass via `jku` header injection | Practitioner | ⏳ Planned | — |
| 06 | JWT authentication bypass via `kid` header path traversal | Practitioner | ⏳ Planned | — |    
| 07 | JWT authentication bypass via algorithm confusion | Expert | ⏳ Planned | — |
| 08 | JWT authentication bypass via algorithm confusion with no exposed key | Expert | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Pin the algorithm** | Verify against a server-side allowlist of algorithms; never trust the header's `alg`. |
| **Always verify** | Use a maintained library and call `verify()`, not `decode()`. |
| **Strong secrets** | ≥256-bit random keys for HS256; rotate them. |
| **Fixed key lookup** | Never use `kid`/`jku` directly in file paths or URLs — map to a fixed keyset. |
| **Short-lived tokens** | Short `exp` plus refresh-token rotation limits replay. |

## 📚 References

- [PortSwigger — JWT attacks](https://portswigger.net/web-security/jwt)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [jwt_tool](https://github.com/ticarpi/jwt_tool)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
