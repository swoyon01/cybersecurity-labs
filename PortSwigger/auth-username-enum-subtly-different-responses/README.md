# Lab 08: Authentication — Username Enumeration via Subtly Different Responses

> **Source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses)  
> **Track:** Authentication  
> **Difficulty:** Apprentice  
> **Status:** ✅ Solved

### 📌 Vulnerability Description

The login form returns subtly different error messages depending on whether the username exists or not. While most responses return `Invalid username or password.`, a valid username returns `Invalid username or password` (without the trailing period). This tiny difference allows an attacker to enumerate valid usernames.

### 🎯 Objective

- Enumerate a valid username from the candidate list.
- Brute-force the password for that username.
- Access the account page.

### 🛠️ Exploitation Steps

#### Step 1: Capture the Login Request

1. Open the lab in Burp Browser.
2. Submit a dummy login (e.g., `test:test123`).
3. In **Proxy > HTTP history**, locate `POST /login`.
4. Right-click → **Send to Intruder**.

<img width="1280" height="684" alt="Screenshot 2026-09-25 220328" src="https://github.com/user-attachments/assets/f87eed07-07db-4266-83fc-f39fbcf7aa47" />


#### Step 2: Configure Payload Position

1. In **Intruder > Positions**, clear all positions.
2. Highlight only the `username` value (`test`) and click **Add §**.
3. Ensure Attack type is **Sniper**.

<img width="1280" height="684" alt="Screenshot 2026-09-25 220508" src="https://github.com/user-attachments/assets/53f119c5-a641-44b5-b180-75749bb55259" />


#### Step 3: Add Username Payload List

1. Go to **Payloads** tab.
2. Set Payload type to **Simple list**.
3. Paste the candidate usernames from the lab description.
4. Verify the payload count is greater than 0.


#### Step 4: Configure Grep - Extract

1. Go to **Settings** tab.
2. Find **Grep - Extract** → click **Add**.
3. In the response panel, select the full error message: `Invalid username or password.`
4. Click **OK** to save.

<img width="1280" height="684" alt="Screenshot 2026-09-25 221734" src="https://github.com/user-attachments/assets/efe9fca1-6b55-401c-96d8-0f1c8d820ea5" />


#### Step 5: Run the Attack

1. Click **Start attack**.
2. Wait for the attack to finish (Community Edition may take a few minutes).
3. Sort by the extracted column.

**Observation:** The username `arcsight` returned `Invalid username or password` **without a trailing period**, confirming it is a valid username.

<img width="1280" height="684" alt="Screenshot 2026-09-25 222211" src="https://github.com/user-attachments/assets/22dad15d-afbc-4d46-97bf-c0564a98df65" />


#### Step 6: Brute-force the Password

1. Return to **Positions**, clear all positions.
2. Set the `password` value as the new payload position.
3. Update the `username` to `arcsight`.
4. In **Payloads**, replace the list with the candidate passwords.
5. Start the attack again.

**Observation:** The password `austin` returned **Status code 302 (Redirect)**, confirming a successful login.

<img width="1280" height="684" alt="Screenshot 2026-09-25 224202" src="https://github.com/user-attachments/assets/a7febbc1-8073-497b-960f-47da655a54c2" />


#### Step 7: Access the Account

1. Use the credentials `arcsight:austin` to log in.
2. The lab is solved successfully.

<img width="1280" height="684" alt="Screenshot 2026-09-25 224224" src="https://github.com/user-attachments/assets/4d057666-cac1-46c1-851e-e31b22c5c0cc" />

<img width="1280" height="684" alt="Screenshot 2026-09-25 224310" src="https://github.com/user-attachments/assets/695cdbb6-6192-4737-b2fd-ac9873150a26" />


### 🧠 Why This Works

- The server returns slightly different responses for valid vs. invalid usernames.
- Even a subtle difference (a missing period) is enough to enumerate users.
- Combined with a weak password list, this leads to full account takeover.

### 🛡️ Remediation

- Always return **identical** error messages for both invalid usernames and invalid passwords.
- Implement rate limiting and account lockout.
- Use CAPTCHA to prevent automated brute-force attacks.

---

## 🧰 Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite Community Edition** | Intercepting, modifying, and brute-forcing requests |
| **Burp Intruder** | Username enumeration and password brute-force |
| **Burp Grep - Extract** | Detecting subtle response differences |
| **Kali Linux** | Operating system |
| **Firefox (Burp Browser)** | Target interaction |

> ⚠️ **Note:** Burp Suite Community Edition has a rate-limited Intruder. For large brute-force tasks, consider using **Turbo Intruder** or a **Python script**.

---

## 📚 Key Takeaways

1. **Subtle differences matter** — Even a missing punctuation mark can leak valid usernames.
2. **Grep - Extract is powerful** — It helps detect tiny differences across thousands of responses.
3. **Community Edition is enough** — You don't need Burp Pro to solve most Authentication labs.
4. **Always enumerate first** — Username enumeration makes password brute-forcing much easier.

---

## ⚠️ Disclaimer

This repository is created for **educational purposes only**. All labs were solved on **PortSwigger's Web Security Academy** platform, which is designed for legal, ethical hacking practice. Never attempt these techniques on systems you do not own or have explicit permission to test.

---

## 🔗 References

- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Authentication Labs](https://portswigger.net/web-security/authentication)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)

---

## 👤 Author

**Saber Hasan Swoyon**  


⭐ If you found this helpful, consider giving this repository a star!
