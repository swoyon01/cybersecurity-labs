# 📏 How to add a new lab

The repository has three levels. **You only ever touch the deepest one** — the lab folder — plus one row in its category table.

```
README.md                        ← portfolio (categories only, never needs editing)
PortSwigger/<Category>/README.md ← category table (one row per lab)
PortSwigger/<Category>/XX-name/  ← the lab itself
```

---

## 1. Create the lab folder

Pick the category, then use a two-digit prefix so labs sort in learning order.

```bash
cd cybersecurity-labs
git pull

# example: a new XSS lab
mkdir -p "PortSwigger/XSS-Cross-Site-Scripting/01-reflected-xss-html-context/screenshots"
```

## 2. Copy the template

```bash
cp TEMPLATES/lab-template.md \
   "PortSwigger/XSS-Cross-Site-Scripting/01-reflected-xss-html-context/README.md"
```

Then fill in: objective → recon → payload → screenshots → root cause → remediation.

## 3. Add screenshots

```
01-reflected-xss-html-context/
├── README.md
└── screenshots/
    ├── 01-baseline-request.png
    ├── 02-payload-injected.png
    └── 03-lab-solved.png
```

Reference them relatively so they render on GitHub:

```markdown
![Baseline request](./screenshots/01-baseline-request.png)
```

> Keep images under ~1 MB (PNG for Burp, JPEG for browser). Crop to the relevant pane — full-desktop screenshots with tiny text look unprofessional in a portfolio.

## 4. Update the category table

Open `PortSwigger/<Category>/README.md` and change the matching row:

```diff
- | 01 | Reflected XSS into HTML context with nothing encoded | Apprentice | ⏳ Planned | — |
+ | 01 | Reflected XSS into HTML context with nothing encoded | 🟢 Apprentice | ✅ Solved | [View](./01-reflected-xss-html-context/README.md) |
```

Also bump the `Labs solved` badge number at the top of that file.

## 5. Commit and push

```bash
git add "PortSwigger/XSS-Cross-Site-Scripting"
git commit -m "Add XSS lab: reflected XSS into HTML context"
git push
```

**Never edit the root `README.md` to add a lab** — it lists categories only, which is what keeps the front page short as the collection grows. (Update its "Recently solved" mini-table and the total count if you like.)

---

## Folder naming convention

| Category | Pattern | Example |
|---|---|---|
| SQL Injection | `sql-injection/0X-name` | `SQL-Injection/07-blind-conditional` |
| Authentication | `authentication/0X-name` | `Authentication/05-2fa-simple-bypass` |
| XSS | `xss/0X-name` | `XSS-Cross-Site-Scripting/02-stored-html-context` |
| JWT | `jwt/0X-name` | `JWT-Attacks/01-unverified-signature` |
| File upload | `file-upload/0X-name` | `File-Upload/02-content-type-bypass` |

Rules: **lowercase**, **hyphens not spaces**, **two-digit prefix**, short but descriptive.

---

## Write-up quality checklist

- [ ] Badges: status, difficulty, platform
- [ ] Objective stated in one sentence
- [ ] Original request + injected request shown as code blocks
- [ ] At least 3 screenshots: baseline, exploit, solved
- [ ] Root cause explained at code level
- [ ] Remediation table (control → implementation)
- [ ] References: PortSwigger topic + OWASP cheat sheet
- [ ] No real credentials, tokens or personal data in screenshots
