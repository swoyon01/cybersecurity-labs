# Lab 19 : Reflected XSS into HTML Context with Nothing Encoded

> **Source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)
> **Track:** Cross-Site Scripting (XSS)
> **Difficulty:** Apprentice
> **Status:** ✅ Solved

---

## 🎯 Objective

Exploit a reflected cross-site scripting vulnerability in the blog's search function, where user input is echoed back into the page's HTML with **no encoding or sanitization at all**, and get `alert(1)` to execute in the browser.

---

## 🛠️ Tools

- Burp Suite Community Edition
- Firefox (Burp Browser) with Developer Tools
- Kali Linux

---

## 🔍 Vulnerability Background

The blog's search feature takes the `search` query parameter and reflects it straight back into the page inside an `<h1>` heading (`0 search results for '<input>'`) with **zero output encoding**. Since the value lands directly in an **HTML context** (not inside an attribute, not inside a script string — just plain HTML body content), any HTML/JavaScript submitted is rendered and executed by the browser exactly as written.

This is the simplest and most direct flavor of reflected XSS: no need to break out of quotes, no need to bypass a filter — the input is dropped in raw.

---

## 🔍 Step-by-Step Methodology

### Step 1 — Find and Confirm the Reflection Point

Submitted a harmless, unique marker string in the search box to see exactly where and how the input comes back in the page:

```
Hay, lets exploit
```

The response rendered:

> `0 search results for 'Hay, lets exploit'`

This confirmed the input is reflected verbatim, unescaped, inside the page's HTML — a strong candidate for reflected XSS.

<img width="1280" height="720" alt="Screenshot 2026-11-04 020759" src="https://github.com/user-attachments/assets/23c16891-ee1f-428f-ac38-39ff0e053cda" />


---

### Step 2 — Confirm Nothing Is Encoded

Inspected the raw HTTP response (not just the rendered page) to make sure special characters like `<`, `>`, and `'` weren't being HTML-entity-encoded (`&lt;`, `&gt;`, `&#x27;`) before being inserted — which would have blocked script execution.

The raw response showed the input placed directly into the `<h1>` tag with no encoding applied whatsoever, confirming the injection point is fully exploitable

<img width="1280" height="684" alt="Screenshot 2026-11-04 014150" src="https://github.com/user-attachments/assets/e5757099-2b81-42f7-9b82-90ada4a7e641" />


<img width="1280" height="684" alt="Screenshot 2026-11-04 020926" src="https://github.com/user-attachments/assets/9abf1b71-1e22-4476-85fa-7c435ef49383" />


---

### Step 3 — Inject the XSS Payload

Replaced the search term with a basic `<script>` payload:

```
<script>alert(1)</script>
```

Request:

```http
GET /?search=<script>alert(1)</script> HTTP/2
Host: ...web-security-academy.net
```

<img width="1280" height="684" alt="image" src="https://github.com/user-attachments/assets/60a10e79-4b0b-428e-a370-647f4694c3d9" />

<img width="1280" height="684" alt="Screenshot 2026-11-04 015849" src="https://github.com/user-attachments/assets/a581d9d9-afb5-409e-b1f3-1281cc3dd01e" />

Since the value is inserted into the page with no encoding, the browser parses `<script>alert(1)</script>` as a real `<script>` element and executes it on page load.

---

### Step 4 — Confirm Execution & Solve the Lab

Loaded the payload URL in the browser. A JavaScript alert box popped up displaying `1`, and the lab status flipped to **Solved**.

<img width="1280" height="684" alt="Screenshot 2026-11-04 015600" src="https://github.com/user-attachments/assets/6693861a-1df7-4b03-91bb-3cdc5b6e36ff" />
<img width="1280" height="684" alt="Screenshot 2026-11-04 015807" src="https://github.com/user-attachments/assets/0a05a73c-a5e5-4e62-b2ac-0cdb785f35a9" />



**Result:** Lab marked as solved — "Congratulations, you solved the lab!" 🎉

<img width="1280" height="684" alt="Screenshot 2026-11-04 015617" src="https://github.com/user-attachments/assets/38031b5b-6f1d-4b0a-a9e8-d1d142dc163f" />


---

## 📝 Attack Flow Summary

| Step | Action | Tool | Purpose |
|------|--------|------|---------|
| 1 | Submit a unique marker string | Browser | Find where input is reflected in the page |
| 2 | Inspect raw HTTP response | Browser DevTools | Confirm no HTML encoding is applied |
| 3 | Inject `<script>alert(1)</script>` | Browser / URL | Craft the XSS payload for an HTML context |
| 4 | Load the payload URL | Browser | Trigger the alert and solve the lab |

---

## 🎯 Key Takeaways

1. **Context determines the payload** — because the input lands in a plain HTML body context (not an attribute or script string), a bare `<script>` tag is enough; no quote-breaking or filter evasion needed.
2. **Always check the raw response, not just the rendered page** — some encoding issues are only visible in the HTTP response source, not the browser's rendered DOM.
3. **A unique marker string speeds up recon** — searching for something like `Hay, lets exploit` makes it easy to spot exactly where and how input is reflected.
4. **Reflected XSS requires a victim to click a crafted link** — unlike stored XSS, this payload only fires when a specific URL is visited, making it useful in phishing-style attacks.

---

## 🛡️ How This Is Fixed (Defender View)

- **HTML-encode all user input** before reflecting it into HTML contexts (`<` → `&lt;`, `>` → `&gt;`, `'` → `&#x27;`, `"` → `&quot;`, `&` → `&amp;`).
- Use a templating engine with **auto-escaping enabled by default** rather than manual string concatenation.
- Apply a strong **Content Security Policy (CSP)** to restrict inline script execution as defense-in-depth.
- Validate and sanitize input on the server side, even though output encoding is the real fix for XSS.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the PortSwigger Web Security Academy. Unauthorized testing on systems you do not own or have explicit permission to test is **illegal and unethical**.

---

## 🔗 References

- [PortSwigger Cross-Site Scripting](https://portswigger.net/web-security/cross-site-scripting)
- [Reflected XSS into HTML Context with Nothing Encoded — Lab](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded)
- [Cross-Site Scripting Cheat Sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [Types of XSS](https://portswigger.net/web-security/cross-site-scripting)

---

## 👤 Author

**Saber Hasan Swoyon**  

*Happy Hacking! 🐱‍💻*
