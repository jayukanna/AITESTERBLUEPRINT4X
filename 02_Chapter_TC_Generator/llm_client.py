"""LLM backend calls: Ollama (local) and Groq (hosted), with provider logic."""

import requests

OLLAMA_MODEL = "gemma3:1b"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class LLMError(Exception):
    """Raised when a provider fails, carrying a user-facing message."""


def generate(config: dict, prompt: str) -> str:
    """Generate a response using the configured provider.

    Provider is one of 'Auto', 'Ollama', 'Groq'.
    Auto tries Ollama first and falls back to Groq when Ollama is
    unreachable or times out. Other modes never fall back silently.
    Raises LLMError with a specific message when generation fails.
    """
    provider = (config.get("LLM_PROVIDER") or "Auto").strip().lower()

    if provider == "groq":
        return _call_groq(config, prompt)
    if provider == "ollama":
        return _call_ollama(config, prompt)

    # Auto: try Ollama, fall back to Groq
    try:
        return _call_ollama(config, prompt)
    except LLMError as ollama_error:
        try:
            return _call_groq(config, prompt)
        except LLMError as groq_error:
            raise LLMError(
                f"Both providers failed. Ollama: {ollama_error} | Groq: {groq_error}"
            ) from None


def _call_ollama(config: dict, prompt: str) -> str:
    base_url = (config.get("OLLAMA_URL") or "http://localhost:11434").rstrip("/")
    token = config.get("OLLAMA_TOKEN")

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }

    try:
        response = requests.post(
            f"{base_url}/api/generate", json=payload, headers=headers, timeout=60
        )
    except requests.exceptions.Timeout:
        raise LLMError(f"Ollama at {base_url} timed out.") from None
    except requests.exceptions.RequestException as exc:
        raise LLMError(f"Could not reach Ollama at {base_url}: {exc}") from None

    if response.status_code != 200:
        raise LLMError(f"Ollama returned HTTP {response.status_code}: {response.text[:300]}")
    data = response.json()
    text = (data.get("response") or "").strip()
    if not text:
        raise LLMError("Ollama returned an empty response.")
    return text


def _call_groq(config: dict, prompt: str) -> str:
    api_key = config.get("GROQ_API_TOKEN")
    if not api_key:
        raise LLMError("Groq API token is not configured in Settings.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }

    try:
        response = requests.post(
            GROQ_API_URL, json=payload, headers=headers, timeout=60
        )
    except requests.exceptions.Timeout:
        raise LLMError("Groq request timed out.") from None
    except requests.exceptions.RequestException as exc:
        raise LLMError(f"Could not reach Groq: {exc}") from None

    if response.status_code != 200:
        raise LLMError(f"Groq returned HTTP {response.status_code}: {response.text[:300]}")
    data = response.json()
    text = (data["choices"][0]["message"]["content"] or "").strip()
    if not text:
        raise LLMError("Groq returned an empty response.")
    return text
