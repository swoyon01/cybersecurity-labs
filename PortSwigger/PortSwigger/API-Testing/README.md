# PortSwigger Web Security Academy — API Testing

**Official topic:** API Testing (5 labs)
**Lab source:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/api-testing)

This folder holds my write-ups for the PortSwigger API Testing labs. Each write-up uses the template in [`templates/lab-writeup-template.md`](../../templates/lab-writeup-template.md).

---

## 🧪 Lab Checklist

| # | Lab | Level | Related topic folder | Status | Write-up |
|:-:|-----|:-----:|----------------------|:------:|----------|
| 1 | Exploiting an API endpoint using documentation | Apprentice | [`09-recon`](../../09-recon/) | ⬜ | `labs/portswigger-api-endpoint-documentation.md` |
| 2 | Finding and exploiting an unused API endpoint | Practitioner | [`09-recon`](../../09-recon/) | ⬜ | `labs/portswigger-unused-api-endpoint.md` |
| 3 | Exploiting a mass assignment vulnerability | Practitioner | [`04-authorization`](../../04-authorization/) | ⬜ | `labs/portswigger-mass-assignment.md` |
| 4 | Exploiting server-side parameter pollution in a query string | Practitioner | [`05-common-vulnerabilities`](../../05-common-vulnerabilities/) | ⬜ | `labs/portswigger-ssppl-query-string.md` |
| 5 | Exploiting server-side parameter pollution in a REST URL | Expert | [`05-common-vulnerabilities`](../../05-common-vulnerabilities/) | ⬜ | `labs/portswigger-ssppl-rest-url.md` |

**Progress:** `0 / 5 solved`

> When you finish a lab, change ⬜ to ✅, save the write-up in `labs/` with the file name shown, and update the main README.

---

## 🧭 What Each Lab Teaches

1. **Documentation:** API docs can reveal endpoints and methods you would not find otherwise. Use them as a map.
2. **Unused endpoint:** a forgotten endpoint may still work and may lack the checks of the main API.
3. **Mass assignment:** the server may accept fields the client should not control, such as discounts or roles.
4. **Parameter pollution (query string):** characters such as `#` can change how the server builds its internal request.
5. **Parameter pollution (REST URL):** path traversal inside a parameter can reach internal API endpoints.

---

## 🔁 Key Techniques to Practise

- Reading API documentation and JavaScript files for endpoints
- Using `OPTIONS` to list allowed methods
- Changing request bodies to add fields the UI never sends
- URL-encoding special characters (`#` becomes `%23`) and testing how the server parses them

---

## ✅ Done When

- All 5 labs are solved and written up.
- Each write-up includes the exact request that solved the lab and the mitigation.
- The topic folders listed above link to the matching write-ups.
