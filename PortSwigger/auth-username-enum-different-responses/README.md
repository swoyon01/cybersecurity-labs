# Lab 07: Authentication — Username Enumeration via Different Responses

> **Source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses)  
> **Track:** Authentication  
> **Difficulty:** Apprentice  
> **Status:** ✅ Solved

---

## 🎯 Objective

Exploit a logic flaw in the login functionality that allows username enumeration via subtly different error messages. Enumerate a valid username, then brute-force the corresponding password to log in as that user.

---

## 🛠️ Tools

- Burp Suite Community Edition
- Firefox
- Kali Linux

---

## 🔍 Step-by-Step Methodology

### Step 1 — Observe Login Behavior

Navigated to the login page and submitted credentials to observe error messages.

**Test 1 — Invalid Username + Invalid Password:**
- Username: `abcd1234`
- Password: `wrongpass`

**Result:** Error message → `Invalid username`

<img width="1280" height="684" alt="Screenshot 2026-09-14 221213" src="https://github.com/user-attachments/assets/63f1294a-144a-4eea-b108-10101deaf61f" />

<img width="1280" height="684" alt="Screenshot 2026-09-14 222216" src="https://github.com/user-attachments/assets/6bd26cd2-6171-4618-848d-cfbde9729167" />


---

---

### Step 2 — Enumerate Usernames with Burp Intruder

Intercepted the login request in Burp Proxy and sent it to **Burp Intruder**.

**Intruder Configuration:**
- **Attack type:** Sniper
- **Payload position:** `abcd1234` parameter
- **Payloads:** Loaded a username wordlist (common usernames)
- **Grep - Match:** Configured to extract responses containing `Incorrect password`

**Payload:**
```
POST /login HTTP/2
Host: ...web-security-academy.net
...

username=§abcd1234§&password=wrongpass
```

**Result:** Found one username (`ad`) that returned `Incorrect password` instead of `valid username`.

<img width="1280" height="684" alt="Screenshot 2026-09-14 222355" src="https://github.com/user-attachments/assets/6509f04f-dfae-44a2-9999-7e9e2424117a" />
<img width="1280" height="684" alt="Screenshot 2026-09-16 160655" src="https://github.com/user-attachments/assets/f4c4b8f2-a327-4afe-9525-f9eb13fd82a4" />



---

### Step 3 — Enumerate Password for Valid User

With the valid username confirmed, sent another Intruder attack targeting the `password` field.

**Intruder Configuration:**
- **Attack type:** Sniper
- **Payload position:** `wrongpass` parameter
- **Payloads:** Loaded a password wordlist
- **Grep - Extract:** Looked for `302 Redirect` or absence of error message

**Payload:**
```
username=ad&password=§wrongpass§
```

**Result:** One password returned a `302 Found` redirect to `/my-account` instead of the login error page.

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/91893039-2619-4bc3-969d-aeb44226cd23" />


---

### Step 4 — Login & Solve the Lab

Used the discovered credentials to log in:
- **Username:** `ad`
- **Password:** `austin`

**Result:** Successfully logged in. Lab marked as solved.

<img width="1280" height="684" alt="Screenshot 2026-09-16 161317" src="https://github.com/user-attachments/assets/e4327cb5-3503-4fbc-b959-788f70bb4189" />


---

## 📝 Attack Flow Summary

| Step | Action | Tool | Purpose |
|------|--------|------|---------|
| 1 | Manual login with fake creds | Browser | Observe error messages |
| 2 | Compare error responses | Browser | Detect username enumeration flaw |
| 3 | Intruder Sniper on `username` | Burp Intruder | Enumerate valid username |
| 4 | Intruder Sniper on `password` | Burp Intruder | Brute-force password for valid user |
| 5 | Login with discovered creds | Browser | Solve the lab |

---

## 🎯 Key Takeaways

1. **Error messages leak information** — Even subtle differences like `Invalid username` vs `Incorrect password` can reveal valid accounts.
2. **Always test with known-bad vs potentially-valid usernames** — Compare responses side-by-side.
3. **Burp Intruder + Grep-Match is powerful** — Automates enumeration by filtering for specific response strings.
4. **Never rely on client-side validation alone** — The server response is what matters.
5. **Use consistent password for username enum** — A fixed wrong password ensures only the username affects the response.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the PortSwigger Web Security Academy. Unauthorized testing on systems you do not own or have explicit permission to test is illegal and unethical.

---

## 🔗 References

- [PortSwigger Authentication Vulnerabilities](https://portswigger.net/web-security/authentication)
- [Username Enumeration via Different Responses](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses)
- [Burp Intruder Documentation](https://portswigger.net/burp/documentation/desktop/tools/intruder)

---

*Happy Hacking! 🐱‍💻*
