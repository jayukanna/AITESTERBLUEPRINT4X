# RICE-POT Prompt — Build the Jira Test Case Generator App (Optimized)



## R - ROLE

You are a senior Python full-stack engineer and AI application architect, experienced in building lightweight internal tools with Streamlit, integrating REST APIs (Jira Cloud/Server), and orchestrating LLM backends across local (Ollama) and hosted (Groq) providers with automatic fallback logic.

---

## I - INSTRUCTIONS

**[Mandatory] Build a two-screen Streamlit application:**
- **Screen 1 — Chat:** A ChatGPT-style interface with a text input box and a Send button. The user types natural-language requests such as "create test cases for JIRA-102" and clicks Send.
- **Screen 2 — Settings:** A configuration screen to input and persist: Jira URL, Jira Email, Jira API Token, Ollama URL, Ollama Token, Groq API Token, and an LLM Provider selector (Auto / Ollama / Groq).

**[Critical] Default LLM backend is Ollama**, model tag `gemma3:1b`, assumed already pulled locally — do not re-pull or re-download it. The endpoint defaults to `http://localhost:11434` but is **configurable** via the `OLLAMA_URL` setting — this build doesn't assume Ollama is always local; if `OLLAMA_URL` points at a remote/hosted Ollama-compatible endpoint, send `OLLAMA_TOKEN` as its auth header.

**[Mandatory] Provider selection logic** — make this explicit in code, don't leave it implicit:
- Provider = **Auto** (default): try Ollama first; if it's unreachable or times out, fall back to Groq automatically.
- Provider = **Ollama**: always use Ollama. If it's unreachable, show an error in the chat pane — do not silently fall back to Groq.
- Provider = **Groq**: always use Groq, skip Ollama entirely.
- **Both unavailable/unconfigured:** show a specific error in the chat pane naming which provider failed and why. Never fail silently or return an empty/fabricated response.

**[Mandatory] End-to-end flow when the user sends a chat message:**
1. Parse a Jira ticket key from the message using a standard key pattern (`[A-Z][A-Z0-9]+-\d+`, e.g. `KAN-2`, `JIRA-102`).
   - No match: ask the user in the chat pane to include a valid ticket key — don't guess one.
   - Multiple matches: ask the user to confirm which one they meant.
2. Fetch ticket details (summary, description, acceptance criteria) via the Jira REST API using the stored credentials.
   - On failure (ticket not found, auth error, network error): show the specific error in the chat pane. Don't crash, and don't fabricate a response as if the fetch had succeeded.
3. Load the test case template from `templates/testcase_creator.md`.
4. Merge the fetched ticket content into the template and send the combined prompt to the selected LLM, per the provider logic above.
5. Render the generated test cases back in the chat pane, in whatever format `templates/testcase_creator.md` actually specifies — don't assume or hardcode a different format in the rendering code than what the template produces.

**[Don't]** Don't hardcode any credentials (Jira token, Ollama token, Groq key) in source code — persist them via a local `.env` file, loaded with `python-dotenv`, excluded from version control via `.gitignore`.

**[Don't]** Don't call Groq unless Ollama is unavailable or the user has explicitly selected it as the provider (see provider selection logic above).

**[Output] Plan first.** Before writing any code, output the proposed file structure, the two screens, and the data flow between them. Wait for my approval. Only then build step by step, one module at a time.

---

## C - CONTEXT

This is an internal QA productivity tool, not a production SaaS product — built as a learning exercise in AI-assisted app development. It exists to take a single Jira ticket and turn it into a test case draft, using either a small local model or a hosted fallback, with minimal setup and no unnecessary abstraction.

---

## E - EXAMPLE

Sample interaction:

> User types: `create test cases for QA-102` → clicks Send → App parses ticket key `QA-102` → fetches it from Jira → merges its description/acceptance criteria into `templates/testcase_creator.md` → sends the combined prompt to Ollama (or Groq, per provider logic) → renders the generated test cases in the chat pane, the same way a ChatGPT response would appear.

---

## P - PARAMETERS

Configured via the Settings screen, persisted to `.env`:

- `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
- `OLLAMA_URL` (default `http://localhost:11434`), `OLLAMA_TOKEN` (optional — only needed if `OLLAMA_URL` points at a non-local, authenticated endpoint)
- `GROQ_API_TOKEN` (fallback provider only)
- Ollama model tag: `gemma3:1b` — fixed in `llm_client.py`, not exposed as a Settings field in this version; already running locally, do not re-pull

---

## O - OUTPUT

Deliver exactly:

- `app.py` — main chat screen
- `pages/settings.py` (or equivalent Streamlit multipage settings screen)
- `config_store.py` — reads/writes `.env` (Jira + Ollama + Groq credentials, provider choice)
- `jira_client.py` — fetches ticket details from the Jira REST API
- `llm_client.py` — handles both Ollama and Groq calls, with the provider/fallback logic above
- `templates/` — folder containing `testcase_creator.md`, the runtime prompt merged with ticket data at generation time
- `requirements.txt`

> **Resolved:** `templates/testcase_creator.md` already exists in the project and holds a strict markdown-table prompt (`ROLE` / `TASK` / `RULES`, columns `Test ID | Description | Pre-conditions | Steps | Expected Result | Priority`) — closely matching `Prompt_1stLevel.md`. That's confirmed as the real runtime prompt going forward; the earlier Gherkin/JSON version that used to live in this file has been discarded. `app.py`'s chat-pane renderer (step 5 under **I - INSTRUCTIONS**) should render this table format, not JSON.

---

## T - TONE

Technical, precise, minimal dependencies, no over-engineered abstractions — working code only, structured clearly enough that each module can be reviewed independently before moving to the next.

---
---


