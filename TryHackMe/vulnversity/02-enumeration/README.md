# 02 — Enumeration

## Discover directories

Run Gobuster on Kali. Replace `TARGET` if the room has been redeployed.

```bash
export TARGET=10.112.130.178
gobuster dir -u "http://${TARGET}:3333" \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -t 50 -x php,html,txt
```

- `dir` uses directory/file discovery mode.
- `-u` sets the web root URL.
- `-w` supplies the wordlist.
- `-t 50` uses 50 concurrent requests; lower it if needed.
- `-x` also tests the listed file extensions.

Important paths discovered:

```text
http://<TARGET>:3333/internal/
http://<TARGET>:3333/internal/index.php
http://<TARGET>:3333/internal/uploads/
```

Open `http://<TARGET>:3333/internal/index.php` in a browser to view the upload form. The form reports a success message when a file is accepted, but success alone does not execute the file.

## Upload-filter observations

The upload filter blocks `.php` but accepts `.phtml`. The extension candidates used during testing were:

```text
php
php3
php4
php5
phtml
phps
pHp
pht
```

An optional harmless extension probe is documented in the `scripts/` folder. The room's successful bypass was `.phtml`.

## Key takeaway

Directory discovery found the web app on the non-standard port and revealed an unauthenticated upload endpoint. The upload directory is reachable at `/internal/uploads/` and serves the uploaded files.
