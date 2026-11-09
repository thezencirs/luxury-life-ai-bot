"""
Sesli Lüks Hayatlar (@Sesliluksbot) — Telegram Bot Yapılandırıcı, guzelai.com + @guzelaicom Pinterest
Senkronizasyonu ve Sade 2K Reels + Kısa Instagram-SEO Copy-Paste Teslim Motoru
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
    mark_concept_used,
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
    tok = (token or get_bot_token()).strip()
    if not tok:
        return {"ok": False, "error": "Telegram bot baglantisi devre disi (yeni bot bekleniyor)."}
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
    """@Sesliluksbot adını, açıklamasını ve hızlı lüks üretim komutlarını Telegram'a kaydeder."""
    tok = token or get_bot_token()
    results = {}
    results["setMyName"] = tg_api(
        "setMyName",
        {"name": "Sesli Lüks Hayatlar • 2K Reels (@Sesliluksbot)"},
        token=tok,
    )
    results["setMyShortDescription"] = tg_api(
        "setMyShortDescription",
        {
            "short_description": "💎 Çok Açılı Milyoner Yaşam, Pırlanta, Saat, Otel & Supercar 2K Reels • guzelai.com & @guzelaicom"
        },
        token=tok,
    )
    results["setMyDescription"] = tg_api(
        "setMyDescription",
        {
            "description": (
                "💎 Sesli Lüks Hayatlar (@Sesliluksbot) — 2K Lüks & Milyoner Yaşam Reels Otomasyonu\n\n"
                "• 🌐 Tüm videolar, çok açılı fotoğraflar ve doğrulanmış mağaza linkleri: https://guzelai.com/#kombinler\n"
                "• 📌 Pinterest Vitrini: https://tr.pinterest.com/guzelaicom/\n"
                "• 🎬 Bota fotoğraf, video veya ürün linki gönderin; çok açılı tam ekran 2K Reels videonuzu ve saf Instagram-SEO copy-paste açıklamanızı anında teslim alın."
            )
        },
        token=tok,
    )
    results["setMyCommands"] = tg_api(
        "setMyCommands",
        {
            "commands": [
                {"command": "start", "description": "Hazır 2K milyoner stok videolarını ve vitrini al"},
                {"command": "stok", "description": "Son üretilen çok açılı 2K lüks stok videolarını gönder"},
                {"command": "uret", "description": "Sıradaki lüks kategoride anında 2K Reels üret"},
                {"command": "taki", "description": "💎 Mücevher & Saat 2K Reels üret"},
                {"command": "makyaj", "description": "💄 Lüks Makyaj & Parfüm 2K Reels üret"},
                {"command": "kombin", "description": "🧥 Old Money Kombin 2K Reels üret"},
                {"command": "otel", "description": "🏨 Ultra Lüks Otel & Yat 2K Reels üret"},
                {"command": "araba", "description": "🏎️ Süper Spor Otomobil 2K Reels üret"},
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
    env_cid = os.environ.get("TELEGRAM_CHAT_ID", f"{DEFAULT_ADMIN_CHAT_ID},995164733").strip()
    for part in env_cid.replace(";", ",").split(","):
        p = part.strip()
        if p and p not in chat_ids:
            chat_ids.append(p)

    req_cid = str(concept.get("requester_chat_id", "")).strip()
    if req_cid and req_cid not in chat_ids:
        chat_ids.append(req_cid)

    # @Sesliluksbot getUpdates üzerinden yeni yazan/başlatan kullanıcıları anında keşfet
    try:
        upd_res = tg_api("getUpdates", {"timeout": 1})
        if upd_res.get("ok"):
            for u in upd_res.get("result") or []:
                msg = u.get("message") or u.get("channel_post") or (u.get("callback_query") or {}).get("message") or {}
                c_obj = msg.get("chat") or {}
                c_id = str(c_obj.get("id", "")).strip()
                if c_id and c_id not in chat_ids:
                    chat_ids.append(c_id)
    except Exception:
        pass

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
    video_path: Optional[str] = None,
    sync_web_and_pinterest: bool = True,
) -> Dict[str, Any]:
    """
    Hazırlanan 2K Lüks Paketi:
    1) `guzelai.com` (`https://guzelai.com/#kombinler` + `/go/{sku}`) üzerine işler,
    2) `@guzelaicom` Pinterest hesabına (`https://tr.pinterest.com/guzelaicom/` + `pinterest-rss.xml`) yayınlar,
    3) `@Sesliluksbot` üzerinden SADECE 2K Video + Kısa Instagram-SEO Copy-Paste Açıklama olarak teslim eder.
    """
    tok = token or get_bot_token()
    out_p = Path(out_dir)
    os.makedirs(out_p, exist_ok=True)

    resolved_vid_p = Path(video_path) if video_path and Path(video_path).exists() else (out_p / "luxury_reel_final.mp4")

    # 1) Önce videoyu, çok açılı görselleri ve 6 ürünün tüm detay/mağaza linklerini guzelai.com'a ve @guzelaicom Pinterest'e işle
    guzelai_sync_res: Dict[str, Any] = {}
    pinterest_sync_res: Dict[str, Any] = {}
    if sync_web_and_pinterest:
        try:
            from guzelai_web_sync import publish_luxury_to_guzelai
            guzelai_sync_res = publish_luxury_to_guzelai(concept, out_dir=out_dir, video_path=str(resolved_vid_p))
            print(f"🌐 [guzelai.com Vitrin & Link Senkronizasyonu]: {guzelai_sync_res}")
        except Exception as gz_err:
            print(f"[guzelai.com Senkronizasyon Uyarısı]: {gz_err}")

        try:
            from pinterest_luxury_publisher import publish_luxury_to_pinterest
            pinterest_sync_res = publish_luxury_to_pinterest(concept, out_dir=out_dir)
            print(f"📌 [@guzelaicom Pinterest Yayın Durumu]: {pinterest_sync_res.get('status')} -> {pinterest_sync_res.get('pin_title', concept.get('title'))}")
        except Exception as pin_err:
            print(f"[@guzelaicom Pinterest Uyarısı]: {pin_err}")

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

    reply_markup_json = json.dumps(build_luxury_inline_keyboard(concept))

    chat_ids = load_target_chat_ids(concept)
    delivery_report: Dict[str, Any] = {}

    for cid in chat_ids:
        res_chat: Dict[str, Any] = {
            "guzelai_published": guzelai_sync_res.get("guzelai_published", False),
            "pinterest_status": pinterest_sync_res.get("status", "ready"),
        }

        # Telegram (@Sesliluksbot) için SADECE 2K Video + Kısa Instagram-SEO Copy-Paste Açıklama gönder (yazıya boğma!)
        if resolved_vid_p.exists():
            with open(resolved_vid_p, "rb") as vf:
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
                if not r_vid.get("ok"):
                    res_chat["tg_note"] = r_vid.get("description", "")

        r_cap = tg_api(
            "sendMessage",
            data={
                "chat_id": cid,
                "text": caption_copy_paste[:4000],
                "disable_web_page_preview": True,
            },
            token=tok,
        )
        res_chat["caption_copypaste"] = r_cap.get("ok", False)

        delivery_report[cid] = res_chat
        print(f"✅ [@Sesliluksbot Teslimat Durumu -> {cid}]: {res_chat}")

    # Sıfır-Tekrar Çift Kilidini (output/zero_repeat_ledger.json Yerel + GitHub API) atomik olarak kilitle
    mark_concept_used(concept, sync_github=True)

    return delivery_report
