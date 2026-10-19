# 🔎 Information Disclosure

> Leaking sensitive data through errors, debug pages, backups, headers, and verbose responses.

[![Category](https://img.shields.io/badge/PortSwigger-Information-Disclosure-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-7-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

Info disclosure is rarely dramatic alone but is the reconnaissance engine behind most serious chains: a stack trace reveals the framework, a backup file reveals source, source reveals credentials.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Verbose errors** | Stack traces with file paths, SQL, framework versions. |
| **Debug pages** | `/cgi-bin/phpinfo.php`, `/debug`, Django `DEBUG=True` error pages. |
| **Backup & source files** | `.bak`, `.old`, `.zip`, `.git/`, `robots.txt`, `sitemap.xml`. |
| **Headers & metadata** | `Server`, `X-Powered-By`, `X-Backend-Server`, comments in HTML. |
| **Timing / response differences** | Behavioural side channels that confirm internal state. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | Information disclosure in error messages | Apprentice | ⏳ Planned | — |
| 02 | Information disclosure on debug page | Apprentice | ⏳ Planned | — |
| 03 | Source code disclosure via backup files | Apprentice | ⏳ Planned | — |
| 04 | Authentication bypass via information disclosure | Apprentice | ⏳ Planned | — |
| 05 | Information disclosure in version control history | Practitioner | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Generic errors** | One global handler; log details server-side, return a correlation id to users. |
| **Disable debug in prod** | Debug off by default; fail the build if `DEBUG=True` reaches production. |
| **No backups in webroot** | Deploy artefacts only; block `.git`, `.env`, `*.bak` at the edge. |
| **Minimal headers** | Strip version banners at the proxy. |

## 📚 References

- [PortSwigger — Information disclosure](https://portswigger.net/web-security/information-disclosure)
- [OWASP A05:2021 Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
