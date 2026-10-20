# 💉 SQL Injection

> Injecting SQL syntax into application queries to read, modify, or destroy data behind the application.

[![Category](https://img.shields.io/badge/PortSwigger-SQL%20Injection-FF6633?style=flat)](https://portswigger.net/web-security/sql-injection)
[![Labs solved](https://img.shields.io/badge/Labs%20solved-6-brightgreen?style=flat)]()
[![Planned](https://img.shields.io/badge/Planned-14-blue?style=flat)]()
[![Back to index](https://img.shields.io/badge/←%20Back%20to%20PortSwigger-555?style=flat)](../README.md)

---

## 📌 Why this category matters

SQL injection is the classic data-breach vulnerability. When user input is concatenated into a query string, an attacker controls the grammar of the query — not just a value. That means authentication bypass, cross-table data theft, and in many stacks full file read or RCE.

## 🧠 Attack surface & variants

| Variant | What it means |
|---|---|
| **In-band (UNION)** | Results are returned in the HTTP response; `UNION SELECT` appends an attacker-controlled result set. |
| **In-band (error-based)** | Data extracted from database error messages. |
| **Blind (boolean)** | Response differs only by content/length — infer data one bit at a time. |
| **Blind (time-based)** | No visible difference; measure response delay (`SLEEP(5)`, `pg_sleep()`). |
| **Out-of-band** | Database makes a DNS/HTTP request carrying the data (Collaborator). |
| **Second-order** | Payload stored safely, then executed when later read by another query. |

## 🗺️ Lab roadmap

| # | Lab | Difficulty | Status | Write-up |
|---|-----|------------|--------|----------|
| 01 | SQL injection vulnerability in WHERE clause allowing retrieval of hidden data | 🟢 Apprentice | ✅ Solved | [View](./01-hidden-data-retrieval/README.md) |
| 02 | SQL injection vulnerability allowing login bypass | 🟢 Apprentice | ✅ Solved | [View](./02-login-bypass/README.md) |
| 03 | SQL injection UNION attack, determining the number of columns | 🟠 Practitioner | ✅ Solved | [View](./03-union-determine-columns/README.md) |
| 04 | SQL injection UNION attack, finding a column containing text | 🟠 Practitioner | ✅ Solved | [View](./04-union-find-text-column/README.md) |
| 05 | SQL injection UNION attack, retrieving data from other tables | 🟠 Practitioner | ✅ Solved | [View](./05-union-retrieve-data/README.md) |
| 06 | SQL injection UNION attack, retrieving multiple values in a single column | 🟠 Practitioner | ✅ Solved | [View](./06-union-single-column-multiple-values/README.md) |
| 07 | SQL injection attack, querying the database type and version (MySQL/MSSQL) | 🟠 Practitioner | ⏳ Planned | — |
| 08 | SQL injection attack, listing the database contents on non-Oracle databases | 🟠 Practitioner | ⏳ Planned | — |
| 09 | Blind SQL injection with conditional responses | 🟠 Practitioner | ⏳ Planned | — |
| 10 | Blind SQL injection with conditional errors | 🟠 Practitioner | ⏳ Planned | — |
| 11 | Blind SQL injection with time delays and information retrieval | 🟠 Practitioner | ⏳ Planned | — |
| 12 | Blind SQL injection with out-of-band interaction | 🟠 Practitioner | ⏳ Planned | — |
| 13 | SQL injection with filter bypass via XML encoding | 🔴 Expert | ⏳ Planned | — |

**Difficulty legend:** 🟢 Apprentice · 🟠 Practitioner · 🔴 Expert · ⏳ Planned

## 🔧 Core payload toolkit

```sql
'                       -- break out of a string literal
' OR 1=1--              -- classic boolean bypass
' ORDER BY 3--          -- find column count
' UNION SELECT NULL,NULL,NULL--
' UNION SELECT username,password FROM users--
' UNION SELECT username||':'||password FROM users--   -- concatenation (Oracle/PostgreSQL)
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--
'; WAITFOR DELAY '0:0:10'--                            -- MSSQL time-based
```

## 🛡️ Defences that actually work

| Control | Implementation |
|---|---|
| **Parameterised queries** | Prepared statements with bound parameters — the only complete fix. |
| **Allowlist input** | Sort order, column names and table names cannot be parameterised; map them from a fixed set. |
| **Least privilege DB user** | No `FILE`, no `xp_cmdshell`, no cross-schema reads for the app account. |
| **ORM discipline** | Use the ORM's query builder; never string-format raw SQL. |
| **WAF + monitoring** | Detection layer, not a fix — log and alert on injection patterns. |

## 🔬 Methodology used in every write-up

1. **Map** the request — which parameter reaches a query?
2. **Probe** with `'`, `"`, `--`, `#`, `)` and compare to a control request.
3. **Classify** the DBMS from error text / version banners.
4. **Extract** with UNION, then blind techniques if output is suppressed.
5. **Document** payload, query transformation (before/after), impact, and the fix.

## 📚 References

- [PortSwigger — SQL injection](https://portswigger.net/web-security/sql-injection)
- [PortSwigger SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PayloadsAllTheThings — SQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)

---

> **Disclaimer:** all testing documented here was performed against deliberately vulnerable PortSwigger Academy labs, in an authorised environment. Never test systems you do not own or have written permission to test.
