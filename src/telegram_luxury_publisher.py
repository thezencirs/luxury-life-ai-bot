"""
Luxury Life AI (@Luxurylifeaibot) — Telegram Bot Yapılandırıcı & 3-Mesajlı (Açıklayıcı Analiz +
Saf Açıklama Copy-Paste + Saf Ürün Linkleri Copy-Paste) 2K Reels Teslim Motoru
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from luxury_viral_concepts import (
    BASE_DIR,
    build_explanatory_director_message,
    build_pure_copy_paste_caption,
    build_pure_copy_paste_links,
)
from telegram_luxury_ingestor import (
    DEFAULT_ADMIN_CHAT_ID,
    DEFAULT_BOT_TOKEN,
    SUBSCRIBERS_FILE,
    get_bot_token,
)


def tg_api(
    method: str,
    data: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    tok = token or get_bot_token()
    url = f"https://api.telegram.org/bot{tok}/{method}"
    try:
        if files:
            resp = requests.post(url, data=data, files=files, timeout=120)
        else:
            resp = requests.post(url, json=data or {}, timeout=35)
        return resp.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


def configure_luxury_bot_profile(token: Optional[str] = None) -> Dict[str, Any]:
    """@Luxurylifeaibot adını, açıklamasını ve hızlı lüks üretim komutlarını Telegram'a kaydeder."""
    tok = token or get_bot_token()
    results = {}
    results["setMyName"] = tg_api(
        "setMyName",
        {"name": "Luxury Life AI • 2K Reels & Stil (@luxurylifeaibot)"},
        token=tok,
    )
    results["setMyShortDescription"] = tg_api(
        "setMyShortDescription",
        {
            "short_description": "💎 Takı, Makyaj, Old Money Kombin, Lüks Otel & Supercar 2K GraphMotion Reels Otomasyonu"
        },
        token=tok,
    )
    results["setMyDescription"] = tg_api(
        "setMyDescription",
        {
            "description": (
                "💎 Luxury Life AI (@luxurylifeaibot) — 2K Lüks Yaşam Instagram Reels Otomasyonu\n\n"
                "• 📸 Bota takı, makyaj, kombin, otel veya lüks araba fotoğrafı, videosu ya da ürün linki gönderin.\n"
                "• 🎬 Gönderdiğiniz tüm görüntü ve yazıları otomatik tetikleyici olarak kullanır; yazım hatalarını düzeltir, doğru açı ve mekanla 2K GraphMotion Plus Reels hazırlar.\n"
                "• 📋 1) Açıklayıcı Analiz, 2) Saf Copy-Paste Açıklama (#reklam #işbirliğiyoktur) ve 3) Saf Copy-Paste Ürün Linkleri sunar."
            )
        },
        token=tok,
    )
    results["setMyCommands"] = tg_api(
        "setMyCommands",
        {
            "commands": [
                {"command": "start", "description": "Komuta merkezini ve kullanım rehberini aç"},
                {"command": "uret", "description": "Sıradaki lüks kategoride anında 2K Reels üret"},
                {"command": "taki", "description": "💎 Mücevher & Saat (Place Vendôme) 2K Reels üret"},
                {"command": "makyaj", "description": "💄 Lüks Makyaj & Parfüm (Paris Vanity) 2K Reels üret"},
                {"command": "kombin", "description": "🧥 Old Money Kombin (Milano) 2K Reels üret"},
                {"command": "otel", "description": "🏨 Ultra Lüks Otel & Tatil (Boğaz/Como) 2K Reels üret"},
                {"command": "araba", "description": "🏎️ Süper Spor Otomobil (Monaco GP) 2K Reels üret"},
            ]
        },
        token=tok,
    )
    return results


def build_luxury_inline_keyboard(concept: Dict[str, Any]) -> Dict[str, Any]:
    """Videonun altına tıklanabilir birebir mağaza linkleri + tek tıkla yeni kategori üretim butonları ekler."""
    items = concept.get("items", {})
    rows: List[List[Dict[str, str]]] = []
    cur_row: List[Dict[str, str]] = []

    for idx, (slot_k, it) in enumerate(items.items(), start=1):
        url = str(it.get("store_url", "")).strip()
        if not url.startswith("http"):
            continue
        em = it.get("emoji", "💎")
        brand = str(it.get("brand", "Mağaza")).split("/")[0].strip()
        price = str(it.get("price", ""))
        btn_txt = f"{idx}️⃣ {em} {brand} ({price})"[:32]
        cur_row.append({"text": btn_txt, "url": url})
        if len(cur_row) == 2:
            rows.append(cur_row)
            cur_row = []
    if cur_row:
        rows.append(cur_row)

    rows.append([
        {"text": "💎 Takı Reels Üret", "callback_data": "gen_cat:taki"},
        {"text": "💄 Makyaj Reels Üret", "callback_data": "gen_cat:makyaj"},
    ])
    rows.append([
        {"text": "🧥 Kombin Reels Üret", "callback_data": "gen_cat:kombin"},
        {"text": "🏨 Otel Reels Üret", "callback_data": "gen_cat:otel"},
    ])
    rows.append([
        {"text": "🏎️ Araba Reels Üret", "callback_data": "gen_cat:araba"},
        {"text": "✨ Otomatik Yeni Üret", "callback_data": "gen_cat:otomatik"},
    ])
    return {"inline_keyboard": rows}


def load_target_chat_ids(concept: Dict[str, Any]) -> List[str]:
    chat_ids: List[str] = []
    env_cid = os.environ.get("TELEGRAM_CHAT_ID", DEFAULT_ADMIN_CHAT_ID).strip()
    if env_cid:
        chat_ids.append(env_cid)

    req_cid = str(concept.get("requester_chat_id", "")).strip()
    if req_cid and req_cid not in chat_ids:
        chat_ids.append(req_cid)

    if SUBSCRIBERS_FILE.exists():
        try:
            sub = json.loads(SUBSCRIBERS_FILE.read_text(encoding="utf-8"))
            for cid in (sub.get("chats") or {}).keys():
                if str(cid) not in chat_ids:
                    chat_ids.append(str(cid))
        except Exception:
            pass
    return chat_ids


def deliver_luxury_package_to_telegram(
    concept: Dict[str, Any],
    out_dir: str = "output",
    token: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Hazırlanan 2K Lüks Paketi @Luxurylifeaibot üzerinden kullanıcıya gönderir:
    - Görsel 1: 2K Viral Hook Kapak Fotoğrafı (hook_cover.jpg)
    - Görsel 2: 9:16 Lüks Story & Moodboard Kolajı (luxury_story_collage.jpg)
    - Video: 2K GraphMotion Plus Reels Videosu (luxury_reel_final.mp4) + Mağaza Link Butonları
    - Mesaj 1 (Açıklayıcı Yazı — Copy-Paste Harici): Viral kaydetme oranı analizi, kamera açısı, mekan, model rejisi ve kullanım rehberi
    - Mesaj 2 (Açıklama Copy-Paste): %100 saf Instagram Reels açıklaması (#reklam #işbirliğiyoktur dahil)
    - Mesaj 3 (Linkler Copy-Paste): %100 saf birebir ürün ve iş birliği linkleri (#reklam #işbirliğiyoktur dahil)
    """
    tok = token or get_bot_token()
    out_p = Path(out_dir)
    os.makedirs(out_p, exist_ok=True)

    explanatory_msg = build_explanatory_director_message(concept)
    caption_copy_paste = build_pure_copy_paste_caption(concept)
    links_copy_paste = build_pure_copy_paste_links(concept)

    (out_p / "1_explanatory_analysis.txt").write_text(explanatory_msg, encoding="utf-8")
    (out_p / "2_instagram_caption_copypaste.txt").write_text(caption_copy_paste, encoding="utf-8")
    (out_p / "3_product_links_copypaste.txt").write_text(links_copy_paste, encoding="utf-8")
    (out_p / "luxury_concept_metadata.json").write_text(
        json.dumps(concept, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    cover_path = out_p / "hook_cover.jpg"
    story_path = out_p / "luxury_story_collage.jpg"
    video_path = out_p / "luxury_reel_final.mp4"
    reply_markup_json = json.dumps(build_luxury_inline_keyboard(concept))

    chat_ids = load_target_chat_ids(concept)
    delivery_report: Dict[str, Any] = {}

    for cid in chat_ids:
        res_chat: Dict[str, Any] = {}

        # 1) 2K Hook Kapak Görseli
        if cover_path.exists():
            with open(cover_path, "rb") as cf:
                r_cov = tg_api("sendPhoto", data={"chat_id": cid}, files={"photo": cf}, token=tok)
                res_chat["hook_cover"] = r_cov.get("ok", False)

        # 2) 9:16 Story Moodboard Kolajı
        if story_path.exists():
            with open(story_path, "rb") as sf:
                r_st = tg_api("sendPhoto", data={"chat_id": cid}, files={"photo": sf}, token=tok)
                res_chat["story_collage"] = r_st.get("ok", False)

        # 3) 2K GraphMotion Plus Reels Videosu
        if video_path.exists():
            with open(video_path, "rb") as vf:
                r_vid = tg_api(
                    "sendVideo",
                    data={
                        "chat_id": cid,
                        "reply_markup": reply_markup_json,
                        "supports_streaming": "true",
                        "width": "1440",
                        "height": "2560",
                    },
                    files={"video": vf},
                    token=tok,
                )
                res_chat["video"] = r_vid.get("ok", False)

        # 4) MESAJ 1 — Copy-Paste Harici Açıklayıcı Reji & Kaydetme Oranı Analizi
        r_exp = tg_api(
            "sendMessage",
            data={
                "chat_id": cid,
                "text": explanatory_msg[:4000],
                "disable_web_page_preview": True,
            },
            token=tok,
        )
        res_chat["msg1_explanatory"] = r_exp.get("ok", False)

        # 5) MESAJ 2 — Saf Instagram Açıklama (Caption) Copy-Paste (Yasal #reklam #işbirliğiyoktur dahil)
        r_cap = tg_api(
            "sendMessage",
            data={
                "chat_id": cid,
                "text": caption_copy_paste[:4000],
                "disable_web_page_preview": True,
            },
            token=tok,
        )
        res_chat["msg2_caption_copypaste"] = r_cap.get("ok", False)

        # 6) MESAJ 3 — Saf Birebir Ürün & İş Birliği Linkleri Copy-Paste (Yasal #reklam #işbirliğiyoktur dahil)
        r_lnk = tg_api(
            "sendMessage",
            data={
                "chat_id": cid,
                "text": links_copy_paste[:4000],
                "disable_web_page_preview": True,
            },
            token=tok,
        )
        res_chat["msg3_links_copypaste"] = r_lnk.get("ok", False)

        delivery_report[cid] = res_chat
        print(f"✅ [@Luxurylifeaibot Teslimatı Tamamlandı -> {cid}]: {res_chat}")

    return delivery_report
