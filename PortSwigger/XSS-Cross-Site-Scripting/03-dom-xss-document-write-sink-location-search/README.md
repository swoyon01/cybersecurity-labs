# Lab 3: DOM XSS in `document.write` Sink Using Source `location.search`

> Write-up for a PortSwigger Web Security Academy lab (DOM-based XSS, Apprentice level).

**Lab link:** https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink

![Status](https://img.shields.io/badge/Status-Solved-success)
![Level](https://img.shields.io/badge/Level-Apprentice-green)
![Category](https://img.shields.io/badge/Category-DOM--based%20XSS-blue)

---

## 1. Lab Description

This lab contains a **DOM-based cross-site scripting (XSS)** vulnerability in the search query tracking functionality. The page uses the JavaScript function `document.write` to write data to the page, and the data comes from `location.search`, which an attacker controls through the URL.

**Goal:** Perform a cross-site scripting attack that calls the `alert` function.

---

## 2. Vulnerability Overview

| Item | Details |
|------|---------|
| Vulnerability | DOM-based XSS |
| Source | `location.search` (the query string of the URL) |
| Sink | `document.write()` |
| Context | Inside the `src` attribute of an `<img>` tag |
| Root cause | The `search` value goes into `document.write` without any encoding or validation |
| Impact | Attacker-controlled JavaScript runs in the victim's browser |

### Source and Sink

- **Source:** where the attacker's data enters the page (here: `location.search`).
- **Sink:** a function that can run or render that data in a dangerous way (here: `document.write`).
- In DOM XSS the problem is in the **client-side JavaScript**. The server only returns the normal page.

---

## 3. Tools Used

- Kali Linux (VirtualBox)
- Firefox with Developer Tools (Inspector and Network tabs)
- Burp Suite Community Edition (optional)

---

## 4. Step-by-Step Solution

### Step 1: Check the comment section
First I opened a blog post and looked at the comment section, because comments are a common place for XSS. A comment with `<script>alert(1)</script>` is shown as plain text.

<img width="1280" height="684" alt="01-comment-section" src="https://github.com/user-attachments/assets/6dd10483-77c6-4f43-b2cb-1a941c24e705" />


### Step 2: Check the response source
In the Network tab, the HTML response shows that the comment is **encoded** (`&lt;script&gt;alert(1)&lt;/script&gt;`). So the comment section is not the vulnerable place in this lab.

<img width="1280" height="684" alt="02-comments-are-encoded" src="https://github.com/user-attachments/assets/e77607a3-b1cb-4221-ba39-768676b1835c" />


### Step 3: Explore the search function and read the code
I then tested the search bar and read the page source. The search page has this script:

```javascript
function trackSearch(query) {
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if(query) {
    trackSearch(query);
}
```

What it does:
1. It reads the `search` parameter from the URL (**source**).
2. It puts the value inside an `<img src="...">` tag using `document.write` (**sink**), with no encoding.

<img width="1280" height="684" alt="03-document-write-source-code" src="https://github.com/user-attachments/assets/3db7a169-3599-417b-9c98-c42425c30f2d" />


### Step 4: Try a simple `<script>` payload
Payload in the search bar:

```html
<script>alert(1)</script>
```

It does **not** work. The payload only becomes part of the `src` value of the image, so the browser treats it as text inside the attribute, not as a new tag.

<img width="1280" height="684" alt="04-script-payload-fails" src="https://github.com/user-attachments/assets/3d883b42-84a5-44e6-80c2-1450c71d0220" />


### Step 5: Break out of the attribute and the tag
Since the input lands inside `src="..."`, the payload must first close the attribute (`"`) and the tag (`>`), then add a new element that runs JavaScript. I used:

```html
"><img src=anything onerror=alert(1)>
```

Final URL:

```
https://<lab-id>.web-security-academy.net/?search="><img src=anything onerror=alert(1)>
```

How it works: the page writes

```html
<img src="/resources/images/tracker.gif?searchTerms="><img src=anything onerror=alert(1)>">
```

- `">` closes the original `src` attribute and the first `<img>` tag.
- `<img src=anything onerror=alert(1)>` is a new image. The file `anything` does not exist, the load fails, and the `onerror` event runs `alert(1)`.

The alert box appears.

<img width="1280" height="684" alt="05-alert-popup" src="https://github.com/user-attachments/assets/d8534a14-5d88-42d5-bca1-165206bf21b0" />


### Step 6: Check the injected element in the DOM
In the Inspector tab, the new element `<img src="anything" onerror="alert(1)">` is now part of the page, next to the original tracker image.

<img width="1280" height="684" alt="06-injected-img-in-dom" src="https://github.com/user-attachments/assets/0ec06420-041a-44cd-ba03-f8eb911953be" />


### Step 7: Lab solved
The lab banner changes to **"Congratulations, you solved the lab!"**

<img width="1280" height="684" alt="07-lab-solved" src="https://github.com/user-attachments/assets/89556f15-a38b-4492-b05c-f6a996444bf9" />


---

## 5. Why It Works

`document.write` writes a string as **HTML**. Because the value from `location.search` is added to that string without encoding, the attacker can add quotes and angle brackets to change the structure of the HTML. The browser then sees a new tag with an event handler and runs it.

---

## 6. Real-World Impact

- Steal session cookies or tokens (if not protected by `HttpOnly`)
- Perform actions as the victim
- Show fake forms or redirect to malicious sites
- The attacker only needs to send the victim a crafted link

---

## 7. Prevention

1. **Avoid dangerous sinks:** do not use `document.write`, `innerHTML` or `eval` with user data.
2. Use safe APIs such as `textContent`, or create elements with `document.createElement` and set attributes with `setAttribute`.
3. **Encode** the data for the right context (for a URL value use `encodeURIComponent`, for HTML use HTML encoding).
4. **Validate** the input and accept only the expected characters.
5. Use a **Content Security Policy (CSP)** to reduce the damage if an XSS bug exists.
6. If HTML must be allowed, use a trusted sanitizer such as DOMPurify.

---

## 8. Key Takeaways

- DOM XSS happens in the browser, so check the page's JavaScript (sources and sinks), not only the server response.
- The context decides the payload. Inside an attribute you must first break out of it.
- If `<script>` does not work, try event-handler payloads like `onerror` or `onload`.

---

## 9. References

- PortSwigger, [DOM-based XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)
- PortSwigger, [Lab: DOM XSS in document.write sink using source location.search](https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink)
- OWASP, [DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)

---

## Disclaimer

This write-up is for **educational purposes only**. The test was done in the intentionally vulnerable PortSwigger lab environment. Do not test these techniques on systems you do not own or do not have written permission to test.

---

## 👤 Author

**Saber Hasan Swoyon**  
