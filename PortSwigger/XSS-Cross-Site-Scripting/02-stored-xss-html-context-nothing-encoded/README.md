# Lab 2: Stored XSS into HTML Context with Nothing Encoded

> Write-up for a PortSwigger Web Security Academy lab (Cross-site scripting, Apprentice level).
> Done by: Hasan Abu Saber

**Lab link:** https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded

![Status](https://img.shields.io/badge/Status-Solved-success)
![Level](https://img.shields.io/badge/Level-Apprentice-green)
![Category](https://img.shields.io/badge/Category-Stored%20XSS-blue)

---

## 1. Lab Description

This lab contains a **stored cross-site scripting (XSS)** vulnerability in the **comment functionality** of a blog.

**Goal:** Submit a comment that calls the `alert` function when the blog post is viewed.

---

## 2. Vulnerability Overview

| Item | Details |
|------|---------|
| Vulnerability | Stored (persistent) XSS |
| Location | Comment form on a blog post page |
| Context | HTML context (the text is placed between HTML tags) |
| Root cause | The comment is saved and later shown on the page **without any output encoding** |
| Impact | Every visitor who opens the post runs the attacker's JavaScript |

### Reflected vs Stored XSS

- **Reflected XSS:** the payload is in the request (for example a URL) and is returned right away in the response. Only the person who opens the crafted link is affected.
- **Stored XSS:** the payload is saved by the server (database) and shown to **all users** who view the page. No special link is needed.

---

## 3. Tools Used

- Web browser (Burp Suite's built-in browser or any normal browser)
- Burp Suite (optional, to see the request and the response)

---

## 4. Step-by-Step Solution

### Step 1: Open the lab and a blog post
1. Click **Access the lab** and log in to the PortSwigger account if asked.
2. Open any blog post with **View post**.
3. Scroll down to the **Leave a comment** form.

📸 *Screenshot: the comment form*

### Step 2: Test how the comment is shown
Submit a normal comment first, for example `hay, its time to fall asleep !`, with any name, a fake email and a website. Go back to the post and check how the text is shown in the page (in the browser, or with **Inspect**).

Result: the comment text is placed inside the HTML of the page.

<img width="1280" height="684" alt="Screenshot 2026-11-04 152640" src="https://github.com/user-attachments/assets/dbbb47e4-ce39-4378-9026-fb81d520f2d4" />
<img width="1280" height="684" alt="Screenshot 2026-11-04 153425" src="https://github.com/user-attachments/assets/0ce56050-3d6b-40e4-8ea5-9fef413e0354" />


### Step 3: Submit the payload
Enter this in the **Comment** field:

```html
<script>alert(1)</script>
```

Fill in the other fields:

| Field | Value |
|-------|-------|
| Comment | `<script>alert(1)</script>` |
| Name | any name |
| Email | `test@test.com` |
| Website | `http://test.com` |

Click **Post Comment**.

<img width="1280" height="684" alt="Screenshot 2026-11-04 153704" src="https://github.com/user-attachments/assets/59ffa1aa-9c57-47eb-a4be-935a01f47b06" />


### Step 4: Trigger the stored payload
Click **Back to blog** and open the same post again. The saved comment is loaded as part of the page, the browser runs the `<script>` tag, and an **alert box** appears.

<img width="1280" height="684" alt="Screenshot 2026-11-04 153733" src="https://github.com/user-attachments/assets/13a17c3c-5f15-45b9-a1ce-5c7f5ff26021" />


### Step 5: Lab solved
The lab banner changes to **"Congratulations, you solved the lab!"**

<img width="1280" height="684" alt="Screenshot 2026-11-04 153719" src="https://github.com/user-attachments/assets/01c5d587-e2c2-470e-b2a8-11515642d16c" />


---

## 5. Why It Works

The server inserts the comment into the page like this (simplified):

```html
<section class="comment">
    <p>
        <script>alert(1)</script>
    </p>
</section>
```

Because nothing is encoded, the browser does not see this as text. It sees a real `<script>` element and runs it. Also, the comment is stored, so it runs **each time** someone loads the post.

---

## 6. Real-World Impact

A real attacker would not use `alert(1)`. A stored XSS can be used to:

- Steal session cookies or tokens (if not protected by `HttpOnly`)
- Perform actions as the victim (change email or password, post content)
- Show fake login forms (phishing)
- Redirect users to malicious sites
- Spread to other users as a worm

---

## 7. Prevention

1. **Output encoding:** encode user data for the context where it is shown. In an HTML context, convert `<` to `&lt;`, `>` to `&gt;`, `&` to `&amp;`, `"` to `&quot;` and `'` to `&#x27;`.
2. **Input validation:** accept only the expected format (a comment needs plain text, not HTML).
3. **Content Security Policy (CSP):** limit where scripts can come from, so injected inline scripts do not run.
4. **Cookie flags:** use `HttpOnly`, `Secure` and `SameSite` to reduce the damage of a stolen session.
5. **Use safe frameworks and APIs:** for example `textContent` instead of `innerHTML`, and template engines that encode by default.
6. If HTML must be allowed, use a well-tested sanitizer library (for example DOMPurify) instead of writing your own filter.

---

## 8. Key Takeaways

- Stored XSS is usually more dangerous than reflected XSS, because it needs no victim interaction beyond viewing the page.
- Always test every place where user input is saved and shown again: comments, profiles, messages, reviews.
- If a simple `<script>` payload works, the application is doing **no encoding at all** in that context.

---

## 9. References

- PortSwigger Web Security Academy, [Cross-site scripting](https://portswigger.net/web-security/cross-site-scripting)
- PortSwigger Web Security Academy, [Stored XSS](https://portswigger.net/web-security/cross-site-scripting/stored)
- OWASP, [XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

---

## Disclaimer

This write-up is for **educational purposes only**. The test was done in the intentionally vulnerable PortSwigger lab environment. Do not test these techniques on systems you do not own or do not have written permission to test.


## 👤 Author

**Saber Hasan Swoyon (孙剑）**  

*Happy Hacking! 🐱‍💻*
