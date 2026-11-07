# Lab 4: DOM XSS in `innerHTML` Sink Using Source `location.search`

> Write-up for a PortSwigger Web Security Academy lab (DOM-based XSS, Apprentice level).

**Lab link:** https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink

![Status](https://img.shields.io/badge/Status-Solved-success)
![Level](https://img.shields.io/badge/Level-Apprentice-green)
![Category](https://img.shields.io/badge/Category-DOM--based%20XSS-blue)

---

## 1. Lab Description

This lab contains a **DOM-based cross-site scripting (XSS)** vulnerability in the search blog functionality. It uses an `innerHTML` assignment, which changes the HTML contents of a `div` element, using data from `location.search`.

**Goal:** Perform a cross-site scripting attack that calls the `alert` function.

---

## 2. Vulnerability Overview

| Item | Details |
|------|---------|
| Vulnerability | DOM-based XSS |
| Source | `location.search` (the query string of the URL) |
| Sink | `innerHTML` |
| Context | HTML content of the element `span#searchMessage` |
| Root cause | The `search` value is assigned to `innerHTML` without encoding or sanitizing |
| Impact | Attacker-controlled JavaScript runs in the victim's browser |

---

## 3. Tools Used

- Kali Linux (VirtualBox)
- Firefox with Developer Tools (Inspector tab)

---

## 4. Step-by-Step Solution

### Step 1: Test the search function
I entered a normal search term, `Security issue`, in the search bar. The page shows **"0 search results for 'Security issue'"** and the term is also in the URL as `?search=Security+issue`. So the page reads the value from the URL and shows it back on the page.

<img width="1280" height="684" alt="Screenshot 2026-11-07 161627" src="https://github.com/user-attachments/assets/2c9a1030-9909-48cb-b0af-0adca3ca2045" />


### Step 2: Find where the input goes in the DOM
In the Inspector tab I searched for my text. It is inside a `span` with the id `searchMessage`:

```html
<h1>
    <span>0 search results for '</span>
    <span id="searchMessage">Security issue</span>
    <span>'</span>
</h1>
```
<img width="1280" height="684" alt="Screenshot 2026-11-07 161406" src="https://github.com/user-attachments/assets/8535641a-1bde-43b1-b1e0-0b194fd421e9" />



### Step 3: Read the JavaScript code
Just below, in the `<script>` tag, I found the code that fills this span:

```javascript
function doSearchQuery(query) {
    document.getElementById('searchMessage').innerHTML = query;
}
var query = (new URLSearchParams(window.location.search)).get('search');
if(query) {
    doSearchQuery(query);
}
```

What it does:
1. It reads the `search` parameter from the URL (**source**).
2. It puts the value into the page with `innerHTML` (**sink**), with no encoding.

<img width="1280" height="684" alt="Screenshot 2026-11-07 161512" src="https://github.com/user-attachments/assets/16be1fed-7cfe-441c-9186-346d80db3459" />


### Step 4: Choose the payload
`innerHTML` does **not** run `<script>` tags that are added this way, so a normal `<script>alert(1)</script>` payload will not work. But it does create other elements, and their event handlers can run. I used an image that fails to load:

```html
<img src=1 onerror=alert(1)>
```

Final URL:

```
https://<lab-id>.web-security-academy.net/?search=<img src=1 onerror=alert(1)>
```

How it works:
- `innerHTML` turns the text into a real `<img>` element.
- `src=1` is not a valid image, so the load fails.
- The `onerror` event runs `alert(1)`.

### Step 5: Lab solved
After opening the URL, the `alert` is triggered and the lab banner changes to **"Congratulations, you solved the lab!"** The broken image icon is visible inside the heading.

<img width="1280" height="684" alt="Screenshot 2026-11-07 163325" src="https://github.com/user-attachments/assets/850aa2d5-af5a-4e39-9864-c33171296632" />


---

## 5. Why It Works

`innerHTML` parses a string as **HTML**. Because the search value is not encoded, the attacker can add a new tag with an event handler. Browsers do not run `<script>` elements inserted with `innerHTML`, but they do run event handlers like `onerror` and `onload`.

---

## 6. Real-World Impact

- Steal session cookies or tokens (if not protected by `HttpOnly`)
- Perform actions as the victim
- Show fake forms or redirect to malicious sites
- The attacker only needs to send the victim a crafted link

---

## 7. Prevention

1. Use **`textContent`** (or `innerText`) instead of `innerHTML` when you only need to show text.
2. If HTML is really needed, **sanitize** it first with a trusted library such as DOMPurify.
3. **Encode** untrusted data for the context where it is used.
4. **Validate** the input and accept only expected characters.
5. Use a **Content Security Policy (CSP)** to reduce the damage if an XSS bug exists.

---

## 8. Key Takeaways

- Find the **source** and the **sink**, then work out what kind of HTML the sink creates.
- `<script>` does not work through `innerHTML`; use event handlers such as `onerror` or `onload` instead.
- Browser developer tools (Inspector) are enough to find this type of bug.

---

## 9. References

- PortSwigger, [DOM-based XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- PortSwigger, [Lab: DOM XSS in innerHTML sink using source location.search](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink)
- OWASP, [DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

---

## Disclaimer

This write-up is for **educational purposes only**. The test was done in the intentionally vulnerable PortSwigger lab environment. Do not test these techniques on systems you do not own or do not have written permission to test.

---

## 👤 Author

**Saber Hasan Swoyon **  

*Happy Hacking! 🐱‍💻*
