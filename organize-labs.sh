#!/usr/bin/env bash
# Reorganise PortSwigger labs into vulnerability categories WITHOUT deleting anything.
# git mv keeps file history (GitHub shows these as renames, not delete+add).
#
#   bash organize-labs.sh            # dry run (default)
#   bash organize-labs.sh --apply    # do it
set -euo pipefail

APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "✗ Not a git repository. Run this from inside cybersecurity-labs."; exit 1
fi

CATEGORIES=(
  SQL-Injection Authentication XSS-Cross-Site-Scripting JWT-Attacks File-Upload
  File-Path-Traversal OS-Command-Injection Access-Control SSRF XXE CSRF
  Information-Disclosure Business-Logic
)

MOVES=(
  "sqli-hidden-data|SQL-Injection|01-hidden-data-retrieval"
  "sqli-login-bypass|SQL-Injection|02-login-bypass"
  "sqli-union-columns|SQL-Injection|03-union-determine-columns"
  "sqli-union-text-column|SQL-Injection|04-union-find-text-column"
  "sqli-union-retrieve-data|SQL-Injection|05-union-retrieve-data"
  "sqli-union-single-column|SQL-Injection|06-union-single-column-multiple-values"
  "auth-username-enum-different-responses|Authentication|01-username-enum-different-responses"
  "auth-username-enum-subtly-different-responses|Authentication|02-username-enum-subtly-different-responses"
  "auth-password-reset-broken-logic|Authentication|03-password-reset-broken-logic"
  "auth-username-enum-response-timing|Authentication|04-username-enum-response-timing"
)

echo "==> Creating category folders"
for c in "${CATEGORIES[@]}"; do
  if [[ $APPLY -eq 1 ]]; then mkdir -p "PortSwigger/$c"; fi
  echo "   PortSwigger/$c"
done

echo
echo "==> Moving labs"
for row in "${MOVES[@]}"; do
  IFS='|' read -r old cat new <<< "$row"
  src="PortSwigger/$old"; dst="PortSwigger/$cat/$new"
  if [[ -d "$dst" && ! -d "$src" ]]; then
    echo "   skip   $dst (already moved)"; continue
  fi
  if [[ ! -d "$src" ]]; then
    echo "   !!     missing $src — check the folder name"; continue
  fi
  echo "   $src  ->  $dst"
  if [[ $APPLY -eq 1 ]]; then git mv "$src" "$dst"; fi
done

echo
if [[ $APPLY -eq 1 ]]; then
  echo "✓ Done. Review with:"
  echo "    git status            # expect R (renames), no D (deletions)"
  echo "    git log --oneline -1"
  echo
  echo "Next: copy the new README files from the portfolio zip, then"
  echo "    git add -A && git commit -m \"Reorganise PortSwigger labs by category\" && git push"
else
  echo "Dry run only. Re-run with --apply to perform the moves."
fi
