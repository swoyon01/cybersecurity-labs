# 🚚 Moving the old repository to the new layout (nothing deleted)

You do **not** need to delete and re-upload your labs. `git mv` is a rename: GitHub records it as `R  old/path → new/path`, and every commit, blame line and file history follows the file into its new folder.

Pick **one** of the three options below.

---

## Option A — Keep the old repo untouched, push the new one as v2 ✅ recommended

Your current `cybersecurity-labs` stays exactly as it is, forever. The clean version becomes a second repo.

```bash
# 1. On GitHub: https://github.com/new
#    Name: cybersecurity-labs-v2   ·   Public   ·   NO README, NO .gitignore, NO license

# 2. Locally, in the unzipped organised folder
cd cybersecurity-labs
git init
git branch -M main
git remote add origin https://github.com/swoyon01/cybersecurity-labs-v2.git
git add -A
git commit -m "Portfolio v2: PortSwigger labs organised by vulnerability category"
git push -u origin main
```

Then archive the old one so nobody lands on the outdated layout:
**old repo → Settings → Danger Zone → Archive this repository** (read-only, nothing lost).

> If git asks for a password, use a **Personal Access Token**: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → scope `repo`.

---

## Option B — Same repo, old layout preserved on a branch

```bash
cd cybersecurity-labs          # your clone
git pull

git checkout -b backup-before-reorg    # snapshot of the current flat layout
git push origin backup-before-reorg

git checkout main
# now copy the organised structure over your working tree, then:
git add -A
git commit -m "Reorganise PortSwigger labs by vulnerability category"
git push origin main
```

On GitHub the branch dropdown now shows `main` (organised) and `backup-before-reorg` (original). Nothing is deleted; you can always `git checkout backup-before-reorg` to see the old tree.

---

## Option C — Rename the old repo, reuse the name

1. Old repo → **Settings → Repository name** → rename to `cybersecurity-labs-v1`.
2. Create a fresh `cybersecurity-labs` and push the organised version (commands from Option A).
3. Old commits and files live on under the `-v1` name.

---

## Why deleting and re-uploading is the wrong move

| Delete & re-upload | `git mv` (rename) |
|---|---|
| Every file loses its history — write-ups look like they were created today | History follows the file: `git log --follow` still works |
| Your commit graph shows one giant "initial commit" | Graph shows a normal incremental project |
| Broken internal links go unnoticed | Links are verifiable in the diff |
| ~1 min per folder manually | One script, idempotent, seconds |

---

## If you prefer doing it by hand in your own clone

Run [`organize-labs.sh`](./organize-labs.sh) from the repo root — it performs exactly the moves below and is safe to re-run:

```bash
bash organize-labs.sh          # preview
bash organize-labs.sh --apply  # perform the moves
```

| Old path | New path |
|---|---|
| `PortSwigger/sqli-hidden-data` | `PortSwigger/SQL-Injection/01-hidden-data-retrieval` |
| `PortSwigger/sqli-login-bypass` | `PortSwigger/SQL-Injection/02-login-bypass` |
| `PortSwigger/sqli-union-columns` | `PortSwigger/SQL-Injection/03-union-determine-columns` |
| `PortSwigger/sqli-union-text-column` | `PortSwigger/SQL-Injection/04-union-find-text-column` |
| `PortSwigger/sqli-union-retrieve-data` | `PortSwigger/SQL-Injection/05-union-retrieve-data` |
| `PortSwigger/sqli-union-single-column` | `PortSwigger/SQL-Injection/06-union-single-column-multiple-values` |
| `PortSwigger/auth-username-enum-different-responses` | `PortSwigger/Authentication/01-username-enum-different-responses` |
| `PortSwigger/auth-username-enum-subtly-different-responses` | `PortSwigger/Authentication/02-username-enum-subtly-different-responses` |
| `PortSwigger/auth-password-reset-broken-logic` | `PortSwigger/Authentication/03-password-reset-broken-logic` |
| `PortSwigger/auth-username-enum-response-timing` | `PortSwigger/Authentication/04-username-enum-response-timing` |

---

## Verify before pushing

```bash
git status                     # every entry should read  R  old -> new
git log --follow PortSwigger/SQL-Injection/01-hidden-data-retrieval/README.md
# check for broken relative links
grep -rn "](\." --include=*.md . | head
```

Nothing should report `D` (deleted) unless you intentionally removed a file.
