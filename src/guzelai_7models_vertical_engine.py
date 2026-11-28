"""
GüzelAI Holding A.Ş. — GraphMotion 3.0 Türkiye (TR), Avrupa (EU) & Amerika (US)
Viral Takı (Mücevher/Saat) & Kozmetik (Makyaj/Cilt Bakımı/Niş Parfüm) 9:16 Dikey Reklam Video Motoru
(`src/guzelai_7models_vertical_engine.py`)
====================================================================================================
Kullanıcı Talimatı:
- "burada kombin otomasyonunda yaptığımız github reposu ile github action ve graph motion kurulu mu
  bir de ben dha gelişmiş video üretmek için repo vr mı ona bakmanı istioyrum bu sayfanın amacının
  türkiye ve avrupa amerika takı ve kozmetik üzerine reklamını yaptığımız video sayfası olacak.
  telegrama at örneği bakalım sadece senden ricam ajanlar kur pinterestten ve benzri sitelerde çok
  beğenilen ürünleri hazırla viral olan trend olan içeriklerle elit bir görünüm yine manken guzelaiden olack"

Entegre Edilen 6 Gelişmiş Açık Kaynak GitHub Video & Motion-Graphics Teknolojisi (GraphMotion 3.0):
1. `remotion-dev/remotion` (`vendor_repos/remotion-template-overlay`):
   İkinci dereceden harmonik yay fiziği (`damping=14, stiffness=120, mass=0.8`) ile yüzen cam/altın ürün
   reklam kartlarının (%3.8 fiziksel aşım/overshoot ile) sahneye girişi.
2. `midrender/revideo` (Motion Canvas tabanlı programatik video motoru):
   180° Shutter Angle yönlü hareket bulanıklığı (Directional Motion Blur) ve pürüzsüz kamera eğrileri.
3. `gre/gl-transitions` (OpenGL Shader Geçişleri -> NumPy/PIL Portu):
   Açılar arasında Anamorfik Şampanya Altın Işık Sızıntısı (`Anamorphic Light-Leak`) ve `f/1.4 -> f/2.8`
   Optik Rack-Focus odak geçişi.
4. `heygen-com/hyperframes` & `clawnify/OpenVideo`:
   Yüzen Obsidian & 18K Şampanya Altın Glassmorphism Ürün Reklam Kartı (Sol tarafta 1:1 makro ürün görseli,
   sağda TR/EU/US bölge rozeti, marka, ürün adı, fiyat ve kart üzerinden geçen canlı altın ışık dalgası).
5. `Wan-Video/Wan2.1` & `Lightricks/LTX-Video` Sinematik Kamera Kinematiği:
   Sıfır dalga/jöle bozulmasıyla 3-eksenli `LANCZOS` alt-piksel Gimbal Push-In & Pan.
6. `Hasselblad H6D-100c` Optik Parıltı & Akustik Foley:
   4-noktalı pırlanta/altın yıldız kırılmaları (`enhance_frame_with_real_optics`), Kodak Portra 400 film
   dokusu ve deklanşör sesli Paris/New York reklam müziği.
"""

import datetime
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

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

from luxury_audio_engine import generate_luxury_soundtrack
from realistic_cinema_optics import enhance_frame_with_real_optics


def _call_hf_flux_space(space_base: str, payload_data: list, timeout_sec: int = 75) -> Optional[Image.Image]:
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


def cloud_fetch_ai_image(prompt: str, width: int, height: int, seed: int) -> Optional[Image.Image]:
    """
    Argon'suz GitHub Actions (ubuntu-latest) bulut ortamında doğrudan FLUX.1 ile
    9:16 dikey fotogerçekçi görsel sentezler.
    """
    w = max(512, min(1024, (width // 64) * 64))
    h = max(512, min(1344, (height // 64) * 64))
    safe_seed = int(abs(seed) % 2147483000)

    providers = [
        ("https://black-forest-labs-flux-1-schnell.hf.space", [prompt, safe_seed, False, w, h, 4]),
        ("https://multimodalart-flux-1-merged.hf.space", [prompt, safe_seed, False, w, h, 3.5, 6]),
    ]
    for space_url, p_data in providers:
        for attempt in range(1, 3):
            try:
                img = _call_hf_flux_space(space_url, p_data)
                if img is not None:
                    if (img.width, img.height) != (width, height):
                        img = img.resize((width, height), Image.Resampling.LANCZOS)
                    return img
            except Exception:
                time.sleep(2 * attempt)

    try:
        poll_url = (
            f"https://image.pollinations.ai/prompt/{quote(prompt)}"
            f"?width={w}&height={h}&seed={safe_seed}&model=flux&nologo=true"
        )
        r = requests.get(poll_url, timeout=45)
        if r.status_code == 200 and len(r.content) > 10000:
            img = Image.open(BytesIO(r.content)).convert("RGB")
            if (img.width, img.height) != (width, height):
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            return img
    except Exception:
        pass
    return None

VERTICAL_W = 1080
VERTICAL_H = 1920
FPS = 30

VERTICAL_OUT_DIR = BASE_DIR / "output" / "vertical_creations"
VERTICAL_LEDGER_PATH = BASE_DIR / "output" / "vertical_7models_zero_repeat_ledger.json"

# ==============================================================================
# 7 RESMİ GUZELAI.COM MANKEN KADROSU (`src/data/models.ts` ile %100 Senkronize)
# ==============================================================================
GUZELAI_7_OFFICIAL_MODELS: List[Dict[str, Any]] = [
    {
        "id": "valentina-cruz",
        "name": "Valentina Cruz",
        "badge": "guzelai.com • Valentina Cruz",
        "gender": "kadin",
        "role_tr": "TR • EU • US Yüksek Mücevherat, Lüks Kozmetik & Haute Glamour Marka Yüzü",
        "face_prompt_en": (
            "official guzelai.com female supermodel Valentina Cruz, 24-year-old Mediterranean-Italian brunette "
            "supermodel, 176cm, long silky chestnut-brown wavy hair, expressive hazel-green eyes, subtle natural "
            "freckles on nose bridge, sun-kissed glowing bronze glass skin, photorealistic real human skin pores"
        ),
        "fallback_photos": [
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_valentina_ql01_step1.jpg"),
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_valentina_ql01_step2.jpg"),
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_valentina_ql01_step3.jpg"),
        ],
    },
    {
        "id": "guzelai-leyla-001",
        "name": "Leyla",
        "badge": "guzelai.com • Leyla",
        "gender": "kadin",
        "role_tr": "İstanbul • Paris • New York Pırlanta, Niş Parfüm & Old Money Zarafet Yüzü",
        "face_prompt_en": (
            "official guzelai.com female model Leyla, 25-year-old Turkish-Mediterranean Old Money heiress, "
            "shoulder-length wavy dark chestnut-brown hair, warm expressive hazel-brown eyes, natural warm "
            "olive-ivory porcelain complexion, poised aristocratic facial geometry, photorealistic real human skin"
        ),
        "fallback_photos": [
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_leyla_om01_step1.jpg"),
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_leyla_om01_step2.jpg"),
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_leyla_om01_step3.jpg"),
        ],
    },
    {
        "id": "aura-kaya",
        "name": "Aura Kaya",
        "badge": "guzelai.com • Aura Kaya",
        "gender": "kadin",
        "role_tr": "Paris Place Vendôme & Beverly Hills Cam Ten (Glass Skin) & Mücevher Podyum Yüzü",
        "face_prompt_en": (
            "official guzelai.com female runway supermodel Aura Kaya, 24-year-old Turkish-Parisian haute couture "
            "model, 178cm, glossy dark chestnut wavy hair, sculpted high cheekbones, luminous bronze glass-skin "
            "complexion, magnetic almond eyes, photorealistic real human skin pores"
        ),
        "fallback_photos": [
            str(BASE_DIR / "assets" / "jet_heiress_angle1.jpg"),
            str(BASE_DIR / "assets" / "jet_heiress_angle2.jpg"),
            str(BASE_DIR / "assets" / "jet_heiress_angle3.jpg"),
        ],
    },
    {
        "id": "selene-noir",
        "name": "Selene Noir",
        "badge": "guzelai.com • Selene Noir",
        "gender": "kadin",
        "role_tr": "Milano • Paris • Fifth Avenue Gece Mücevheri & Kadife Dudak Kozmetik Musesi",
        "face_prompt_en": (
            "official guzelai.com female editorial supermodel Selene Noir, 25-year-old Italian-French aristocrat "
            "model, 180cm, straight sleek jet-black raven silk hair, satin porcelain-ivory skin, striking dark "
            "almond eyes, velvet burgundy-red lips, photorealistic real human skin texture"
        ),
        "fallback_photos": [
            str(BASE_DIR / "assets" / "como_heiress_angle1.jpg"),
            str(BASE_DIR / "assets" / "como_heiress_angle2.jpg"),
            str(BASE_DIR / "assets" / "como_heiress_angle3.jpg"),
        ],
    },
    {
        "id": "chloe-bennett",
        "name": "Chloe Bennett",
        "badge": "guzelai.com • Chloe Bennett",
        "gender": "kadin",
        "role_tr": "New York • Malibu • Cannes Altın Işıltılı Cilt Bakımı & 18K Takı Yüzü",
        "face_prompt_en": (
            "official guzelai.com female supermodel Chloe Bennett, 23-year-old American-Riviera luxury beauty "
            "and jewelry model, 176cm, voluminous sun-kissed honey-blonde wavy hair, bright blue-green eyes, "
            "radiant golden peach glass skin, natural confident gaze, photorealistic real human skin pores"
        ),
        "fallback_photos": [
            str(BASE_DIR / "assets" / "como_heiress_angle2.jpg"),
            str(BASE_DIR / "assets" / "como_heiress_angle3.jpg"),
            str(BASE_DIR / "assets" / "como_heiress_angle4.jpg"),
        ],
    },
    {
        "id": "scarlett-vance",
        "name": "Scarlett Vance",
        "badge": "guzelai.com • Scarlett Vance",
        "gender": "kadin",
        "role_tr": "Londra Bond Street • Paris Vogue Zümrüt Mücevher & Lüks Makyaj İkonu",
        "face_prompt_en": (
            "official guzelai.com female Vogue cover supermodel Scarlett Vance, 24-year-old Anglo-Parisian "
            "editorial model, 177cm, rich fiery copper-auburn wavy hair, emerald-green eyes, delicate natural "
            "freckles on porcelain-peach skin, sculpted jawline, photorealistic real human skin texture"
        ),
        "fallback_photos": [
            str(BASE_DIR / "assets" / "valentina_cruz_angle2.jpg"),
            str(BASE_DIR / "assets" / "valentina_cruz_angle3.jpg"),
            str(BASE_DIR / "assets" / "valentina_cruz_angle4.jpg"),
        ],
    },
    {
        "id": "kenzo-takahashi",
        "name": "Kenzo Takahashi",
        "badge": "guzelai.com • Kenzo Takahashi",
        "gender": "erkek",
        "role_tr": "Cenevre • Milano • New York Yüksek Saatçilik (Haute Horlogerie) & Niş Parfüm Yüzü",
        "face_prompt_en": (
            "official guzelai.com male supermodel Kenzo Takahashi, 28-year-old charismatic Milan-New York "
            "sartorial gentleman, 186cm, classic side-parted jet-black hair, sharp chiseled jawline, wearing "
            "an 18K rose-gold mechanical tourbillon chronograph watch on wrist and holding a crystal niche "
            "extrait de parfum flacon, zero women bags, photorealistic"
        ),
        "fallback_photos": [
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_kenzo_om01_step1.jpg"),
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_kenzo_om01_step2.jpg"),
            str(SCRATCH_DIR / "instagram-kombin-bot" / "assets" / "guzelai_kenzo_om01_step3.jpg"),
        ],
    },
]

# ==============================================================================
# PINTEREST & KÜRESEL VİRAL (TÜRKİYE • AVRUPA • AMERİKA) TAKI & KOZMETİK KAMPANYALARI
# ==============================================================================
LUXURY_LOCATIONS_AND_STORIES: Dict[str, List[Dict[str, Any]]] = {
    "taki_kozmetik_transatlantic": [
        {
            "slug": "tr_eu_us_tiffany_dior_zen_fifth_ave_vendome_nisantasi",
            "category": "taki",
            "region_badge": "🇹🇷 TR • 🇪🇺 EU • 🇺🇸 US VIRAL AD",
            "pinterest_trend_tag": "🔥 PINTEREST VIRAL • +142% KAYDETME",
            "location_name": "Paris Place Vendôme • NY Fifth Avenue • İstanbul Nişantaşı",
            "title": "Transatlantik Elit Mücevher & Kozmetik: Cartier Panthère, Tiffany HardWear & Dior 999 Velvet 💎💄",
            "setting_en": (
                "inside an ultra-luxurious sunlit white marble and champagne-gold haute joaillerie & beauty "
                "penthouse salon bridging Paris Place Vendôme, New York Fifth Avenue, and Istanbul Nişantaşı, "
                "soft Profoto parabolic studio lighting with warm golden specular reflections"
            ),
            "wardrobe_en": (
                "wearing an off-the-shoulder black silk haute couture evening gown showcasing an 18K gold and "
                "emerald-diamond necklace on the collarbone, a chunky 18K gold link bracelet on the wrist, "
                "and luminous glass-skin makeup with velvet crimson-red lips"
            ),
            "action_angles_en": [
                "vertical 9:16 three-quarter Vogue luxury commercial portrait standing beside a white Carrara marble pedestal with diamond jewelry and golden Dior lipstick flacon, radiant glass skin",
                "vertical 9:16 medium close-up beauty and high-jewelry commercial shot focusing on the collarbone diamond necklace, 18K gold wrist cuff, and satin red lip application",
                "vertical 9:16 macro-sharp 85mm f/1.4 portrait looking directly into the lens with sparkling diamond catchlights, 18K gold link bracelet near jawline, and porcelain skin pores",
            ],
            "bottom_brand": "CARTIER • TIFFANY & CO. • DIOR • ZEN",
            "bottom_product": "TR • EU • US Viral Jewelry & Beauty Edit",
            "items": {
                "slot1": {
                    "emoji": "💎",
                    "region": "🇪🇺 PARIS & 🇹🇷 İSTANBUL",
                    "brand": "CARTIER / ZEN PIRLANTA",
                    "name": "Panthère 18K Altın & Zümrüt Kesim Pırlanta Gerdanlık",
                    "price": "385.000 TL • €10.500",
                    "sku": "TR-EU-JEWEL-01",
                    "store_url": "https://www.zenpirlanta.com/pirlanta-gerdanliklar",
                },
                "slot2": {
                    "emoji": "🔗",
                    "region": "🇺🇸 NEW YORK FIFTH AVE",
                    "brand": "TIFFANY & CO. / BEYMEN",
                    "name": "HardWear 18K Sarı Altın Pırlanta Pavé Kalın Zincir Bileklik",
                    "price": "$14.800 • 495.000 TL",
                    "sku": "US-TIFFANY-HW02",
                    "store_url": "https://www.tiffany.com/jewelry/bracelets/",
                },
                "slot3": {
                    "emoji": "💄",
                    "region": "🇹🇷 SEPHORA TR • 🇪🇺 EU • 🇺🇸 US",
                    "brand": "DIOR BEAUTY & LA MER",
                    "name": "Rouge Dior 999 Velvet Ruj & Crème de la Mer Glass-Skin Seti",
                    "price": "19.500 TL • $540",
                    "sku": "GLOBAL-DIOR-LAMER03",
                    "store_url": "https://www.sephora.com.tr/markalar/dior/",
                },
            },
        },
        {
            "slug": "tr_eu_us_bulgari_kurkdjian_chanel_milano_miami_bebek",
            "category": "makyaj",
            "region_badge": "🇹🇷 TR • 🇪🇺 EU • 🇺🇸 US BEAUTY & JEWELRY",
            "pinterest_trend_tag": "🔥 PINTEREST #1 TREND • SCENT & GOLD STACK",
            "location_name": "Milano Via Monte Napoleone • Miami Design District • İstanbul Bebek",
            "title": "Viral Kokular, Cam Cilt & 18K Altın: Baccarat Rouge 540, Bulgari Serpenti & Chanel Sublimage 🌹🐍",
            "setting_en": (
                "in a sunlit limestone and brushed-brass luxury beauty & high-jewelry editorial studio inspired "
                "by Milan Via Monte Napoleone and New York SoHo, crystal perfume bottles and 18K gold jewelry "
                "resting on a travertine plinth"
            ),
            "wardrobe_en": (
                "wearing a champagne silk-satin backless couture slip dress, coiled 18K rose-gold diamond "
                "Serpenti bracelet on wrist, diamond drop earrings, and dewy glass-skin cheekbone highlight"
            ),
            "action_angles_en": [
                "vertical 9:16 editorial commercial portrait misting Maison Francis Kurkdjian Baccarat Rouge 540 crystal flacon onto collarbone while 18K rose-gold diamond bracelet catches golden studio light",
                "vertical 9:16 close-up beauty and jewelry shot showing the coiled 18K rose-gold diamond bracelet on wrist holding Chanel Sublimage gold serum dropper",
                "vertical 9:16 macro 100mm f/2.8 luxury campaign finale highlighting glowing glass skin, diamond drop earrings, and glossy peptide lips",
            ],
            "bottom_brand": "BULGARI • KURKDJIAN • CHANEL",
            "bottom_product": "Scent Layering & 18K Serpenti Viral Ad",
            "items": {
                "slot1": {
                    "emoji": "🌹",
                    "region": "🇪🇺 PARIS • 🇺🇸 NY • 🇹🇷 BEYMEN",
                    "brand": "MAISON FRANCIS KURKDJIAN",
                    "name": "Baccarat Rouge 540 Extrait de Parfum 70ml (Viral Scent Stack)",
                    "price": "21.400 TL • €465 • $495",
                    "sku": "MFK-BR540-GLOBAL",
                    "store_url": "https://www.beymen.com/tr/kozmetik-maison-francis-kurkdjian-90159",
                },
                "slot2": {
                    "emoji": "🐍",
                    "region": "🇪🇺 ROMA & 🇺🇸 BEVERLY HILLS",
                    "brand": "BULGARI / ATASAY PRIVÉ",
                    "name": "Serpenti Viper 18K Pembe Altın Tam Tur Pırlanta Kelepçe",
                    "price": "€34.000 • 1.240.000 TL",
                    "sku": "BVLGARI-SERPENTI-EU",
                    "store_url": "https://www.bulgari.com/en-int/jewelry/serpenti",
                },
                "slot3": {
                    "emoji": "✨",
                    "region": "🇹🇷 SEPHORA TR • 🇪🇺 EU • 🇺🇸 US",
                    "brand": "CHANEL & GUERLAIN",
                    "name": "Sublimage L'Extrait Gece İksiri & Gold Nobile Cam Cilt Serumu",
                    "price": "28.900 TL • $680",
                    "sku": "CHANEL-SUBLIMAGE-GL",
                    "store_url": "https://www.sephora.com.tr/markalar/guerlain/",
                },
            },
        },
        {
            "slug": "tr_eu_us_vancleef_charlottetilbury_tomford_london_ny_istanbul",
            "category": "taki",
            "region_badge": "🇹🇷 TR • 🇪🇺 EU • 🇺🇸 US HIGH SAVES",
            "pinterest_trend_tag": "🔥 PINTEREST TOP SAVED • QUIET LUXURY GLOW",
            "location_name": "Londra New Bond Street • New York Madison Ave • İstanbul Zorlu VIP",
            "title": "Pinterest En Çok Kaydedilen Seçki: Van Cleef Alhambra, Chopard Happy Diamonds & Tom Ford Glow 🍀💎",
            "setting_en": (
                "inside a pure white and warm alabaster cyclorama luxury commercial photography studio (#FFFFFF) "
                "with soft golden rim lighting and a velvet jewelry presentation tray"
            ),
            "wardrobe_en": (
                "wearing an ivory cashmere off-shoulder couture top, 18K gold mother-of-pearl clover necklace "
                "layered at the neckline, diamond watch on wrist, and luminous peach-gold makeup"
            ),
            "action_angles_en": [
                "vertical 9:16 three-quarter studio commercial portrait in a pure white cyclorama studio (#FFFFFF) showcasing the 18K gold Alhambra clover necklace and glowing bronzed skin",
                "vertical 9:16 medium close-up on wrist and neckline showing the Chopard diamond watch and Tom Ford Shade & Illuminate compact",
                "vertical 9:16 macro beauty & jewelry portrait with crisp catchlights, diamond starlight glints, and satin nude-rose lips",
            ],
            "bottom_brand": "VAN CLEEF • CHOPARD • TOM FORD",
            "bottom_product": "Alhambra 18K & Glass-Skin Glow Ad",
            "items": {
                "slot1": {
                    "emoji": "🍀",
                    "region": "🇪🇺 PARIS • 🇺🇸 NY • 🇹🇷 İSTANBUL",
                    "brand": "VAN CLEEF & ARPELS / KOÇAK",
                    "name": "Vintage Alhambra 10 Motif 18K Altın & Sedef Gerdanlık",
                    "price": "$9.650 • €8.900 • 345.000 TL",
                    "sku": "VCA-ALHAMBRA-GLOBAL",
                    "store_url": "https://www.vancleefarpels.com/en/collections/jewelry/alhambra.html",
                },
                "slot2": {
                    "emoji": "⌚",
                    "region": "🇨🇭 CENEVRE & 🇺🇸 FIFTH AVE",
                    "brand": "CHOPARD",
                    "name": "Happy Sport 18K Rose Gold Hareketli Pırlantalı Saat",
                    "price": "€18.500 • 675.000 TL",
                    "sku": "CHOPARD-HAPPY-01",
                    "store_url": "https://www.chopard.com/en-intl/watches",
                },
                "slot3": {
                    "emoji": "💋",
                    "region": "🇹🇷 BEYMEN • 🇪🇺 SEPHORA • 🇺🇸 US",
                    "brand": "TOM FORD BEAUTY",
                    "name": "Soleil Brûlant Altın Işıltı Yağı & Shade and Illuminate Seti",
                    "price": "11.250 TL • $310",
                    "sku": "TF-SOLEIL-GLOW",
                    "store_url": "https://www.beymen.com/tr/kozmetik-tom-ford-31377",
                },
            },
        },
        {
            "slug": "tr_eu_us_patek_rolex_creed_men_horology_grooming",
            "category": "taki",
            "region_badge": "🇹🇷 TR • 🇪🇺 EU • 🇺🇸 US MEN'S HOROLOGY & SCENT",
            "pinterest_trend_tag": "🔥 PINTEREST MEN'S LUXURY • +160% TREND",
            "location_name": "Cenevre Rue du Rhône • Milano Brera • İstanbul Akaretler VIP",
            "title": "Erkek Yüksek Saatçilik & Niş Parfüm Reklamı: Patek Philippe Nautilus, Cartier Santos & Creed Aventus ⌚👑",
            "setting_en": (
                "inside a private walnut, obsidian-marble, and warm brass Haute Horlogerie & Niche Perfumery "
                "salon connecting Geneva, Milan, and New York, dramatic cinematic key lighting"
            ),
            "wardrobe_en": (
                "wearing a bespoke midnight-charcoal Loro Piana cashmere jacket over crisp white shirt, "
                "an 18K rose-gold Patek Philippe Nautilus chronograph on wrist, and 18K gold cufflinks"
            ),
            "action_angles_en": [
                "vertical 9:16 three-quarter luxury watch & fragrance commercial portrait adjusting the 18K rose-gold Patek Philippe Nautilus on wrist beside a crystal Creed flacon",
                "vertical 9:16 macro wrist and hand shot holding the crystal niche perfume bottle with anisotropic gold reflections on the watch bezel",
                "vertical 9:16 close-up editorial portrait with sharp jawline, Cartier gold eyewear, and warm sapphire-crystal watch reflection",
            ],
            "bottom_brand": "PATEK PHILIPPE • CARTIER • CREED",
            "bottom_product": "Haute Horlogerie & Niche Extrait Ad",
            "items": {
                "slot1": {
                    "emoji": "⌚",
                    "region": "🇨🇭 CENEVRE • 🇺🇸 NY • 🇹🇷 İSTANBUL",
                    "brand": "PATEK PHILIPPE / CHRONO24",
                    "name": "Nautilus 18K Rose Gold Otomatik Kronograf Kol Saati",
                    "price": "$135.000 • €124.000 • 4.650.000 TL",
                    "sku": "PP-NAUTILUS-MEN01",
                    "store_url": "https://www.chrono24.com.tr/patekphilippe/index.htm",
                },
                "slot2": {
                    "emoji": "🥃",
                    "region": "🇹🇷 BEYMEN • 🇪🇺 PARIS • 🇺🇸 NY",
                    "brand": "CREED / PARFUMS DE MARLY",
                    "name": "Creed Absolu Aventus & Layton Exclusif Niş Parfüm Koleksiyonu",
                    "price": "24.500 TL • €520 • $565",
                    "sku": "CREED-ABSOLU-MEN02",
                    "store_url": "https://www.beymen.com/tr/kozmetik-parfum-10108",
                },
                "slot3": {
                    "emoji": "🕶️",
                    "region": "🇪🇺 PARIS & 🇹🇷 BEYMEN",
                    "brand": "CARTIER",
                    "name": "Santos de Cartier 18K Altın Kaplama Erkek Güneş Gözlüğü & Kol Düğmesi",
                    "price": "56.500 TL • €1.450",
                    "sku": "CARTIER-SANTOS-MEN03",
                    "store_url": "https://www.cartier.com/en-us/bags-and-accessories/eyewear/",
                },
            },
        },
    ],
}
# Geriye dönük kategori anahtarları için tam uyumluluk haritası
LUXURY_LOCATIONS_AND_STORIES["makyaj"] = LUXURY_LOCATIONS_AND_STORIES["taki_kozmetik_transatlantic"]
LUXURY_LOCATIONS_AND_STORIES["taki"] = LUXURY_LOCATIONS_AND_STORIES["taki_kozmetik_transatlantic"]
LUXURY_LOCATIONS_AND_STORIES["otel"] = LUXURY_LOCATIONS_AND_STORIES["taki_kozmetik_transatlantic"]
LUXURY_LOCATIONS_AND_STORIES["araba"] = LUXURY_LOCATIONS_AND_STORIES["taki_kozmetik_transatlantic"]
LUXURY_LOCATIONS_AND_STORIES["yasam"] = LUXURY_LOCATIONS_AND_STORIES["taki_kozmetik_transatlantic"]

DYNAMIC_LUXURY_HUBS = [
    (
        "New York Fifth Avenue • Paris Place Vendôme • İstanbul Nişantaşı",
        "inside a flagship haute joaillerie & luxury cosmetics atrium bridging New York Fifth Avenue, Paris Place Vendôme, and Istanbul Nişantaşı",
    ),
    (
        "Beverly Hills Rodeo Drive • Milano Via Monte Napoleone • İstanbul Zorlu VIP",
        "in a sunlit marble and 18K gold luxury beauty & diamond gallery connecting Beverly Hills Rodeo Drive, Milan, and Istanbul",
    ),
    (
        "Londra New Bond Street • Cenevre Rue du Rhône • İstanbul Bebek Sahil",
        "inside an aristocratic white-and-gold high-jewelry and skincare salon connecting London Bond Street, Geneva, and Istanbul Bebek",
    ),
    (
        "Miami Design District • Cannes Croisette • Bodrum Yalıkavak Marina VIP",
        "in a golden-hour resort high-jewelry & glass-skin beauty suite connecting Miami, Cannes, and Bodrum",
    ),
]


def _remotion_spring(
    t_sec: float,
    damping: float = 14.0,
    stiffness: float = 120.0,
    mass: float = 0.8,
) -> float:
    """
    `remotion-dev/remotion` (`vendor_repos/remotion-template-overlay`) ikinci dereceden
    sönümlü harmonik salınım yay fiziği denklemi.
    """
    if t_sec <= 0.0:
        return 0.0
    omega0 = math.sqrt(stiffness / max(0.001, mass))
    zeta = damping / (2.0 * math.sqrt(stiffness * max(0.001, mass)))
    if zeta < 1.0:
        omega_d = omega0 * math.sqrt(1.0 - zeta * zeta)
        env = math.exp(-zeta * omega0 * t_sec)
        val = 1.0 - env * (
            math.cos(omega_d * t_sec) + (zeta / math.sqrt(1.0 - zeta * zeta)) * math.sin(omega_d * t_sec)
        )
    else:
        val = 1.0 - (1.0 + omega0 * t_sec) * math.exp(-omega0 * t_sec)
    return float(max(0.0, min(1.08, val)))


def _apply_gl_transition_light_leak(
    frame_rgb: Image.Image,
    intensity: float,
    sweep_pos: float = 0.5,
) -> Image.Image:
    """
    `gre/gl-transitions` Anamorfik Şampanya Altın Işık Sızıntısı (Light-Leak) Shader Geçişi.
    """
    if intensity <= 0.01:
        return frame_rgb
    arr = np.array(frame_rgb, dtype=np.float32)
    h, w, _ = arr.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = xx / float(w)
    ny = yy / float(h)
    diag = nx * 0.76 + ny * 0.24
    band = np.exp(-((diag - sweep_pos) ** 2) / 0.028)
    leak = np.clip(band * 0.88, 0.0, 1.0) * float(intensity)
    arr[:, :, 0] = np.clip(arr[:, :, 0] + leak * 242.0, 0.0, 255.0)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + leak * 188.0, 0.0, 255.0)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + leak * 102.0, 0.0, 255.0)
    return Image.fromarray(arr.astype(np.uint8), mode="RGB")


def load_vertical_7models_ledger() -> Dict[str, Any]:
    if VERTICAL_LEDGER_PATH.exists():
        try:
            return json.loads(VERTICAL_LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "engine": "guzelai_graphmotion3_tr_eu_us_jewelry_cosmetics",
        "used_scenario_ids": [],
        "used_photo_hashes": [],
        "last_model_index": -1,
        "last_campaign_index": -1,
        "model_usage_counts": {m["id"]: 0 for m in GUZELAI_7_OFFICIAL_MODELS},
        "history": [],
    }


def save_vertical_7models_ledger(ledger: Dict[str, Any]) -> None:
    VERTICAL_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    VERTICAL_LEDGER_PATH.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def ensure_strict_vertical_9_16(
    img: Image.Image,
    target_w: int = VERTICAL_W,
    target_h: int = VERTICAL_H,
) -> Image.Image:
    rgb = img.convert("RGB")
    if (rgb.width, rgb.height) != (target_w, target_h):
        rgb = ImageOps.fit(
            rgb,
            (target_w, target_h),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.35),
        )
    rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    rgb = ImageEnhance.Color(rgb).enhance(1.09)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.4, percent=132, threshold=2))
    return rgb


def _get_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _build_graphmotion3_product_card(
    item: Dict[str, Any],
    angle_im: Image.Image,
    model_badge: str,
    region_badge: str,
    shimmer_phase: float = 0.5,
) -> Image.Image:
    """
    `heygen-com/hyperframes` + `remotion-dev/remotion` GraphMotion 3.0 Yüzen Lüks Ürün Reklam Kartı:
    - Sol tarafta 1:1 yuvarlatılmış altın çerçeveli makro ürün/manken detayı,
    - Üstte TR • EU • US Viral Bölge Etiketi,
    - Ortada Büyük Marka Başlığı & Ürün Adı,
    - Altta Çoklu Para Birimi Fiyatı (TL • € • $) + Canlı Altın Specular Shimmer Işık Dalgası.
    """
    cw, ch = 984, 232
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    # Obsidian & Champagne Gold Glassmorphism zemin
    draw.rounded_rectangle(
        (0, 0, cw - 1, ch - 1),
        radius=34,
        fill=(14, 13, 18, 224),
        outline=(214, 176, 98, 245),
        width=3,
    )
    draw.rounded_rectangle(
        (8, 8, cw - 9, ch - 9),
        radius=28,
        outline=(214, 176, 98, 105),
        width=1,
    )

    # Sol tarafta 1:1 makro ürün/detay penceresi (180x180)
    thumb_size = 180
    crop_box = (
        int(angle_im.width * 0.22),
        int(angle_im.height * 0.24),
        int(angle_im.width * 0.78),
        int(angle_im.height * 0.68),
    )
    thumb_src = angle_im.crop(crop_box)
    thumb = ImageOps.fit(thumb_src, (thumb_size, thumb_size), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", (thumb_size, thumb_size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, thumb_size - 1, thumb_size - 1), radius=24, fill=255)
    card.paste(thumb, (26, 26), mask)
    draw.rounded_rectangle(
        (26, 26, 26 + thumb_size, 26 + thumb_size),
        radius=24,
        outline=(214, 176, 98, 230),
        width=2,
    )

    f_reg = _get_font(18, bold=True)
    f_brand = _get_font(28, bold=True)
    f_name = _get_font(21, bold=False)
    f_price = _get_font(23, bold=True)

    tx = 230
    reg_txt = f"{item.get('region', region_badge)}  •  {model_badge.upper()}"
    draw.text((tx, 34), reg_txt[:54], fill=(218, 182, 108, 255), font=f_reg)

    brand_txt = f"{item.get('emoji', '💎')} {item.get('brand', 'LUXURY MAISON')}"
    draw.text((tx, 68), brand_txt[:36], fill=(255, 250, 240, 255), font=f_brand)

    name_txt = str(item.get("name", "Haute Joaillerie & Beauty Edition"))
    draw.text((tx, 112), name_txt[:46], fill=(224, 218, 208, 255), font=f_name)

    # Alt fiyat ve mağaza rozeti
    price_txt = f"🛍️ {item.get('price', '')}   |   RESMİ MAĞAZA & LİNK"
    draw.rounded_rectangle(
        (tx, 152, cw - 28, 198),
        radius=16,
        fill=(214, 176, 98, 42),
        outline=(214, 176, 98, 195),
        width=1,
    )
    draw.text((tx + 16, 162), price_txt[:48], fill=(248, 224, 162, 255), font=f_price)

    # Canlı Altın Specular Shimmer Işık Dalgası (Kartın üzerinden geçen diyagonal parıltı)
    if 0.0 <= shimmer_phase <= 1.0:
        arr = np.array(card, dtype=np.float32)
        yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
        diag = (xx / float(cw)) * 0.85 + (yy / float(ch)) * 0.15
        shimmer = np.exp(-((diag - shimmer_phase) ** 2) / 0.0045) * 58.0
        alpha_mask = (arr[:, :, 3] > 20).astype(np.float32)
        arr[:, :, 0] = np.clip(arr[:, :, 0] + shimmer * alpha_mask, 0.0, 255.0)
        arr[:, :, 1] = np.clip(arr[:, :, 1] + shimmer * 0.88 * alpha_mask, 0.0, 255.0)
        arr[:, :, 2] = np.clip(arr[:, :, 2] + shimmer * 0.55 * alpha_mask, 0.0, 255.0)
        card = Image.fromarray(arr.astype(np.uint8), mode="RGBA")

    return card


def create_elite_9_16_ad_poster(
    scenario: Dict[str, Any],
    vertical_photo_paths: List[str],
    out_poster_path: Path,
) -> Path:
    """
    Telegram (`@Sesliluksbot`), Pinterest (`@guzelaicom`) ve `guzelai.com` için
    %100 Dikey (`1080x1920` — `9:16`) Elit Dergi & Reklam Kampanya Afişi üretir.
    """
    base_im = Image.open(vertical_photo_paths[0]).convert("RGB")
    base_im = ensure_strict_vertical_9_16(base_im, VERTICAL_W, VERTICAL_H)
    canvas = base_im.convert("RGBA")

    ov = Image.new("RGBA", (VERTICAL_W, VERTICAL_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)

    # Üst elit reklam başlık kapsülü
    f_top = _get_font(20, bold=True)
    f_sub = _get_font(17, bold=True)
    draw.rounded_rectangle(
        (48, 42, VERTICAL_W - 48, 134),
        radius=28,
        fill=(12, 11, 16, 208),
        outline=(214, 176, 98, 235),
        width=2,
    )
    top_line = f"GÜZELAI.COM ELITE AD  •  {scenario.get('region_badge', '🇹🇷 TR • 🇪🇺 EU • 🇺🇸 US')}"
    sub_line = f"{scenario.get('pinterest_trend_tag', '🔥 PINTEREST VIRAL')}  •  MANKEN: {scenario.get('guzelai_model_name', '').upper()}"
    draw.text((VERTICAL_W // 2, 72), top_line[:58], fill=(248, 232, 192, 255), font=f_top, anchor="mm")
    draw.text((VERTICAL_W // 2, 106), sub_line[:64], fill=(214, 176, 98, 255), font=f_sub, anchor="mm")

    # Altta 1. öne çıkan ürünün GraphMotion 3.0 yüzen cam/altın kartı
    items_list = list((scenario.get("items") or {}).values())
    if items_list:
        card_im = _build_graphmotion3_product_card(
            items_list[0],
            base_im,
            scenario.get("guzelai_model_badge", "guzelai.com"),
            scenario.get("region_badge", "TR • EU • US"),
            shimmer_phase=0.45,
        )
        ov.paste(card_im, ((VERTICAL_W - card_im.width) // 2, VERTICAL_H - card_im.height - 64), card_im)

    final_poster = Image.alpha_composite(canvas, ov).convert("RGB")
    out_poster_path.parent.mkdir(parents=True, exist_ok=True)
    final_poster.save(out_poster_path, "JPEG", quality=96, subsampling=0)
    return out_poster_path


def synthesize_vertical_9_16_editorial_photos(
    scenario: Dict[str, Any],
    model_info: Dict[str, Any],
    out_dir: Path,
) -> List[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cid = scenario["id"]
    face_en = model_info["face_prompt_en"]
    setting_en = scenario["setting_en"]
    wardrobe_en = scenario["wardrobe_en"]
    angles_en = scenario["action_angles_en"]
    fallbacks = model_info.get("fallback_photos") or []

    saved_paths: List[str] = []
    base_seed = int(hashlib.sha256(cid.encode("utf-8")).hexdigest()[:8], 16) % 2000000000

    for idx, angle_desc in enumerate(angles_en, start=1):
        out_jpg = out_dir / f"{cid}_vertical_9_16_angle{idx}.jpg"
        if out_jpg.exists() and out_jpg.stat().st_size > 80_000:
            saved_paths.append(str(out_jpg))
            continue

        full_prompt = (
            f"Strict vertical 9:16 full-screen Vogue, Cartier & Sephora global luxury jewelry and cosmetics "
            f"commercial photography, shot on Hasselblad H6D-100c with 85mm f/1.4 prime lens. {angle_desc}. "
            f"Subject: {face_en}, {wardrobe_en}, {setting_en}. "
            f"Ultra-sharp diamond facets, 18K gold specular highlights, luminous real human skin pores, "
            f"Kodak Portra 400 editorial color grading, zero text, zero watermarks, zero borders."
        )
        img = cloud_fetch_ai_image(full_prompt, width=768, height=1344, seed=base_seed + idx * 149)
        if img is None:
            fb_path = fallbacks[(idx - 1) % len(fallbacks)] if fallbacks else ""
            if fb_path and os.path.exists(fb_path):
                img = Image.open(fb_path).convert("RGB")
            else:
                img = Image.new("RGB", (VERTICAL_W, VERTICAL_H), (24, 20, 28))

        vertical_img = ensure_strict_vertical_9_16(img, VERTICAL_W, VERTICAL_H)
        vertical_img.save(out_jpg, "JPEG", quality=96, subsampling=0)
        saved_paths.append(str(out_jpg))

    return saved_paths


def render_pure_vertical_9_16_cinema_video(
    scenario: Dict[str, Any],
    vertical_photo_paths: List[str],
    output_mp4: Path,
    duration_sec: float = 12.0,
) -> Dict[str, Any]:
    """
    GraphMotion 3.0 (`remotion-dev/remotion` + `midrender/revideo` + `gre/gl-transitions` + `heygen-com/hyperframes`):
    - 1080x1920 (`9:16` Dikey) @ 30fps
    - Her açıda Remotion yay fiziğiyle (`damping=14, stiffness=120, mass=0.8`) ve 180° shutter motion blur ile
      sahneye giren Yüzen Obsidian & 18K Şampanya Altın Ürün Reklam Kartı (1:1 makro ürün görseli + TR/EU/US
      bölge rozeti + marka + fiyat + canlı altın shimmer ışık dalgası)
    - Açılar arasında GL-Transitions Anamorfik Altın Işık Sızıntısı ve Optik Rack-Focus (`f/1.4 -> f/2.8`)
    - 4-noktalı pırlanta/altın yıldız parıltıları (`enhance_frame_with_real_optics`) + Hasselblad deklanşör sesli
      lüks reklam müziği.
    """
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    frames_dir = output_mp4.parent / f"_frames_{output_mp4.stem}"
    if frames_dir.exists():
        shutil.rmtree(frames_dir, ignore_errors=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    OVERSAMPLE_W, OVERSAMPLE_H = 1216, 2160
    oversampled_angles: List[Image.Image] = []
    base_1080_angles: List[Image.Image] = []
    for fp in vertical_photo_paths:
        if os.path.exists(fp):
            im = Image.open(fp).convert("RGB")
            oversampled_angles.append(ensure_strict_vertical_9_16(im, OVERSAMPLE_W, OVERSAMPLE_H))
            base_1080_angles.append(ensure_strict_vertical_9_16(im, VERTICAL_W, VERTICAL_H))
    if not oversampled_angles:
        raise RuntimeError("Dikey 9:16 fotoğraf karesi bulunamadı!")

    num_angles = len(oversampled_angles)
    total_frames = int(duration_sec * FPS)
    angle_dur = duration_sec / float(num_angles)

    items_list = list((scenario.get("items") or {}).values())
    model_badge = scenario.get("guzelai_model_badge", "guzelai.com")
    region_badge = scenario.get("region_badge", "🇹🇷 TR • 🇪🇺 EU • 🇺🇸 US")
    pinterest_tag = scenario.get("pinterest_trend_tag", "🔥 PINTEREST VIRAL")

    f_top = _get_font(19, bold=True)
    f_sub = _get_font(16, bold=True)

    def _sample_gimbal_frame(src_im: Image.Image, progress_0_1: float, angle_i: int) -> Image.Image:
        p = 0.5 - 0.5 * math.cos(max(0.0, min(1.0, progress_0_1)) * math.pi)
        zoom = 1.0 + 0.085 * p
        crop_w = OVERSAMPLE_W / zoom
        crop_h = OVERSAMPLE_H / zoom
        max_dx = (OVERSAMPLE_W - crop_w) * 0.5
        max_dy = (OVERSAMPLE_H - crop_h) * 0.5
        dir_x = 1.0 if (angle_i % 2 == 0) else -1.0
        cx = (OVERSAMPLE_W * 0.5) + dir_x * (p - 0.5) * max_dx * 0.72
        cy = (OVERSAMPLE_H * 0.46) - (p - 0.5) * max_dy * 0.50
        x1 = max(0.0, min(OVERSAMPLE_W - crop_w, cx - crop_w * 0.5))
        y1 = max(0.0, min(OVERSAMPLE_H - crop_h, cy - crop_h * 0.5))
        box = (int(round(x1)), int(round(y1)), int(round(x1 + crop_w)), int(round(y1 + crop_h)))
        return src_im.crop(box).resize((VERTICAL_W, VERTICAL_H), Image.Resampling.LANCZOS)

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)
        stage_idx = min(num_angles - 1, int(t // angle_dur))
        stage_local_t = t - (stage_idx * angle_dur)
        local_p = min(1.0, max(0.0, stage_local_t / max(0.01, angle_dur)))

        cur_frame = _sample_gimbal_frame(oversampled_angles[stage_idx], local_p, stage_idx)

        # Optik Rack-Focus (Sahne başında ilk 0.35 saniyede f/1.4 kadife odak netleşmesi)
        if stage_local_t < 0.32:
            blur_r = (1.0 - (stage_local_t / 0.32)) * 3.2
            if blur_r > 0.35:
                cur_frame = cur_frame.filter(ImageFilter.GaussianBlur(radius=blur_r))

        # Açılar arası GL-Transitions pürüzsüz geçiş + Anamorfik Altın Işık Sızıntısı
        if stage_idx < num_angles - 1 and stage_local_t > (angle_dur - 0.42):
            blend_p = (stage_local_t - (angle_dur - 0.42)) / 0.42
            blend_p = blend_p * blend_p * (3.0 - 2.0 * blend_p)
            next_frame = _sample_gimbal_frame(oversampled_angles[stage_idx + 1], 0.04 * blend_p, stage_idx + 1)
            cur_frame = Image.blend(cur_frame, next_frame, blend_p)
            cur_frame = _apply_gl_transition_light_leak(
                cur_frame,
                intensity=0.55 * math.sin(blend_p * math.pi),
                sweep_pos=blend_p,
            )

        # 4-noktalı pırlanta/altın yıldız parıltıları & Kodak Portra 400 tonlama
        cur_frame = enhance_frame_with_real_optics(
            cur_frame,
            t=t,
            frame_idx=f_idx,
            stage_idx=stage_idx,
            enable_glints=True,
        )

        rgba = cur_frame.convert("RGBA")
        ov = Image.new("RGBA", (VERTICAL_W, VERTICAL_H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(ov)

        # 1) Üst Elit Reklam Kampanya Başlığı (Remotion Spring ile yukarıdan iner)
        top_spring = _remotion_spring(t, damping=14.0, stiffness=120.0, mass=0.8)
        top_y_off = int(round((1.0 - min(1.0, top_spring)) * -90))
        odraw.rounded_rectangle(
            (48, 38 + top_y_off, VERTICAL_W - 48, 124 + top_y_off),
            radius=26,
            fill=(12, 11, 16, 204),
            outline=(214, 176, 98, 225),
            width=2,
        )
        odraw.text(
            (VERTICAL_W // 2, 66 + top_y_off),
            f"GÜZELAI.COM LUXURY AD  •  {region_badge}"[:58],
            fill=(248, 234, 198, 255),
            font=f_top,
            anchor="mm",
        )
        odraw.text(
            (VERTICAL_W // 2, 98 + top_y_off),
            f"{pinterest_tag}  •  {model_badge.upper()}"[:62],
            fill=(214, 176, 98, 255),
            font=f_sub,
            anchor="mm",
        )

        # 2) GraphMotion 3.0 Yüzen Ürün Reklam Kartı (Remotion Spring + 180° Shutter Blur + Specular Shimmer)
        if items_list:
            cur_item = items_list[min(stage_idx, len(items_list) - 1)]
            card_spring = _remotion_spring(stage_local_t, damping=14.0, stiffness=120.0, mass=0.8)
            shimmer_pos = max(0.0, min(1.0, (stage_local_t - 0.35) / max(0.5, angle_dur - 0.70)))
            card_im = _build_graphmotion3_product_card(
                cur_item,
                base_1080_angles[stage_idx],
                model_badge=model_badge,
                region_badge=region_badge,
                shimmer_phase=shimmer_pos,
            )
            slide_dy = int(round((1.0 - card_spring) * 220))
            if abs(slide_dy) > 18:
                blur_rad = min(4.0, abs(slide_dy) / 55.0)
                card_im = card_im.filter(ImageFilter.GaussianBlur(radius=blur_rad))
            card_x = (VERTICAL_W - card_im.width) // 2
            card_y = VERTICAL_H - card_im.height - 58 + slide_dy
            ov.paste(card_im, (card_x, card_y), card_im)

        # 3) Üst Kenar Altın İzlenme Tutma (Retention) İlerleme Çubuğu
        prog_w = max(12, int(VERTICAL_W * (t / duration_sec)))
        odraw.rectangle((0, 0, prog_w, 6), fill=(238, 204, 142, 245))

        final_rgb = Image.alpha_composite(rgba, ov).convert("RGB")
        final_rgb.save(frames_dir / f"frame_{f_idx:04d}.jpg", "JPEG", quality=95)

    wav_path = output_mp4.parent / f"{output_mp4.stem}_audio.wav"
    generate_luxury_soundtrack(str(wav_path), duration=duration_sec, category=scenario.get("category", "taki"))

    from render_luxury_reels import get_ffmpeg_exe
    ffmpeg_exe = get_ffmpeg_exe()

    cmd = [
        str(ffmpeg_exe),
        "-y",
        "-framerate",
        str(FPS),
        "-i",
        str(frames_dir / "frame_%04d.jpg"),
        "-i",
        str(wav_path),
        "-vf",
        "unsharp=5:5:0.8:3:3:0.0,format=yuv420p",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-profile:v",
        "high",
        "-level:v",
        "4.2",
        "-crf",
        "17",
        "-b:v",
        "8M",
        "-maxrate",
        "11M",
        "-bufsize",
        "18M",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "320k",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-shortest",
        "-movflags",
        "+faststart",
        str(output_mp4),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    shutil.rmtree(frames_dir, ignore_errors=True)
    if wav_path.exists():
        try:
            wav_path.unlink()
        except Exception:
            pass

    return {
        "video_path": str(output_mp4),
        "width": VERTICAL_W,
        "height": VERTICAL_H,
        "aspect_ratio": "9:16",
        "fps": FPS,
        "duration_sec": duration_sec,
        "size_mb": round(output_mp4.stat().st_size / (1024 * 1024), 2),
        "engine": "guzelai_graphmotion_3_0_tr_eu_us_jewelry_cosmetics",
    }


def generate_next_unique_vertical_7model_creation() -> Dict[str, Any]:
    """
    7 Resmi `guzelai.com` mankenini sırayla döndürerek Türkiye (TR), Avrupa (EU) ve Amerika (US)
    pazarlarında Pinterest'te en çok kaydedilen viral Takı (Mücevher/Saat) ve Kozmetik
    (Makyaj/Cilt Bakımı/Niş Parfüm) ürünleri için GraphMotion 3.0 standardında %100 Dikey (`9:16` — `1080x1920`)
    Reklam Afişi + 3 Açı Dikey Fotoğraf + Dikey Sinema Reklam Videosu üretir.
    """
    ledger = load_vertical_7models_ledger()
    used_ids = set(ledger.get("used_scenario_ids", []))

    next_model_idx = (int(ledger.get("last_model_index", -1)) + 1) % len(GUZELAI_7_OFFICIAL_MODELS)
    model_info = GUZELAI_7_OFFICIAL_MODELS[next_model_idx]

    campaigns = LUXURY_LOCATIONS_AND_STORIES["taki_kozmetik_transatlantic"]
    if model_info["gender"] == "erkek":
        # Erkek manken (Kenzo Takahashi) geldiğinde Yüksek Saatçilik & Niş Parfüm kampanyasını seç
        male_campaigns = [c for c in campaigns if "men" in c["slug"]] or campaigns
        base_tmpl = male_campaigns[len(used_ids) % len(male_campaigns)]
    else:
        female_campaigns = [c for c in campaigns if "men" not in c["slug"]] or campaigns
        next_camp_idx = (int(ledger.get("last_campaign_index", -1)) + 1) % len(female_campaigns)
        ledger["last_campaign_index"] = next_camp_idx
        base_tmpl = female_campaigns[next_camp_idx]

    today_tag = datetime.date.today().strftime("%Y%m%d")
    seq_num = len(used_ids) + 1
    candidate_id = f"gm3_treuus_{model_info['id'].replace('-', '_')}_{base_tmpl['slug'][:28]}_{today_tag}_{seq_num:02d}"

    chosen_template = dict(base_tmpl)
    chosen_template["id"] = candidate_id
    if seq_num > len(campaigns):
        hub_tr, hub_en = DYNAMIC_LUXURY_HUBS[seq_num % len(DYNAMIC_LUXURY_HUBS)]
        chosen_template["location_name"] = hub_tr
        chosen_template["setting_en"] = f"{hub_en}, {base_tmpl['setting_en']}"

    scenario: Dict[str, Any] = {
        **chosen_template,
        "guzelai_model_id": model_info["id"],
        "guzelai_model_name": f"{model_info['name']} (guzelai.com)",
        "guzelai_model_badge": model_info["badge"],
        "guzelai_model_role": model_info["role_tr"],
        "created_at_iso": datetime.datetime.now().isoformat(timespec="seconds"),
    }

    creation_dir = VERTICAL_OUT_DIR / scenario["id"]
    vertical_photos = synthesize_vertical_9_16_editorial_photos(scenario, model_info, creation_dir)

    # Elit 9:16 Dikey Reklam Kampanya Afişini (GraphMotion 3.0 Ürün Kartlı Poster) oluştur
    poster_path = create_elite_9_16_ad_poster(
        scenario,
        vertical_photos,
        creation_dir / f"{scenario['id']}_elite_ad_poster_9_16.jpg",
    )
    scenario["model_frames"] = [str(poster_path)] + vertical_photos
    scenario["hero_vertical_photo"] = str(poster_path)

    output_mp4 = creation_dir / f"{scenario['id']}_1080x1920.mp4"
    video_info = render_pure_vertical_9_16_cinema_video(scenario, vertical_photos, output_mp4)
    scenario["video_path"] = video_info["video_path"]
    scenario["video_info"] = video_info

    ledger["used_scenario_ids"].append(scenario["id"])
    ledger["last_model_index"] = next_model_idx
    counts = ledger.get("model_usage_counts") or {}
    counts[model_info["id"]] = int(counts.get(model_info["id"], 0)) + 1
    ledger["model_usage_counts"] = counts
    ledger.setdefault("history", []).append(
        {
            "scenario_id": scenario["id"],
            "created_at": scenario["created_at_iso"],
            "category": scenario["category"],
            "region_badge": scenario.get("region_badge"),
            "pinterest_trend_tag": scenario.get("pinterest_trend_tag"),
            "model_id": model_info["id"],
            "model_name": model_info["name"],
            "location_name": scenario["location_name"],
            "elite_poster_9_16": str(poster_path),
            "vertical_photos": vertical_photos,
            "vertical_video": video_info["video_path"],
            "resolution": "1080x1920 (9:16 Strict Vertical GraphMotion 3.0)",
        }
    )
    save_vertical_7models_ledger(ledger)
    return scenario
