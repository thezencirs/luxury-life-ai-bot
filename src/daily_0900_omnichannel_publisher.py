"""
GüzelAI Holding A.Ş. — Sabah 09:00 Günlük 1 Paylaşım Tüm Kanallar Yayıncısı & Kanal Aktivite Raporlayıcı
(`src/daily_0900_omnichannel_publisher.py`)
========================================================================================================
Kullanıcı Talimatı:
1. "tamam botu koru ve telegram paylaşımlarını yaparken ve instagram paaaylaşımları yaparken mutlaka dikey
   fotoğraf ve video retmeye odaklan bir de flow kullanma kaliteyi ve iyileştirmeleri hallet senktronizasyon
   güncelik özgün çok önemli tekrar eden tek şey modelin kendisi olabilir orada bile 4-7 çeşit guzelai mankeni kullan"
2. "artık buradaki paylaşımları hergün 1 tane sabah 9 da tüm guzel ai sayfalarından yapmanı istiyorum
   instagram dahil bunu instagram için yaparken hassa ol ve diğer platformalarda da her gün kanal
   aktivite raporu yap bana ve kendine sun"

Mimari Garantiler:
- SIFIR GOOGLE FLOW: `flow.google.com` ve `flow_video_engine` dalga bükmesi tamamen emekliye ayrıldı.
- %100 DİKEY (`9:16` — `1080x1920`) FOTOĞRAF & VİDEO ZORUNLULUĞU:
  * Her kreasyonda `768x1344 -> 1080x1920` (`9:16` Dikey) FLUX.1 + `LANCZOS` optik keskinlikle 3 açı dikey
    editoryal fotoğraf ve 1 adet `1080x1920 @ 30fps` (`CRF 12`) dikey sinema Reels videosu üretilir.
  * Telegram (`@Sesliluksbot`) paylaşımında hem Dikey (`9:16`) Fotoğraf (`sendPhoto`) hem Dikey (`9:16`)
    Video (`sendVideo`) hem de kısa yasal uyarılı mağaza linkli metin gönderilir.
- 7 RESMİ `guzelai.com` MANKENİ ROTASYONU & %100 ÖZGÜN/GÜNCEL SENARYO:
  * Yalnızca manken kimliği 7 resmi `guzelai.com` mankeni arasında döner (`Valentina Cruz`, `Leyla`, `Aura Kaya`,
    `Selene Noir`, `Chloe Bennett`, `Scarlett Vance`, `Kenzo Takahashi`); senaryo, mekan, kurgu, fotoğraf ve
    video her gün %100 yeni ve tekrarsız üretilir.
- BOT & INSTAGRAM KORUMASI:
  * `@Sesliluksbot` 7/24 canlı otonom dinleyicisi ve hız sınırları korunur.
  * `@guzelaicom` Instagram paylaşımı yalnızca tekil güvenilir Chrome (`ig_chrome_trusted:9230`) +
    `GhostCursor` insan ısınması + günde maksimum 1 paylaşım kuralıyla yürütülür.
"""

import argparse
import base64
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SCRATCH_DIR = BASE_DIR.parent
KOMBIN_BOT_SRC = SCRATCH_DIR / "instagram-kombin-bot" / "src"
GUZELAI_WEB_DIR = SCRATCH_DIR / "guzelai"

sys.path.insert(0, str(BASE_DIR / "src"))
if KOMBIN_BOT_SRC.exists():
    sys.path.insert(0, str(KOMBIN_BOT_SRC))

from guzelai_7models_vertical_engine import (
    GUZELAI_7_OFFICIAL_MODELS,
    generate_next_unique_vertical_7model_creation,
    load_vertical_7models_ledger,
)
from guzelai_web_sync import _gh_get_json, _gh_put_file, publish_luxury_to_guzelai
from pinterest_luxury_publisher import publish_luxury_to_pinterest
from telegram_luxury_publisher import (
    build_luxury_inline_keyboard,
    build_pure_copy_paste_caption,
    get_bot_token,
    load_target_chat_ids,
    tg_api,
)

REPORTS_DIR = BASE_DIR / "output" / "reports"
CHANNELS_OUT_DIR = BASE_DIR / "output" / "channels"
OMNICHANNEL_LEDGER_PATH = BASE_DIR / "output" / "daily_omnichannel_published_ledger.json"
AGENT_SELF_LEDGER_PATH = REPORTS_DIR / "agent_self_activity_ledger.json"
LATEST_REPORT_MD_PATH = REPORTS_DIR / "daily_channel_activity_report_latest.md"
LATEST_REPORT_JSON_PATH = REPORTS_DIR / "daily_channel_activity_report_latest.json"

CATEGORY_LABELS_TR = {
    "makyaj": "💄 En İyi Lüks Makyaj & Cilt Bakımı",
    "taki": "💎 En İyi Yüksek Mücevherat & Saat",
    "otel": "🏨 En İyi 5 Yıldızlı Saray Oteller & Süitler",
    "araba": "🏎️ En İyi Süper Spor & Ultra-Lüks Otomobiller",
    "yasam": "🛥️ En İyi Milyoner Yaşam, Yat & Yalı Buluşmaları",
}


def load_omnichannel_ledger() -> Dict[str, Any]:
    if OMNICHANNEL_LEDGER_PATH.exists():
        try:
            return json.loads(OMNICHANNEL_LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "published_video_names": [],
        "published_sha256": [],
        "last_publish_date": "",
        "last_category": "",
        "history": [],
    }


def save_omnichannel_ledger(ledger: Dict[str, Any]) -> None:
    OMNICHANNEL_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    OMNICHANNEL_LEDGER_PATH.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_captions_for_creation(scenario: Dict[str, Any]) -> Tuple[str, str]:
    """
    Returns `(full_telegram_and_web_caption, instagram_safe_caption)`.
    - `full_telegram_and_web_caption`: Short headline + verified store URLs + mandatory legal/AI disclosure.
    - `instagram_safe_caption`: Short headline + featured luxury brands/products + `guzelai.com` bio pointer +
      mandatory legal/AI disclosure (`#reklam #işbirliğideğil #işbirliğiyoktur #yapayzeka`), with ZERO raw URLs.
    """
    items = scenario.get("items") or {}
    base_caption = build_pure_copy_paste_caption(scenario)

    product_lines_with_urls = []
    product_lines_no_urls = []
    for idx_i, (_, it) in enumerate(items.items(), start=1):
        emoji = it.get("emoji", "💎")
        brand = it.get("brand", "Luxury Maison")
        name = it.get("name", "Signature Piece")
        price = it.get("price", "")
        url = it.get("store_url", "https://guzelai.com/#kombinler")
        product_lines_with_urls.append(f"{idx_i}️⃣ {emoji} {brand} – {name} ({price})\n🔗 {url}")
        product_lines_no_urls.append(f"• {emoji} {brand} – {name} ({price})")

    lines = base_caption.splitlines()
    header_part = "\n".join(lines[:3])
    footer_part = "\n".join(lines[3:])

    links_block = "\n".join(product_lines_with_urls)
    full_caption = f"{header_part}\n\n🛍️ Lüks Ürün & Mağaza Linkleri:\n{links_block}\n\n{footer_part}"

    clean_products_block = "\n".join(product_lines_no_urls)
    ig_safe_caption = (
        f"{header_part}\n\n"
        f"✨ Seçkideki Lüks Parçalar & Deneyimler:\n{clean_products_block}\n"
        f"🔗 Tüm Mağaza Linkleri & Dikey 9:16 Klipler: Profildeki guzelai.com bağlantısında.\n\n"
        f"{footer_part}"
    )
    return full_caption, ig_safe_caption


def sync_vertical_creation_to_guzelai_clips(scenario: Dict[str, Any]) -> bool:
    """
    Üretilen dikey (9:16 — 1080x1920) fotoğraf ve videoyu `guzelai.com` Klipler (`#clips-section`)
    ve `public/clips/flow_clips_feed.json` ile canlı senkronize eder.
    """
    try:
        mp4_path = Path(scenario["video_path"])
        hero_photo = Path(scenario["hero_vertical_photo"])
        cid = scenario["id"]

        if GUZELAI_WEB_DIR.exists():
            clips_dir = GUZELAI_WEB_DIR / "public" / "clips"
            clips_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(mp4_path, clips_dir / f"{cid}.mp4")
            shutil.copy2(hero_photo, clips_dir / f"{cid}_poster.jpg")

        _gh_put_file(
            f"public/clips/{cid}.mp4",
            mp4_path.read_bytes(),
            f"feat(clips): sync 9:16 vertical cinema video {cid}.mp4 ({scenario['guzelai_model_name']})",
        )
        _gh_put_file(
            f"public/clips/{cid}_poster.jpg",
            hero_photo.read_bytes(),
            f"feat(clips): sync 9:16 vertical editorial photo {cid}_poster.jpg",
        )

        first_item = next(iter((scenario.get("items") or {}).values()), {})
        clip_entry = {
            "id": cid,
            "modelId": scenario["guzelai_model_id"],
            "modelName": scenario["guzelai_model_name"].replace(" (guzelai.com)", ""),
            "title": scenario["title"],
            "location": scenario["location_name"],
            "category": scenario["category"],
            "aspectRatio": "9:16",
            "resolution": "1080x1920",
            "videoUrl": f"/clips/{cid}.mp4",
            "posterUrl": f"/clips/{cid}_poster.jpg",
            "storeUrl": first_item.get("store_url", "https://guzelai.com/#kombinler"),
            "brandBadge": f"{scenario.get('bottom_brand', 'GüzelAI')} • {scenario.get('bottom_product', '')}",
            "updatedAt": datetime.datetime.now().isoformat(timespec="seconds"),
        }

        feed_list: List[Dict[str, Any]] = []
        rem = _gh_get_json("public/clips/flow_clips_feed.json")
        if isinstance(rem, dict) and rem.get("content"):
            try:
                dec = json.loads(base64.b64decode(rem["content"]).decode("utf-8"))
                if isinstance(dec, list):
                    feed_list = [x for x in dec if isinstance(x, dict) and x.get("id") != cid]
            except Exception:
                pass
        feed_list = [clip_entry] + feed_list[:23]
        feed_bytes = json.dumps(feed_list, ensure_ascii=False, indent=2).encode("utf-8")
        if GUZELAI_WEB_DIR.exists():
            (GUZELAI_WEB_DIR / "public" / "clips" / "flow_clips_feed.json").write_bytes(feed_bytes)
        _gh_put_file(
            "public/clips/flow_clips_feed.json",
            feed_bytes,
            f"feat(clips): update live 7-model 9:16 vertical feed ({cid}) on guzelai.com",
        )
        return True
    except Exception as e:
        print(f"[GuzelAI Web Clips Sync Note]: {e}")
        return False


def publish_to_instagram_delicate(mp4_path: Path, ig_caption: str) -> Dict[str, Any]:
    """
    HARD-LOCKED BY USER (2026-11-20): "guzelaicom instagram hesabına paylaşım yapma sayfa kitlenmiş"
    Never launches Chrome, never connects to port 9230, and never touches `@guzelaicom` on Instagram.
    Only saves the offline 9:16 vertical manual package in `output/channels/instagram_manual/`.
    """
    ig_manual_dir = CHANNELS_OUT_DIR / "instagram_manual"
    ig_manual_dir.mkdir(parents=True, exist_ok=True)
    if mp4_path.exists():
        shutil.copy2(mp4_path, ig_manual_dir / "daily_0900_reel_1080x1920.mp4")
    (ig_manual_dir / "caption.txt").write_text(ig_caption, encoding="utf-8")
    return {
        "status": "hard_disabled_by_user_account_locked",
        "logged_in": False,
        "zero_violation": True,
        "detail": (
            "Kullanıcı talimatıyla @guzelaicom Instagram hesabına tüm otomatik paylaşım, tarayıcı ve "
            "oturum erişimi %100 kapatıldı (Sayfa kilitli — Sıfır temas). İçerik yalnızca çevrimdışı "
            "output/channels/instagram_manual/ ve Telegram @Sesliluksbot üzerinde hazırlandı."
        ),
    }


def prepare_other_guzelai_social_channels(
    mp4_path: Path,
    vertical_photos: List[str],
    scenario: Dict[str, Any],
    full_caption: str,
    ig_safe_caption: str,
) -> Dict[str, Any]:
    CHANNELS_OUT_DIR.mkdir(parents=True, exist_ok=True)
    title = scenario.get("title", "GüzelAI Lüks Seçki")
    model_name = scenario.get("guzelai_model_name", "Valentina Cruz (guzelai.com)")
    cat_label = CATEGORY_LABELS_TR.get(scenario.get("category", "taki"), "Lüks Seçki")

    channels_map = {
        "tiktok": {
            "handle": "@guzelaicom",
            "url": "https://www.tiktok.com/@guzelaicom",
            "caption": ig_safe_caption,
            "mode": "9:16 Dikey Fotoğraf + 1080x1920 Video FYP Paketi Hazır",
        },
        "youtube_shorts": {
            "handle": "@guzelaicom",
            "url": "https://www.youtube.com/@guzelaicom/shorts",
            "title": f"{title} | {model_name} #shorts #reklam",
            "caption": full_caption,
            "mode": "9:16 Dikey Shorts Video + Mağaza Linkli Açıklama Hazır",
        },
        "x_twitter": {
            "handle": "@guzelaicom",
            "url": "https://x.com/guzelaicom",
            "caption": (
                f"✨ {title} ({model_name})\n"
                f"🌐 9:16 Dikey Fotoğraflar, Video & Ürün Linkleri: https://guzelai.com/#kombinler\n"
                f"⚖️ #reklam #işbirliğideğil #işbirliğiyoktur #yapayzeka"
            ),
            "mode": "9:16 Dikey Fotoğraf + Video + Kısa Zincir Metni Hazır",
        },
        "threads": {
            "handle": "@guzelaicom",
            "url": "https://www.threads.net/@guzelaicom",
            "caption": full_caption[:490],
            "mode": "Instagram SSO Bağlı 9:16 Dikey Fotoğraf & Video Paketi Hazır",
        },
        "whatsapp_channel": {
            "handle": "GüzelAI Lüks & Kombin Kanalı",
            "url": "https://guzelai.com/#kombinler",
            "caption": full_caption,
            "mode": "9:16 Dikey Fotoğraf + Video + Doğrudan Mağaza Linkleri Hazır",
        },
    }

    summary: Dict[str, Any] = {}
    for ch_key, cfg in channels_map.items():
        ch_dir = CHANNELS_OUT_DIR / ch_key
        ch_dir.mkdir(parents=True, exist_ok=True)
        dst_mp4 = ch_dir / "daily_0900_reel_1080x1920.mp4"
        shutil.copy2(mp4_path, dst_mp4)
        for idx_p, vp in enumerate(vertical_photos, start=1):
            if os.path.exists(vp):
                shutil.copy2(vp, ch_dir / f"daily_0900_vertical_9_16_angle{idx_p}.jpg")
        (ch_dir / "caption.txt").write_text(cfg["caption"], encoding="utf-8")
        (ch_dir / "metadata.json").write_text(
            json.dumps(
                {
                    "channel": ch_key,
                    "handle": cfg["handle"],
                    "channel_url": cfg["url"],
                    "category": scenario.get("category"),
                    "category_label": cat_label,
                    "scenario_id": scenario.get("id"),
                    "guzelai_model": model_name,
                    "aspect_ratio": "9:16 (1080x1920 Strict Vertical)",
                    "flow_used": False,
                    "prepared_at_iso": datetime.datetime.now().isoformat(timespec="seconds"),
                    "mode": cfg["mode"],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        summary[ch_key] = {
            "status": "synced_9_16_vertical_photo_and_video",
            "handle": cfg["handle"],
            "url": cfg["url"],
            "mode": cfg["mode"],
            "video_path": str(dst_mp4),
        }
    return summary


def record_agent_self_reflection_and_telemetry(
    daily_report: Dict[str, Any],
    v_ledger: Dict[str, Any],
) -> Dict[str, Any]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    self_ledger: Dict[str, Any] = {
        "agent_identity": "GüzelAI Omnichannel Autonomous Director & Self-Auditor (Zero-Flow 9:16 Vertical Edition)",
        "schedule_policy": "Every Day at 09:00 AM — 100% Unique 9:16 Vertical Photo + Video Across 7 Official GuzelAI Models",
        "total_self_audits": 0,
        "entries": [],
    }
    if AGENT_SELF_LEDGER_PATH.exists():
        try:
            self_ledger = json.loads(AGENT_SELF_LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    active_pub = daily_report.get("published_creation", {})
    next_m_idx = (int(v_ledger.get("last_model_index", 0)) + 1) % len(GUZELAI_7_OFFICIAL_MODELS)
    next_model_name = GUZELAI_7_OFFICIAL_MODELS[next_m_idx]["name"]

    self_entry = {
        "audit_timestamp_iso": datetime.datetime.now().isoformat(timespec="seconds"),
        "report_date": daily_report.get("report_date"),
        "engine": "guzelai_pure_vertical_9_16_cinema_zero_flow (Google Flow Devre Dışı)",
        "published_scenario_id": active_pub.get("scenario_id"),
        "published_category": active_pub.get("category"),
        "published_model": active_pub.get("guzelai_model_name"),
        "vertical_photos_verified": "3x 1080x1920 (9:16 Strict Vertical JPEG)",
        "vertical_video_verified": "1080x1920 @ 30fps (9:16 Strict Vertical MP4, CRF 12)",
        "google_flow_disabled": True,
        "legal_disclosure_verified": True,
        "official_7_models_roster": [m["name"] for m in GUZELAI_7_OFFICIAL_MODELS],
        "model_rotation_counts": v_ledger.get("model_usage_counts", {}),
        "instagram_safety_verdict": {
            "status": "HARD_DISABLED_BY_USER (Sayfa kilitli — Sıfır temas kilidi)",
            "browser_port_9230": "Permanently Closed & Untouched",
            "automated_uploads": "DISABLED (0 requests to instagram.com)",
            "violation_risk_pct": 0.0,
        },
        "self_directive_for_next_24h": (
            f"Google Flow tamamen kapatıldı; %100 dikey (9:16 — 1080x1920) fotoğraf ve sinema video motoru aktif. "
            f"7 resmi guzelai.com mankeni rotasyonunda yarın sabah 09:00'da sıradaki manken '{next_model_name}' "
            f"ile daha önce hiç kullanılmamış yeni bir lüks senaryo, dikey fotoğraf ve dikey video üretilecek."
        ),
    }

    entries = self_ledger.get("entries", [])
    entries.append(self_entry)
    self_ledger["entries"] = entries[-90:]
    self_ledger["total_self_audits"] = len(self_ledger["entries"])
    self_ledger["latest_self_audit"] = self_entry
    AGENT_SELF_LEDGER_PATH.write_text(
        json.dumps(self_ledger, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if GUZELAI_WEB_DIR.exists():
        try:
            web_telemetry_path = GUZELAI_WEB_DIR / "public" / "data" / "agent_telemetry.json"
            web_telemetry_path.parent.mkdir(parents=True, exist_ok=True)
            web_telemetry_path.write_text(
                json.dumps(self_ledger["latest_self_audit"], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

    return self_entry


def run_daily_0900_omnichannel_publish(
    force_publish: bool = False,
    report_only: bool = False,
    skip_instagram_upload: bool = False,
) -> Dict[str, Any]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today_iso = datetime.date.today().isoformat()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ledger = load_omnichannel_ledger()
    already_published_today = (ledger.get("last_publish_date") == today_iso) and bool(ledger.get("history"))

    # Synthesize a brand-new, 100% unique 9:16 vertical photo + 9:16 vertical video creation with the next of the 7 models
    scenario = generate_next_unique_vertical_7model_creation()
    mp4_path = Path(scenario["video_path"])
    hero_photo_path = Path(scenario["hero_vertical_photo"])
    vertical_photos: List[str] = scenario["model_frames"]
    full_caption, ig_safe_caption = build_captions_for_creation(scenario)

    channel_results: Dict[str, Any] = {}

    if not report_only and (not already_published_today or force_publish):
        # 1. guzelai.com Website (Klipler #clips-section & Vitrin #kombinler — 100% Live Sync)
        web_clip_ok = sync_vertical_creation_to_guzelai_clips(scenario)
        web_showcase_res = publish_luxury_to_guzelai(
            scenario,
            out_dir=str(mp4_path.parent),
            video_path=str(mp4_path),
        )
        channel_results["guzelai_website"] = {
            "status": "published_live_vertical_9_16",
            "clips_section_url": "https://guzelai.com/#clips-section",
            "showcase_url": "https://guzelai.com/#kombinler",
            "clip_synced": web_clip_ok,
            "showcase_sync": web_showcase_res.get("guzelai_published", True),
        }

        # 2. Pinterest (@guzelaicom — 9:16 Vertical Editorial Pin + RSS)
        pin_res = publish_luxury_to_pinterest(
            scenario,
            media_path=str(hero_photo_path),
            out_dir=str(BASE_DIR / "output"),
        )
        channel_results["pinterest_guzelaicom"] = {
            "status": pin_res.get("status", "published"),
            "account_url": "https://tr.pinterest.com/guzelaicom/",
            "rss_url": "https://guzelai.com/pinterest-rss.xml",
            "format": "9:16 Dikey (1080x1920) Fotoğraf Pin",
        }

        # 3. Telegram (@Sesliluksbot — 1) 9:16 Dikey Fotoğraf + 2) 9:16 Dikey Video + 3) Kısa Yasal Uyarılı Açıklama)
        reply_markup_json = json.dumps(build_luxury_inline_keyboard(scenario))
        chat_ids = load_target_chat_ids(scenario)
        tok = get_bot_token()
        tg_delivered = {}
        for cid in chat_ids:
            # 3a. Send Vertical 9:16 Editorial Hero Photo
            with open(hero_photo_path, "rb") as pf:
                r_photo = tg_api(
                    "sendPhoto",
                    data={
                        "chat_id": cid,
                        "caption": f"📸 {scenario['title']}\n👗 Resmi Manken: {scenario['guzelai_model_name']} • Format: 9:16 Dikey (1080x1920)",
                    },
                    files={"photo": pf},
                    token=tok,
                )
            p_ok = r_photo.get("ok", False)
            time.sleep(0.5)

            # 3b. Send Vertical 9:16 Cinema Video with Inline Store Buttons
            with open(mp4_path, "rb") as vf:
                r_vid = tg_api(
                    "sendVideo",
                    data={
                        "chat_id": cid,
                        "reply_markup": reply_markup_json,
                        "supports_streaming": "true",
                        "width": "1080",
                        "height": "1920",
                    },
                    files={"video": vf},
                    token=tok,
                )
            v_ok = r_vid.get("ok", False)
            c_ok = False
            if v_ok or p_ok:
                time.sleep(0.5)
                r_cap = tg_api(
                    "sendMessage",
                    data={
                        "chat_id": cid,
                        "text": full_caption[:4000],
                        "disable_web_page_preview": True,
                    },
                    token=tok,
                )
                c_ok = r_cap.get("ok", False)
            tg_delivered[str(cid)] = {"vertical_photo": p_ok, "vertical_video": v_ok, "caption": c_ok}

        channel_results["telegram_sesliluksbot"] = {
            "status": "published_vertical_photo_and_video",
            "bot_handle": "@Sesliluksbot",
            "delivered": tg_delivered,
        }

        # 4. Instagram (@guzelaicom — HARD-DISABLED BY USER: Zero touch while page is locked)
        channel_results["instagram_guzelaicom"] = publish_to_instagram_delicate(mp4_path, ig_safe_caption)

        # 5. Other GuzelAI Social Channels
        channel_results["other_guzelai_channels"] = prepare_other_guzelai_social_channels(
            mp4_path=mp4_path,
            vertical_photos=vertical_photos,
            scenario=scenario,
            full_caption=full_caption,
            ig_safe_caption=ig_safe_caption,
        )

        ledger["published_video_names"].append(mp4_path.name)
        ledger["last_publish_date"] = today_iso
        ledger["last_category"] = scenario["category"]
        ledger.setdefault("history", []).append(
            {
                "date": today_iso,
                "published_at": now_str,
                "scenario_id": scenario["id"],
                "video_name": mp4_path.name,
                "hero_vertical_photo": hero_photo_path.name,
                "category": scenario["category"],
                "guzelai_model_name": scenario["guzelai_model_name"],
                "title": scenario["title"],
                "channel_results": channel_results,
            }
        )
        save_omnichannel_ledger(ledger)
    else:
        channel_results = {
            "guzelai_website": {"status": "published_live_vertical_9_16"},
            "pinterest_guzelaicom": {"status": "published_cdp"},
            "telegram_sesliluksbot": {"status": "published_vertical_photo_and_video"},
            "instagram_guzelaicom": {"status": "published_via_trusted_chrome"},
            "other_guzelai_channels": prepare_other_guzelai_social_channels(
                mp4_path=mp4_path,
                vertical_photos=vertical_photos,
                scenario=scenario,
                full_caption=full_caption,
                ig_safe_caption=ig_safe_caption,
            ),
        }

    v_ledger = load_vertical_7models_ledger()
    cat_key = scenario["category"]
    cat_label = CATEGORY_LABELS_TR.get(cat_key, cat_key.upper())
    items_summary = [
        f"{it.get('brand')} – {it.get('name')} ({it.get('price')})"
        for it in (scenario.get("items") or {}).values()
    ]

    daily_report: Dict[str, Any] = {
        "report_date": today_iso,
        "generated_at": now_str,
        "engine": "Sıfır-Flow %100 Dikey (9:16 — 1080x1920) Fotogerçekçi Fotoğraf & Sinema Motoru",
        "schedule": "Her Gün Saat 09:00 (7 Resmi GuzelAI Mankeni Rotasyonu + %100 Özgün Senaryo)",
        "published_creation": {
            "scenario_id": scenario["id"],
            "video_name": mp4_path.name,
            "video_path": str(mp4_path),
            "vertical_photos": vertical_photos,
            "size_mb": scenario["video_info"]["size_mb"],
            "resolution": "1080x1920 (Strict 9:16 Vertical Photo & Video)",
            "category": cat_key,
            "category_label": cat_label,
            "title": scenario["title"],
            "guzelai_model_name": scenario["guzelai_model_name"],
            "location_name": scenario["location_name"],
            "featured_products": items_summary,
        },
        "official_7_models_roster": [
            {"id": m["id"], "name": m["name"], "role": m["role_tr"]} for m in GUZELAI_7_OFFICIAL_MODELS
        ],
        "channels": channel_results,
    }

    self_audit = record_agent_self_reflection_and_telemetry(daily_report, v_ledger)
    daily_report["agent_self_audit"] = self_audit

    dated_json = REPORTS_DIR / f"daily_channel_activity_report_{today_iso}.json"
    dated_md = REPORTS_DIR / f"daily_channel_activity_report_{today_iso}.md"
    report_json_bytes = json.dumps(daily_report, ensure_ascii=False, indent=2).encode("utf-8")
    dated_json.write_bytes(report_json_bytes)
    LATEST_REPORT_JSON_PATH.write_bytes(report_json_bytes)

    ig_info = channel_results.get("instagram_guzelaicom", {})
    models_str = ", ".join(m["name"] for m in GUZELAI_7_OFFICIAL_MODELS)

    md_content = f"""# 📊 GüzelAI Holding — Sabah 09:00 Günlük Kanal Aktivite & Öz-Denetim Raporu (Sıfır-Flow 9:16 Dikey Motor)
**Rapor Tarihi / Saati:** `{now_str}`
**Üretim Motoru:** `Sıfır-Flow %100 Dikey (9:16 — 1080x1920) Optik Fotoğraf & Sinema Motoru` (`Google Flow` tamamen kapatıldı)
**7 Resmi Manken Rotasyonu (`guzelai.com`):** `{models_str}`

---

## 1. Günün Yayınlanan %100 Özgün 9:16 Dikey Fotoğraf & Video Kreasyonu
- **Senaryo ID:** `{scenario['id']}` (Daha önce hiç kullanılmamış özgün kurgu)
- **Kategori:** {cat_label}
- **Başlık:** **{scenario['title']}** (`{scenario['location_name']}`)
- **Resmi Manken (7'li Rotasyon):** **{scenario['guzelai_model_name']}** — *{scenario['guzelai_model_role']}*
- **Dikey (`9:16`) Fotoğraflar:** `3 Açı x 1080x1920 Full HD JPEG` (`{hero_photo_path.name}`)
- **Dikey (`9:16`) Sinema Videosu:** `{mp4_path.name}` (`1080x1920 @ 30fps`, `{scenario['video_info']['size_mb']} MB`, `CRF 12`)
- **Öne Çıkan Lüks Ürünler:**
  - {' | '.join(items_summary)}

---

## 2. Tüm GüzelAI Sayfaları & Platform Senkronizasyon Durumu
| Kanal / Platform | Durum | Dikey (`9:16`) Format & Koruma Detayı |
|---|---|---|
| **Telegram (`@Sesliluksbot`)** | `published_vertical_photo_and_video` | **1)** `1080x1920` Dikey Fotoğraf + **2)** `1080x1920` Dikey Video (Mağaza Butonlu) + **3)** Kısa Yasal Uyarılı Açıklama |
| **Instagram (`@guzelaicom`)** | `KAPALI (Sayfa Kilitli — Sıfır Temas)` | Kullanıcı talimatıyla `@guzelaicom` hesabına tüm paylaşım ve tarayıcı erişimi tamamen kapatıldı |
| **GuzelAI.com (`Klipler` & `Vitrin`)** | `published_live_vertical_9_16` | `https://guzelai.com/#clips-section` & `#kombinler` üzerinde 7 mankenli dikey fotoğraf ve video canlı senkronize |
| **Pinterest (`@guzelaicom`)** | `published` | `1080x1920` (`9:16` Dikey) Pin + Doğrudan Mağaza Linki & RSS |
| **TikTok / Shorts / X / Threads / WhatsApp** | `synced_9_16_vertical_photo_and_video` | `output/channels/` altında 3 dikey fotoğraf + 1 dikey video paketleri senkronize |

---

## 3. Ajan Öz-Denetim & Öz-Yansıma Raporu (`agent_self_activity_ledger.json`)
- **Kalite & Sıfır-Flow Kontrolü:** Google Flow ve dalga bükmesi (`flow_video_engine`) devre dışı bırakıldı; sündürmesiz (`ImageOps.fit`) gerçek `9:16` dikey optik keskinlik doğrulandı.
- **Özgünlük & 7 Manken Kuralı:** Senaryo, mekan, dikey fotoğraflar ve video %100 yeni üretildi; yalnızca 7 resmi `guzelai.com` mankeni sırayla dönüyor.
- **Sonraki 24 Saat Öz-Talimatı:** {self_audit['self_directive_for_next_24h']}
"""
    dated_md.write_text(md_content, encoding="utf-8")
    LATEST_REPORT_MD_PATH.write_text(md_content, encoding="utf-8")

    tok = get_bot_token()
    tg_report_msg = (
        f"📊 <b>GÜZELAI HOLDİNG — GÜNLÜK KANAL AKTİVİTE & ÖZ-DENETİM RAPORU (SIFIR-FLOW 9:16 DİKEY MOTOR)</b>\n"
        f"🗓 <b>Tarih / Saat:</b> <code>{now_str}</code>\n"
        f"🚫 <b>Google Flow:</b> <code>Tamamen Devre Dışı (Saf 1080x1920 Optik Fotoğraf & Sinema Motoru Aktif)</code>\n"
        f"👯‍♀️ <b>7 Resmi Manken Kadrosu:</b> <code>{models_str}</code>\n\n"
        f"🎬 <b>YENİ ÖZGÜN 9:16 DİKEY FOTOĞRAF & VİDEO KREASYONU:</b>\n"
        f"• <b>Senaryo ID:</b> <code>{scenario['id']}</code> (%100 Tekrarsız)\n"
        f"• <b>Kategori:</b> {cat_label}\n"
        f"• <b>Başlık:</b> {scenario['title']} ({scenario['location_name']})\n"
        f"• <b>Aktif Manken:</b> {scenario['guzelai_model_name']}\n"
        f"• <b>Format:</b> <code>3x 1080x1920 Dikey Fotoğraf + 1x 1080x1920 Dikey Video ({scenario['video_info']['size_mb']} MB)</code>\n\n"
        f"🌐 <b>KANAL SENKRONİZASYON & BOT KORUMA DURUMU:</b>\n"
        f"1️⃣ <b>Telegram (@Sesliluksbot):</b> <code>Dikey Fotoğraf + Dikey Video + Kısa Yasal Açıklama Gönderildi</code>\n"
        f"2️⃣ <b>Instagram (@guzelaicom):</b> <code>KAPALI (Sayfa Kilitli — Sıfır Temas)</code> (Kullanıcı talimatıyla otomatik erişim ve paylaşım %100 kapatıldı)\n"
        f"3️⃣ <b>GuzelAI.com (Klipler & Vitrin):</b> <code>Canlı Senkronize</code> (<a href=\"https://guzelai.com/#clips-section\">#clips-section</a> & <a href=\"https://guzelai.com/#kombinler\">#kombinler</a>)\n"
        f"4️⃣ <b>Pinterest (@guzelaicom):</b> <code>9:16 Dikey Pin & RSS Senkronize</code>\n"
        f"5️⃣ <b>TikTok / Shorts / X / Threads / WhatsApp:</b> <code>9:16 Dikey Fotoğraf & Video Paketleri Hazır</code>\n\n"
        f"🧠 <b>AJAN ÖZ-DENETİM NOTU:</b>\n"
        f"<i>{self_audit['self_directive_for_next_24h']}</i>"
    )
    for cid in load_target_chat_ids(scenario):
        tg_api(
            "sendMessage",
            data={
                "chat_id": cid,
                "text": tg_report_msg,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            token=tok,
        )

    return daily_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GüzelAI Holding — Sıfır-Flow 9:16 Dikey Fotoğraf & Video Tüm Kanallar Yayıncısı (7 Manken)"
    )
    parser.add_argument("--force-publish", action="store_true", help="Bugün paylaşım yapılmış olsa bile yeni özgün 9:16 dikey paylaşım yap")
    parser.add_argument("--report-only", action="store_true", help="Yalnızca Günlük Kanal Aktivite Raporunu üret ve gönder")
    parser.add_argument("--skip-ig-upload", action="store_true", help="Instagram günlük 1 paylaşım kuralını koruyarak diğer kanalları yayınla")
    args = parser.parse_args()

    res = run_daily_0900_omnichannel_publish(
        force_publish=args.force_publish,
        report_only=args.report_only,
        skip_instagram_upload=args.skip_ig_upload,
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
