# 💻 OS Command Injection

> Injecting shell metacharacters into a parameter that is passed to a system command.

[![Category](https://img.shields.io/badge/PortSwigger-OS-Command-Injection-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-8-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

Command injection is a direct path to remote code execution with the privileges of the web server. Blind variants are just as dangerous once you can exfiltrate data out-of-band.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Simple / in-band** | Output of the injected command is returned in the HTTP response. |
| **Time-based blind** | `; sleep 10` proves execution when no output is reflected. |
| **Output redirection** | Write results into a web-accessible file: `> /var/www/images/out.txt`. |
| **Out-of-band** | Force the server to call back to Burp Collaborator with `nslookup`/`curl`. |
| **Filter bypass** | `$IFS`, `${IFS}`, newline `%0a`, `||`, `&&`, `%09`, command substitution. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | OS command injection, simple case | Apprentice | ⏳ Planned | — |
| 02 | Blind OS command injection with time delays | Apprentice | ⏳ Planned | — |
| 03 | Blind OS command injection with output redirection | Apprentice | ⏳ Planned | — |
| 04 | Blind OS command injection with out-of-band interaction | Practitioner | ⏳ Planned | — |
| 05 | Blind OS command injection with out-of-band data exfiltration | Practitioner | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Avoid the shell** | Use library APIs (e.g. `subprocess.run([...], shell=False)`) instead of string commands. |
| **Allowlist arguments** | Validate against a strict pattern; reject metacharacters. |
| **Least privilege** | Web process should have no shell access or write permissions. |
| **Sandbox / container** | Drop capabilities, read-only filesystem, egress filtering. |

## 📚 References

- [PortSwigger — OS command injection](https://portswigger.net/web-security/os-command-injection)
- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
