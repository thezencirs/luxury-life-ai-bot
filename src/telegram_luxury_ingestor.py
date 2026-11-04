"""
Luxury Life AI (@Luxurylifeaibot) — Ham Materyal (Fotoğraf, Çoklu Görsel, Video, Ürün Linki, Konsept Metni)
Yakalayıcı, Akıllı Mesaj Birleştirici, Yazım Düzeltici ve Birebir Görsel/Link Sentez Motoru
"""
import base64
import hashlib
import html
import json
import os
import re
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from luxury_viral_concepts import (
    BASE_DIR,
    LUXURY_MASTER_ARCHETYPES,
    SANTORINI_OIA_CUSTOM_TEMPLATE,
    VIRAL_RETENTION_FRAMEWORKS,
    detect_luxury_category,
    normalize_and_correct_user_text,
    resolve_smart_collaboration_url,
)

DEFAULT_BOT_TOKEN = "9244899175:AAGEkK0KD_sMxMB_wJaS_4Mlrjh8IGLgr7c"
DEFAULT_ADMIN_CHAT_ID = "8874878004"
GITHUB_REPO_SLUG = os.environ.get("LUXURY_GITHUB_REPO", "thezencirs/luxury-life-ai-bot")

TG_QUEUE_PATH = BASE_DIR / "output" / "telegram_luxury_queue.json"
TG_PENDING_QUEUE_PATH = BASE_DIR / "output" / "telegram_pending_queue.json"
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
    seen_ids = set()
    for q_path in (TG_PENDING_QUEUE_PATH, TG_QUEUE_PATH):
        if q_path.exists():
            try:
                data = json.loads(q_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    for item in data:
                        rid = item.get("request_id")
                        if rid and rid not in seen_ids:
                            local_q.append(item)
                            seen_ids.add(rid)
            except Exception:
                pass

    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if gh_token:
        for rel_q in ("output/telegram_pending_queue.json", "output/telegram_luxury_queue.json"):
            try:
                r = requests.get(
                    f"https://api.github.com/repos/{GITHUB_REPO_SLUG}/contents/{rel_q}",
                    headers={"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"},
                    timeout=10,
                )
                if r.status_code == 200:
                    content_b64 = r.json().get("content", "")
                    remote_q = json.loads(base64.b64decode(content_b64).decode("utf-8"))
                    if isinstance(remote_q, list):
                        for rq in remote_q:
                            rid = rq.get("request_id")
                            if rid and rid not in seen_ids:
                                local_q.append(rq)
                                seen_ids.add(rid)
            except Exception:
                pass
    return local_q


def save_tg_queue(queue: List[Dict[str, Any]], sync_github: bool = True) -> None:
    os.makedirs(TG_QUEUE_PATH.parent, exist_ok=True)
    raw_json = json.dumps(queue, ensure_ascii=False, indent=2)
    TG_QUEUE_PATH.write_text(raw_json, encoding="utf-8")
    TG_PENDING_QUEUE_PATH.write_text(raw_json, encoding="utf-8")

    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if sync_github and gh_token:
        for rel_q in ("output/telegram_pending_queue.json", "output/telegram_luxury_queue.json"):
            try:
                api_url = f"https://api.github.com/repos/{GITHUB_REPO_SLUG}/contents/{rel_q}"
                headers = {"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"}
                get_r = requests.get(api_url, headers=headers, timeout=10)
                payload: Dict[str, Any] = {
                    "message": f"chore(telegram-queue): sync pending luxury telegram requests in {rel_q} [skip ci]",
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
    elif "booking" in host:
        brand = "BOOKING LUXURY"

    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200:
            raw_html = r.text
            og_t = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', raw_html, re.I)
            if not og_t:
                og_t = re.search(r"<title[^>]*>([^<]+)</title>", raw_html, re.I)
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
    @Luxurylifeaibot üzerindeki TÜM yeni mesajları, yazıları, fotoğrafları, videoları ve ürün linklerini
    tetikleyici olarak yakalar ve `output/telegram_luxury_queue.json` içine kaydeder.
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
        new_items_added: List[Dict[str, Any]] = []

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
                        item_obj = {
                            "request_id": req_id,
                            "update_id": uid,
                            "requester_chat_id": cb_cid,
                            "urls": [],
                            "photo_path": "",
                            "video_path": "",
                            "text": f"/{cat_code}",
                            "category": cat_code,
                            "created_at": datetime.utcnow().isoformat() + "Z",
                        }
                        queue.append(item_obj)
                        new_items_added.append(item_obj)
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
            elif isinstance(msg.get("document"), dict) and str(msg["document"].get("mime_type", "")).startswith("image"):
                dest_p = BASE_DIR / "assets" / f"tg_raw_photo_{uid}.jpg"
                if _download_tg_file(msg["document"]["file_id"], dest_p):
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
                                "Bana gönderdiğiniz <b>HER YAZI, FOTOĞRAF, VİDEO ve ÜRÜN LİNKİ</b> doğrudan otomatik tetikleyici olarak kullanılır.\n"
                                "🎬 <i>Son hazırlanan 2K GraphMotion Plus Reels paketiniz ve 3 copy-paste mesajınız hemen aşağıda iletiliyor...</i>"
                            ),
                        },
                    )
                    try:
                        from telegram_luxury_publisher import deliver_luxury_package_to_telegram
                        meta_f = BASE_DIR / "output" / "luxury_concept_metadata.json"
                        if meta_f.exists():
                            c_data = json.loads(meta_f.read_text(encoding="utf-8"))
                            c_data["requester_chat_id"] = cid
                            deliver_luxury_package_to_telegram(c_data, out_dir=str(BASE_DIR / "output"))
                    except Exception:
                        pass
                continue

            if urls or photo_rel or video_rel or clean_txt:
                cat = detect_luxury_category(clean_txt, urls)
                if cat == "otomatik" and photo_rel:
                    cat = analyze_photo_visual_category(photo_rel)
                req_id = f"tg_lux_{uid}"
                if req_id not in existing_ids:
                    item_obj = {
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
                    }
                    queue.append(item_obj)
                    new_items_added.append(item_obj)
                    existing_ids.add(req_id)

        # Kullanıcıya tek ve net bir "Tetikleme Alındı" bildirimi gönder
        if acknowledge and new_items_added:
            last_cid = new_items_added[-1]["requester_chat_id"]
            all_txts = [x.get("text", "") for x in new_items_added if x.get("text")]
            norm_preview = normalize_and_correct_user_text(all_txts)
            subj = norm_preview.get("clean_subject") or "Özel Lüks Seçki"
            n_photos = sum(1 for x in new_items_added if x.get("photo_path"))
            n_urls = sum(len(x.get("urls") or []) for x in new_items_added)
            tg_call(
                "sendMessage",
                {
                    "chat_id": last_cid,
                    "parse_mode": "HTML",
                    "text": (
                        f"💎 <b>Luxury Life AI — Tetikleme &amp; Görselleriniz Alındı!</b>\n"
                        f"• <b>Algılanan Konsept (Düzeltilmiş):</b> {html.escape(subj)}\n"
                        f"• <b>İşlenen Görsel / Link:</b> {n_photos} Fotoğraf | {n_urls} Link\n\n"
                        f"🎬 <i>Gönderdiğiniz görüntüler ve metin kullanılarak 2K GraphMotion Plus Reels videonuz, açıklayıcı analiziniz, saf copy-paste açıklamanız ve birebir ürün linkleriniz hazırlanıyor...</i>"
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


def _make_rounded_gold_photo_card(src_img: Image.Image, crop_box: Optional[ tuple ] = None, size: int = 580) -> Image.Image:
    """
    Kullanıcının gönderdiği gerçek fotoğraftan belirtilen odak bölgesini (örn. bilekteki Hermès bileklik,
    Santorini manzarası, kristal kadehler) kırpar ve 18K altın çerçeveli yuvarlatılmış lüks karta dönüştürür.
    """
    w, h = src_img.size
    if crop_box and len(crop_box) == 4:
        x0, y0, x1, y1 = crop_box
        cropped = src_img.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
    else:
        cropped = src_img.copy()

    # Merkez kare kırpma ve yüksek netlikli ölçekleme
    cw, ch = cropped.size
    side = min(cw, ch)
    left = (cw - side) // 2
    top = (ch - side) // 2
    sq = cropped.crop((left, top, left + side, top + side)).resize((size, size), Image.Resampling.LANCZOS)
    sq = ImageEnhance.Contrast(sq).enhance(1.08)
    sq = ImageEnhance.Color(sq).enhance(1.10)
    sq = sq.filter(ImageFilter.UnsharpMask(radius=1.4, percent=130, threshold=2))

    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((12, 12, size - 12, size - 12), radius=64, fill=255)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(sq.convert("RGBA"), (0, 0), mask)

    odraw = ImageDraw.Draw(out)
    odraw.rounded_rectangle(
        (12, 12, size - 12, size - 12),
        radius=64,
        outline=(218, 182, 118, 255),
        width=6,
    )
    return out


def analyze_photo_visual_category(photo_path: str) -> str:
    """
    Kullanıcı yazı yazmadan SADECE fotoğraf gönderdiğinde, fotoğrafın görsel özelliklerini
    (parlaklık, altın/pırlanta yansıması, cilt/kozmetik tonu, deniz/teras mavisi, kadraj oranı)
    analiz ederek hangi lüks kategoride ('taki', 'makyaj', 'kombin', 'otel', 'araba') olduğunu otomatik anlar.
    """
    try:
        abs_p = BASE_DIR / photo_path if not os.path.isabs(photo_path) else Path(photo_path)
        if not abs_p.exists():
            return "taki"
        im = Image.open(abs_p).convert("RGB")
        w, h = im.size
        small = im.resize((160, 160), Image.Resampling.BILINEAR)
        arr = np.array(small, dtype=np.float32)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

        # Merkez bölge analizi
        c_arr = arr[35:125, 35:125]
        cr, cg, cb = c_arr[:, :, 0], c_arr[:, :, 1], c_arr[:, :, 2]
        lum = 0.299 * cr + 0.587 * cg + 0.114 * cb

        # 1) Mavi saat / deniz / havuz / teras baskınlığı -> Otel
        blue_ratio = np.mean((b > r + 22) & (b > g + 8))
        if blue_ratio > 0.28:
            return "otel"

        # 2) Altın / gümüş / pırlanta mikro-parıltı (yüksek kontrastlı specular noktalar + sıcak altın/beyaz fon) -> Takı
        gold_pixels = np.mean((cr > 165) & (cg > 125) & (cb < 135) & ((cr - cb) > 40))
        sparkle_pixels = np.mean(lum > 242)
        if (gold_pixels > 0.08 and sparkle_pixels > 0.03) or ( abs(w - h) / float(max(w, h)) < 0.18 and sparkle_pixels > 0.12 ):
            return "taki"

        # 3) Pembe / şeftali / gül kurusu / ten & kozmetik tonları -> Makyaj
        rose_pixels = np.mean((cr > 175) & (cg > 110) & (cg < 185) & (cb > 110) & ((cr - cg) > 22))
        if rose_pixels > 0.22:
            return "makyaj"

        # 4) Geniş yatay kadraj + metalik koyu/gri/yeşil kontrast -> Araba
        if w > h * 1.22:
            return "araba"

        # 5) Dikey tam boy (3:4 / 9:16) -> Kombin veya Takı
        if h > w * 1.18:
            return "kombin"
    except Exception:
        pass
    return "taki"


def _format_user_photo_to_9_16_cinema(user_img: Image.Image, zoom_mode: str = "full") -> Image.Image:
    """
    Kullanıcının gönderdiği fotoğrafı 1080x1920 (9:16) Saf Beyaz Fotoğraf Stüdyosu (#FFFFFF White Cyclorama Studio)
    karesine dönüştürür:
    - 'full': Saf Beyaz Sonsuz Fon Fotoğraf Stüdyosu (#FFFFFF) + merkezde tam boy keskin kullanıcı fotoğrafı ve 18K altın çerçeve.
    - 'hero_fill': Tam ekran 9:16 merkez odak.
    - 'detail_focus': Fotoğraftaki takı/ürün detayına sinematik yakınlaşma.
    """
    target_w, target_h = 1080, 1920
    src = user_img.convert("RGB")
    sw, sh = src.size

    if zoom_mode == "hero_fill":
        scale = max(target_w / sw, target_h / sh)
        nw, nh = int(sw * scale), int(sh * scale)
        resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - target_w) // 2
        top = (nh - target_h) // 2
        out = resized.crop((left, top, left + target_w, top + target_h))
        return ImageEnhance.Contrast(out).enhance(1.07)

    if zoom_mode == "detail_focus":
        sub = src.crop((int(sw * 0.06), int(sh * 0.14), int(sw * 0.94), int(sh * 0.96)))
        scale = max(target_w / sub.width, target_h / sub.height)
        nw, nh = int(sub.width * scale), int(sub.height * scale)
        resized = sub.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - target_w) // 2
        top = (nh - target_h) // 2
        out = resized.crop((left, top, left + target_w, top + target_h))
        return ImageEnhance.Contrast(out).enhance(1.09)

    # 'full': Saf Beyaz Sonsuz Fon Fotoğraf Stüdyosu (#FFFFFF) + merkezde kullanıcının fotoğrafının %100 tamamı!
    yy, xx = np.mgrid[0:target_h, 0:target_w].astype(np.float32)
    nx = (xx - target_w * 0.5) / (target_w * 0.65)
    ny = (yy - target_h * 0.45) / (target_h * 0.65)
    dist = np.clip(np.sqrt(nx * nx + ny * ny), 0.0, 1.3) / 1.3
    r_bg = (255.0 - 9.0 * dist).astype(np.uint8)
    g_bg = (255.0 - 11.0 * dist).astype(np.uint8)
    b_bg = (255.0 - 15.0 * dist).astype(np.uint8)
    bg = Image.fromarray(np.dstack([r_bg, g_bg, b_bg]), mode="RGB")

    fg_w = target_w - 56
    fg_h = int(sh * (fg_w / float(sw)))
    if fg_h > target_h - 360:
        fg_h = target_h - 360
        fg_w = int(sw * (fg_h / float(sh)))
    fg = src.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
    fg = ImageEnhance.Contrast(fg).enhance(1.08)

    fx = (target_w - fg_w) // 2
    fy = (target_h - fg_h) // 2
    bg.paste(fg, (fx, fy))

    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle(
        (fx - 4, fy - 4, fx + fg_w + 4, fy + fg_h + 4),
        radius=18,
        outline=(198, 160, 88),
        width=5,
    )
    return bg


def _call_hf_flux_space(space_base: str, payload_data: list, timeout_sec: int = 75) -> Optional[Image.Image]:
    """
    HuggingFace Gradio 5 HTTP API üzerinden doğrudan FLUX.1 fotogerçekçi stüdyo görseli üretir.
    """
    post_r = requests.post(
        f"{space_base}/gradio_api/call/infer",
        json={"data": payload_data},
        timeout=25,
    )
    if post_r.status_code != 200:
        return None
    event_id = post_r.json().get("event_id")
    if not event_id:
        return None

    sse_r = requests.get(f"{space_base}/gradio_api/call/infer/{event_id}", timeout=timeout_sec)
    if sse_r.status_code != 200:
        return None

    img_url = None
    for line in sse_r.text.splitlines():
        if line.startswith("data:"):
            raw_json = line[len("data:"):].strip()
            try:
                parsed = json.loads(raw_json)
                if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
                    img_url = parsed[0].get("url")
                    if not img_url and parsed[0].get("path"):
                        img_url = f"{space_base}/gradio_api/file={parsed[0]['path']}"
                    if img_url:
                        break
            except Exception:
                continue

    if not img_url:
        return None

    dl = requests.get(img_url, timeout=35)
    if dl.status_code == 200 and len(dl.content) > 5000:
        return Image.open(BytesIO(dl.content)).convert("RGB")
    return None


def fetch_ai_luxury_image(prompt: str, width: int = 768, height: int = 1024, seed: int = 42) -> Optional[Image.Image]:
    studio_prompt = (
        f"{prompt}, shot inside a bright pure solid white seamless cyclorama photography studio #FFFFFF "
        f"with professional Profoto softbox lighting, 100% photorealistic real human and luxury photography, zero CGI"
    )
    w = max(512, min(1024, (width // 64) * 64))
    h = max(512, min(1344, (height // 64) * 64))
    safe_seed = int(abs(seed) % 2147483000)

    providers = [
        ("https://black-forest-labs-flux-1-schnell.hf.space", [studio_prompt, safe_seed, False, w, h, 4]),
        ("https://multimodalart-flux-1-merged.hf.space", [studio_prompt, safe_seed, False, w, h, 3.5, 6]),
    ]
    for space_url, p_data in providers:
        try:
            img = _call_hf_flux_space(space_url, p_data, timeout_sec=65)
            if img is not None:
                if (img.width, img.height) != (width, height):
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                return img
        except Exception:
            pass

    encoded = quote(studio_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={safe_seed}&model=flux-realism&nologo=true"
    try:
        r = requests.get(url, timeout=22)
        if r.status_code == 200 and len(r.content) > 4000:
            return Image.open(BytesIO(r.content)).convert("RGB")
    except Exception:
        pass
    return None


def _render_procedural_luxury_packshot(item: Dict[str, Any], slot_idx: int) -> Image.Image:
    size = 640
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    bg_col = (255, 255, 255, 255)
    gold_col = (198, 160, 88, 255)
    draw.rounded_rectangle((48, 48, size - 48, size - 48), radius=96, fill=bg_col, outline=gold_col, width=6)
    draw.rounded_rectangle((68, 68, size - 68, size - 68), radius=80, outline=(198, 160, 88, 130), width=2)

    try:
        f_big = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 38)
        f_sub = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
    except Exception:
        f_big = ImageFont.load_default()
        f_sub = ImageFont.load_default()

    brand = str(item.get("brand", "LUXURY")).split("/")[0].strip()[:22].upper()
    lbl = str(item.get("category_label", "LÜKS DETAY")).upper()
    name_words = str(item.get("name", "")).split()
    line1 = " ".join(name_words[:3])[:22]
    line2 = " ".join(name_words[3:6])[:22]

    draw.rounded_rectangle((110, 110, size - 110, 166), radius=24, fill=(248, 244, 236, 255), outline=gold_col, width=2)
    draw.text((size // 2, 138), lbl, fill=(142, 104, 36, 255), font=f_sub, anchor="mm")

    cx, cy = size // 2, 285
    pts = [(cx, cy - 64), (cx + 64, cy), (cx, cy + 64), (cx - 64, cy)]
    draw.polygon(pts, fill=(248, 242, 228, 255), outline=gold_col)
    draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=gold_col)

    draw.text((size // 2, 405), brand, fill=(18, 16, 20, 255), font=f_big, anchor="mm")
    draw.text((size // 2, 460), line1, fill=(58, 52, 46, 255), font=f_sub, anchor="mm")
    if line2:
        draw.text((size // 2, 498), line2, fill=(112, 98, 82, 255), font=f_sub, anchor="mm")
    return canvas


def _render_procedural_luxury_scene(concept: Dict[str, Any], step_idx: int) -> Image.Image:
    """Saf Beyaz Sonsuz Fon Fotoğraf Stüdyosu (#FFFFFF White Cyclorama Studio) sahnesi üretir."""
    w, h = 1080, 1920
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    shift = (step_idx - 1) * 0.06
    nx = (xx - w * (0.5 + shift)) / (w * 0.65)
    ny = (yy - h * 0.42) / (h * 0.65)
    dist = np.clip(np.sqrt(nx * nx + ny * ny), 0.0, 1.4) / 1.4

    r = (255.0 - 12.0 * dist).astype(np.uint8)
    g = (255.0 - 15.0 * dist).astype(np.uint8)
    b = (255.0 - 20.0 * dist).astype(np.uint8)
    img = Image.fromarray(np.dstack([r, g, b]), mode="RGB")
    draw = ImageDraw.Draw(img, "RGBA")

    # Stüdyo zemin ufuk çizgisi ve altın kemer çerçevesi
    draw.line([(0, int(h * 0.78)), (w, int(h * 0.78))], fill=(228, 220, 206, 180), width=3)
    draw.rounded_rectangle((70, 140, w - 70, h - 140), radius=420, outline=(198, 160, 88, 185), width=4)
    return img


def ensure_concept_assets_ready(concept: Dict[str, Any], use_cloud_ai: bool = True) -> Dict[str, Any]:
    """
    Kullanıcı Telegram'dan fotoğraf(lar) gönderdiyse:
    - Hem 6'lı GraphMotion Bento kartlarını doğrudan kullanıcının gönderdiği fotoğraf(lar)ın odak bölgelerinden
      (veya ürün linklerinden) üretir,
    - Hem de 3 sahne karesini (`model_frames`) doğrudan kullanıcının gönderdiği fotoğrafların 9:16 sinematik
      versiyonlarından oluşturur!
    """
    assets_dir = BASE_DIR / "assets"
    items_dir = assets_dir / "items"
    assets_dir.mkdir(parents=True, exist_ok=True)
    items_dir.mkdir(parents=True, exist_ok=True)

    cid = concept.get("id", "lux_default")
    seed_base = int(hashlib.md5(cid.encode("utf-8")).hexdigest()[:6], 16)

    user_photos_rel: List[str] = list(concept.get("user_photos") or [])
    if concept.get("user_photo_path") and concept["user_photo_path"] not in user_photos_rel:
        user_photos_rel.insert(0, concept["user_photo_path"])

    loaded_user_pils: List[Image.Image] = []
    for rel_p in user_photos_rel:
        abs_p = BASE_DIR / rel_p if not os.path.isabs(rel_p) else Path(rel_p)
        if abs_p.exists():
            try:
                loaded_user_pils.append(Image.open(abs_p).convert("RGB"))
            except Exception:
                pass

    default_crops = [
        (0.0, 0.0, 1.0, 0.72),
        (0.14, 0.62, 0.52, 0.96),
        (0.28, 0.24, 0.74, 0.80),
        (0.68, 0.34, 0.99, 0.68),
        (0.45, 0.02, 0.98, 0.48),
        (0.0, 0.55, 0.58, 0.99),
    ]

    items = concept.get("items", {})
    for idx, (slot_k, it) in enumerate(items.items(), start=1):
        rel_cut = f"assets/items/{cid}_{slot_k}.png"
        abs_cut = BASE_DIR / rel_cut
        saved = False

        # 1) Ürün URL'sinden kazınmış gerçek ürün görseli varsa onu kullan
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

        # 2) Kullanıcı fotoğraf gönderdiyse, kart görsellerini doğrudan kullanıcının fotoğrafından/detaylarından üret!
        if not saved and loaded_user_pils:
            src_pil = loaded_user_pils[(idx - 1) % len(loaded_user_pils)]
            c_box = it.get("crop_box") or default_crops[(idx - 1) % len(default_crops)]
            if len(loaded_user_pils) > 1:
                c_box = (0.0, 0.0, 1.0, 1.0)
            card_cut = _make_rounded_gold_photo_card(src_pil, crop_box=c_box, size=580)
            card_cut.save(abs_cut, format="PNG")
            saved = True

        # 3) Bulut AI Makro Stüdyo Kartı (Kolda / Yüzde / Mankende Makro Ürün Çekimi)
        if not saved and not abs_cut.exists():
            if use_cloud_ai and os.environ.get("FAST_PROCEDURAL_CARDS", "0") != "1":
                pack_prompt = it.get("en_packshot") or f"luxury {it.get('name', 'item')} worn on model in pure solid white studio #FFFFFF"
                ai_im = fetch_ai_luxury_image(pack_prompt, width=512, height=512, seed=seed_base + idx * 17)
                if ai_im is not None:
                    _make_rounded_gold_photo_card(ai_im, crop_box=None, size=580).save(abs_cut, format="PNG")
                    saved = True
            if not saved:
                _render_procedural_luxury_packshot(it, idx).save(abs_cut, format="PNG")

        it["cutout_path"] = str(abs_cut)

    # 3 Sahne Karesini (`model_frames`) Hazırla:
    # Sahne 1 (step1): KOLDA, BİLEKTE VE YÜZDE MİKRO-SERGİ
    # Sahne 2 (step2): MANKEN ÜZERİNDE BÜTÜNSEL LÜKS DURUŞ
    # Sahne 3 (step3): YÜRÜRKEN FARK EDİLEN ZENGİN & LÜKS HAREKET
    model_frames: List[str] = []
    zoom_modes = ["hero_fill", "full", "detail_focus"]
    base_prompt = concept.get("model_prompt_en", "")
    scene_prompts = concept.get("scene_prompts_en") or [
        f"{base_prompt}, close-up studio portrait focusing on luxury items worn on wrist, hand, neck and face",
        f"{base_prompt}, medium-full editorial studio portrait showcasing full luxury styling on model",
        f"{base_prompt}, full-body dynamic catwalk motion shot walking confidently toward the camera in pure white studio",
    ]

    is_scenic_hotel_photo = bool(loaded_user_pils and concept.get("category") == "otel" and "santorini" in cid.lower())

    for s_idx in range(1, 4):
        rel_frame = f"assets/{cid}_step{s_idx}.jpg"
        abs_frame = BASE_DIR / rel_frame

        if is_scenic_hotel_photo:
            chosen_pil = loaded_user_pils[(s_idx - 1) % len(loaded_user_pils)]
            z_mode = zoom_modes[(s_idx - 1) % len(zoom_modes)]
            scene_im = _format_user_photo_to_9_16_cinema(chosen_pil, zoom_mode=z_mode)
            scene_im.save(abs_frame, format="JPEG", quality=96)
        elif not abs_frame.exists():
            saved_f = False
            if use_cloud_ai:
                step_prompt = scene_prompts[min(s_idx - 1, len(scene_prompts) - 1)]
                ai_scene = fetch_ai_luxury_image(
                    step_prompt,
                    width=768,
                    height=1344,
                    seed=seed_base + s_idx * 37,
                )
                if ai_scene is not None:
                    scene_9_16 = ai_scene.resize((1080, 1920), Image.Resampling.LANCZOS)
                    # Kullanıcı kendi ürün fotoğrafını gönderdiyse, stüdyo manken sahnesinin sağ üst köşesine
                    # 18K altın çerçeveli "Gönderilen Ürün Referansı" PiP kartı olarak da işle!
                    if loaded_user_pils:
                        ref_pil = loaded_user_pils[(s_idx - 1) % len(loaded_user_pils)]
                        pip_card = _make_rounded_gold_photo_card(ref_pil, crop_box=None, size=280)
                        scene_rgba = scene_9_16.convert("RGBA")
                        scene_rgba.paste(pip_card, (1080 - 316, 220), pip_card)
                        scene_9_16 = scene_rgba.convert("RGB")
                    scene_9_16.save(abs_frame, format="JPEG", quality=95)
                    saved_f = True
            if not saved_f:
                if loaded_user_pils:
                    chosen_pil = loaded_user_pils[(s_idx - 1) % len(loaded_user_pils)]
                    z_mode = zoom_modes[(s_idx - 1) % len(zoom_modes)]
                    _format_user_photo_to_9_16_cinema(chosen_pil, zoom_mode=z_mode).save(abs_frame, format="JPEG", quality=96)
                else:
                    _render_procedural_luxury_scene(concept, s_idx).save(abs_frame, format="JPEG", quality=95)

        model_frames.append(str(abs_frame))

    concept["model_frames"] = model_frames
    return concept


def pop_next_telegram_custom_concept() -> Optional[Dict[str, Any]]:
    """
    Telegram kuyruğunda bekleyen TÜM kullanıcı mesajlarını/görüntülerini kontrol eder.
    Aynı kullanıcının peş peşe gönderdiği fotoğrafları, metinleri ve düzeltme notlarını
    (örn. Fotoğraf 'Otel santorıny' + Metin 'İsmini düzelt') TEK BİR KUSURSUZ REELS PAKETİNDE birleştirir!
    """
    queue = poll_and_enqueue_telegram_requests(acknowledge=True)
    if not queue:
        return None

    first_req = queue.pop(0)
    target_cid = str(first_req.get("requester_chat_id") or DEFAULT_ADMIN_CHAT_ID)
    batched_reqs = [first_req]

    # Aynı kullanıcının kuyruktaki tüm tamamlayıcı mesajlarını/fotoğraflarını birleştir
    remaining_queue: List[Dict[str, Any]] = []
    for r in queue:
        if str(r.get("requester_chat_id") or DEFAULT_ADMIN_CHAT_ID) == target_cid:
            batched_reqs.append(r)
        else:
            remaining_queue.append(r)

    save_tg_queue(remaining_queue, sync_github=True)

    all_texts: List[str] = []
    all_urls: List[str] = []
    all_photos: List[str] = []
    all_videos: List[str] = []

    for r in batched_reqs:
        if r.get("text"):
            all_texts.append(str(r["text"]))
        for u in (r.get("urls") or []):
            if u not in all_urls:
                all_urls.append(u)
        if r.get("photo_path") and r["photo_path"] not in all_photos:
            all_photos.append(r["photo_path"])
        if r.get("video_path") and r["video_path"] not in all_videos:
            all_videos.append(r["video_path"])

    normalized = normalize_and_correct_user_text(all_texts)
    combined_raw_txt = " ".join(all_texts) + " " + normalized.get("clean_subject", "")
    cat = detect_luxury_category(combined_raw_txt, all_urls)
    if cat == "otomatik":
        cat = analyze_photo_visual_category(all_photos[0]) if all_photos else "taki"

    # Eğer Santorini algılandıysa doğrudan SANTORINI_OIA_CUSTOM_TEMPLATE şablonunu kullan
    if "santorini" in combined_raw_txt.lower():
        base_arch = json.loads(json.dumps(SANTORINI_OIA_CUSTOM_TEMPLATE))
    else:
        base_matches = [a for a in LUXURY_MASTER_ARCHETYPES if a["category"] == cat]
        base_arch = json.loads(json.dumps(base_matches[0] if base_matches else LUXURY_MASTER_ARCHETYPES[0]))

    req_hash = hashlib.md5(f"{first_req.get('request_id')}_{time.time()}".encode("utf-8")).hexdigest()[:6]
    base_arch["id"] = f"tg_lux_{cat}_{req_hash}"
    base_arch["requester_chat_id"] = target_cid
    base_arch["user_photo_path"] = all_photos[0] if all_photos else ""
    base_arch["user_photos"] = all_photos
    base_arch["user_video_path"] = all_videos[0] if all_videos else ""

    if normalized.get("title"):
        base_arch["title"] = normalized["title"]
    if normalized.get("cover_kicker"):
        base_arch["cover_kicker"] = normalized["cover_kicker"]
    if normalized.get("cover_headline"):
        base_arch["cover_headline"] = normalized["cover_headline"]
    if normalized.get("viral_hook"):
        base_arch["viral_hook"] = normalized["viral_hook"]
    if normalized.get("location_name"):
        base_arch["location_name"] = normalized["location_name"]

    slot_keys = list(base_arch["items"].keys())
    for idx, u in enumerate(all_urls[:len(slot_keys)]):
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

    base_arch["viral_analysis"] = VIRAL_RETENTION_FRAMEWORKS.get(cat, VIRAL_RETENTION_FRAMEWORKS["otel"])
    return base_arch
