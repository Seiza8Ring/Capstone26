import os
import json
import eel
import socket
import requests

# Optional: OpenAI support if key is set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are GlobalSpeak Assistant: a concise, helpful multilingual AI that assists with language learning, translation tips, and communication guidance. "
    "Be friendly, brief, and provide examples. Avoid unsafe or disallowed content."
)

@eel.expose
def translate(text: str, target: str) -> dict:
    try:
        if not text.strip():
            return {"ok": False, "error": "Empty text"}
        if not target:
            target = "en"
        url = (
            "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto"
            f"&tl={target}&dt=t&q=" + requests.utils.quote(text)
        )
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        translated = "".join([seg[0] for seg in data[0]])
        src_lang = data[2] if len(data) > 2 else "auto"
        return {"ok": True, "text": translated, "detected": src_lang}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _assistant_fallback(messages: list, system_prompt: str) -> str:
    # Simple local heuristic fallback: echo with guidance
    last_user = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
    guidance = "Here is a concise response based on your request."
    if "translate" in last_user.lower():
        guidance = "Here are translation tips and a brief answer."
    return f"{guidance}\n\n{last_user[:400]}"

@eel.expose
def assistant_reply(messages_json: str, system_prompt: str = None) -> dict:
    try:
        messages = json.loads(messages_json) if isinstance(messages_json, str) else messages_json
    except Exception:
        return {"ok": False, "error": "Invalid messages payload"}

    system_prompt = system_prompt or SYSTEM_PROMPT

    # Try OpenAI if available
    if OPENAI_API_KEY:
        try:
            import openai  # type: ignore
            openai.api_key = OPENAI_API_KEY
            # Compose messages for Chat API
            chat_messages = [{"role": "system", "content": system_prompt}] + messages
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_messages,
                temperature=0.3,
            )
            content = completion["choices"][0]["message"]["content"]
            return {"ok": True, "text": content}
        except Exception as e:
            # Fall back to local if OpenAI fails
            return {"ok": True, "text": _assistant_fallback(messages, system_prompt), "note": f"fallback: {e}"}

    # Local fallback
    return {"ok": True, "text": _assistant_fallback(messages, system_prompt)}


def _pick_browser_mode() -> str | None:
    """Detect a preferred browser (Brave/Chrome) on Windows for Eel.
    Returns 'chrome' if a Chromium-based browser is found and registered via eel.browsers,
    otherwise returns None to let Eel open the system default browser.
    """
    try:
        if os.name == "nt":
            candidates = [
                r"C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                r"C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            ]
            for path in candidates:
                if os.path.exists(path):
                    # Use Chromium-compatible launcher in Eel
                    eel.browsers.set_path("chrome", path)
                    return "chrome"
        # Non-Windows or not found: let Eel/webbrowser choose default
        return None
    except Exception:
        return None

def main():
    web_dir = os.path.join(os.path.dirname(__file__), "web")
    eel.init(web_dir)

    # Pick a free port to avoid collisions
    def get_free_port() -> int:
        s = socket.socket()
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    port = get_free_port()

    # Choose Chrome/Brave app mode if available; else default browser
    browser_mode = _pick_browser_mode()
    mode = 'chrome-app' if browser_mode == 'chrome' else None
    cmdline_args = [
        '--new-window',
        '--disable-translate',
        '--disable-features=TranslateUI',
        '--force-device-scale-factor=1',
        '--window-size=955,646',
    ] if mode else None

    eel.start(
        'index.html',
        host='127.0.0.1',
        port=port,
        mode=mode,
        cmdline_args=cmdline_args,
        size=(955, 646),
    )


if __name__ == "__main__":
    main()