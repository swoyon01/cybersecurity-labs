# Scripts and test data

This directory contains small helpers used during the authorized Vulnversity lab:

- `extensions.txt` — extension candidates for the upload-filter test.
- `upload.sh` — uploads one local file to the room form and requests the resulting upload URL to verify it.

## Usage

From the repository root on Kali:

```bash
bash ./scripts/upload.sh ./test.phtml 10.112.130.178
```

Replace the IP with the current room target. The script posts the form fields `file` and `submit=Upload`, then sends a GET request to `/internal/uploads/<filename>`.

**Important:** when the file is a reverse-shell payload, start the netcat listener first. The script's final GET triggers the uploaded PHP file. Use only against your own active lab target.

Dependencies: Bash, `curl`, `grep`, `sed`, `head`, and `wc` (commonly available on Kali).
