# 🌐 Server-Side Request Forgery

> Making the server issue requests to internal services, cloud metadata, or arbitrary hosts.

[![Category](https://img.shields.io/badge/PortSwigger-SSRF-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-10-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

SSRF turns an internet-facing app into a proxy into your private network. Against cloud hosts, `169.254.169.254` can hand over IAM credentials — a classic path to full cloud takeover.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Local server** | `stockApi=http://localhost/admin` reaches an internal-only endpoint. |
| **Internal network scan** | Enumerate `192.168.0.0/24` hosts and ports through the parameter. |
| **Blacklist bypass** | `127.1`, `2130706433`, `0x7f000001`, `[::1]`, DNS rebinding, `127.0.0.1.nip.io`. |
| **Allowlist bypass** | Abuse open redirects or `@` confusion: `http://allowed.com@evil.com`. |
| **Blind SSRF** | No response reflected — detect with Burp Collaborator and build an exfil channel. |
| **Cloud metadata** | `http://169.254.169.254/latest/meta-data/iam/security-credentials/`. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | Basic SSRF against the local server | Apprentice | ⏳ Planned | — |
| 02 | Basic SSRF against another back-end system | Apprentice | ⏳ Planned | — |
| 03 | SSRF with blacklist-based input filter | Apprentice | ⏳ Planned | — |
| 04 | SSRF with filter bypass via open redirection | Practitioner | ⏳ Planned | — |
| 05 | Blind SSRF with out-of-band detection | Practitioner | ⏳ Planned | — |
| 06 | SSRF with whitelist-based input filter | Expert | ⏳ Planned | — |
| 07 | Blind SSRF with Shellshock exploitation | Expert | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Allowlist destinations** | Resolve DNS first, then validate the resolved IP against an allowlist. |
| **Block metadata** | Deny link-local `169.254.0.0/16` and loopback unless explicitly required. |
| **No redirects** | Disable following redirects, or re-validate each hop. |
| **Network segmentation** | Egress firewall rules; IMDSv2 with hop limit 1 on AWS. |

## 📚 References

- [PortSwigger — SSRF](https://portswigger.net/web-security/ssrf)
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
