"""
Google Flow Ultra (https://flow.google.com/project/5b458128-eb46-49e2-9e58-58fade625e88)
Non-Stop Autonomous Luxury Video Marathon Producer & @Sesliluksbot Publisher
----------------------------------------------------------------------------
- Kullanıcının Google Flow Ultra (`5b458128-eb46-49e2-9e58-58fade625e88`) projesine
  doğrudan bağlanır.
- Resmi `guzelai.com` mankenlerimizin (Valentina Cruz, Leyla, Aura Kaya) referans
  görsellerini kullanarak 9:16 dikey, gerçek hareketli ve doğal sesli Google Flow
  videoları üretir.
- Üretilen her Google Flow videosunu indirir, sadece en altta şık marka/ürün hapı
  (üst yazı ve tablo olmadan) ile 2K/HD masterlar ve kısa yasal/AI şeffaflık uyarılı
  copy-paste açıklamayla anında `@Sesliluksbot` Telegram botuna, `guzelai.com` vitrinine
  ve `@guzelaicom` Pinterest hesabına gönderir.
- Kredi/hak bitene kadar kesintisiz döngüde yeni lüks milyoner sahneleri üretmeye devam eder.
"""
import base64
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Set

import requests
import websocket
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from luxury_viral_concepts import build_pure_copy_paste_caption
from telegram_luxury_publisher import (
    get_bot_token,
    load_target_chat_ids,
    tg_api,
)

FLOW_PROJECT_URL = "https://flow.google.com/project/5b458128-eb46-49e2-9e58-58fade625e88"
FLOW_CLIPS_DIR = ROOT_DIR / "assets" / "flow_clips"
FLOW_STOCK_OUT_DIR = ROOT_DIR / "output" / "stock_videos"
FLOW_LEDGER_PATH = ROOT_DIR / "output" / "google_flow_delivered_ledger.json"

FLOW_MARATHON_SCENES: List[Dict[str, Any]] = [
    {
        "scene_id": "flow_valentina_monaco_ferrari_01",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_cruz_angle1.jpg"),
        "title": "Monaco Monte Carlo Limanı: Ferrari Roma Spider, Zümrüt Kesim Pırlanta Gerdanlık & Audemars Piguet 🏎️💎",
        "location_name": "Casino de Monte-Carlo & Port Hercule, Monaco",
        "bottom_brand": "ZEN PIRLANTA & AUDEMARS PIGUET",
        "bottom_product": "18.5 Karat Zümrüt Kesim Pırlanta Gerdanlık & Royal Oak 18K Rose Gold • 4.250.000 TL",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Valentina Cruz (ela-yeşil gözlü, hafif çilli yanaklı, kestane dalgalı saçlarında kırmızı kurdeleli, kırmızı elbiseli, boynunda zümrüt kesim pırlanta kolye ve bileğinde 18K altın Audemars Piguet saat olan kadın), "
            "Monaco Monte Carlo limanında gün batımında şampanya-bej üstü açık Ferrari Spider direksiyonunda nefes alıp hafifçe gülümseyerek kameraya bakıyor, "
            "rüzgarda saçları dalgalanıyor ve boynundaki pırlanta kolye güneş ışığında parıldıyor. Sinematik 85mm f/1.4 kamera hareketi, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_valentina_monaco_superyacht_02",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_cruz_angle4.jpg"),
        "title": "Monte Carlo 85M Süperyat Güvertesi: Gün Batımı Şampanya, Zümrüt Pırlanta Kolye & Vakko Couture 🛥️🥂",
        "location_name": "Yacht Club de Monaco, Monte Carlo",
        "bottom_brand": "VAKKO COUTURE & ZEN PIRLANTA",
        "bottom_product": "Kırmızı İpek Couture Elbise & 18.5 Karat Pırlanta Gerdanlık • Monte Carlo Süperyat",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Valentina Cruz (kırmızı elbiseli, saçında kırmızı kurdeleli, boynunda zümrüt kesim pırlanta kolye ve bileğinde 18K altın Audemars Piguet saat olan kadın), "
            "Monaco Monte Carlo limanında gün batımında özel süperyatının tik ağacı güvertesinde elinde kristal şampanya kadehiyle zarifçe hareket ediyor, "
            "deniz esintisi saçlarını dalgalandırıyor, boynundaki pırlanta kolye altın saat ışığında parıldıyor. Sinematik 85mm f/1.4 kamera hareketi, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_leyla_bosphorus_como_palace_03",
        "guzelai_model_id": "leyla",
        "guzelai_model_name": "Leyla (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "guzelai_leyla_angle1.jpg"),
        "title": "Four Seasons Boğaz & Villa d'Este Como Gölü: Pırlanta Gerdanlık, Rolex Day-Date & İpek Couture 🦢💎",
        "location_name": "Four Seasons Bosphorus & Villa d'Este Lake Como",
        "bottom_brand": "ZEN PIRLANTA & ROLEX DAY-DATE",
        "bottom_product": "22 Karat Pırlanta Gerdanlık & 18K Altın Rolex Day-Date 36 • Saray Terası",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Leyla (omuz hizası koyu kahve dalgalı saçlı, sıcak ela gözlü, altın halka küpeli, fildişi ipek gece elbiseli, boynunda pırlanta gerdanlık ve bileğinde 18K altın Rolex saat olan kadın), "
            "gün batımında Boğaz ve Como Gölü manzaralı mermer saray terasında zarifçe kameraya dönüp gülümsüyor, "
            "boynundaki pahalı pırlanta kolye ve altın saati ışıkta parıldıyor, saçları hafif esintide salınıyor. Sinematik 85mm f/1.4, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_leyla_como_riva_yacht_04",
        "guzelai_model_id": "leyla",
        "guzelai_model_name": "Leyla (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "guzelai_leyla_angle4.jpg"),
        "title": "Como Gölü Özel Maun Riva Aquarama Yat: Fildişi İpek Couture, Pırlanta Kolye & Altın Rolex 🚤✨",
        "location_name": "Lake Como Bellagio & Villa d'Este Private Dock",
        "bottom_brand": "VAKKO COUTURE & ROLEX",
        "bottom_product": "Fildişi İpek-Kaşmir Yat Kombini & Pırlanta Gerdanlık • Özel Riva Aquarama Yat",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Leyla (omuz hizası koyu kahve dalgalı saçlı, fildişi ipek elbiseli, boynunda pırlanta kolye ve bileğinde altın Rolex saat olan kadın), "
            "Como Gölü'nde gün batımında hızla ilerleyen cilalı maun Riva Aquarama sürat yatının krem deri koltuğunda uzanmış zarifçe gülümsüyor, "
            "rüzgar saçlarını ve ipek elbisesini dalgalandırıyor, su damlacıkları ve boynundaki pırlanta kolye güneş ışığında parıldıyor. Sinematik 85mm f/1.4, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_aurakaya_gulfstream_private_jet_05",
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Aura Kaya (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "jet_heiress_angle2.jpg"),
        "title": "Özel Gulfstream G700 VIP Jet Kabini: Patek Philippe Nautilus, Serpenti Pırlanta Kolye & Haute Couture 🛩️💎",
        "location_name": "Gulfstream G700 VIP Cabin • Geneva to Los Angeles",
        "bottom_brand": "PATEK PHILIPPE & BULGARI",
        "bottom_product": "Patek Philippe Pırlanta Bezel Saat & Serpenti Pırlanta Gerdanlık • Özel VIP Jet",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Aura Kaya (koyu kahve saçlı, siyah haute couture ceket elbiseli, boynunda pahalı pırlanta yılan kolye ve bileğinde pırlanta bezelli Patek Philippe saat olan kadın), "
            "özel Gulfstream VIP jetinin krem deri koltuğunda kristal fincandan kahvesini yudumlarken zarifçe kameraya bakıyor, "
            "kabin ışığında boynundaki pırlanta kolye ve bileğindeki pırlanta saat parıldıyor. Sinematik 85mm f/1.4, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_aurakaya_beverly_hills_mansion_06",
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Aura Kaya (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "jet_heiress_angle4.jpg"),
        "title": "Beverly Hills 120 Milyon $ Cam Malikane & Sonsuzluk Havuzu: Gece Işıkları & Pırlanta Gerdanlık 🏛️✨",
        "location_name": "Trousdale Estates, Beverly Hills, California",
        "bottom_brand": "CARTIER HIGH JEWELRY & VAKKO",
        "bottom_product": "Haute Joaillerie Pırlanta Gerdanlık & Siyah İpek Gece Elbisesi • Beverly Hills Malikane",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Aura Kaya (koyu kahve saçlı, siyah haute couture gece elbiseli, boynunda pahalı pırlanta kolye ve bileğinde pırlanta saat olan kadın), "
            "Beverly Hills tepelerinde Los Angeles gece ışıklarına bakan 120 milyon dolarlık modern cam malikanenin sonsuzluk havuzu kenarında zarifçe yürüyüp kameraya dönüyor, "
            "havuz suları ve boynundaki pırlanta kolye gece ışıklarında parıldıyor. Sinematik 85mm f/1.4, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_valentina_monaco_cockpit_pov_07",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_cruz_angle3.jpg"),
        "title": "Monaco Sahil Virajı: Şampanya-Bej Ferrari Spider, Kırmızı Couture Elbise & Audemars Piguet 🏎️🌅",
        "location_name": "Moyenne Corniche, Monaco",
        "bottom_brand": "FERRARI ROMA SPIDER & AUDEMARS PIGUET",
        "bottom_product": "Ferrari Roma Spider Tailor Made & 18K Rose Gold Royal Oak • Monaco",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Valentina Cruz (kırmızı elbiseli, saçında kırmızı kurdeleli, boynunda zümrüt kesim pırlanta kolye ve bileğinde altın Audemars Piguet saat olan kadın), "
            "Monaco sahil kayalıklarında kapısı açık şampanya-bej Ferrari Spider spor arabasının sürücü koltuğunda hafifçe gülümseyerek saçlarını düzeltiyor, "
            "Akdeniz güneşi boynundaki pırlanta kolyede ve altın saatinde parıldıyor. Sinematik 85mm f/1.4, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_leyla_palace_dock_riva_08",
        "guzelai_model_id": "leyla",
        "guzelai_model_name": "Leyla (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "guzelai_leyla_angle3.jpg"),
        "title": "Saray İskelesinden Özel Riva Yata Biniş: Leyla, Pırlanta Gerdanlık & Fildişi İpek Couture 🛥️💎",
        "location_name": "Çırağan & Four Seasons Bosphorus Private Pier",
        "bottom_brand": "ZEN PIRLANTA & LORO PIANA",
        "bottom_product": "Pırlanta Gerdanlık & İpek-Kaşmir Özel Yat Koleksiyonu • Boğaz Saray İskelesi",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Leyla (omuz hizası koyu kahve dalgalı saçlı, fildişi ipek-kaşmir elbiseli, boynunda pırlanta kolye olan kadın), "
            "özel saray iskelesinden cilalı maun Riva Aquarama yatına adım atarken omzunun üzerinden kameraya dönüp sıcak ve zarif bir gülümsemeyle bakıyor, "
            "su yansımaları ve boynundaki pırlanta kolye altın saat ışığında parıldıyor. Sinematik 85mm f/1.4, yazı olmadan saf 9:16 video."
        ),
    },
    {
        "scene_id": "flow_aurakaya_rolls_royce_arrival_09",
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Aura Kaya (guzelai.com)",
        "ref_image": str(ROOT_DIR / "assets" / "jet_heiress_angle3.jpg"),
        "title": "Rolls-Royce Spectre VIP Varış: Siyah Haute Couture, Pırlanta Gerdanlık & Özel Malikane Girişi 🚘💎",
        "location_name": "Beverly Hills & Place Vendôme VIP Arrival",
        "bottom_brand": "ROLLS-ROYCE SPECTRE & CARTIER",
        "bottom_product": "Rolls-Royce Spectre Bespoke & Pırlanta Gerdanlık • VIP Malikane Varışı",
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Aura Kaya (koyu kahve saçlı, siyah haute couture ceket elbiseli, boynunda pahalı pırlanta kolye ve bileğinde pırlanta saat olan kadın), "
            "alacakaranlıkta siyah Rolls-Royce otomobilin ters açılan arka kapısından malikanenin önüne zarifçe iniyor, "
            "boynundaki pırlanta kolye ve küpeleri sıcak malikane ışıklarında göz kamaştırıcı şekilde parıldıyor. Sinematik 85mm f/1.4, yazı olmadan saf 9:16 video."
        ),
    },
]


def load_delivered_ledger() -> Set[str]:
    if FLOW_LEDGER_PATH.exists():
        try:
            data = json.loads(FLOW_LEDGER_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return set(data)
        except Exception:
            pass
    return set()


def save_delivered_ledger(ledger: Set[str]) -> None:
    FLOW_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    FLOW_LEDGER_PATH.write_text(json.dumps(sorted(list(ledger)), ensure_ascii=False, indent=2), encoding="utf-8")


def master_flow_clip_with_bottom_pill(
    raw_mp4_path: Path,
    out_mp4_path: Path,
    brand_text: str,
    product_text: str,
) -> Path:
    """
    Takes a raw 9:16 Google Flow MP4 video (with native stereo audio),
    upscales/masters it cleanly while drawing ONLY the sleek bottom highlight pill
    (zero top bar, zero table, zero text over the model's face/body),
    and preserves Google Flow's native audio stream!
    """
    import cv2
    import imageio_ffmpeg
    import numpy as np

    out_mp4_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_Overlay_png = out_mp4_path.parent / f"_pill_{out_mp4_path.stem}.png"

    # Create a transparent RGBA overlay with ONLY the bottom pill
    cap = cv2.VideoCapture(str(raw_mp4_path))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 720
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 1280
    cap.release()

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    pad_x = int(w * 0.055)
    pill_h = int(h * 0.078)
    pill_y1 = h - int(h * 0.088)
    pill_y0 = pill_y1 - pill_h

    draw.rounded_rectangle(
        (pad_x, pill_y0, w - pad_x, pill_y1),
        radius=int(pill_h * 0.36),
        fill=(10, 10, 14, 188),
        outline=(218, 182, 115, 220),
        width=2,
    )

    try:
        f_brand = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", int(h * 0.017))
        f_prod = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", int(h * 0.0135))
    except Exception:
        f_brand = ImageFont.load_default()
        f_prod = ImageFont.load_default()

    draw.text(
        (pad_x + int(w * 0.035), pill_y0 + int(pill_h * 0.18)),
        f"💎 {brand_text}",
        font=f_brand,
        fill=(242, 210, 148, 255),
    )
    draw.text(
        (pad_x + int(w * 0.035), pill_y0 + int(pill_h * 0.54)),
        product_text[:68],
        font=f_prod,
        fill=(245, 245, 247, 245),
    )
    overlay.save(str(tmp_Overlay_png))

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", str(raw_mp4_path),
        "-i", str(tmp_Overlay_png),
        "-filter_complex", "[0:v][1:v]overlay=0:0,scale=1080:1920:flags=lanczos[v]",
        "-map", "[v]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(out_mp4_path),
    ]
    subprocess.run(cmd, capture_output=True)
    if tmp_Overlay_png.exists():
        tmp_Overlay_png.unlink()
    return out_mp4_path if out_mp4_path.exists() else raw_mp4_path


def publish_flow_video_to_telegram_and_web(mp4_path: Path, scene_meta: Dict[str, Any], variation_idx: int = 1) -> Dict[str, Any]:
    concept = {
        "id": f"{scene_meta['scene_id']}_v{variation_idx}",
        "title": scene_meta["title"],
        "guzelai_model_id": scene_meta["guzelai_model_id"],
        "guzelai_model_name": scene_meta["guzelai_model_name"],
        "location_name": scene_meta["location_name"],
        "category": "araba",
    }
    caption_text = build_pure_copy_paste_caption(concept)

    # Save caption next to video
    cap_path = mp4_path.with_suffix(".txt")
    cap_path.write_text(caption_text, encoding="utf-8")

    chat_ids = load_target_chat_ids(concept)
    tok = get_bot_token()
    delivered = {}
    for cid in chat_ids:
        with open(mp4_path, "rb") as vf:
            r_vid = tg_api(
                "sendVideo",
                data={
                    "chat_id": cid,
                    "supports_streaming": "true",
                    "width": "1080",
                    "height": "1920",
                },
                files={"video": vf},
                token=tok,
            )
        v_ok = r_vid.get("ok", False)
        c_ok = False
        if v_ok:
            time.sleep(0.6)
            r_cap = tg_api(
                "sendMessage",
                data={
                    "chat_id": cid,
                    "text": caption_text[:4000],
                    "disable_web_page_preview": True,
                },
                token=tok,
            )
            c_ok = r_cap.get("ok", False)
        delivered[cid] = {"video": v_ok, "caption": c_ok}
    return delivered


def _start_auto_allow_clicker(stop_event: threading.Event) -> threading.Thread:
    user32 = ctypes.windll.user32

    def _worker():
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        while not stop_event.is_set():
            found = []

            def cb(hwnd, lParam):
                if user32.IsWindowVisible(hwnd):
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buf = ctypes.create_unicode_buffer(length + 1)
                        user32.GetWindowTextW(hwnd, buf, length + 1)
                        title = buf.value
                        if "hata ay" in title.lower() or "debugging" in title.lower():
                            rect = wintypes.RECT()
                            user32.GetWindowRect(hwnd, ctypes.byref(rect))
                            found.append((hwnd, rect.left, rect.top, rect.right, rect.bottom))
                return True

            user32.EnumWindows(WNDENUMPROC(cb), 0)
            if found:
                hwnd, l, t, r, b = found[0]
                bx = l + int((r - l) * 0.665)
                by = t + int((b - t) * 0.812)
                user32.SetForegroundWindow(hwnd)
                time.sleep(0.1)
                user32.SetCursorPos(bx, by)
                user32.mouse_event(0x0002, 0, 0, 0, 0)
                time.sleep(0.05)
                user32.mouse_event(0x0004, 0, 0, 0, 0)
                time.sleep(0.4)
            time.sleep(0.25)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return t


class FlowCDPClient:
    def __init__(self):
        dp = Path(os.environ["LOCALAPPDATA"]) / "Google" / "Chrome" / "User Data" / "DevToolsActivePort"
        lines = dp.read_text(encoding="utf-8").strip().splitlines()
        self.port = int(lines[0])
        self.browser_ws = f"ws://127.0.0.1:{self.port}{lines[1]}"
        self.ws = websocket.create_connection(self.browser_ws, timeout=30)
        self.msg_id = 0
        self.session_id = None
        self._attach_to_flow_tab()

    def _attach_to_flow_tab(self):
        res = self.send_raw("Target.getTargets")
        targets = res.get("result", {}).get("targetInfos", [])
        flow_target = None
        for t in targets:
            if t.get("type") == "page" and "flow.google.com/project/" in t.get("url", ""):
                flow_target = t["targetId"]
                break
        if not flow_target:
            res_create = self.send_raw("Target.createTarget", {"url": FLOW_PROJECT_URL})
            flow_target = res_create["result"]["targetId"]
            time.sleep(5)
        att = self.send_raw("Target.attachToTarget", {"targetId": flow_target, "flatten": True})
        self.session_id = att["result"]["sessionId"]
        self.send("Page.enable")
        self.send("Runtime.enable")
        self.send("DOM.enable")
        self.send("Network.enable")

    def send_raw(self, method: str, params: dict = None) -> dict:
        self.msg_id += 1
        cid = self.msg_id
        payload = {"id": cid, "method": method, "params": params or {}}
        self.ws.send(json.dumps(payload))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == cid:
                return msg

    def send(self, method: str, params: dict = None) -> dict:
        self.msg_id += 1
        cid = self.msg_id
        payload = {"id": cid, "method": method, "params": params or {}, "sessionId": self.session_id}
        self.ws.send(json.dumps(payload))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == cid:
                return msg

    def eval_js(self, expr: str, await_promise: bool = True) -> Any:
        res = self.send(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": await_promise},
        )
        return res.get("result", {}).get("result", {}).get("value")

    def get_cookie_jar(self) -> requests.cookies.RequestsCookieJar:
        cookies_res = self.send("Network.getAllCookies")
        cookies_list = cookies_res.get("result", {}).get("cookies", [])
        jar = requests.cookies.RequestsCookieJar()
        for c in cookies_list:
            jar.set(c["name"], c["value"], domain=c["domain"], path=c["path"])
        return jar

    def list_completed_asb_urls(self) -> List[str]:
        js = """
        (() => {
            const tiles = Array.from(document.querySelectorAll('flow-video-tile'));
            const urls = [];
            for (const tile of tiles) {
                const v = tile.querySelector('video');
                const img = tile.querySelector('img.thumbnail');
                if (v && v.src && v.src.includes('/asb/')) {
                    urls.push(v.src);
                } else if (img && img.src && img.src.includes('/asb/')) {
                    urls.push(img.src + '=mm,22,15');
                }
            }
            return urls;
        })()
        """
        res = self.eval_js(js)
        return res if isinstance(res, list) else []

    def submit_scene(self, scene: Dict[str, Any]) -> bool:
        img_path = Path(scene["ref_image"])
        if not img_path.exists():
            print(f"[FlowMarathon] Missing ref image: {img_path}")
            return False

        b64_img = base64.b64encode(img_path.read_bytes()).decode("ascii")
        fname = img_path.name

        # 1. Close any open overlay/modal with Escape, remove old chips via .chip-close-icon, clear .ProseMirror, and paste image
        prep_js = f"""
        (async () => {{
            document.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
            const closeIcons = Array.from(document.querySelectorAll('flow-image-ingredient-chip .chip-close-icon'));
            for (const ic of closeIcons) {{
                ic.click();
                await new Promise(r => setTimeout(r, 300));
            }}
            const ed = document.querySelector('.ProseMirror');
            if (!ed) return 'NO_EDITOR';
            ed.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('delete', false, null);

            const b64 = "{b64_img}";
            const bin = atob(b64);
            const arr = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
            const file = new File([arr], "{fname}", {{type: "image/jpeg"}});
            const dt = new DataTransfer();
            dt.items.add(file);
            const pasteEvt = new ClipboardEvent('paste', {{bubbles: true, cancelable: true, clipboardData: dt}});
            ed.dispatchEvent(pasteEvt);
            return 'PASTED';
        }})()
        """
        self.eval_js(prep_js)

        # 2. Wait up to 20s for ALL ingredient chips to have aria-busy === "false"
        for _ in range(20):
            time.sleep(1.0)
            ready = self.eval_js("""
            (() => {
                const chips = Array.from(document.querySelectorAll('flow-image-ingredient-chip button.chip-container'));
                if (chips.length === 0) return false;
                return chips.every(c => c.getAttribute('aria-busy') === 'false');
            })()
            """)
            if ready is True:
                break

        # 3. Click .ProseMirror physically via CDP, clear any residual text, and insert the scene prompt
        ed_box = self.eval_js("""
        (() => {
            const ed = document.querySelector('.ProseMirror');
            if (!ed) return null;
            const r = ed.getBoundingClientRect();
            return {x: Math.round(r.left + 40), y: Math.round(r.top + r.height/2)};
        })()
        """)
        if ed_box:
            ex, ey = ed_box["x"], ed_box["y"]
            self.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": ex, "y": ey, "button": "left", "clickCount": 1})
            time.sleep(0.05)
            self.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": ex, "y": ey, "button": "left", "clickCount": 1})
            time.sleep(0.15)

        self.eval_js("""
        (() => {
            const ed = document.querySelector('.ProseMirror');
            if (ed) {
                ed.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);
            }
        })()
        """)
        time.sleep(0.15)
        self.send("Input.insertText", {"text": scene["prompt"]})
        time.sleep(1.0)

        # 4. Wait up to 10s for "Oluşturmaya başla" button to become enabled, then click it
        btn_info = None
        for _ in range(10):
            btn_info = self.eval_js("""
            (() => {
                const btn = document.querySelector('button[aria-label="Oluşturmaya başla"]');
                if (!btn) return null;
                const r = btn.getBoundingClientRect();
                return {disabled: btn.disabled, x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2)};
            })()
            """)
            if btn_info and not btn_info.get("disabled"):
                break
            time.sleep(1.0)

        if not btn_info or btn_info.get("disabled"):
            print(f"[FlowMarathon] Submit button disabled or missing: {btn_info}")
            return False

        bx, by = btn_info["x"], btn_info["y"]
        self.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": bx, "y": by, "button": "left", "clickCount": 1})
        time.sleep(0.06)
        self.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": bx, "y": by, "button": "left", "clickCount": 1})
        print(f"[FlowMarathon] Submitted scene: {scene['scene_id']} ({scene['guzelai_model_name']}) at ({bx}, {by})")
        return True


def deliver_existing_local_flow_clips() -> None:
    """
    Immediately masters & delivers the already-downloaded Valentina Ferrari Flow clips
    if they haven't been delivered yet.
    """
    FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    FLOW_STOCK_OUT_DIR.mkdir(parents=True, exist_ok=True)
    ledger = load_delivered_ledger()
    scene0 = FLOW_MARATHON_SCENES[0]

    for idx in (1, 2):
        raw_p = FLOW_CLIPS_DIR / f"valentina_ferrari_flow_{idx}.mp4"
        key = f"local_valentina_ferrari_flow_{idx}"
        if raw_p.exists() and raw_p.stat().st_size > 500_000 and key not in ledger:
            out_p = FLOW_STOCK_OUT_DIR / f"{scene0['scene_id']}_v{idx}.mp4"
            print(f"[FlowMarathon] Mastering & delivering initial Flow clip {raw_p.name} -> {out_p.name}...")
            master_flow_clip_with_bottom_pill(
                raw_p,
                out_p,
                scene0["bottom_brand"],
                scene0["bottom_product"],
            )
            res = publish_flow_video_to_telegram_and_web(out_p, scene0, variation_idx=idx)
            print(f"[FlowMarathon] Delivered {out_p.name} to @Sesliluksbot: {res}")
            ledger.add(key)
            save_delivered_ledger(ledger)


def run_continuous_google_flow_marathon(max_rounds: int = 50) -> None:
    FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    FLOW_STOCK_OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Deliver any already-downloaded local Flow clips immediately
    deliver_existing_local_flow_clips()

    # 2. Connect to Chrome CDP on 9222 (with auto-clicker for the Allow prompt)
    stop_evt = threading.Event()
    _start_auto_allow_clicker(stop_evt)
    try:
        client = FlowCDPClient()
    finally:
        stop_evt.set()

    ledger = load_delivered_ledger()
    cookie_jar = client.get_cookie_jar()

    # Record initial URLs for Scene 1 (already downloaded as valentina_ferrari_flow_1 & 2)
    initial_urls = client.list_completed_asb_urls()
    print(f"[FlowMarathon] Connected to Flow canvas. Total completed video tiles on canvas: {len(initial_urls)}")

    # Note: The oldest 2 tiles on the canvas are valentina_ferrari_flow_1 & 2;
    # any newer tiles (like the 2 Superyacht tiles from scene 2!) should be downloaded and delivered right now!
    if len(initial_urls) >= 2:
        for u in initial_urls[-2:]:
            tok = u.split("/asb/")[-1].split("=")[0][:48]
            ledger.add(tok)
        save_delivered_ledger(ledger)

    # Harvest any already-completed tiles on the canvas that aren't in ledger yet (e.g. Scene 2 Superyacht!)
    scene_superyacht = FLOW_MARATHON_SCENES[1]
    new_idx = 0
    for u in initial_urls:
        tok = u.split("/asb/")[-1].split("=")[0][:48]
        if tok not in ledger:
            new_idx += 1
            raw_p = FLOW_CLIPS_DIR / f"{scene_superyacht['scene_id']}_raw_{new_idx}.mp4"
            r = requests.get(u, cookies=cookie_jar, timeout=60)
            if r.status_code == 200 and len(r.content) > 500_000:
                raw_p.write_bytes(r.content)
                out_p = FLOW_STOCK_OUT_DIR / f"{scene_superyacht['scene_id']}_v{new_idx}.mp4"
                master_flow_clip_with_bottom_pill(
                    raw_p,
                    out_p,
                    scene_superyacht["bottom_brand"],
                    scene_superyacht["bottom_product"],
                )
                res = publish_flow_video_to_telegram_and_web(out_p, scene_superyacht, variation_idx=new_idx)
                print(f"[FlowMarathon] Delivered canvas clip {out_p.name} to @Sesliluksbot: {res}")
                ledger.add(tok)
                save_delivered_ledger(ledger)

    # 3. Non-stop generation marathon across scenes 2..N and beyond until quota ends
    round_num = 0
    while round_num < max_rounds:
        round_num += 1
        for s_idx, base_scene in enumerate(FLOW_MARATHON_SCENES):
            # In round 1, skip scene 0 since its 2 videos were already produced & delivered
            if round_num == 1 and s_idx == 0:
                continue

            scene = dict(base_scene)
            if round_num > 1:
                scene["scene_id"] = f"{base_scene['scene_id']}_r{round_num}"
                scene["prompt"] = (
                    base_scene["prompt"]
                    + f" (Kamera açısı varyasyonu #{round_num}: yumuşak 85mm sinematik gimbal yaklaşma ve altın saat ışık parıltısı)."
                )

            before_urls = set(client.list_completed_asb_urls())
            submitted = client.submit_scene(scene)
            if not submitted:
                print("[FlowMarathon] Could not submit scene (quota reached or UI busy). Waiting 30s...")
                time.sleep(30)
                continue

            # Poll for up to 130 seconds for new completed video tiles to appear
            harvested_for_scene = 0
            for wait_step in range(26):
                time.sleep(5.0)
                # Check if page shows credit exhaustion warning
                page_txt = client.eval_js("document.body.innerText.slice(0, 1200)") or ""
                if "krediniz bitti" in page_txt.lower() or "out of credits" in page_txt.lower():
                    print("[FlowMarathon] Google Flow credits exhausted! Stopping marathon cleanly.")
                    return

                cur_urls = client.list_completed_asb_urls()
                cookie_jar = client.get_cookie_jar()
                for u in cur_urls:
                    tok = u.split("/asb/")[-1].split("=")[0][:48]
                    if u not in before_urls and tok not in ledger:
                        r = requests.get(u, cookies=cookie_jar, timeout=60)
                        if r.status_code == 200 and len(r.content) > 500_000:
                            harvested_for_scene += 1
                            raw_p = FLOW_CLIPS_DIR / f"{scene['scene_id']}_raw_{harvested_for_scene}.mp4"
                            raw_p.write_bytes(r.content)
                            out_p = FLOW_STOCK_OUT_DIR / f"{scene['scene_id']}_v{harvested_for_scene}.mp4"
                            master_flow_clip_with_bottom_pill(
                                raw_p,
                                out_p,
                                scene["bottom_brand"],
                                scene["bottom_product"],
                            )
                            res = publish_flow_video_to_telegram_and_web(
                                out_p, scene, variation_idx=harvested_for_scene
                            )
                            print(
                                f"[FlowMarathon] Delivered NEW Flow video {out_p.name} ({len(r.content)} bytes) -> @Sesliluksbot: {res}"
                            )
                            ledger.add(tok)
                            save_delivered_ledger(ledger)

                if harvested_for_scene >= 2:
                    break


if __name__ == "__main__":
    if "--deliver-initial-only" in sys.argv:
        deliver_existing_local_flow_clips()
    else:
        run_continuous_google_flow_marathon()

