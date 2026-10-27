# 🐚 Lab: Remote Code Execution via Web Shell Upload

> **Lab URL:** [PortSwigger Web Security Academy](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload)
> **Category:** File upload vulnerabilities
> **Difficulty:** 🟡 Apprentice
> **Status:** ✅ Solved

---

## 📋 Lab Description

This lab contains a vulnerable image upload function on the user's **My account** page. The application places no real restriction on the type of file that can be uploaded as an avatar: a `.php` file is accepted and stored under a predictable, publicly reachable path. Because the server executes PHP files in that directory, uploading a file containing PHP code and then requesting it directly turns the upload feature into **remote code execution (RCE)**.

To solve the lab, upload a basic PHP web shell as your avatar and use it to read the contents of `/home/carlos/secret`.

The lab-provided credentials are `wiener:peter`.

> **Scope:** This walkthrough is for the intentionally vulnerable PortSwigger training lab only. Do not test these techniques against systems you do not own or have explicit authorization to test.

---

## 🔍 Reconnaissance

### Step 1: Explore the avatar upload feature

1. Log in with `wiener:peter` and go to **My account**.
2. The page has an **Avatar** upload field backed by `POST /my-account/avatar`, which accepts a `multipart/form-data` request.
3. A normal upload (e.g. an actual image file) is accepted and served back from `/files/avatars/<filename>`.

<img width="1280" height="684" alt="Screenshot 2026-10-27 144415" src="https://github.com/user-attachments/assets/faa63040-b03d-4f67-b3a5-52779cc3cd3f" />


### Step 2: Check whether the file type is actually validated

Instead of uploading an image, try selecting a file with a `.php` extension and see whether the client or server blocks it.

<img width="1280" height="684" alt="Screenshot 2026-10-27 145052" src="https://github.com/user-attachments/assets/bd18b660-f8d8-4114-aaa0-1404c075d08c" />


---

## 🚀 Exploitation

### Step 3: Upload a PHP web shell

Intercept the upload request in Burp Suite and replace the file contents with a one-line PHP web shell. Two payloads were tested for this lab:

**Shell 1 — `shall.php` (read the file directly):**
```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

**Shell 2 — `read.php` (stream the file contents):**
```php
<?php readfile('/home/carlos/secret'); ?>
```

Send the request with `filename="shall.php"` and `Content-Type: application/x-php`. The server does not reject the extension or MIME type, and responds confirming the upload:

```
The file avatars/shall.php has been uploaded.
```

<img width="1280" height="684" alt="Screenshot 2026-10-27 150011" src="https://github.com/user-attachments/assets/72338c2c-079e-4cdb-9e9b-13d4cdeeec9d" />


### Step 4: Request the uploaded shell to trigger execution

Because uploaded avatars are served from `/files/avatars/<filename>` and the server executes `.php` files in that path, simply browsing to the uploaded shell runs the embedded PHP code:

```
GET /files/avatars/shall.php
```

The response is the contents of `/home/carlos/secret` — confirming arbitrary file read / code execution on the server.

### Step 5: Confirm with the second payload

The same technique was repeated with the `readfile()` variant, uploaded as `read.php`, to confirm the vulnerability isn't limited to one function:

<img width="1280" height="684" alt="Screenshot 2026-10-27 150914" src="https://github.com/user-attachments/assets/28185a33-734c-4179-b718-543b91d85d1b" />


<img width="1280" height="684" alt="Screenshot 2026-10-27 151424" src="https://github.com/user-attachments/assets/8a5ee070-ed39-4c1b-b86d-515ed544f44f" />


### Step 6: Lab solved

Submitting the leaked secret value confirms the lab is solved.

<img width="1280" height="684" alt="Screenshot 2026-10-27 150358" src="https://github.com/user-attachments/assets/cb6506b5-9259-4f15-89d7-db171740d381" />


---

## 🔄 Attack Flow Summary

| Step | Action | Expected result |
|---|---|---|
| 1 | Inspect the avatar upload feature (`POST /my-account/avatar`) | Uploaded files served from `/files/avatars/<filename>` |
| 2 | Attempt to upload a `.php` file instead of an image | No server-side extension/content-type filtering |
| 3 | Upload a PHP web shell (`file_get_contents()` or `readfile()`) as the avatar | `200 OK` — "The file avatars/\<name\>.php has been uploaded." |
| 4 | Request the uploaded shell directly (`GET /files/avatars/<name>.php`) | PHP code executes on the server |
| 5 | Read `/home/carlos/secret` via the shell | Secret value disclosed |
| 6 | Submit the secret | Lab solved |

---

## 🧠 Key Takeaways

### 1. Root cause

The avatar upload endpoint does not validate the uploaded file's extension or content. Any file type — including server-executable PHP — is accepted and written into a directory that the web server will execute. There is no separation between "user-uploaded content" and "code the server will run."

### 2. Impact

An authenticated, unprivileged user can obtain **full remote code execution** on the server by uploading and then invoking a web shell, with no need for an existing injection point elsewhere in the app. This gives an attacker read/write access to the filesystem and the ability to run arbitrary commands, depending on what the shell does — here, enough to read `/home/carlos/secret`.

### 3. Mitigation strategies

| Defense | Recommendation |
|---|---|
| **Validate file type server-side** | Check both the file extension and the actual file content (magic bytes), never trust the client-supplied `Content-Type` alone. |
| **Use an allow-list, not a block-list** | Only permit a small, known-safe set of extensions (e.g. `.jpg`, `.png`, `.gif`). |
| **Never execute uploaded files** | Store uploads outside the webroot, or in a location configured to never execute scripts (disable script execution for the uploads directory). |
| **Rename uploads** | Store files under a generated/random name unrelated to the user-supplied filename, and don't preserve the original extension blindly. |
| **Serve uploads from a separate origin/domain with no execution rights** | Removes the ability to execute uploaded code even if a malicious file is stored. |
| **Principle of least privilege** | The web server process should not have permission to read sensitive files such as `/home/carlos/secret` in the first place. |

---

## 📚 References

- [PortSwigger — File upload vulnerabilities](https://portswigger.net/web-security/file-upload)
- [PortSwigger — Remote code execution via web shell upload (lab)](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload)
- [OWASP — Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)

---

## 📸 Screenshots

All screenshots live in [`./screenshots`](./screenshots), in the order referenced above:

1. `01-avatar-upload-form.png` — the avatar upload feature on My Account
2. `02-selecting-shell-file.png` — selecting a `.php` file for upload
3. `03-upload-shell1-file_get_contents.png` — Burp Repeater: uploading `shall.php` (`file_get_contents()` payload) and the server's acceptance response
4. `04-lab-solved.png` — lab marked as solved
5. `05-upload-shell2-readfile-response.png` — Burp Repeater: requesting the second shell (`readfile()` payload)
6. `06-secret-retrieved.png` — the secret value returned directly by the uploaded shell

> 📝 **Author:** Saber Hasan Swoyon
> 📅 **Date solved:** 2026-10-27
