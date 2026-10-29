# Lab: Broken Brute-Force Protection, IP Block

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

> ⚠️ Additionally, this attack **only works if the requests land in the exact order they're sent** (guess → reset → guess → reset). To guarantee that, the Intruder attack's **Resource Pool must be throttled to a maximum of 1 concurrent request**. With the default concurrency, requests race each other and can arrive out of order, so a failed guess might land *after* the reset request instead of before it — breaking the bypass and getting the IP blocked anyway.

---

## 🔍 Step-by-Step Methodology

### Step 1 — Confirm the Brute-Force Protection Exists

Tried a few manual login attempts with the target username (`carlos`) and random passwords via Burp Repeater. After several attempts, the server responded with:

> "You have made too many incorrect login attempts. Please try again in 1 minute(s)."

This confirmed an IP-based lockout was active.

<img width="1280" height="684" alt="Screenshot 2026-10-29 165230" src="https://github.com/user-attachments/assets/2a690696-6c2b-4b83-ae90-f85569888de9" />


---

### Step 2 — Rule Out a Naive Sniper Attack

Attempted a straightforward Burp Intruder **Sniper** attack against the `password` parameter for `carlos` using a candidate password wordlist. As expected, after a handful of requests the IP got blocked and every subsequent request returned the "too many attempts" error — this approach doesn't work on its own.

<img width="1280" height="684" alt="Screenshot 2026-10-29 165538" src="https://github.com/user-attachments/assets/2261bbba-ef76-4225-bac3-2f19f5c9aef3" />


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

<img width="1280" height="684" alt="Screenshot 2026-10-29 170932" src="https://github.com/user-attachments/assets/5ee5f389-a8c5-4439-8312-2bccea6d307a" />


**Resource Pool — the critical setting:** Under Intruder's **Resource Pool** tab, created/assigned a dedicated pool and set **"Maximum concurrent requests" to 1**. This forces Burp to send requests strictly one at a time, in order, instead of firing them in parallel. Without this, the `wiener` reset request and a `carlos` guess could be sent and answered out of sequence, letting failed attempts stack up and trigger the IP block before the reset ever lands.



Every odd request logs in successfully as `wiener` (resetting the block), while every even request tests a password guess against `carlos`.

---

### Step 4 — Confirm the Counter-Reset Request Succeeds

Spot-checked one of the `wiener` / `peter` requests in the attack to confirm it returns a `302 Found` redirect to `/my-account`, proving the reset step is working and the IP stays unblocked throughout the attack.

<img width="1280" height="684" alt="Screenshot 2026-10-29 171353" src="https://github.com/user-attachments/assets/d128d77a-b152-4e04-a211-597bb548734e" />


---

### Step 5 — Identify the Successful `carlos` Login

Sorted the Intruder results by **status code**. One result stood out: `carlos` paired with the password `freedom` returned a `302 Found` (all other `carlos` guesses returned `200 OK`, i.e. the login page again).


Opened that request/response pair to confirm the `302 Found` redirects to `/my-account?id=carlos`, proving the credentials are valid.

<img width="1280" height="684" alt="Screenshot 2026-10-29 171418" src="https://github.com/user-attachments/assets/eec61236-19d0-494c-9a3e-b147f5e2368f" />

---

### Step 6 — Login & Solve the Lab

Used the discovered credentials to log in via the browser:

- **Username:** `carlos`
- **Password:** `freedom`

**Result:** Successfully logged in as `carlos`. Lab marked as solved. 🎉

<img width="1280" height="684" alt="Screenshot 2026-10-29 171630" src="https://github.com/user-attachments/assets/bb5b5d55-86cf-4b0e-93c6-579ce0fb72c5" />


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
4. **Throttle concurrency to 1** — requests must be sent in the correct order (guess → reset → guess → reset) for the bypass to hold, so the Intruder Resource Pool's max concurrent requests must be set to 1; parallel requests can arrive out of order and break the whole attack.
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

*Happy Hacking! by Swoyon 🐱‍💻*
