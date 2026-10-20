# 🧩 Business Logic Vulnerabilities

> Abusing the intended workflow of an application rather than a technical flaw in it.

[![Category](https://img.shields.io/badge/PortSwigger-Business-Logic-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-12-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

Logic bugs cannot be found by scanners because the code works exactly as designed — the design is wrong. They usually map directly to money: negative quantities, discount stacking, workflow reordering.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Client-side trust** | Price and quantity validated in JS only — tamper the request. |
| **Negative values / integer abuse** | Negative quantity produces a credit instead of a charge. |
| **Flow bypass** | Skip a required step: pay after shipping, or confirm without verifying. |
| **Rule stacking** | Apply the same coupon repeatedly, combine mutually exclusive rules. |
| **Dual-use endpoints** | Admin-grade functionality reachable by a normal role. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | Excessive trust in client-side controls | Apprentice | ⏳ Planned | — |
| 02 | High-level logic vulnerability | Apprentice | ⏳ Planned | — |
| 03 | Inconsistent security controls | Apprentice | ⏳ Planned | — |
| 04 | Flawed enforcement of business rules | Apprentice | ⏳ Planned | — |
| 05 | Low-level logic flaw | Practitioner | ⏳ Planned | — |
| 06 | Inconsistent handling of exceptional input | Practitioner | ⏳ Planned | — |
| 07 | Weak isolation on dual-use endpoint | Practitioner | ⏳ Planned | — |
| 08 | Insufficient workflow validation | Practitioner | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Server-side truth** | Recalculate price, totals and eligibility on the server for every request. |
| **State machine** | Model the workflow explicitly; reject messages out of order. |
| **Domain invariants** | Assert quantity > 0, total ≥ 0, coupon single-use, at the data layer. |
| **Threat modelling** | Walk the business flow end-to-end with an attacker's goals in mind. |

## 📚 References

- [PortSwigger — Business logic vulnerabilities](https://portswigger.net/web-security/logic-flaws)
- [OWASP WSTG — Business Logic Testing](https://owasp.org/www-project-web-security-testing-guide/)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
