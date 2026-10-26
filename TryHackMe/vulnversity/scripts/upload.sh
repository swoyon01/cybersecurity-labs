#!/bin/bash
# upload.sh — upload a file to the Vulnversity internal upload form and verify it landed.
# usage: ./upload.sh <local-file> [machine-ip]
#
# Sends BOTH the "file" field and the "submit" field, because the PHP backend
# gates on isset($_POST['submit']) — without it the file is silently discarded.

set -u

FILE="${1:-}"
IP="${2:-${IP:-}}"

if [ -z "$FILE" ] || [ -z "$IP" ]; then
  echo "usage: $0 <local-file> <machine-ip>"
  echo "   or: export IP=10.10.10.10 && $0 <local-file>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "[!] local file not found: $FILE"
  exit 1
fi

ACTION="http://$IP:3333/internal/index.php"
BASE=$(basename "$FILE")

echo "[*] target : $ACTION"
echo "[*] file   : $FILE  ($(wc -c < "$FILE") bytes)"
echo

RESP=$(curl -s -i --max-time 20 \
        -F "file=@$FILE" \
        -F "submit=Upload" \
        "$ACTION")

echo "[*] HTTP status: $(printf '%s' "$RESP" | head -1 | tr -d '\r')"
echo "[*] response size: $(printf '%s' "$RESP" | wc -c) bytes"
echo

echo "[*] server said:"
printf '%s' "$RESP" | grep -iE 'success|not allowed|extension|error|invalid|uploaded' \
  | sed 's/<[^>]*>//g' | tr -s ' \t' ' ' | head -5
echo

CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
        "http://$IP:3333/internal/uploads/$BASE")

echo "[*] GET /internal/uploads/$BASE -> $CODE"

case "$CODE" in
  200) echo "[+] File is there." ;;
  404) echo "[-] 404: the upload did not land. Check the 'server said' line above." ;;
  403) echo "[?] 403: exists but directory listing/exec is blocked." ;;
  *)   echo "[?] unexpected status $CODE" ;;
esac
