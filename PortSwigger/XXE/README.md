# 📄 XML External Entity Injection

> Abusing XML parser features to read files, perform SSRF, or trigger denial of service.

[![Category](https://img.shields.io/badge/PortSwigger-XXE-FF6633?style=flat)](https://portswigger.net/web-security)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-0-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-8-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

XXE is silently present wherever XML is parsed — SOAP, SAML, DOCX/XLSX, SVG, RSS. A single `<!ENTITY>` can read `/etc/passwd`, hit the metadata endpoint, or exfiltrate data via an external DTD.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **In-band file read** | `SYSTEM "file:///etc/passwd"` reflected in the response. |
| **XXE to SSRF** | `SYSTEM "http://169.254.169.254/..."` — combine with SSRF impact. |
| **Blind XXE** | Out-of-band interaction with Burp Collaborator. |
| **Parameter entities** | `%xxe;` used in an external DTD when general entities are blocked. |
| **Error-based** | Leak file contents inside a parser error message. |
| **XInclude / SVG / DOCX** | Same primitives in different parsers and file formats. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|---|---|---|---|
| 01 | Exploiting XXE using external entities to retrieve files | Apprentice | ⏳ Planned | — |
| 02 | Exploiting XXE to perform SSRF attacks | Apprentice | ⏳ Planned | — |
| 03 | Blind XXE with out-of-band interaction | Practitioner | ⏳ Planned | — |
| 04 | Blind XXE with out-of-band interaction via XML parameter entities | Practitioner | ⏳ Planned | — |
| 05 | Exploiting blind XXE to exfiltrate data using a malicious external DTD | Practitioner | ⏳ Planned | — |
| 06 | Exploiting blind XXE to retrieve data via error messages | Practitioner | ⏳ Planned | — |
| 07 | Exploiting XInclude to retrieve files | Practitioner | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

> Add a lab by copying [`TEMPLATES/lab-template.md`](../../TEMPLATES/lab-template.md) into a new `XX-lab-name/` folder, then tick the row above.

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Disable DTDs** | `XMLConstants.FEATURE_SECURE_PROCESSING`, `disallow-doctype-decl=true`, `resolve_entities=False`. |
| **Disable external entities** | Explicitly turn off external general/parameter entities in the parser. |
| **Prefer JSON / safe parsers** | Use defusedxml, disable XInclude, avoid DocumentBuilder defaults. |
| **Patch libraries** | Old parsers default to permissive — upgrade. |

## 📚 References

- [PortSwigger — XXE](https://portswigger.net/web-security/xxe)
- [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
- [defusedxml](https://github.com/tiran/defusedxml)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
