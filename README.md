# 🛡️ Cybersecurity Labs Portfolio

> A structured, reproducible record of hands-on security work — PortSwigger Web Security Academy labs, TryHackMe rooms, and custom security tooling — built on the way to becoming an **Application Security Engineer**.

[![TryHackMe](https://img.shields.io/badge/TryHackMe-Swoyon-212C42?style=flat&logo=tryhackme)](https://tryhackme.com/p/swoyon)
[![PortSwigger](https://img.shields.io/badge/PortSwigger-Learner-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs](https://img.shields.io/badge/Labs%20completed-16-brightgreen?style=flat)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat)](./LICENSE)

---

## 📊 Progress overview

| Platform | Completed | In progress | Focus |
|----------|:---------:|:-----------:|-------|
| **PortSwigger Web Security Academy** | 10 | 2 | Web app vulnerabilities |
| **TryHackMe** | 5 | 1 | CTF, Linux, networking |
| **Custom Tools & Code Review** | 2 | 1 | Python offsec tooling |

---

## 🗺️ Where to start

| If you want to see… | Go to |
|---|---|
| 🔐 Web application security work | [`PortSwigger/`](./PortSwigger) |
| 🖥️ CTF / Linux / network rooms | [`TryHackMe/`](./TryHackMe) |
| 🐍 Scripts and secure-coding review | [`Custom_Tools/`](./Custom_Tools) |
| ✍️ The write-up template I use | [`TEMPLATES/`](./TEMPLATES) |
| 📏 How to add a new lab | [`HOW_TO_ADD_NEW_LAB.md`](./HOW_TO_ADD_NEW_LAB.md) |

---

## 🕷️ PortSwigger Web Security Academy

All labs are organised **by vulnerability type**, following the official Academy topic taxonomy. The main page stays short on purpose — categories only. Detail lives one click deeper.

| Category | Solved | Planned | Labs |
|----------|:------:|:-------:|------|
| 💉 **SQL Injection** | **6** | 13 | [Browse →](./PortSwigger/SQL-Injection) |
| 🔐 **Authentication** | **4** | 14 | [Browse →](./PortSwigger/Authentication) |
| 🧪 **Cross-Site Scripting (XSS)** | — | 30 | [Browse →](./PortSwigger/XSS-Cross-Site-Scripting) |
| 🔑 **JWT Attacks** | **3** | 8 | [Browse →](./PortSwigger/JWT-Attacks) |
| 📤 **File Upload** | — | 7 | [Browse →](./PortSwigger/File-Upload) |
| 📂 **File Path Traversal** | — | 7 | [Browse →](./PortSwigger/File-Path-Traversal) |
| 💻 **OS Command Injection** | — | 5 | [Browse →](./PortSwigger/OS-Command-Injection) |
| 🚪 **Access Control & IDOR** | — | 12 | [Browse →](./PortSwigger/Access-Control) |
| 🌐 **SSRF** | — | 7 | [Browse →](./PortSwigger/SSRF) |
| 📄 **XXE** | — | 7 | [Browse →](./PortSwigger/XXE) |
| 🎭 **CSRF** | — | 9 | [Browse →](./PortSwigger/CSRF) |
| 🔎 **Information Disclosure** | — | 5 | [Browse →](./PortSwigger/Information-Disclosure) |
| 🧩 **Business Logic** | — | 8 | [Browse →](./PortSwigger/Business-Logic) |

> **10 solved · 132 planned.** Each category page lists its labs, payload toolkit, defences, and roadmap — so this table never has to grow.

### Recently solved

| Lab | Category | Difficulty |
|-----|----------|------------|
| [Username Enumeration via Response Timing](./PortSwigger/Authentication/04-username-enum-response-timing) | Authentication | 🟠 Practitioner |
| [Password Reset Broken Logic](./PortSwigger/Authentication/03-password-reset-broken-logic) | Authentication | 🟢 Apprentice |
| [UNION Attack — Multiple Values in a Single Column](./PortSwigger/SQL-Injection/06-union-single-column-multiple-values) | SQL Injection | 🟠 Practitioner |

---

## 🎯 TryHackMe

| # | Room | Focus | Difficulty | Write-up |
|---|------|-------|------------|----------|
| 01 | Brooklyn Nine Nine | CTF / Linux commands | Easy | [View](./TryHackMe/brooklyn-nine-nine/README.md) |
| 02 | Bolt Room | Web / CTF | Easy | [View](./TryHackMe/bolt-room/README.md) |
| 03 | Hacker Bounty | CTF / Web | Easy | [View](./TryHackMe/hacker-bounty/README.md) |
| 04 | Ignite | Web / CTF | Easy | [View](./TryHackMe/ignite-room/README.md) |
| 05 | Pickle Rick | CTF / Linux privesc | Easy | [View](./TryHackMe/pickle-rick/README.md) |
| 06 | Network Services | SMB / Telnet / FTP / SSH | Medium | 📄 Write-up pending |

---

## 🛠️ Tools & Code Review

| # | Project | Language | What it demonstrates | Status |
|---|---------|----------|----------------------|--------|
| 01 | [Domain to IP](./Custom_Tools/domain_to_ip) | Python | DNS resolution CLI with input validation | ✅ Complete |
| 02 | [Broken Flask API — code review](./Custom_Tools/AppSec%20_code_review/broken-flask-api) | Python / Flask | Vulnerable vs. secure implementation of the same API | ✅ Complete |

---

## 🧠 Skills demonstrated across this repository

| Domain | Evidence |
|---|---|
| **Web exploitation** | UNION-based and boolean SQLi, username enumeration (body + timing oracles), password-reset logic flaws |
| **Tooling** | Burp Suite Proxy / Repeater / Intruder, FoxyProxy, custom Python scripts |
| **Methodology** | Structured recon → exploit → root cause → remediation in every write-up |
| **Secure coding** | Parameterised queries, output encoding, auth hardening, deny-by-default authorisation |
| **Reporting** | Consistent lab format: objective, payloads, impact, mitigation, references |

---

## 📁 Repository structure

```
cybersecurity-labs/
├── README.md                     ← portfolio index (this page)
├── LICENSE
├── HOW_TO_ADD_NEW_LAB.md
├── TEMPLATES/
│   ├── lab-template.md
│   └── category-template.md
├── PortSwigger/
│   ├── README.md                 ← category index + progress bars
│   ├── SQL-Injection/            ← 6 labs
│   ├── Authentication/           ← 4 labs
│   └── XSS-Cross-Site-Scripting/ ← ready for the next lab
├── TryHackMe/                    ← 5 room write-ups
└── Custom_Tools/                 ← Python offsec tooling + code review
```

The layout is deliberately **three levels deep**: portfolio → category → lab. It scales to hundreds of labs without the front page becoming a wall of tables.

---

## 🎓 About me

**Saber Hasan Swoyon** — Software Engineering undergraduate

- 🛡️ Aspiring **Application Security (AppSec) Engineer**
- 🐍 **Stack:** Python · Linux · Networking · Web Security
- 📚 **Currently:** PortSwigger Web Security Academy, working through SQLi → Authentication → XSS → JWT
- 🌏 **Languages:** English · 中文 (HSK4) · বাংলা
- 🎯 **Goal:** MSc in Cybersecurity → AppSec engineering role

## 🛠️ Environment

```
OS:        Kali Linux (VirtualBox)
Browser:   Firefox + FoxyProxy
Proxy:     Burp Suite Community Edition
Editor:    VS Code / Vim
Languages: Python, Bash, SQL
```

---

## 🤝 Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/swoyon)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:swoyon@email.com)

---

> **Disclaimer:** every lab documented here comes from an authorised training platform (PortSwigger Web Security Academy, TryHackMe) or from code I wrote myself. Nothing here was tested against systems I do not own or have written permission to assess.

---

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=16&duration=3000&pause=1000&color=00FF41&center=true&vCenter=true&width=500&lines=Learning+by+doing.;One+lab+at+a+time.;Building+the+future+of+security." alt="Typing SVG" />
</p>
