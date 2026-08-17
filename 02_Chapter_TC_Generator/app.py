"""Jira Test Case Generator — main chat screen."""

import os
import re

import streamlit as st

import config_store
import jira_client
import llm_client

TICKET_KEY_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")
TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates", "testcase_creator.md"
)


def load_template() -> str:
    with open(TEMPLATE_PATH, encoding="utf-8") as fh:
        return fh.read()


def find_ticket_keys(message: str) -> list:
    return TICKET_KEY_PATTERN.findall(message)


def build_prompt(template: str, ticket: dict, count: int) -> str:
    requirements = (
        f"Ticket: {ticket['key']} - {ticket['summary']}\n\n"
        f"Description:\n{ticket['description']}\n\n"
        f"Acceptance Criteria:\n{ticket['acceptance_criteria']}"
    )
    return template.replace("[NUMBER]", str(count)).replace(
        "[PASTE REQUIREMENTS HERE]", requirements
    )


def render_ticket_request(key: str, config: dict) -> str:
    """Fetch a ticket, build the prompt, call the LLM, return the raw response."""
    ticket = jira_client.fetch_ticket(config, key)
    template = load_template()
    count = 10  # default number of test cases per generation
    prompt = build_prompt(template, ticket, count)
    return llm_client.generate(config, prompt)


def handle_message(message: str) -> None:
    keys = find_ticket_keys(message)
    if not keys:
        st.session_state.pending_key = None
        st.chat_message("assistant").write(
            "I couldn't find a Jira ticket key in your message. "
            "Please include one, e.g. `JIRA-102` or `QA-102`."
        )
        return

    if len(keys) == 1:
        _process_key(keys[0])
        return

    # Multiple keys: ask the user to confirm which one.
    st.session_state.pending_key = None
    st.session_state.pending_choices = keys
    st.chat_message("assistant").write(
        f"I found multiple ticket keys: {', '.join(keys)}. "
        "Which one would you like test cases for?"
    )


def _process_key(key: str) -> None:
    st.session_state.pending_key = None
    st.session_state.pending_choices = None
    config = config_store.load_config()

    with st.spinner(f"Fetching {key} from Jira..."):
        try:
            ticket = jira_client.fetch_ticket(config, key)
        except jira_client.JiraError as exc:
            st.chat_message("assistant").error(str(exc))
            return

    with st.spinner("Generating test cases..."):
        try:
            template = load_template()
            prompt = build_prompt(template, ticket, 10)
            result = llm_client.generate(config, prompt)
        except llm_client.LLMError as exc:
            st.chat_message("assistant").error(str(exc))
            return

    st.chat_message("assistant").markdown(result)


def handle_reply(text: str) -> None:
    """Resolve a pending multiple-key confirmation."""
    choices = st.session_state.get("pending_choices") or []
    choice = next((k for k in choices if k.lower() in text.lower()), None)
    if choice:
        _process_key(choice)
    else:
        st.chat_message("assistant").write(
            f"I didn't recognize that ticket key. Please choose one of: "
            f"{', '.join(choices)}."
        )


def main() -> None:
    st.set_page_config(page_title="Jira Test Case Generator", layout="wide")
    st.title("Jira Test Case Generator")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_choices" not in st.session_state:
        st.session_state.pending_choices = None

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Type a message, e.g. 'create test cases for JIRA-102'")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.get("pending_choices"):
            handle_reply(prompt)
        else:
            handle_message(prompt)


if __name__ == "__main__":
    main()
