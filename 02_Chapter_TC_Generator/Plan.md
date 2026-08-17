Plan: Jira Test Case Generator App
Objective
Build a lightweight internal QA productivity tool that accepts a Jira ticket key, fetches the issue details from Jira, merges that data into a reusable test case prompt template, sends the prompt to an LLM backend, and renders the generated test cases in a chat-like interface.

Source of truth
This plan is based on RICE-POT_TestCaseGen_Optimized.md and the approved prompt template at testcase_creator.md.

Project structure
app.py
pages/settings.py
config_store.py
jira_client.py
llm_client.py
requirements.txt
.gitignore
.env
templates/
testcase_creator.md
Screen 1: Chat
Purpose:

ChatGPT-style interface with input and Send button
User types a message such as “create test cases for JIRA-102”
App parses the Jira issue key
If no valid key is found, asks the user to provide one
If multiple keys are found, asks which one they meant
Displays the generated test cases in the chat pane
Screen 2: Settings
Purpose:

Persist all runtime configuration values locally
Fields:
Jira URL
Jira Email
Jira API Token
Ollama URL
Ollama Token
Groq API Token
LLM Provider: Auto / Ollama / Groq
Required provider logic
Auto: try Ollama first; if unreachable or timed out, fall back to Groq
Ollama: always use Ollama; do not silently fall back
Groq: always use Groq; skip Ollama
If both are unavailable or misconfigured, show a specific error naming the failed provider and reason
Required end-to-end behavior
Parse a Jira ticket key from the message using the standard pattern
If no ticket key is found, ask for one
If multiple ticket keys are found, ask the user to confirm which one
Fetch the Jira ticket details using the stored Jira credentials
If Jira fetch fails, show the specific error and stop gracefully
Load the test case template from templates/testcase_creator.md
Merge the ticket data into the template
Send the combined prompt to the selected LLM
Render the generated answer in the chat pane in the exact template format
Security and configuration rules
Do not hardcode secrets in source code
Store credentials in a local .env file
Use python-dotenv
Exclude .env from version control with .gitignore
Do not call Groq unless Ollama is unavailable or Groq was explicitly selected
Module responsibilities
app.py
Main chat interface
Reads user input
Parses Jira ticket keys
Calls Jira and LLM flows
Displays results in a chat-like pane
pages/settings.py
Settings page for creds and provider selection
Saves and loads persisted config
config_store.py
Reads and writes .env values
Returns runtime config to the app
jira_client.py
Connects to Jira REST API
Authenticates with email + token
Fetches summary, description, and acceptance criteria
Handles auth, network, and missing-ticket errors cleanly
llm_client.py
Handles both Ollama and Groq calls
Implements provider selection and fallback rules
Sends explicit error messages when providers fail
templates/testcase_creator.md
Contains the strict markdown-table prompt
Defines the exact output contract
Must be used as the authoritative format for the generated test cases
Data flow
User message in chat
→ app.py parses Jira ticket key
→ app.py loads saved configuration
→ jira_client.py fetches issue details from Jira
→ app.py loads the template
→ ticket data is merged into the template
→ llm_client.py selects the provider and sends the final prompt
→ model output is rendered in the chat pane

Implementation phases
Setup and config foundation
Jira integration
LLM integration
Chat UI
Settings UI
Final verification and refinement
Verification checklist
App loads and renders both screens
Valid ticket keys are parsed correctly
Missing or multiple keys produce clear prompts
Jira failures show precise error messages
Ollama fallback works in Auto mode
Groq mode behaves correctly
Ollama-only mode does not fall back silently
Generated output matches the exact table format from the template
Scope decisions
Minimal, internal-tool scope only
No over-engineering or unnecessary abstraction
Default Ollama model is gemma3:1b
Do not re-pull the model
Keep the final output format aligned to the markdown table prompt contract
