# GlobalSpeak (Eel UI)

Modern, clean desktop app using Python + Eel with three pages: Dashboard, Translator, Assistant.

## Run

1. Create venv (recommended) and install deps:

```
pip install -r requirements.txt
```

2. (Optional) Set OpenAI key to power the Assistant (fallback is local heuristic):

- Windows PowerShell
```
$env:OPENAI_API_KEY = "sk-..."
```

3. Start app:

```
python main.py
```

## Structure

- `main.py` – Eel entrypoint and exposed functions `translate()` and `assistant_reply()`
- `web/` – UI assets
  - `index.html` – Dashboard
  - `translator.html` – Translator UI (uses `eel.translate`)
  - `assistant.html` – Chat UI with custom prompt (uses `eel.assistant_reply`)
  - `styles.css` – Minimal design tokens
  - `app.js` – Shared client behaviors

## Notes

- Translator uses the public `translate.googleapis.com` endpoint. For heavy usage, consider a paid API.
- Assistant uses OpenAI if `OPENAI_API_KEY` is set; otherwise a concise local fallback.
