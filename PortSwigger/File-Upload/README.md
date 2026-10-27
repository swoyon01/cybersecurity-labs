# 📤 File Upload Vulnerabilities

> Bypassing upload restrictions to achieve remote code execution or overwrite sensitive files.

[![Category](https://img.shields.io/badge/PortSwigger-File-Upload-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-10-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

If an upload is only validated by client-side checks, extension blacklists, or `Content-Type`, an attacker can land a web shell on the server. It is one of the most direct routes from a web bug to full RCE.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **Web shell upload** | Unrestricted `.php`/`.jsp`/`.aspx` upload executed by the web server. |
| **Content-Type bypass** | Validation trusts the multipart `Content-Type` header only. |
| **Extension bypass** | Blacklists defeated with `.php5`, `.phtml`, `.pHp`, trailing dot/space, `%00`, double extensions. |
| **Path traversal in filename** | Filename `../../shell.php` writes outside the upload directory. |
| **Polyglot files** | Valid image header + PHP payload passes magic-byte checks and still executes. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | Remote code execution via web shell upload | Apprentice | ✅ Solved | [View](./01-rce-web-shell-upload/README.md) | |
| 02 | Web shell upload via Content-Type restriction bypass | Apprentice | ⏳ Planned | — |
| 03 | Web shell upload via path traversal | Practitioner | ⏳ Planned | — |
| 04 | Web shell upload via extension blacklist bypass | Practitioner | ⏳ Planned | — |
| 05 | Web shell upload via obfuscated file extension | Practitioner | ⏳ Planned | — |
| 06 | Remote code execution via polyglot web shell upload | Expert | ⏳ Planned | — |
| 07 | Web shell upload via race condition | Expert | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Allowlist, not blacklist** | Validate extension against an allowlist plus real MIME/magic-byte check. |
| **Random filenames** | Generate the stored name server-side; never use the client's filename. |
| **Store outside webroot** | Serve uploaded files through a handler, or from object storage with no execution. |
| **Disable execution** | `php_admin_flag engine off`, `noexec` mounts, separate upload domain. |
| **Size + type limits** | Cap size, reject double extensions, scan with AV. |

## 📚 References

- [PortSwigger — File upload vulnerabilities](https://portswigger.net/web-security/file-upload)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
