"""Diagnose Jira auth/permission issues.

Run from the project folder:   python jira_diagnose.py
Prints the real HTTP status for each call so we can tell WHY the 404 happens.
Safe to delete afterwards. Prints only a masked token.
"""

import requests

import config_store

config = config_store.load_config()
base = (config.get("JIRA_URL") or "").rstrip("/")
email = config.get("JIRA_EMAIL") or ""
token = config.get("JIRA_API_TOKEN") or ""
auth = (email, token)
headers = {"Accept": "application/json"}

print("=" * 60)
print(f"Base URL : {base!r}")
print(f"Email    : {email!r}")
print(f"Token    : len={len(token)}  starts={token[:10]!r}  ends={token[-6:]!r}")
print("=" * 60)


def call(label, path):
    url = base + path
    try:
        r = requests.get(url, auth=auth, headers=headers, timeout=20)
    except Exception as exc:  # noqa: BLE001
        print(f"\n[{label}] {path}\n  ERROR {type(exc).__name__}: {exc}")
        return None
    print(f"\n[{label}] {path}\n  HTTP {r.status_code}")
    body = r.text[:400].replace("\n", " ")
    print(f"  {body}")
    return r


# 1. Does authentication work at all?
me = call("AUTH CHECK", "/rest/api/3/myself")
if me is not None and me.status_code == 200:
    data = me.json()
    print(f"  --> Authenticated as: {data.get('emailAddress')} / {data.get('displayName')}")

# 2. Which projects can this token actually see?
projects = call("PROJECTS", "/rest/api/3/project/search?maxResults=50")
if projects is not None and projects.status_code == 200:
    keys = [p["key"] for p in projects.json().get("values", [])]
    print(f"  --> Visible project keys: {keys}")
    print(f"  --> Is 'KAN' visible? {'KAN' in keys}")

# 3. The actual failing call.
call("ISSUE KAN-2", "/rest/api/3/issue/KAN-2")

# 4. Search — distinguishes 'no permission' from 'wrong key'.
call("SEARCH KAN", "/rest/api/3/search/jql?jql=project%3DKAN&maxResults=5")

print("\n" + "=" * 60)
print("HOW TO READ THIS:")
print("  AUTH CHECK 200 + ISSUE 404  -> auth is fine; permission or wrong site/key")
print("  AUTH CHECK 401             -> API token invalid/revoked, or scoped-token issue")
print("  AUTH CHECK 200 but KAN not in project list -> account can't browse that project")
print("=" * 60)
