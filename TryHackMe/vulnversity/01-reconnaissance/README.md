# 01 — Reconnaissance

All commands in this section run on the Kali/attacker machine. Use the target IP shown on the active TryHackMe room page; the address below matches the supplied session screenshot.

```bash
export TARGET=$IP
ping -c 3 "$TARGET"
```

`ping -c 3` sends three connectivity checks. If there are no replies, check that the TryHackMe machine is running and the VPN/AttackBox connection is active.

## Scan all TCP ports

```bash
nmap -p- --min-rate 5000 -T4 "$TARGET" -oN nmap-all-ports.txt
```

- `-p-` checks all TCP ports.
- `--min-rate 5000` asks Nmap to scan quickly; omit it on an unstable connection.
- `-T4` uses a faster timing profile for a lab.
- `-oN` saves the output to `nmap-all-ports.txt`.

## Detect services and versions

```bash
nmap -sV -sC -p 21,22,139,445,3128,3333 "$TARGET" -oN nmap-services.txt
```

- `-sV` probes service/version information.
- `-sC` runs Nmap's default scripts.
- `-p` limits the scan to the ports found in the first scan.

Expected open ports for this room:

```text
21/tcp    FTP
22/tcp    SSH
139/tcp   SMB
445/tcp   SMB
3128/tcp  Squid proxy
3333/tcp  Apache HTTP
```

There are **6 open ports**. The web application is on **3333**, not port 80.

## Notes

- Save scan results locally for reference; `.gitignore` excludes `nmap-*.txt` so machine-specific output is not committed by accident.
- The versions observed in this deployment are recorded in the root README. Values may vary if the room changes.
