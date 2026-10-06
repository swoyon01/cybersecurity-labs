# Lab 10: Authentication — Username Enumeration via Response Timing

> **Source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing)  
> **Track:** Authentication  
> **Difficulty:** Practitioner  
> **Status:** ✅ Solved

---

## 🎯 Objective

Exploit a logic flaw in the login functionality that allows username enumeration via **response timing differences**. Enumerate a valid username by measuring how long the server takes to respond, then brute-force that user's password and log in as them.

---

## 🛠️ Tools

- Burp Suite Community Edition
- Firefox (Burp Browser)
- Kali Linux

---

## 🔍 Vulnerability Background



The application takes a **measurably longer time to respond when the username is valid** than when it is invalid.

Why? When the username exists, the server must:

1. Look up the user's stored password hash
2. Hash the submitted password
3. **Compare** it against the stored hash

When the username does **not** exist, the server skips the expensive password-hashing step and fails fast — returning a response much quicker.

This tiny timing difference is the leak. By amplifying it (submitting a **very long password**), even valid vs invalid usernames can be told apart by response time alone.

> ⚠️ Additionally, the lab enforces **IP-based rate limiting** — too many failed attempts from the same IP will block further attempts. To bypass this, we rotate the `X-Forwarded-For` header value on each request.

---

## 🔍 Step-by-Step Methodology

### Step 1 — Capture the Login Request
<img width="1280" height="684" alt="Screenshot 2026-10-02 015732" src="https://github.com/user-attachments/assets/870aafec-79d5-428e-9880-30ab22ce6229" />


Navigated to the lab's login page and submitted dummy credentials (`test` / `test123`) while interception was on in Burp Proxy.

Captured the request:

```http
POST /login HTTP/2
Host: ...web-security-academy.net
Cookie: session=...
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

username=test&password=test123
```

---

### Step 2 — Amplify the Timing Difference with a Long Password

A short password hashes almost instantly, making timing differences hard to detect. To amplify the signal, the password value is replaced with a **very long string** (100+ characters).

This forces the server to spend significantly more time hashing the password **only when the username is valid**.

Request sent to Intruder:

```http
POST /login HTTP/2
Host: ...web-security-academy.net
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

username=§test§&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

<img width="1280" height="684" alt="Screenshot 2026-10-02 024244" src="https://github.com/user-attachments/assets/3b279688-d8bb-437f-8e33-dda0edc9f639" />


---

### Step 3 — Enumerate Usernames with Burp Intruder (Pitchfork Attack)

Sent the request to Burp Intruder and configured a **Pitchfork attack** so that the username and the `X-Forwarded-For` header value rotate in parallel — one unique IP per username guess. This bypasses the IP-based rate limiting while still enumerating usernames.

**Intruder Configuration:**
- **Attack type:** Pitchfork
- **Payload position 1:** `username` parameter
- **Payload position 2:** `X-Forwarded-For` header value
- **Payloads 1:** Loaded a username wordlist (common usernames from the lab description)
- **Payloads 2:** Numeric payload — `120.120.120.0` to `120.120.120.100` (or a list of unique IPs)
- **Long fixed password:** Kept constant across all requests (important — only the username should vary)
- **Resource pool:** Throttled to **1 concurrent request** (timing attacks are noisy; concurrency destroys accuracy)

**Payload layout:**

```http
POST /login HTTP/2
Host: ...web-security-academy.net
X-Forwarded-For: 120.120.120.§120§
Cookie: session=...
Content-Type: application/x-www-form-urlencoded

username=§test§&password=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

After the attack finished, sorted the results by **response time** (`Response completed` column). One username — `applications` — stood out with a significantly higher response time (**2247 ms** vs. ~340 ms for all others), confirming it as a valid user.

<img width="1280" height="684" alt="Screenshot 2026-10-02 215743" src="https://github.com/user-attachments/assets/a44cc0f9-2081-4d8f-a7da-76de06de7f42" />
<img width="1280" height="684" alt="Screenshot 2026-10-02 215843" src="https://github.com/user-attachments/assets/20c75c1e-740e-4200-8a9d-72b18ceb7bce" />


---

### Step 4 — Enumerate the Password

With the valid username confirmed, sent a second Intruder attack — this time on the `password` field using the valid username.

**Intruder Configuration:**
- **Attack type:** Sniper
- **Payload position:** `password` parameter
- **Payloads:** Loaded a password wordlist
- **Grep - Match / status check:** Looked for `302 Found` redirect to `/my-account` instead of the `200 OK` login page

**Payload:**

```http
username=applications&password=§test123§
```

**Result:** One password — `pass` — returned a `302 Found` redirect — the correct credentials.

<img width="1280" height="684" alt="Screenshot 2026-10-02 220536" src="https://github.com/user-attachments/assets/ad53f760-5e1a-427b-aa69-849b297f5594" />


---

### Step 5 — Login & Solve the Lab

Used the discovered credentials to log in via the browser:

- **Username:** `applications`
- **Password:** `pass`

**Result:** Successfully logged in. Lab marked as solved. 🎉

<img width="1280" height="684" alt="Screenshot 2026-10-02 220734" src="https://github.com/user-attachments/assets/b97f7bae-8d16-4de0-9fa9-5534413e35ee" />


---

## 📝 Attack Flow Summary

| Step | Action | Tool | Purpose |
|------|--------|------|---------|
| 1 | Capture login request | Burp Proxy | Get baseline request |
| 2 | Replace password with long string | Burp Repeater | Amplify timing difference |
| 3 | Pitchfork attack on `username` + `X-Forwarded-For` | Burp Intruder | Enumerate valid username via response time while bypassing IP rate limiting |
| 4 | Sniper attack on `password` | Burp Intruder | Brute-force password for valid user |
| 5 | Login with discovered creds | Browser | Solve the lab |

---

## 🎯 Key Takeaways

1. **Response timing leaks information** — Even without different error messages, *how fast* the server answers can reveal valid usernames.
2. **Crypto operations amplify timing** — Password hashing (especially deliberately slow algorithms) makes valid usernames measurably slower. A long submitted password makes the gap obvious.
3. **Use a Pitchfork attack** — Rotating username and `X-Forwarded-For` in parallel bypasses IP-based rate limiting while still enumerating usernames.
4. **Rotate `X-Forwarded-For`** — Many apps trust this header for client IP; spoofing it lets you evade lockouts.
5. **Control the variables** — Keep the password identical across username attempts; only the tested value should vary.
6. **Throttle concurrency** — Run Intruder with 1 thread/resource pool. Network jitter and parallel requests make timing data unreliable.
7. **Repeat measurements** — Noisy results should be re-tested; a single outlier is not proof.
8. **Fixes matter** — Apps should perform the *same* amount of work for valid and invalid usernames (e.g., dummy hash comparison) so response times stay uniform.

---

## 🛡️ How This Is Fixed (Defender View)

- Perform a **dummy password hash comparison** for non-existent users so valid and invalid logins take equal time.
- Use **constant-time comparison** for secrets.
- Add **rate limiting and CAPTCHA** on login and forgot-password endpoints.
- Return **identical generic error messages** regardless of which field was wrong.
- Never let response *timing* or *content* differ between valid and invalid usernames.
- **Never trust `X-Forwarded-For` for security decisions** — derive client IP from the actual TCP connection.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the PortSwigger Web Security Academy. Unauthorized testing on systems you do not own or have explicit permission to test is **illegal and unethical**.

---

## 🔗 References

- [PortSwigger Authentication Vulnerabilities](https://portswigger.net/web-security/authentication)
- [Username Enumeration via Response Timing — Lab](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing)
- [Burp Intruder Documentation](https://portswigger.net/burp/documentation/desktop/tools/intruder)
- [Burp Intruder: Pitchfork Attack Type](https://portswigger.net/burp/documentation/desktop/tools/intruder/attack-types)

---

*Happy Hacking! 🐱‍💻*
