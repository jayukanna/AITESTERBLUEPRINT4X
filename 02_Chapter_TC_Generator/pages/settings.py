"""Jira Test Case Generator — settings screen."""

import streamlit as st

import config_store


def main() -> None:
    st.set_page_config(page_title="Settings", layout="wide")
    st.title("Settings")

    config = config_store.load_config()

    st.subheader("Jira")
    jira_url = st.text_input("Jira URL", value=config.get("JIRA_URL", ""))
    jira_email = st.text_input("Jira Email", value=config.get("JIRA_EMAIL", ""))
    jira_token = st.text_input(
        "Jira API Token", value=config.get("JIRA_API_TOKEN", ""), type="password"
    )

    st.subheader("Ollama")
    ollama_url = st.text_input(
        "Ollama URL", value=config.get("OLLAMA_URL", "http://localhost:11434")
    )
    ollama_token = st.text_input(
        "Ollama Token (optional)", value=config.get("OLLAMA_TOKEN", ""), type="password"
    )

    st.subheader("Groq (fallback)")
    groq_token = st.text_input(
        "Groq API Token", value=config.get("GROQ_API_TOKEN", ""), type="password"
    )

    st.subheader("LLM Provider")
    provider = st.selectbox(
        "Provider",
        options=["Auto", "Ollama", "Groq"],
        index=["Auto", "Ollama", "Groq"].index(
            config.get("LLM_PROVIDER", "Auto")
            if config.get("LLM_PROVIDER", "Auto") in ["Auto", "Ollama", "Groq"]
            else "Auto"
        ),
    )

    if st.button("Save Settings"):
        config_store.save_config(
            {
                "JIRA_URL": jira_url,
                "JIRA_EMAIL": jira_email,
                "JIRA_API_TOKEN": jira_token,
                "OLLAMA_URL": ollama_url,
                "OLLAMA_TOKEN": ollama_token,
                "GROQ_API_TOKEN": groq_token,
                "LLM_PROVIDER": provider,
            }
        )
        st.success("Settings saved.")


if __name__ == "__main__":
    main()
