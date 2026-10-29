#16 Lab: Broken Brute-Force Protection, IP Block

> **Source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/authentication/other-mechanisms/lab-broken-brute-force-protection-ip-block)
> **Track:** Authentication
> **Difficulty:** Practitioner
> **Status:** ✅ Solved

---

## 🎯 Objective

Exploit a logic flaw in the brute-force protection mechanism that only tracks **failed** login attempts per IP. By interleaving a known valid login with password guesses, the failed-attempt counter keeps getting reset, letting an attacker brute-force a target's password without ever triggering the IP block.

---

## 🛠️ Tools

- Burp Suite Community Edition
- Firefox (Burp Browser)
- Kali Linux

---

## 🔍 Vulnerability Background

The application locks out an IP address after a set number of **consecutive failed** login attempts. However, the counter resets to zero as soon as **one successful login** occurs from that IP — regardless of whose account it belongs to.

Since the lab gives us valid credentials for our own account (`wiener:peter`), we can:

1. Submit a guess for the target account (`carlos`) — this counts as a failed attempt.
2. Immediately submit our own valid credentials (`wiener:peter`) — this succeeds and **resets the failed-attempt counter**.
3. Repeat, cycling through a password wordlist for `carlos`, with a valid `wiener` login after every guess.

This way the IP never accumulates enough consecutive failures to get blocked, and we can brute-force `carlos`'s password at will.

---

## 🔍 Step-by-Step Methodology

### Step 1 — Confirm the Brute-Force Protection Exists

Tried a few manual login attempts with the target username (`carlos`) and random passwords via Burp Repeater. After several attempts, the server responded with:

> "You have made too many incorrect login attempts. Please try again in 1 minute(s)."

This confirmed an IP-based lockout was active.

<img width="1280" height="684" alt="Screenshot 2026-10-29 165230" src="https://github.com/user-attachments/assets/db26db24-231f-4737-8f8a-841ad1c80a30" />


---

### Step 2 — Rule Out a Naive Sniper Attack

Attempted a straightforward Burp Intruder **Sniper** attack against the `password` parameter for `carlos` using a candidate password wordlist. As expected, after a handful of requests the IP got blocked and every subsequent request returned the "too many attempts" error — this approach doesn't work on its own.

<img width="1280" height="684" alt="Screenshot 2026-10-29 165538" src="https://github.com/user-attachments/assets/aa028fbc-02cb-4fda-9843-f84aabef22fa" />


---

### Step 3 — Build a Pitchfork Attack That Resets the Counter

Sent the login request to Burp Intruder and switched to a **Pitchfork attack**, placing two payload positions:

```http
POST /login HTTP/2
Host: ...web-security-academy.net
Content-Type: application/x-www-form-urlencoded

username=§wiener§&password=§peter§
```

**Intruder Configuration:**
- **Attack type:** Pitchfork
- **Payload position 1 (`username`):** alternating list — `wiener`, `carlos`, `wiener`, `carlos`, …
- **Payload position 2 (`password`):** alternating list — `peter` (the known-valid password), `<candidate password #1>`, `peter`, `<candidate password #2>`, …
- **Resource pool:** Throttled to **1 concurrent request** (requests must land in order so the reset lands before the next guess)

Every odd request logs in successfully as `wiener` (resetting the block), while every even request tests a password guess against `carlos`.

📸 **`screenshots/03-pitchfork-payload-config.png`**

---

### Step 4 — Confirm the Counter-Reset Request Succeeds

Spot-checked one of the `wiener` / `peter` requests in the attack to confirm it returns a `302 Found` redirect to `/my-account`, proving the reset step is working and the IP stays unblocked throughout the attack.

<img width="1280" height="684" alt="Screenshot 2026-10-29 170932" src="https://github.com/user-attachments/assets/53271f39-f11a-415c-9d40-56ae98fa0439" />


---

### Step 5 — Identify the Successful `carlos` Login

Sorted the Intruder results by **status code**. One result stood out: `carlos` paired with the password `freedom` returned a `302 Found` (all other `carlos` guesses returned `200 OK`, i.e. the login page again).

<img width="1280" height="684" alt="Screenshot 2026-10-29 171353" src="https://github.com/user-attachments/assets/9ac81e52-1baf-40e4-ba91-adf533cc670c" />


Opened that request/response pair to confirm the `302 Found` redirects to `/my-account?id=carlos`, proving the credentials are valid.

<img width="1280" height="684" alt="Screenshot 2026-10-29 171418" src="https://github.com/user-attachments/assets/abb33c4b-80d2-404b-81e2-dbdc8f4f898d" />


---

### Step 6 — Login & Solve the Lab

Used the discovered credentials to log in via the browser:

- **Username:** `carlos`
- **Password:** `freedom`

**Result:** Successfully logged in as `carlos`. Lab marked as solved. 🎉

<img width="1280" height="684" alt="Screenshot 2026-10-29 171630" src="https://github.com/user-attachments/assets/92025633-2e9c-4d36-9af6-560909f54d78" />


---

## 📝 Attack Flow Summary

| Step | Action | Tool | Purpose |
|------|--------|------|---------|
| 1 | Trigger lockout manually | Burp Repeater | Confirm brute-force protection exists |
| 2 | Plain Sniper attack on `carlos` | Burp Intruder | Show naive brute-force gets blocked |
| 3 | Pitchfork: alternate `wiener`/`peter` with `carlos`/guess | Burp Intruder | Reset the failed-attempt counter every other request |
| 4 | Verify reset request returns 302 | Burp Intruder / Repeater | Confirm the bypass is working mid-attack |
| 5 | Find `carlos` guess that returns 302 | Burp Intruder | Identify the correct password |
| 6 | Login with discovered creds | Browser | Solve the lab |

---

## 🎯 Key Takeaways

1. **Counters that reset on success are a logic flaw** — if a successful login (by *anyone*, from the same IP) resets the failed-attempt count, the lockout can be trivially bypassed.
2. **A known-good credential becomes an attack tool** — your own valid login can be weaponized as a "counter reset" request.
3. **Use a Pitchfork attack** — lets two payload lists advance in lockstep, interleaving the reset login with each guess.
4. **Throttle concurrency** — requests must be sent in the correct order (guess → reset → guess → reset) for the bypass to hold, so concurrency should be limited.
5. **IP-based protection alone is weak** — it doesn't account for the targeted account vs. the account that's successfully logging in being different.

---

## 🛡️ How This Is Fixed (Defender View)

- Lock based on the **targeted username**, not just the source IP (or both, combined intelligently).
- Don't let a successful login on a **different account** reset the failed-attempt counter for the one being attacked.
- Add **CAPTCHA** or progressive delays after repeated failures, independent of other accounts' activity.
- Monitor for the alternating-success pattern (a classic sign of this bypass technique).

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the PortSwigger Web Security Academy. Unauthorized testing on systems you do not own or have explicit permission to test is **illegal and unethical**.

---

## 🔗 References

- [PortSwigger Authentication Vulnerabilities](https://portswigger.net/web-security/authentication)
- [Broken Brute-Force Protection, IP Block — Lab](https://portswigger.net/web-security/authentication/other-mechanisms/lab-broken-brute-force-protection-ip-block)
- [Burp Intruder Documentation](https://portswigger.net/burp/documentation/desktop/tools/intruder)
- [Burp Intruder: Pitchfork Attack Type](https://portswigger.net/burp/documentation/desktop/tools/intruder/attack-types)

---

*Happy Hacking! 🐱‍💻*
