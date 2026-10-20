# 📂 File Path Traversal

> Breaking out of an intended directory to read or write arbitrary files (`../../etc/passwd`).

[![Category](https://img.shields.io/badge/PortSwigger-File-Path-Traversal-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-8-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

Path traversal leaks source code, credentials, SSH keys and `/etc/passwd`, and often combines with file upload for RCE. Filtering is usually where it fails — not the concept.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Simple traversal** | `?filename=../../../etc/passwd` with no filtering. |
| **Absolute path bypass** | `filename=/etc/passwd` when only relative sequences are blocked. |
| **Non-recursive stripping** | `....//....//` survives a single-pass `../` removal. |
| **URL encoding** | `%2e%2e%2f`, double encoding `%252e%252e%252f`, overlong UTF-8. |
| **Start-of-path validation** | `/var/www/images/../../../etc/passwd` satisfies a `startsWith` check. |
| **Null byte** | `../../../etc/passwd%00.png` against older runtimes. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | File path traversal, simple case | Apprentice | ⏳ Planned | — |
| 02 | File path traversal, traversal sequences blocked with absolute path bypass | Apprentice | ⏳ Planned | — |
| 03 | File path traversal, traversal sequences stripped non-recursively | Apprentice | ⏳ Planned | — |
| 04 | File path traversal, traversal sequences stripped with superfluous URL-decode | Practitioner | ⏳ Planned | — |
| 05 | File path traversal, validation of start of path | Practitioner | ⏳ Planned | — |
| 06 | File path traversal, validation of start of path with absolute path bypass | Practitioner | ⏳ Planned | — |
| 07 | File path traversal, validation of start of path with double URL-decode | Expert | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Canonicalise first** | Resolve the final absolute path, then verify it is inside the allowed base directory. |
| **No user filenames** | Map an opaque ID to a server-side path instead of accepting a name. |
| **Allowlist** | Accept only known filenames / extensions. |
| **Chroot / sandbox** | Constrain the process so traversal cannot reach the OS. |

## 📚 References

- [PortSwigger — Directory traversal](https://portswigger.net/web-security/file-path-traversal)
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
