"""
Pinterest Auto-Publisher for @guzelaicom (archzencir@gmail.com) — Sesli Lüks Hayatlar (@Sesliluksbot)
-----------------------------------------------------------------------------------------------------
Her üretilen çok açılı lüks milyoner Reels konseptini ve 9:16 insan/yaşam karelerini:
1) Pinterest SEO uyumlu Başlık (<=100 karakter), Açıklama (<=500 karakter), Hedef Link (https://guzelai.com/#kombinler)
   ve zorunlu #reklam #işbirliğiyoktur ibaresiyle `output/pinterest_pin.json` ve `output/pinterest_pin.txt` olarak kaydeder.
2) Yerel kalıcı Chrome profili (`C:\\Users\\zenci\\.gemini\\antigravity\\scratch\\pinterest_chrome_profile`, port 9232)
   üzerinden doğrudan `@guzelaicom` (`https://tr.pinterest.com/guzelaicom/`) hesabına Pin olarak yükler.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PINTEREST_ACCOUNT_HANDLE = "guzelaicom"
PINTEREST_PROFILE_URL = "https://tr.pinterest.com/guzelaicom/"
PINTEREST_BOARD_URL = "https://tr.pinterest.com/thezencirs/guzelaicom/"
PINTEREST_EMAIL = os.environ.get("PINTEREST_EMAIL", "archzencir@gmail.com")
PINTEREST_PASSWORD = os.environ.get("PINTEREST_PASSWORD", "K@rd3s.34-48/mugla")
PINTEREST_CDP_PORT = 9232
PINTEREST_PROFILE_DIR = Path(r"C:\Users\zenci\.gemini\antigravity\scratch\pinterest_chrome_profile")


def build_luxury_pinterest_pin_data(concept: Dict[str, Any]) -> Dict[str, Any]:
    """Lüks & Milyoner konsepti için @guzelaicom Pinterest Pin SEO verisini hazırlar."""
    raw_title = (
        concept.get("title")
        or concept.get("cover_headline")
        or "Milyoner & Lüks Yaşam Seçkisi | GüzelAI.com"
    )
    loc = concept.get("location_name", "Monaco & Como")
    pin_title = f"{raw_title} • {loc}"[:100]

    items = concept.get("items") or {}
    first_item = next(iter(items.values()), {}) if isinstance(items, dict) else {}
    hero_brand = str(first_item.get("brand", "Pırlanta & Saat")).strip()
    hero_name = str(first_item.get("name", "Lüks Seçki")).strip()
    hero_price = str(first_item.get("price", "")).strip()
    hero_sku = str(first_item.get("sku", "")).strip()

    desc_lines = [
        f"✨ {raw_title} ({loc})",
        f"💎 Öne Çıkan: {hero_brand} – {hero_name} ({hero_price})",
        "🌐 Tüm Videolar, Çok Açılı Görseller & Mağaza Linkleri: https://guzelai.com/#kombinler",
        "📲 Telegram: https://t.me/Sesliluksbot",
        "⚠️ İş birliği yoktur, lüks yaşam ve stil seçkisidir (#reklam #işbirliğiyoktur).",
        "#lüksyaşam #oldmoney #milyoner #pırlanta #luksaraba #luksotel #guzelaicom #reklam",
    ]
    description = "\n".join(desc_lines)[:495]

    dest_link = f"https://guzelai.com/go/{hero_sku}" if hero_sku else "https://guzelai.com/#kombinler"

    return {
        "account_handle": PINTEREST_ACCOUNT_HANDLE,
        "account_url": PINTEREST_PROFILE_URL,
        "board_url": PINTEREST_BOARD_URL,
        "account_email": PINTEREST_EMAIL,
        "title": pin_title,
        "description": description,
        "destination_link": dest_link,
        "showcase_url": "https://guzelai.com/#kombinler",
        "board_name": "Lüks Yaşam & Kombin Vitrini",
        "alt_text": f"{raw_title} - {hero_brand} {hero_name} (@guzelaicom Pinterest)",
    }


def save_luxury_pinterest_outputs(concept: Dict[str, Any], out_dir: str = "output") -> Dict[str, Any]:
    os.makedirs(out_dir, exist_ok=True)
    pin_data = build_luxury_pinterest_pin_data(concept)
    cid = str(concept.get("id", "luxury_pin")).strip()

    for fname_json in ("pinterest_pin.json", f"{cid}_pinterest_pin.json"):
        p_json = Path(out_dir) / fname_json
        p_json.write_text(json.dumps(pin_data, ensure_ascii=False, indent=2), encoding="utf-8")

    txt_content = (
        f"HESAP: @{PINTEREST_ACCOUNT_HANDLE} ({PINTEREST_PROFILE_URL})\n"
        f"BAŞLIK: {pin_data['title']}\n"
        f"HEDEF LİNK: {pin_data['destination_link']}\n"
        f"VİTRİN: {pin_data['showcase_url']}\n"
        f"PANO: {pin_data['board_name']}\n\n"
        f"AÇIKLAMA:\n{pin_data['description']}\n"
    )
    for fname_txt in ("pinterest_pin.txt", f"{cid}_pinterest_pin.txt"):
        p_txt = Path(out_dir) / fname_txt
        p_txt.write_text(txt_content, encoding="utf-8")

    return pin_data


def _ensure_pinterest_chrome(port: int = PINTEREST_CDP_PORT, profile_dir: Path = PINTEREST_PROFILE_DIR) -> Optional[str]:
    chrome_exe = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    if not chrome_exe.exists():
        return None
    profile_dir.mkdir(parents=True, exist_ok=True)
    tabs = []
    try:
        tabs = requests.get(f"http://127.0.0.1:{port}/json", timeout=2).json()
    except Exception:
        chrome_cmd = (
            f'"{chrome_exe}" '
            f"--remote-debugging-port={port} "
            f"--remote-allow-origins=* "
            f'--user-data-dir="{profile_dir}" '
            f"--no-first-run --no-default-browser-check "
            f"--disable-blink-features=AutomationControlled "
            f'--window-size=1180,900 "https://tr.pinterest.com/pin-creation-tool/"'
        )
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList '{chrome_cmd}'",
            ],
            capture_output=True,
        )
        for _ in range(12):
            time.sleep(1)
            try:
                tabs = requests.get(f"http://127.0.0.1:{port}/json", timeout=2).json()
                if any(t.get("type") == "page" for t in tabs):
                    break
            except Exception:
                pass
    page_tab = next((t for t in tabs if t.get("type") == "page"), None)
    return page_tab.get("webSocketDebuggerUrl") if page_tab else None


def publish_luxury_to_pinterest(
    concept: Dict[str, Any],
    out_dir: str = "output",
    media_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    1) Pinterest Pin SEO paketini (`pinterest_pin.json` ve `pinterest_pin.txt`) kaydeder.
    2) Yerel Chrome CDP profili (`pinterest_chrome_profile`) açıksa veya başlatılabiliyorsa
       `@guzelaicom` Pinterest hesabında Pin oluşturma aracına yükler.
    """
    pin_data = save_luxury_pinterest_outputs(concept, out_dir=out_dir)

    m_frames = concept.get("model_frames") or []
    chosen_media: Optional[Path] = None
    if media_path and Path(media_path).exists():
        chosen_media = Path(media_path).resolve()
    elif m_frames and Path(m_frames[0]).exists():
        chosen_media = Path(m_frames[0]).resolve()
    else:
        fallback_cov = Path(out_dir) / "hook_cover.jpg"
        if fallback_cov.exists():
            chosen_media = fallback_cov.resolve()

    if not chosen_media or not chosen_media.exists():
        return {"status": "saved_metadata_only", "pin_data": pin_data}

    if os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("SKIP_LOCAL_CDP_PINTEREST") == "1":
        return {"status": "rss_and_metadata_ready", "pin_data": pin_data, "media": str(chosen_media)}

    try:
        import websocket  # type: ignore
    except Exception:
        return {"status": "rss_and_metadata_ready", "pin_data": pin_data, "media": str(chosen_media)}

    ws_url = _ensure_pinterest_chrome()
    if not ws_url:
        return {"status": "rss_and_metadata_ready", "pin_data": pin_data, "media": str(chosen_media)}

    ws = None
    try:
        ws = websocket.create_connection(ws_url, timeout=25)
        msg_id = 0

        def cdp(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            nonlocal msg_id
            msg_id += 1
            ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
            while True:
                resp = json.loads(ws.recv())
                if resp.get("id") == msg_id:
                    return resp.get("result", {})

        def pump_frames(seconds: float) -> None:
            end_t = time.time() + seconds
            while time.time() < end_t:
                try:
                    cdp("Page.captureScreenshot", {"format": "jpeg", "quality": 20})
                except Exception:
                    pass
                time.sleep(0.5)

        cdp("Page.enable")
        cdp("DOM.enable")
        cdp("Runtime.enable")
        cdp("Input.enable")
        cdp("Page. navigate", {"url": "https://tr.pinterest.com/pin-creation-tool/"}) if False else cdp(
            "Page.navigate", {"url": "https://tr.pinterest.com/pin-creation-tool/"}
        )
        pump_frames(6)

        eval_res = cdp(
            "Runtime.evaluate",
            {"expression": "document.querySelector('input[type=\"file\"]')", "returnByValue": False},
        )
        obj_id = (eval_res.get("result") or {}).get("objectId")
        if not obj_id:
            return {"status": "rss_and_metadata_ready", "pin_data": pin_data, "media": str(chosen_media)}

        cdp("DOM.setFileInputFiles", {"objectId": obj_id, "files": [str(chosen_media)]})
        pump_frames(5)

        fill_pin_js = f"""
        (function(title, desc, link) {{
            function setNativeValue(el, value) {{
                const valueSetter = Object.getOwnPropertyDescriptor(el, 'value')?.set;
                const prototype = Object.getPrototypeOf(el);
                const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, 'value')?.set;
                if (valueSetter && valueSetter !== prototypeValueSetter) {{
                    prototypeValueSetter.call(el, value);
                }} else if (valueSetter) {{
                    valueSetter.call(el, value);
                }} else {{
                    el.value = value;
                }}
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const tInput = document.querySelector('input[id*="title"], input[placeholder*="Başlık"], input[placeholder*="Title"]');
            if (tInput) {{ tInput.focus(); setNativeValue(tInput, title); }}

            const lInput = document.querySelector('input[id*="link"], input[placeholder*="bağlantı"], input[placeholder*="link"], input[type="url"]');
            if (lInput) {{ lInput.focus(); setNativeValue(lInput, link); }}

            const dEditor = document.querySelector('div[contenteditable="true"]');
            if (dEditor) {{
                dEditor.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('insertText', false, desc);
            }}
            return "PIN_FIELDS_SET";
        }})({json.dumps(pin_data['title'])}, {json.dumps(pin_data['description'])}, {json.dumps(pin_data['destination_link'])})
        """
        cdp("Runtime.evaluate", {"expression": fill_pin_js, "returnByValue": True})
        pump_frames(2.5)

        pub_js = """
        (function() {
            const btn = Array.from(document.querySelectorAll('button')).find(b => /Yayınla|Publish|Kaydet|Save/i.test((b.innerText || '').trim()));
            if (btn && !btn.disabled) {
                btn.click();
                return "CLICKED_PUBLISH: " + btn.innerText.trim();
            }
            return "NO_PUBLISH_BTN";
        })()
        """
        pub_res = (cdp("Runtime.evaluate", {"expression": pub_js, "returnByValue": True}).get("result") or {}).get("value")
        pump_frames(5)
        return {
            "status": "published_cdp",
            "account": f"@{PINTEREST_ACCOUNT_HANDLE}",
            "action": pub_res,
            "pin_title": pin_data["title"],
            "destination_link": pin_data["destination_link"],
        }
    except Exception as e:
        return {
            "status": "rss_and_metadata_ready",
            "account": f"@{PINTEREST_ACCOUNT_HANDLE}",
            "note": str(e),
            "pin_data": pin_data,
        }
    finally:
        if ws is not None:
            try:
                ws.close()
            except Exception:
                pass
