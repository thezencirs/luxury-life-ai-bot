"""
Luxury Life AI (@Luxurylifeaibot) — Ham Materyal (Fotoğraf, Video, Ürün Linki, Konsept) Yakalayıcı,
Birebir Ürün & İş Birliği Link Kazıyıcı ve %100 Fotogerçekçi Model / Dekupe Sentez Motoru
"""
import base64
import hashlib
import json
import os
import re
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

import html
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from luxury_viral_concepts import (
    BASE_DIR,
    LUXURY_MASTER_ARCHETYPES,
    VIRAL_RETENTION_FRAMEWORKS,
    detect_luxury_category,
    resolve_smart_collaboration_url,
)

DEFAULT_BOT_TOKEN = "9244899175:AAGEkK0KD_sMxMB_wJaS_4Mlrjh8IGLgr7c"
DEFAULT_ADMIN_CHAT_ID = "995164733"
GITHUB_REPO_SLUG = os.environ.get("LUXURY_GITHUB_REPO", "thezencirs/luxury-life-ai-bot")

TG_QUEUE_PATH = BASE_DIR / "output" / "telegram_luxury_queue.json"
SUBSCRIBERS_FILE = BASE_DIR / "assets" / "telegram_subscribers.json"


def get_bot_token() -> str:
    return os.environ.get("TELEGRAM_BOT_TOKEN", DEFAULT_BOT_TOKEN).strip()


def tg_call(method: str, payload: Optional[dict] = None, timeout: int = 20) -> dict:
    tok = get_bot_token()
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/{method}",
            json=payload or {},
            timeout=timeout,
        )
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _download_tg_file(file_id: str, dest: Path) -> bool:
    tok = get_bot_token()
    try:
        info = tg_call("getFile", {"file_id": file_id})
        if not info.get("ok"):
            return False
        fp = info["result"]["file_path"]
        r = requests.get(f"https://api.telegram.org/file/bot{tok}/{fp}", timeout=60)
        if r.status_code == 200 and len(r.content) > 500:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            return True
    except Exception:
        pass
    return False


def load_tg_queue() -> List[Dict[str, Any]]:
    os.makedirs(TG_QUEUE_PATH.parent, exist_ok=True)
    local_q: List[Dict[str, Any]] = []
    if TG_QUEUE_PATH.exists():
        try:
            data = json.loads(TG_QUEUE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list):
                local_q = data
        except Exception:
            pass

    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if gh_token:
        try:
            r = requests.get(
                f"https://api.github.com/repos/{GITHUB_REPO_SLUG}/contents/output/telegram_luxury_queue.json",
                headers={"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"},
                timeout=10,
            )
            if r.status_code == 200:
                content_b64 = r.json().get("content", "")
                remote_q = json.loads(base64.b64decode(content_b64).decode("utf-8"))
                if isinstance(remote_q, list):
                    existing_ids = {item.get("request_id") for item in local_q}
                    for rq in remote_q:
                        if rq.get("request_id") and rq.get("request_id") not in existing_ids:
                            local_q.append(rq)
        except Exception:
            pass
    return local_q


def save_tg_queue(queue: List[Dict[str, Any]], sync_github: bool = True) -> None:
    os.makedirs(TG_QUEUE_PATH.parent, exist_ok=True)
    raw_json = json.dumps(queue, ensure_ascii=False, indent=2)
    TG_QUEUE_PATH.write_text(raw_json, encoding="utf-8")

    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if sync_github and gh_token:
        try:
            api_url = f"https://api.github.com/repos/{GITHUB_REPO_SLUG}/contents/output/telegram_luxury_queue.json"
            headers = {"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"}
            get_r = requests.get(api_url, headers=headers, timeout=10)
            payload: Dict[str, Any] = {
                "message": "chore(telegram-queue): sync pending luxury telegram requests [skip ci]",
                "content": base64.b64encode(raw_json.encode("utf-8")).decode("ascii"),
            }
            if get_r.status_code == 200 and get_r.json().get("sha"):
                payload["sha"] = get_r.json()["sha"]
            requests.put(api_url, headers=headers, json=payload, timeout=12)
        except Exception:
            pass


def trigger_github_workflow_dispatch(category: str = "otomatik") -> bool:
    """Kuyrukta bekleyen Telegram isteği olduğunda GitHub Actions iş akışını anında tetikler."""
    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if not gh_token:
        return False
    try:
        r = requests.post(
            f"https://api.github.com/repos/{GITHUB_REPO_SLUG}/actions/workflows/luxury_reels_pipeline.yml/dispatches",
            headers={"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"},
            json={"ref": "main", "inputs": {"category": category, "force_run": "1"}},
            timeout=12,
        )
        return r.status_code in (200, 201, 204)
    except Exception:
        return False


def scrape_product_url(url: str, fallback_idx: int = 1, default_cat: str = "kombin") -> Dict[str, Any]:
    """
    Kullanıcının Telegram'dan attığı ürün linkini (Beymen, Sephora, Trendyol, Vakko, Zara, Atasay vb.)
    kazıyarak birebir ürün adını, markasını, fiyatını, görselini ve doğrudan linkini çıkarır.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    brand = "LÜKS MAĞAZA"
    name = "Seçkin Lüks Koleksiyon Parçası"
    price_str = "Özel Fiyat"
    img_url = ""
    sku = f"LUX-{100 + fallback_idx}"

    host = re.sub(r"^https?://(www\.)?", "", url.lower()).split("/")[0]
    if "beymen" in host:
        brand = "BEYMEN"
    elif "sephora" in host:
        brand = "SEPHORA"
    elif "vakko" in host:
        brand = "VAKKO"
    elif "trendyol" in host:
        brand = "TRENDYOL LUXURY"
    elif "zara" in host:
        brand = "ZARA"
    elif "massimodutti" in host:
        brand = "MASSIMO DUTTI"
    elif "swarovski" in host:
        brand = "SWAROVSKI"
    elif "atasay" in host:
        brand = "ATASAY"
    elif "zenpirlanta" in host:
        brand = "ZEN PIRLANTA"
    elif "porsche" in host:
        brand = "PORSCHE"
    elif "mandarinoriental" in host:
        brand = "MANDARIN ORIENTAL"

    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200:
            raw_html = r.text
            og_t = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', raw_html, re.I)
            if not og_t:
                og_t = re.search(r'<title[^>]*>([^<]+)</title>', raw_html, re.I)
            if og_t:
                raw_t = html.unescape(og_t.group(1)).split("|")[0].split("-")[0].strip()
                if len(raw_t) > 4:
                    name = raw_t[:68]

            og_i = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', raw_html, re.I)
            if og_i:
                img_url = html.unescape(og_i.group(1)).strip()

            price_m = re.search(r"(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*(?:TL|₺)", raw_html)
            if price_m:
                price_str = f"{price_m.group(1)}₺"
    except Exception:
        pass

    return {
        "category_label": f"Özel Seçim #{fallback_idx}",
        "emoji": "💎",
        "brand": brand,
        "name": name,
        "price": price_str,
        "price_val": 5000.0,
        "sku": sku,
        "color": "Lüks Ton",
        "store_url": url,
        "image_url": img_url,
    }


def poll_and_enqueue_telegram_requests(acknowledge: bool = True) -> List[Dict[str, Any]]:
    """
    @Luxurylifeaibot üzerindeki tüm yeni mesajları, ürün linklerini, fotoğrafları ve ham videoları
    yakalayıp `output/telegram_luxury_queue.json` içine kaydeder.
    """
    sub_data = {"chats": {}, "last_update_id": 0}
    if SUBSCRIBERS_FILE.exists():
        try:
            sub_data = json.loads(SUBSCRIBERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    offset = int(sub_data.get("last_update_id", 0)) + 1
    res = tg_call("getUpdates", {"offset": offset, "timeout": 2})
    queue = load_tg_queue()
    existing_ids = {q.get("request_id") for q in queue}

    if res.get("ok"):
        updates = res.get("result", [])
        changed_sub = False
        for upd in updates:
            uid = int(upd.get("update_id", 0))
            if uid > int(sub_data.get("last_update_id", 0)):
                sub_data["last_update_id"] = uid
                changed_sub = True

            if "callback_query" in upd:
                cb = upd["callback_query"]
                cb_id = cb.get("id")
                cb_data = cb.get("data", "")
                cb_chat = (cb.get("message") or {}).get("chat") or {}
                cb_cid = str(cb_chat.get("id", DEFAULT_ADMIN_CHAT_ID))
                if cb_id:
                    tg_call("answerCallbackQuery", {"callback_query_id": cb_id, "text": "💎 Lüks Reels üretimi başlatıldı!"})
                if cb_data.startswith("gen_cat:"):
                    cat_code = cb_data.split(":", 1)[1]
                    req_id = f"tg_cb_{uid}"
                    if req_id not in existing_ids:
                        queue.append({
                            "request_id": req_id,
                            "update_id": uid,
                            "requester_chat_id": cb_cid,
                            "urls": [],
                            "photo_path": "",
                            "video_path": "",
                            "text": f"/{cat_code}",
                            "category": cat_code,
                            "created_at": datetime.utcnow().isoformat() + "Z",
                        })
                        existing_ids.add(req_id)
                continue

            msg = upd.get("message") or upd.get("channel_post")
            if not isinstance(msg, dict):
                continue
            chat = msg.get("chat") or {}
            cid = str(chat.get("id", ""))
            if not cid:
                continue

            user_title = chat.get("title") or chat.get("username") or chat.get("first_name") or cid
            sub_data.setdefault("chats", {})[cid] = {
                "id": chat.get("id"),
                "type": chat.get("type", "private"),
                "title": user_title,
                "username": chat.get("username", ""),
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            changed_sub = True

            text = (msg.get("text") or "").strip()
            caption = (msg.get("caption") or "").strip()
            combined = text or caption
            urls = re.findall(r"https?://[^\s<>\"']+", combined)
            clean_txt = re.sub(r"https?://[^\s<>\"']+", "", combined).strip()

            photo_rel = ""
            if msg.get("photo"):
                best_p = msg["photo"][-1]
                dest_p = BASE_DIR / "assets" / f"tg_raw_photo_{uid}.jpg"
                if _download_tg_file(best_p["file_id"], dest_p):
                    photo_rel = f"assets/tg_raw_photo_{uid}.jpg"

            video_rel = ""
            vid_obj = msg.get("video") or msg.get("document")
            if isinstance(vid_obj, dict) and str(vid_obj.get("mime_type", "")).startswith("video"):
                dest_v = BASE_DIR / "assets" / f"tg_raw_video_{uid}.mp4"
                if _download_tg_file(vid_obj["file_id"], dest_v):
                    video_rel = f"assets/tg_raw_video_{uid}.mp4"

            cmd_only = text.lower().split("@")[0] if text else ""
            if cmd_only in ("/start", "/analiz", "/yardim") and not urls and not photo_rel and not video_rel:
                if acknowledge:
                    tg_call(
                        "sendMessage",
                        {
                            "chat_id": cid,
                            "parse_mode": "HTML",
                            "text": (
                                "💎 <b>Luxury Life AI (@Luxurylifeaibot) Komuta Merkezine Hoş Geldiniz!</b>\n\n"
                                "Bana doğrudan:\n"
                                "• 📸 <b>Takı, Makyaj, Kombin, Otel veya Araba fotoğrafı / ham videosu</b> atabilirsiniz.\n"
                                "• 🔗 <b>Ürün linki</b> (Beymen, Sephora, Vakko, Trendyol, Zara vb.) gönderebilirsiniz.\n"
                                "• 🚀 Veya <b>/taki</b>, <b>/makyaj</b>, <b>/kombin</b>, <b>/otel</b>, <b>/araba</b>, <b>/uret</b> yazarak anında yüksek kaydetme oranlı 2K GraphMotion Plus Reels üretebilirsiniz!\n\n"
                                "<i>Hazırlanan her video; 1) Açıklayıcı Reji & Tutuş Analizi, 2) Saf Copy-Paste Instagram Açıklaması (#reklam #işbirliğiyoktur dahil) ve 3) Saf Copy-Paste Ürün/İş Birliği Linkleri ile teslim edilir.</i>"
                            ),
                        },
                    )
                continue

            if urls or photo_rel or video_rel or clean_txt:
                cat = detect_luxury_category(clean_txt, urls)
                for cw in ("/uret", "/yayinla", "/paylas", "/taki", "/makyaj", "/kombin", "/otel", "/araba"):
                    clean_txt = re.sub(rf"(?i)^{re.escape(cw)}\b", "", clean_txt).strip()

                req_id = f"tg_lux_{uid}"
                if req_id not in existing_ids:
                    cat_tr_map = {
                        "taki": "💎 Mücevher & Saat",
                        "makyaj": "💄 Lüks Makyaj & Parfüm",
                        "kombin": "🧥 Old Money Kombin",
                        "otel": "🏨 Ultra Lüks Otel & Tatil",
                        "araba": "🏎️ Süper Spor Otomobil",
                        "otomatik": "✨ Otomatik Lüks Seçki",
                    }
                    queue.append({
                        "request_id": req_id,
                        "update_id": uid,
                        "requester_chat_id": cid,
                        "requester_name": user_title,
                        "urls": urls,
                        "photo_path": photo_rel,
                        "video_path": video_rel,
                        "text": clean_txt,
                        "category": cat,
                        "created_at": datetime.utcnow().isoformat() + "Z",
                    })
                    existing_ids.add(req_id)
                    if acknowledge:
                        tg_call(
                            "sendMessage",
                            {
                                "chat_id": cid,
                                "parse_mode": "HTML",
                                "text": (
                                    f"💎 <b>Luxury Life AI — Ham Materyal &amp; Talep Alındı!</b>\n"
                                    f"• <b>Algılanan Kategori:</b> {cat_tr_map.get(cat, '✨ Lüks Yaşam')}\n"
                                    f"• <b>Algılanan Link / Medya:</b> {len(urls)} Link | {'📸 Fotoğraf Var' if photo_rel else ''} {'🎬 Video Var' if video_rel else ''}\n\n"
                                    f"🎬 <i>Doğru kamera açısı, lüks mekan, %100 gerçekçi model, 2K GraphMotion Plus video ve birebir ürün linkleriniz hazırlanıyor (5-10 dk içinde teslim edilir)...</i>"
                                ),
                            },
                        )

        if changed_sub:
            SUBSCRIBERS_FILE.parent.mkdir(parents=True, exist_ok=True)
            SUBSCRIBERS_FILE.write_text(json.dumps(sub_data, ensure_ascii=False, indent=2), encoding="utf-8")

    save_tg_queue(queue, sync_github=bool(queue))
    return queue


def remove_white_studio_background(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    arr = np.array(rgba, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    sat = np.max(arr[:, :, :3], axis=2) - np.min(arr[:, :, :3], axis=2)
    white_mask = (lum > 240.0) & (sat < 18.0)
    soft_mask = (lum > 226.0) & (sat < 26.0)
    alpha = arr[:, :, 3].copy()
    alpha[white_mask] = 0.0
    edge_zone = soft_mask & (~white_mask)
    alpha[edge_zone] = alpha[edge_zone] * np.clip((242.0 - lum[edge_zone]) / 16.0, 0.0, 1.0)
    arr[:, :, 3] = alpha
    out = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    bbox = out.split()[3].point(lambda p: 255 if p > 20 else 0).getbbox()
    if bbox:
        out = out.crop(bbox)
    return out


def fetch_ai_luxury_image(prompt: str, width: int = 768, height: int = 1024, seed: int = 42) -> Optional[Image.Image]:
    """Pollinations FLUX-realism üzerinden hızlı bulut görsel sentezler (timeout korumalı)."""
    encoded = quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&model=flux-realism&nologo=true"
    try:
        r = requests.get(url, timeout=18)
        if r.status_code == 200 and len(r.content) > 4000:
            return Image.open(BytesIO(r.content)).convert("RGB")
    except Exception:
        pass
    return None


def _render_procedural_luxury_packshot(item: Dict[str, Any], slot_idx: int) -> Image.Image:
    """Bulut AI API yavaşsa veya çevrimdışıysa, sıfır gecikmeyle şeffaf lüks mücevher/kozmetik/moda ürün ikonu üretir."""
    size = 640
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Kadife & Altın Çerçeveli Lüks Madalyon Diski
    palettes = [
        ((24, 20, 18, 250), (218, 182, 118, 255)),
        ((42, 18, 26, 250), (235, 198, 138, 255)),
        ((16, 28, 24, 250), (212, 175, 108, 255)),
        ((28, 24, 34, 250), (225, 192, 132, 255)),
        ((38, 26, 18, 250), (228, 188, 120, 255)),
        ((18, 22, 32, 250), (216, 180, 114, 255)),
    ]
    bg_col, gold_col = palettes[(slot_idx - 1) % len(palettes)]

    draw.rounded_rectangle((48, 48, size - 48, size - 48), radius=96, fill=bg_col, outline=gold_col, width=6)
    draw.rounded_rectangle((68, 68, size - 68, size - 68), radius=80, outline=(gold_col[0], gold_col[1], gold_col[2], 130), width=2)

    try:
        f_big = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 40)
        f_sub = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
    except Exception:
        f_big = ImageFont.load_default()
        f_sub = ImageFont.load_default()

    brand = str(item.get("brand", "LUXURY"))[:22].upper()
    lbl = str(item.get("category_label", "LÜKS DETAY")).upper()
    name_words = str(item.get("name", "")).split()
    line1 = " ".join(name_words[:3])[:22]
    line2 = " ".join(name_words[3:6])[:22]

    # Üst altın taç barı
    draw.rounded_rectangle((120, 110, size - 120, 166), radius=24, fill=(gold_col[0], gold_col[1], gold_col[2], 45), outline=gold_col, width=2)
    draw.text((size // 2, 138), lbl, fill=gold_col, font=f_sub, anchor="mm")

    # Merkez elmas/altın geometrik amblem
    cx, cy = size // 2, 285
    pts = [(cx, cy - 68), (cx + 68, cy), (cx, cy + 68), (cx - 68, cy)]
    draw.polygon(pts, fill=(gold_col[0], gold_col[1], gold_col[2], 65), outline=gold_col)
    draw.ellipse((cx - 32, cy - 32, cx + 32, cy + 32), fill=gold_col)

    draw.text((size // 2, 405), brand, fill=(255, 255, 255, 255), font=f_big, anchor="mm")
    draw.text((size // 2, 460), line1, fill=(235, 222, 198, 255), font=f_sub, anchor="mm")
    if line2:
        draw.text((size // 2, 498), line2, fill=(210, 196, 172, 255), font=f_sub, anchor="mm")

    return canvas


def _render_procedural_luxury_scene(concept: Dict[str, Any], step_idx: int) -> Image.Image:
    """
    Bulut görsel servisi gecikirse veya ek sahne gerekirse, 1440x2560 2K QHD+ sinematik
    Obsidian & Champagne Gold lüks sahne karesi üretir.
    """
    w, h = 1080, 1920
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    shift = (step_idx - 1) * 0.08
    nx = (xx - w * (0.5 + shift)) / (w * 0.65)
    ny = (yy - h * 0.42) / (h * 0.65)
    dist = np.clip(np.sqrt(nx * nx + ny * ny), 0.0, 1.4) / 1.4

    cat = concept.get("category", "kombin")
    tone_map = {
        "taki": ((36, 26, 18), (10, 8, 12)),
        "makyaj": ((52, 34, 38), (16, 10, 14)),
        "kombin": ((44, 34, 26), (12, 10, 10)),
        "otel": ((22, 38, 48), (8, 14, 22)),
        "araba": ((18, 34, 26), (8, 12, 10)),
    }
    c_inner, c_outer = tone_map.get(cat, tone_map["kombin"])
    r = (c_inner[0] * (1.0 - dist) + c_outer[0] * dist).astype(np.uint8)
    g = (c_inner[1] * (1.0 - dist) + c_outer[1] * dist).astype(np.uint8)
    b = (c_inner[2] * (1.0 - dist) + c_outer[2] * dist).astype(np.uint8)
    img = Image.fromarray(np.dstack([r, g, b]), mode="RGB")
    draw = ImageDraw.Draw(img, "RGBA")

    # Altın bokeh ışık küreleri
    rng = np.random.default_rng(100 + step_idx * 17)
    for _ in range(28):
        bx = int(rng.integers(60, w - 60))
        by = int(rng.integers(120, h - 220))
        br = int(rng.integers(18, 95))
        ba = int(rng.integers(18, 58))
        draw.ellipse((bx - br, by - br, bx + br, by + br), fill=(238, 202, 135, ba))

    img = img.filter(ImageFilter.GaussianBlur(radius=4))
    draw = ImageDraw.Draw(img, "RGBA")

    # Mimari altın kemer / vitrin silüeti
    draw.rounded_rectangle((70, 140, w - 70, h - 140), radius=420, outline=(218, 182, 118, 165), width=4)
    draw.rounded_rectangle((96, 166, w - 96, h - 166), radius=400, outline=(218, 182, 118, 85), width=2)
    return img


def ensure_concept_assets_ready(concept: Dict[str, Any], use_cloud_ai: bool = True) -> Dict[str, Any]:
    """
    Seçilen lüks konseptin 6 ürün dekupe görselini (`cutout_path`) ve 3 sahne/model karesini (`model_frames`)
    hazırlar. Kullanıcı Telegram'dan fotoğraf veya video gönderdiyse doğrudan onu başrole yerleştirir!
    """
    assets_dir = BASE_DIR / "assets"
    items_dir = assets_dir / "items"
    assets_dir.mkdir(parents=True, exist_ok=True)
    items_dir.mkdir(parents=True, exist_ok=True)

    cid = concept.get("id", "lux_default")
    seed_base = int(hashlib.md5(cid.encode("utf-8")).hexdigest()[:6], 16)

    user_photo_rel = concept.get("user_photo_path", "")
    user_photo_pil: Optional[Image.Image] = None
    if user_photo_rel and (BASE_DIR / user_photo_rel).exists():
        try:
            user_photo_pil = Image.open(BASE_DIR / user_photo_rel).convert("RGB")
        except Exception:
            user_photo_pil = None

    # 1) 6 Ürün Dekupe Görselini Hazırla
    items = concept.get("items", {})
    for idx, (slot_k, it) in enumerate(items.items(), start=1):
        rel_cut = f"assets/items/{cid}_{slot_k}.png"
        abs_cut = BASE_DIR / rel_cut
        if not abs_cut.exists():
            saved = False
            # Ürün URL'sinden kazınmış görsel varsa indir
            img_u = it.get("image_url", "")
            if img_u and img_u.startswith("http"):
                try:
                    ir = requests.get(img_u, timeout=12)
                    if ir.status_code == 200 and len(ir.content) > 1500:
                        raw_im = Image.open(BytesIO(ir.content)).convert("RGB")
                        remove_white_studio_background(raw_im).save(abs_cut, format="PNG")
                        saved = True
                except Exception:
                    pass

            # Kullanıcı fotoğraf gönderdiyse 1. karta doğrudan kullanıcının ham görselini dekupe/kart olarak koy
            if not saved and idx == 1 and user_photo_pil is not None:
                u_crop = user_photo_pil.copy()
                u_crop.thumbnail((640, 640), Image.Resampling.LANCZOS)
                u_rgba = u_crop.convert("RGBA")
                u_rgba.save(abs_cut, format="PNG")
                saved = True

            # Bulut AI Packshot (Hızlı mod)
            if not saved and use_cloud_ai and os.environ.get("FAST_PROCEDURAL_CARDS", "0") != "1":
                pack_prompt = it.get("en_packshot") or f"luxury {it.get('name', 'item')} isolated on pure solid white background #FFFFFF"
                ai_im = fetch_ai_luxury_image(pack_prompt, width=512, height=512, seed=seed_base + idx * 11)
                if ai_im is not None:
                    remove_white_studio_background(ai_im).save(abs_cut, format="PNG")
                    saved = True

            if not saved:
                _render_procedural_luxury_packshot(it, idx).save(abs_cut, format="PNG")

        it["cutout_path"] = str(abs_cut)

    # 2) 3 Sahne / Model Yürüyüş Karesini Hazırla
    model_frames: List[str] = []
    base_prompt = concept.get("model_prompt_en", "")
    pose_variants = [
        "cinematic golden hour shot, elegant confident pose, sharp 85mm f/1.4 focus",
        "dynamic mid-stride movement, luxury editorial lighting, 8k magazine realism",
        "close editorial angle showcasing luxury details and aura, golden rim light",
    ]
    for s_idx, pose_mod in enumerate(pose_variants, start=1):
        rel_frame = f"assets/{cid}_step{s_idx}.jpg"
        abs_frame = BASE_DIR / rel_frame
        if not abs_frame.exists():
            saved_f = False
            if s_idx == 1 and user_photo_pil is not None:
                # Kullanıcının gönderdiği fotoğrafı 9:16 lüks çerçeveye yerleştir
                bg_scene = _render_procedural_luxury_scene(concept, s_idx)
                u_copy = user_photo_pil.copy()
                u_copy.thumbnail((960, 1440), Image.Resampling.LANCZOS)
                bg_scene.paste(u_copy, ((1080 - u_copy.width) // 2, (1920 - u_copy.height) // 2))
                bg_scene.save(abs_frame, format="JPEG", quality=95)
                saved_f = True

            if not saved_f and use_cloud_ai:
                full_p = f"{base_prompt}, {pose_mod}"
                ai_scene = fetch_ai_luxury_image(full_p, width=768, height=1344, seed=seed_base + s_idx * 31)
                if ai_scene is not None:
                    ai_scene.resize((1080, 1920), Image.Resampling.LANCZOS).save(abs_frame, format="JPEG", quality=95)
                    saved_f = True

            if not saved_f:
                _render_procedural_luxury_scene(concept, s_idx).save(abs_frame, format="JPEG", quality=95)

        model_frames.append(str(abs_frame))

    concept["model_frames"] = model_frames
    return concept


def pop_next_telegram_custom_concept() -> Optional[Dict[str, Any]]:
    """
    Telegram kuyruğunda bekleyen kullanıcı isteği varsa alır, kategorisini ve ürün linklerini
    çözümler ve tam teşekküllü bir Luxury Concept sözlüğüne dönüştürür.
    """
    queue = poll_and_enqueue_telegram_requests(acknowledge=True)
    if not queue:
        return None

    req = queue.pop(0)
    save_tg_queue(queue, sync_github=True)

    cat = req.get("category", "otomatik")
    if cat == "otomatik":
        cat = detect_luxury_category(req.get("text", ""), req.get("urls", []))
    if cat == "otomatik":
        cat = "kombin"

    # İlgili kategorideki şablonu temel al ve kullanıcının link/fotoğraf/metin verilerini üzerine işle
    base_matches = [a for a in LUXURY_MASTER_ARCHETYPES if a["category"] == cat]
    base_arch = json.loads(json.dumps(base_matches[0] if base_matches else LUXURY_MASTER_ARCHETYPES[0]))

    req_hash = hashlib.md5(f"{req.get('request_id')}_{time.time()}".encode("utf-8")).hexdigest()[:6]
    base_arch["id"] = f"tg_lux_{cat}_{req_hash}"
    base_arch["requester_chat_id"] = req.get("requester_chat_id", DEFAULT_ADMIN_CHAT_ID)
    base_arch["user_photo_path"] = req.get("photo_path", "")
    base_arch["user_video_path"] = req.get("video_path", "")

    user_txt = (req.get("text") or "").strip()
    if len(user_txt) > 6:
        base_arch["title"] = f"{user_txt} ✨"
        base_arch["cover_headline"] = user_txt.upper()[:52]
        base_arch["viral_hook"] = f"💎 {user_txt}! Doğru açı, mekan ve birebir ürün linkleriyle kaydetmelik lüks reçete 👇✨"

    urls = req.get("urls") or []
    slot_keys = list(base_arch["items"].keys())
    for idx, u in enumerate(urls[:len(slot_keys)]):
        sk = slot_keys[idx]
        scraped = scrape_product_url(u, fallback_idx=idx + 1, default_cat=cat)
        base_arch["items"][sk].update({
            "brand": scraped["brand"],
            "name": scraped["name"],
            "price": scraped["price"],
            "sku": scraped["sku"],
            "store_url": scraped["store_url"],
            "image_url": scraped.get("image_url", ""),
        })

    base_arch["viral_analysis"] = VIRAL_RETENTION_FRAMEWORKS.get(cat, VIRAL_RETENTION_FRAMEWORKS["kombin"])
    return base_arch
