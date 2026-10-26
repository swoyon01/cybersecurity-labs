# 06 — Flags

Flag values are intentionally **not** stored in this public write-up. TryHackMe generates values for the active deployment; record them locally and submit them on the room page.

| Flag | Target path | Value |
|---|---|---|
| User | `/home/bill/user.txt` | Not published |
| Root | `/root/root.txt` | Not published |

Commands to read them from the appropriate remote shell:

```sh
cat /home/bill/user.txt
cat /root/root.txt
```

For the root file, first verify the privileged shell with `id` and confirm `euid=0(root)`. Do not place flag values in screenshots or commit them to a public GitHub repository.
