# 🕷️ PortSwigger Web Security Academy

> Every solved lab from the PortSwigger Web Security Academy, organised by vulnerability type using the official Academy topic taxonomy.

[![PortSwigger](https://img.shields.io/badge/Platform-PortSwigger%20Web%20Security%20Academy-FF6633?style=flat&logo=burpsuite&logoColor=white)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-10-brightgreen?style=flat)]()
[![Categories](https://img.shields.io/badge/Categories-13-blue?style=flat)]()

---

## 📊 Progress by category

| # | Category | Solved | Planned | Coverage | Open |
|---|----------|:------:|:-------:|----------|------|
| 01 | **SQL Injection** | 6 | 13 | `██████░░░░░░` | [Browse →](./SQL-Injection) |
| 02 | **Authentication** | 4 | 14 | `████░░░░░░░░` | [Browse →](./Authentication) |
| 03 | **Cross-Site Scripting (XSS)** | 0 | 30 | `░░░░░░░░░░░░` | [Browse →](./XSS-Cross-Site-Scripting) |
| 04 | **JWT Attacks** | 4 | 8 | `██████░░░░░░░` | [Browse →](./JWT-Attacks) |
| 05 | **File Upload** | 1 | 7 | `░░░░░░░░░░░░` | [Browse →](./File-Upload) |
| 06 | **File Path Traversal** | 0 | 7 | `░░░░░░░░░░░░` | [Browse →](./File-Path-Traversal) |
| 07 | **OS Command Injection** | 0 | 5 | `░░░░░░░░░░░░` | [Browse →](./OS-Command-Injection) |
| 08 | **Access Control & IDOR** | 0 | 12 | `░░░░░░░░░░░░` | [Browse →](./Access-Control) |
| 09 | **SSRF** | 0 | 7 | `░░░░░░░░░░░░` | [Browse →](./SSRF) |
| 10 | **XXE** | 0 | 7 | `░░░░░░░░░░░░` | [Browse →](./XXE) |
| 11 | **CSRF** | 0 | 9 | `░░░░░░░░░░░░` | [Browse →](./CSRF) |
| 12 | **Information Disclosure** | 0 | 5 | `░░░░░░░░░░░░` | [Browse →](./Information-Disclosure) |
| 13 | **Business Logic** | 0 | 8 | `░░░░░░░░░░░░` | [Browse →](./Business-Logic) |

**Total: 10 solved · 132 planned**

---

## 🗂️ How this repository is organised

```
PortSwigger/
├── README.md                     ← you are here (category index)
├── SQL-Injection/
│   ├── README.md                 ← category overview + lab table
│   ├── 01-hidden-data-retrieval/
│   │   ├── README.md             ← full walkthrough
│   │   └── screenshots/          ← Burp + browser proof
│   └── 02-login-bypass/ ...
├── Authentication/
└── XSS-Cross-Site-Scripting/ ... (one folder per Academy topic)
```

**Three levels, three purposes**

| Level | File | Purpose |
|---|---|---|
| Portfolio | [`/README.md`](../README.md) | Categories only — stays short no matter how many labs exist |
| Category | `PortSwigger/<Topic>/README.md` | Progress, roadmap, payload toolkit, defences |
| Lab | `PortSwigger/<Topic>/XX-lab-name/README.md` | Objective → recon → payload → screenshots → root cause → fix |

---

## ✍️ Write-up standard

Every lab README contains the same sections, so the collection reads as a coherent methodology rather than a pile of notes:

| Section | What it proves |
|---|---|
| 🎯 Objective | You understood the goal |
| 🔍 Reconnaissance | You can find the injection point, not just follow a spoiler |
| 🚀 Exploitation | Payload + transformed query, step by step |
| 📸 Proof of Concept | Screenshots of request, response and solved banner |
| 🧠 Root Cause | Code-level reason the vulnerability exists |
| 🛡️ Remediation | The control that would have prevented it |
| 📚 References | PortSwigger topic, OWASP cheat sheet |

Template: [`TEMPLATES/lab-template.md`](../TEMPLATES/lab-template.md)

---

## 🧭 Difficulty legend

| Badge | Level | Meaning |
|---|---|---|
| 🟢 | Apprentice | The vulnerability in its purest form |
| 🟠 | Practitioner | Realistic defences to bypass |
| 🔴 | Expert | Chained or heavily filtered exploitation |

---

> **Disclaimer:** all labs documented here are from the deliberately vulnerable PortSwigger Web Security Academy. Techniques are shared for educational purposes only and must never be used against systems without written authorisation.
