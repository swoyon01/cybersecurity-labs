# 🧪 XSS — Cross-Site Scripting

> Client-side code injection — running JavaScript in a victim's browser through reflected, stored, and DOM-based sinks.

[![Category](https://img.shields.io/badge/PortSwigger-XSS-Cross-Site-Scripting-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-30-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

XSS is one of the most common web vulnerabilities. It bypasses the Same-Origin Policy and lets an attacker read data the victim can read, act as the victim, and hijack sessions. It is the standard entry point for CSRF-bypass and account-takeover chains.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Reflected XSS** | Payload is echoed from the current HTTP request — usually a search or error parameter. |
| **Stored XSS** | Payload is persisted server-side (comments, profiles, filenames) and fires for every viewer. |
| **DOM-based XSS** | Payload flows through client-side JS sinks such as `innerHTML`, `document.write`, `eval`, `location`. |
| **Context breakouts** | Breaking out of HTML attributes, `<script>` blocks, template strings, JSON and `href`/`javascript:` contexts. |
| **XSS chains** | Stealing cookies, bypassing CSRF tokens, chaining with CORS misconfig or file upload. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | Reflected XSS into HTML context with nothing encoded | Apprentice | ⏳ Planned | — |
| 02 | Stored XSS into HTML context with nothing encoded | Apprentice | ⏳ Planned | — |
| 03 | DOM XSS in `document.write` sink using source `location.search` | Apprentice | ⏳ Planned | — |
| 04 | DOM XSS in `innerHTML` sink using source `location.search` | Apprentice | ⏳ Planned | — |
| 05 | XSS into attribute with angle brackets HTML-encoded | Apprentice | ⏳ Planned | — |
| 06 | Exploiting cross-site scripting to steal cookies | Practitioner | ⏳ Planned | — |
| 07 | Exploiting XSS to bypass CSRF defenses | Practitioner | ⏳ Planned | — |
| 08 | Reflected XSS with event handlers and `href` attributes blocked | Expert | ⏳ Planned | — |
| 09 | Stored XSS into `onclick` event with angle brackets and quotes encoded | Expert | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Output encoding** | Context-aware encoding (HTML, attribute, JS, URL) at the sink — not on input. |
| **CSP** | A strict `Content-Security-Policy` with nonces removes most script-injection impact. |
| **Framework escaping** | React/Angular/Vue auto-escape; treat `dangerouslySetInnerHTML` / `v-html` as a review flag. |
| **Trusted Types** | Sinks refuse strings, eliminating DOM XSS by design. |
| **HttpOnly cookies** | Limits session theft impact (does not fix XSS itself). |

## 📚 References

- [PortSwigger — Cross-site scripting](https://portswigger.net/web-security/cross-site-scripting)
- [PortSwigger XSS cheat sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
