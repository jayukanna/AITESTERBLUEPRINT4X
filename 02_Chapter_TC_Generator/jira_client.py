"""Fetch Jira ticket details via the Jira Cloud REST API."""

import requests

ACCEPTANCE_CRITERIA_FIELD = "customfield_10044"  # Jira Cloud native Acceptance Criteria field


class JiraError(Exception):
    """Raised when a ticket cannot be fetched, with a user-facing message."""


def fetch_ticket(config: dict, issue_key: str) -> dict:
    """Fetch summary, description and acceptance criteria for a Jira issue.

    Returns a dict with 'summary', 'description', 'acceptance_criteria' and
    'url'. Raises JiraError with a specific message on any failure.
    """
    jira_url = (config.get("JIRA_URL") or "").rstrip("/")
    if not jira_url:
        raise JiraError("Jira URL is not configured. Set it in Settings first.")

    email = config.get("JIRA_EMAIL")
    token = config.get("JIRA_API_TOKEN")
    if not email or not token:
        raise JiraError("Jira credentials are not configured. Set them in Settings first.")

    endpoint = f"{jira_url}/rest/api/3/issue/{issue_key}"
    try:
        response = requests.get(
            endpoint,
            auth=(email, token),
            headers={"Accept": "application/json"},
            timeout=15,
        )
    except requests.exceptions.Timeout:
        raise JiraError(f"Jira request for {issue_key} timed out.") from None
    except requests.exceptions.RequestException as exc:
        raise JiraError(f"Could not reach Jira at {jira_url}: {exc}") from None

    if response.status_code == 404:
        raise JiraError(f"Ticket {issue_key} was not found in Jira.")
    if response.status_code == 401 or response.status_code == 403:
        raise JiraError(
            "Jira authentication failed. Check your Jira email and API token in Settings."
        )
    if response.status_code != 200:
        raise JiraError(
            f"Jira returned HTTP {response.status_code} for {issue_key}: "
            f"{response.text[:300]}"
        )

    data = response.json()
    fields = data.get("fields", {})

    summary = fields.get("summary") or "Not specified"
    description = fields.get("description")
    description = _plain_text(description) if description else "Not specified"

    acceptance = fields.get(ACCEPTANCE_CRITERIA_FIELD)
    if not acceptance:
        acceptance = fields.get("customfield_10044")
    acceptance_criteria = _plain_text(acceptance) if acceptance else "Not specified"

    return {
        "key": issue_key,
        "summary": summary,
        "description": description,
        "acceptance_criteria": acceptance_criteria,
        "url": f"{jira_url}/browse/{issue_key}",
    }


def _plain_text(content) -> str:
    """Convert a Jira ADF (Atlassian Document Format) node to plain text."""
    if isinstance(content, str):
        return content
    if not isinstance(content, dict):
        return str(content)
    parts = []
    for node in content.get("content", []):
        if node.get("type") == "text":
            parts.append(node.get("text", ""))
        elif "content" in node:
            parts.append(_plain_text(node))
        elif node.get("type") == "codeBlock":
            parts.append(_plain_text(node))
    text = " ".join(part.strip() for part in parts if part.strip())
    return text or "Not specified"
