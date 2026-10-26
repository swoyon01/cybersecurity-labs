# Screenshots / evidence

This folder holds evidence from the Vulnversity lab. The included file `06-suid-bash-permission.png` is the screenshot supplied in the conversation; it shows the service link/enable steps and `/bin/bash` with permissions `-rwsr-xr-x`.

Suggested files to add as you collect proof:

| Filename | Screenshot content |
|---|---|
| `01-nmap-open-ports.png` | Six open ports, including HTTP on 3333 |
| `02-gobuster-internal.png` | Discovery of `/internal/` |
| `03-upload-success.png` | The `.phtml` upload form response |
| `04-reverse-shell-www-data.png` | Netcat connection and `id`/`whoami` as `www-data` |
| `05-user-flag-redacted.png` | User task completed; flag value obscured |
| `06-suid-bash-permission.png` | SUID bit set on `/bin/bash` (included) |
| `07-root-shell-redacted.png` | `id` showing `euid=0(root)`; no flag value visible |
| `08-room-complete.png` | Room completion screen, if desired |

The included screenshot also shows an earlier `Permission denied` when `/root/root.txt` was checked before escalation. The lower portion proves the Bash SUID bit was later set; capture a new screenshot after verifying `euid=0(root)` for final root proof.

Before publishing, review each image and redact flags, passwords, tokens, or any personal details you do not want public.
