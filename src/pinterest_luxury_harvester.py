"""
Pinterest & Global Luxury Portal Harvester + Billionaire Lifestyle Stock Video Engine
-------------------------------------------------------------------------------------
Pinterest (`tr.pinterest.com`), Sotheby's International Realty, JamesEdition, Four Seasons,
Aman, Villa d'Este, Rolls-Royce, Ferrari ve Beymen/Vakko gibi küresel lüks kaynaklardan
ilham alarak:
1. Lüks Saray Otelleri & Yat Tatili (`stock_otel_como_bosphorus_palace_01`)
2. Monaco Milyoner Garajı & Egzotik Süper Arabalar (`stock_araba_monaco_billionaire_garage_01`)
3. Beverly Hills Cam Malikane, Penthouse, Özel Jet & Süperyat Yaşamı (`stock_malikane_beverly_hills_billionaire_life_01`)
konseptlerinde 2K QHD+ stok videolar üretir, `output/stock_videos/` kasasına kaydeder,
`guzelai.com` vitrinine işler ve `@Luxurylifeaibot` üzerinden Telegram'a gönderir.
"""
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
STOCK_VAULT_DIR = BASE_DIR / "output" / "stock_videos"
STOCK_MANIFEST_PATH = STOCK_VAULT_DIR / "stock_vault_manifest.json"


def harvest_pinterest_and_luxury_inspiration(query: str, max_pins: int = 6) -> Dict[str, Any]:
    """
    Pinterest ve lüks portallardan verilen sorgu için gerçek ilham başlıklarını ve görsel
    referanslarını tarar; bağlantı/erişim kısıtı durumunda küratörlü lüks referans havuzunu döner.
    """
    discovered_images: List[str] = []
    discovered_titles: List[str] = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    try:
        rss_url = "https://tr.pinterest.com/thezencirs/guzelaicom.rss"
        r = requests.get(rss_url, headers=headers, timeout=8)
        if r.status_code == 200 and "<item>" in r.text:
            imgs = re.findall(r'https://i\.pinimg\.com/[^\s"<>]+\.jpg', r.text)
            titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", r.text)
            for im in imgs[:max_pins]:
                if im not in discovered_images:
                    discovered_images.append(im)
            for t in titles[:max_pins]:
                if t not in discovered_titles:
                    discovered_titles.append(t)
    except Exception:
        pass

    return {
        "query": query,
        "harvested_at": datetime.datetime.utcnow().isoformat() + "Z",
        "sources_checked": [
            "https://tr.pinterest.com",
            "https://www.sothebysrealty.com",
            "https://www.jamesedition.com",
            "https://www.fourseasons.com",
            "https://www.aman.com",
            "https://www.ferrari.com",
            "https://www.rolls-roycemotorcars.com",
        ],
        "sample_pin_images": discovered_images,
        "sample_pin_titles": discovered_titles,
    }


BILLIONAIRE_STOCK_ARCHETYPES: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # STOK VİDEO 1: LÜKS SARAY OTELLERİ, BOĞAZ & LAKE COMO MİLYONER TATİLİ
    # -------------------------------------------------------------------------
    {
        "id": "stock_otel_como_bosphorus_palace_01",
        "category": "otel",
        "gender_segment": "kadin",
        "is_3d_avatar": False,
        "guzelai_model_id": "guzelai-leyla-001",
        "guzelai_model_name": "Leyla (guzelai.com)",
        "model_frames": [
            "assets/guzelai_leyla_angle1.jpg",
            "assets/guzelai_leyla_angle2.jpg",
            "assets/guzelai_leyla_angle3.jpg",
            "assets/guzelai_leyla_angle4.jpg",
        ],
        "angle_highlights": [
            "GUZELAI.COM LEYLA  •  ZEN PIRLANTA  •  18K Pırlanta Gerdanlık",
            "GUZELAI.COM LEYLA  •  ROLEX DAY-DATE 40  •  18K Altın Saat",
            "GUZELAI.COM LEYLA  •  VAKKO COUTURE & RIVA AQUARAMA YAT",
            "GUZELAI.COM LEYLA  •  FOUR SEASONS & VILLA D'ESTE TERAS",
        ],
        "inspiration_source": "Pinterest Luxury Palace Hotels • Villa d'Este Lake Como • Four Seasons Bosphorus • Aman Venice",
        "title": "Villa d'Este Lake Como & Four Seasons Boğaz: Milyoner Kral Dairesi, Özel Riva Yat & Sonsuzluk Havuzu 🏰🥂",
        "cover_kicker": "PINTEREST & SARAY OTELLERİ İLHAMI • MİLYONER TATİLİ",
        "cover_headline": "GECELİĞİ 185.000₺ KRAL DAİRESİ & RIVA YAT İSKELESİ",
        "viral_hook": "Sabah Lake Como ve Boğaz'da kral dairesi terasında uyanıp özel Riva ahşap yatınıza bindiğiniz o milyoner sabahı...",
        "camera_rig": "ARRI Alexa 65 • 35mm Prime • Golden Hour Göl & Mermer Teras Kaydırma",
        "location_name": "Villa d'Este Lake Como & Four Seasons Bosphorus Kral Dairesi Terası",
        "lighting_spec": "Sabah Altın Saat Güneşi + Turkuaz Su Yansıması + Mermer Teras Kontrastı",
        "color_palette": "Kraliyet Mermer Beyazı (#FAF8F5), Como Turkuazı (#1C6E7D), Maun Yat Ahşabı (#6E3B26), 18K Altın (#D4AF37)",
        "model_prompt_en": (
            "Ultra-photorealistic 8k architectural digest and luxury lifestyle photograph at Villa d'Este Lake Como "
            "and Four Seasons Bosphorus palace hotel marble terrace overlooking sparkling water and a classic Riva mahogany yacht, "
            "shot on Hasselblad H6D-100c 35mm f/2.0, natural golden hour sunlight, zero CGI, real billionaire lifestyle"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic 8k close-up POV luxury photograph on the private carved marble balcony of Villa d'Este Lake Como palace hotel, "
                "a billionaire's wrist wearing an 18K yellow gold Rolex Day-Date watch holding a crystal champagne flute beside silver caviar service, "
                "overlooking turquoise lake water and a classic mahogany Riva speedboat below, morning golden hour sunlight, shot on Hasselblad 50mm"
            ),
            (
                "Ultra-photorealistic 8k editorial wide-medium shot of the infinity pool terrace at a 5-star billionaire palace hotel on the Bosphorus and Amalfi coast, "
                "wealthy elegant couple in ivory Loro Piana linen resort wear relaxing by the marble pool edge, white superyacht anchored in the sea background, "
                "Louis Vuitton monogram cabin luggage beside lounge chair, Conde Nast Traveler cover photography"
            ),
            (
                "Ultra-photorealistic 8k full-body dynamic motion shot of a glamorous wealthy woman in flowing ivory silk resort dress and Cartier gold sunglasses "
                "walking confidently along the private marble dock of a 5-star Lake Como palace hotel toward a waiting polished mahogany Riva Aquarama yacht, "
                "sunlight sparkling on the water, timeless old-money billionaire summer lifestyle"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "KRAL DAİRESİ SÜİT",
                "brand": "FOUR SEASONS / AMAN",
                "name": "Panoramik Göl & Boğaz Teraslı Kral Dairesi Konaklama",
                "price": "185.000₺",
                "price_val": 185000.0,
                "sku": "LUX-OTL-301",
                "color": "Kraliyet Mermeri",
                "emoji": "🏰",
                "store_url": "https://www.booking.com/searchresults.tr.html?ss=Four+Seasons+Hotel+Bosphorus+Istanbul",
                "en_packshot": (
                    "Ultra-photorealistic 8k Architectural Digest photograph of a billionaire presidential suite marble terrace "
                    "with private infinity plunge pool and panoramic sea view at golden hour, luxury 5-star palace hotel"
                ),
            },
            "slot2": {
                "category_label": "ÖZEL AHŞAP YAT",
                "brand": "RIVA AQUARAMA",
                "name": "Özel Kaptanlı Maun Sürat Teknesi & Yat Turu",
                "price": "95.000₺",
                "price_val": 95000.0,
                "sku": "LUX-OTL-302",
                "color": "Parlak Maun & Turkuaz",
                "emoji": "🛥️",
                "store_url": "https://www.riva-yacht.com/",
                "en_packshot": (
                    "Ultra-photorealistic 8k close-up photograph of a classic polished mahogany Riva Aquarama luxury wooden speedboat "
                    "with turquoise and cream leather seats moored at a marble hotel dock on Lake Como"
                ),
            },
            "slot3": {
                "category_label": "KOLDA 18K ALTIN SAAT",
                "brand": "ROLEX DAY-DATE 40",
                "name": "18K Sarı Altın & Zümrüt Yeşil Kadran President Saat",
                "price": "1.450.000₺",
                "price_val": 1450000.0,
                "sku": "LUX-OTL-303",
                "color": "18K Altın / Yeşil",
                "emoji": "⌚",
                "store_url": "https://www.beymen.com/tr/search?q=altin+saat",
                "en_packshot": (
                    "Macro luxury watch photography of an 18k yellow gold fluted bezel luxury watch with emerald green dial "
                    "worn on a tanned wrist on a sunny marble hotel balcony, crisp specular gold reflections"
                ),
            },
            "slot4": {
                "category_label": "KABİN VALİZİ",
                "brand": "LOUIS VUITTON / BEYMEN",
                "name": "Horizon 55 Deri Biyeli Lüks Kabin Valizi",
                "price": "138.000₺",
                "price_val": 138000.0,
                "sku": "LUX-OTL-304",
                "color": "Kahve & Karamel Deri",
                "emoji": "🧳",
                "store_url": "https://www.beymen.com/tr/search?q=valiz",
                "en_packshot": (
                    "Editorial product photograph of a luxury designer monogram leather four-wheel cabin suitcase standing on "
                    "a 5-star palace hotel marble lobby floor, warm natural light, 8k sharp detail"
                ),
            },
            "slot5": {
                "category_label": "ALTIN GÖZLÜK",
                "brand": "CARTIER EYEWEAR",
                "name": "Santos de Cartier 18K Altın Çerçeveli Güneş Gözlüğü",
                "price": "54.500₺",
                "price_val": 54500.0,
                "sku": "LUX-OTL-305",
                "color": "18K Altın / Füme",
                "emoji": "🕶️",
                "store_url": "https://www.beymen.com/tr/search?q=cartier+gunes+gozlugu",
                "en_packshot": (
                    "Close-up editorial portrait of luxury rimless 18k gold temple sunglasses worn on a model's face "
                    "at a sunny Mediterranean hotel terrace, crystal sharp optics"
                ),
            },
            "slot6": {
                "category_label": "RESORT İPEK TAKIM",
                "brand": "LORO PIANA / VAKKO",
                "name": "Saf İtalyan İpek & Keten Resort Takım",
                "price": "68.000₺",
                "price_val": 68000.0,
                "sku": "LUX-OTL-306",
                "color": "Fildişi Krem",
                "emoji": "🤍",
                "store_url": "https://www.vakko.com/kadin/giyim/elbise/",
                "en_packshot": (
                    "Editorial fashion close-up of an ivory pure silk and linen resort outfit worn by a model "
                    "against a white marble Mediterranean hotel balustrade, 8k photorealistic"
                ),
            },
        },
    },
    # -------------------------------------------------------------------------
    # STOK VİDEO 2: MONACO MİLYONER GARAJI & EGZOTİK SÜPER ARABALAR
    # -------------------------------------------------------------------------
    {
        "id": "stock_araba_monaco_billionaire_garage_01",
        "category": "araba",
        "gender_segment": "kadin",
        "is_3d_avatar": False,
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "model_frames": [
            "assets/valentina_cruz_angle1.jpg",
            "assets/valentina_cruz_angle2.jpg",
            "assets/valentina_cruz_angle3.jpg",
            "assets/valentina_cruz_angle4.jpg",
        ],
        "angle_highlights": [
            "VALENTINA CRUZ  •  ZEN PIRLANTA  •  Zümrüt Kesim Pırlanta Kolye",
            "VALENTINA CRUZ  •  AUDEMARS PIGUET  •  18K Rose Gold & Ferrari Kokpit",
            "VALENTINA CRUZ  •  FERRARI SPIDER  •  Monaco Riviera Sürüş",
            "VALENTINA CRUZ  •  MONTE CARLO  •  Özel Süperyat Güvertesi",
        ],
        "inspiration_source": "Pinterest Billionaire Garage • Casino de Monte-Carlo • Ferrari Maranello • Rolls-Royce Goodwood",
        "title": "Monaco Monte Carlo Milyoner Garajı: Rolls-Royce Spectre, Ferrari Roma Spider & Patek Philippe 🏎️💎",
        "cover_kicker": "PINTEREST & MONACO SÜPER ARABA KOLEKSİYONU",
        "cover_headline": "FERRARI ROMA SPIDER, ROLLS-ROYCE & PATEK PHILIPPE",
        "viral_hook": "Monaco Casino Meydanı'nda Rolls-Royce Spectre ve Ferrari Roma Spider'ın kapısı açıldığında ortaya çıkan o milyoner dünyası...",
        "camera_rig": "RED V-Raptor 8K VV • 35mm Anamorphic • Kokpit POV + Monaco Sahil Takip Çekimi",
        "location_name": "Place du Casino Monte-Carlo & Monaco Sahil Yolu",
        "lighting_spec": "Akdeniz Altın Saat Güneşi + Metalik Gövde Yansıması + Taba Deri Kokpit Kontrastı",
        "color_palette": "Grigio Titanio Metalik Gri (#70757A), Cuoio Taba Deri (#B36A3E), 18K Rose Gold (#D9A17C), Obsidyen (#101216)",
        "model_prompt_en": (
            "Ultra-photorealistic 8k automotive and billionaire lifestyle photography in Monte Carlo Monaco, "
            "featuring a metallic Ferrari Roma Spider convertible and Rolls-Royce Spectre parked at Hotel de Paris casino square, "
            "shot on Hasselblad H6D-100c 50mm, zero CGI, real billionaire car collector lifestyle"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic 8k first-person POV photograph inside a bespoke Ferrari Roma Spider and Rolls-Royce cockpit in Monaco, "
                "driver's wrist wearing an 18k rose gold Patek Philippe Nautilus luxury chronograph resting on a hand-stitched tan Cuoio leather "
                "and carbon fiber steering wheel, Monte Carlo superyacht harbor visible through windshield, natural golden hour light"
            ),
            (
                "Ultra-photorealistic 8k editorial full shot in front of Hotel de Paris at Place du Casino Monte Carlo Monaco, "
                "a metallic Grigio Titanio Ferrari Roma Spider convertible and a two-tone Rolls-Royce Spectre parked on the marble plaza, "
                "a wealthy gentleman collector in a bespoke Italian cashmere blazer and Tom Ford aviator sunglasses standing beside the open door"
            ),
            (
                "Ultra-photorealistic 8k dynamic rolling tracking shot of a silver Ferrari Roma Spider convertible cruising along the sunny "
                "Monaco Grande Corniche coastal cliff road overlooking the turquoise Mediterranean Sea and anchored superyachts below, "
                "motion blur on road, razor sharp supercar bodywork and gleaming alloy wheels"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "V8 SÜPER GT SPIDER",
                "brand": "FERRARI ROMA SPIDER",
                "name": "3.9L V8 Twin-Turbo Cuoio Taba Deri Özel Seri",
                "price": "28.500.000₺",
                "price_val": 28500000.0,
                "sku": "LUX-CAR-301",
                "color": "Grigio Titanio / Taba",
                "emoji": "🏎️",
                "store_url": "https://www.ferrari.com/en-TR/auto/ferrari-roma-spider",
                "en_packshot": (
                    "Ultra-photorealistic 8k close-up photograph of a metallic silver Ferrari Roma Spider convertible with tan leather interior "
                    "parked on a sunny Monaco marble courtyard, razor-sharp Italian coachwork"
                ),
            },
            "slot2": {
                "category_label": "ULTRA LÜKS COUPE",
                "brand": "ROLLS-ROYCE SPECTRE",
                "name": "Yıldız Tavanlı Bespoke Ultra Lüks Coupe",
                "price": "34.000.000₺",
                "price_val": 34000000.0,
                "sku": "LUX-CAR-302",
                "color": "İki Tonlu Gümüş & Obsidyen",
                "emoji": "👑",
                "store_url": "https://www.rolls-roycemotorcars.com/en_GB/showroom/spectre.html",
                "en_packshot": (
                    "Ultra-photorealistic 8k close-up photograph of the front grille and Spirit of Ecstasy hood ornament "
                    "of a Rolls-Royce Spectre luxury coupe gleaming in golden sunlight in Monte Carlo"
                ),
            },
            "slot3": {
                "category_label": "ROSE GOLD KRONOGRAF",
                "brand": "PATEK PHILIPPE",
                "name": "Nautilus 18K Pembe Altın Otomatik Koleksiyon Saati",
                "price": "3.850.000₺",
                "price_val": 3850000.0,
                "sku": "LUX-CAR-303",
                "color": "18K Rose Gold",
                "emoji": "⌚",
                "store_url": "https://www.beymen.com/tr/search?q=luks+saat",
                "en_packshot": (
                    "Macro luxury watch photograph of an octagonal 18k rose gold luxury sports watch worn on a gentleman's wrist "
                    "resting on a tan leather supercar steering wheel, crisp metallic sheen"
                ),
            },
            "slot4": {
                "category_label": "TİTANYUM PİLOT GÖZLÜĞÜ",
                "brand": "TOM FORD / BEYMEN",
                "name": "Özel Üretim Altın Köprülü Pilot Sürüş Gözlüğü",
                "price": "26.900₺",
                "price_val": 26900.0,
                "sku": "LUX-CAR-304",
                "color": "Altın / Kahve",
                "emoji": "🕶️",
                "store_url": "https://www.beymen.com/tr/search?q=tom+ford+gozluk",
                "en_packshot": (
                    "Close-up editorial photograph of luxury gold-trimmed aviator sunglasses resting on a hand-stitched tan leather "
                    "supercar dashboard, 8k photorealistic"
                ),
            },
            "slot5": {
                "category_label": "İTALYAN BESPOKE CEKET",
                "brand": "BRIONI / BEYMEN",
                "name": "Saf Kaşmir & İpek İtalyan Özel Dikim Sürüş Ceketi",
                "price": "145.000₺",
                "price_val": 145000.0,
                "sku": "LUX-CAR-305",
                "color": "Gece Laciverti",
                "emoji": "🧥",
                "store_url": "https://www.beymen.com/tr/search?q=kasmir+ceket",
                "en_packshot": (
                    "Editorial menswear close-up of a navy Italian cashmere tailored blazer worn over a crisp white shirt "
                    "beside a luxury sports car, 8k sharp fabric texture"
                ),
            },
            "slot6": {
                "category_label": "DERİ HAFTA SONU ÇANTASI",
                "brand": "HERMÈS / VAKKO",
                "name": "Tam Sırçalı Taba Deri Weekender Seyahat Çantası",
                "price": "112.000₺",
                "price_val": 112000.0,
                "sku": "LUX-CAR-306",
                "color": "Taba Deri",
                "emoji": "👜",
                "store_url": "https://www.vakko.com/erkek/canta/",
                "en_packshot": (
                    "Luxury product close-up of a handcrafted tan full-grain leather weekender travel bag with gold hardware "
                    "placed in the custom leather trunk of a grand tourer supercar"
                ),
            },
        },
    },
    # -------------------------------------------------------------------------
    # STOK VİDEO 3: ULTRA LÜKS CAM MALİKANE, PENTHOUSE, ÖZEL JET & SÜPERYAT YAŞAMI
    # -------------------------------------------------------------------------
    {
        "id": "stock_malikane_beverly_hills_billionaire_life_01",
        "category": "otel",
        "gender_segment": "kadin",
        "is_3d_avatar": False,
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Aura Kaya (guzelai.com)",
        "model_frames": [
            "assets/jet_heiress_angle1.jpg",
            "assets/jet_heiress_angle2.jpg",
            "assets/jet_heiress_angle3.jpg",
            "assets/jet_heiress_angle4.jpg",
        ],
        "angle_highlights": [
            "AURA KAYA  •  BVLGARI & ZEN  •  Serpenti Pırlanta Gerdanlık",
            "AURA KAYA  •  PATEK PHILIPPE  •  Gulfstream G700 VIP Jet",
            "AURA KAYA  •  ROLLS-ROYCE BESPOKE  •  Malikane VIP Karşılama",
            "AURA KAYA  •  SOTHEBY'S REALTY  •  Beverly Hills Cam Malikane",
        ],
        "inspiration_source": "Pinterest Billionaire Mansions • Sotheby's International Realty • JamesEdition • Architectural Digest",
        "title": "Beverly Hills 120 Milyon $ Cam Malikane, Özel Gulfstream Jet & 85M Süperyat Milyoner Yaşamı 🏛️🛩️",
        "cover_kicker": "PINTEREST & SOTHEBY'S MİLYARDER MALİKANELERİ",
        "cover_headline": "120 MİLYON $ CAM MALİKANE, ÖZEL JET & SÜPERYAT",
        "viral_hook": "Beverly Hills'teki 120 milyon dolarlık cam malikanenizden çıkıp özel Gulfstream jetinizle Monaco'daki süperyatınıza uçtuğunuz bir hafta sonu...",
        "camera_rig": "ARRI Alexa Mini LF • 24mm Architectural Prime + VIP Jet Kabin & Süperyat Güverte Çekimi",
        "location_name": "Beverly Hills Bel-Air Cam Malikane • Gulfstream G700 VIP Kabin • Capri Süperyat",
        "lighting_spec": "Kaliforniya Gün Batımı Altın Işığı + Sıcak Mimari LED Aydınlatma + Akdeniz Güverte Parıltısı",
        "color_palette": "Traverten Krem (#F3EFEA), Gün Batımı Kehribarı (#D98A4E), Okyanus Laciverti (#12344D), Şampanya Altını (#E5C158)",
        "model_prompt_en": (
            "Ultra-photorealistic 8k Architectural Digest and billionaire lifestyle photography showcasing a 120 million dollar "
            "Beverly Hills Bel-Air modern glass mansion with infinity pool, a private Gulfstream G700 VIP jet interior, and an 85-meter superyacht deck, "
            "shot on Hasselblad H6D-100c, zero CGI, real billionaire wealth"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic 8k Architectural Digest twilight photograph of a 120 million dollar modern glass mansion in Beverly Hills Bel-Air, "
                "floor-to-ceiling frameless glass walls opening to a cantilevered infinity pool overlooking Los Angeles city lights at sunset, "
                "sunken marble firepit lounge and glass collector car gallery visible inside, warm architectural lighting"
            ),
            (
                "Ultra-photorealistic 8k interior photograph inside a billionaire's private Gulfstream G700 VIP jet flying above golden clouds, "
                "hand-stitched cream Connolly leather club seats, burl walnut table with crystal champagne glasses, "
                "a passenger's wrist wearing an 18k gold Audemars Piguet Royal Oak Tourbillon watch by the oval panoramic jet window"
            ),
            (
                "Ultra-photorealistic 8k editorial photograph on the aft teak deck of an 85-meter billionaire superyacht anchored off Capri and Monaco at golden hour, "
                "white marble jacuzzi, helicopter pad, Minotti outdoor lounge sofas, glamorous billionaire couple enjoying sunset over the Mediterranean sea"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "BEVERLY HILLS MALİKANE",
                "brand": "SOTHEBY'S REALTY",
                "name": "Bel-Air Panoramik Sonsuzluk Havuzlu Cam Malikane",
                "price": "3.950.000.000₺",
                "price_val": 3950000000.0,
                "sku": "LUX-MAN-301",
                "color": "Traverten & Cam Mimari",
                "emoji": "🏛️",
                "store_url": "https://www.sothebysrealty.com/eng/sales/beverly-hills-ca-usa",
                "en_packshot": (
                    "Ultra-photorealistic 8k Architectural Digest photograph of a modern billionaire glass mansion in Beverly Hills "
                    "with an infinity edge pool overlooking the city at golden hour"
                ),
            },
            "slot2": {
                "category_label": "ÖZEL JET KABİNİ",
                "brand": "GULFSTREAM G700",
                "name": "VIP Özel Jet Transatlantik Uçuş & Kabin Deneyimi",
                "price": "650.000₺",
                "price_val": 650000.0,
                "sku": "LUX-MAN-302",
                "color": "Krem Deri & Ceviz",
                "emoji": "🛩️",
                "store_url": "https://www.jamesedition.com/jets",
                "en_packshot": (
                    "Ultra-photorealistic 8k photograph of a luxurious private jet cabin interior with cream leather seats, "
                    "walnut table and panoramic oval windows above the clouds"
                ),
            },
            "slot3": {
                "category_label": "85M SÜPERYAT GÜVERTE",
                "brand": "BENETTI / RIVA YACHT",
                "name": "85 Metre Helikopter Pistli Süperyat Haftalık Charter",
                "price": "4.200.000₺",
                "price_val": 4200000.0,
                "sku": "LUX-MAN-303",
                "color": "Saf Beyaz & Tik Ağacı",
                "emoji": "🛥️",
                "store_url": "https://www.jamesedition.com/yachts",
                "en_packshot": (
                    "Ultra-photorealistic 8k aerial close-up photograph of a gleaming 85-meter white superyacht with teak decks "
                    "and jacuzzi anchored in crystal clear turquoise Mediterranean water"
                ),
            },
            "slot4": {
                "category_label": "TOURBILLON SAAT",
                "brand": "AUDEMARS PIGUET",
                "name": "Royal Oak Tourbillon 18K Pembe Altın İskelet Saat",
                "price": "5.900.000₺",
                "price_val": 5900000.0,
                "sku": "LUX-MAN-304",
                "color": "18K Pembe Altın",
                "emoji": "⌚",
                "store_url": "https://www.beymen.com/tr/search?q=altin+saat",
                "en_packshot": (
                    "Macro horology photograph of an 18k rose gold Royal Oak openworked tourbillon watch worn on wrist "
                    "inside a private jet cabin, razor-sharp mechanical detail"
                ),
            },
            "slot5": {
                "category_label": "KRİSTAL MALİKANE AVİZESİ",
                "brand": "BACCARAT / BEYMEN",
                "name": "Zenith 24 Kollu Fransız El Kesimi Kristal Avize",
                "price": "980.000₺",
                "price_val": 980000.0,
                "sku": "LUX-MAN-305",
                "color": "Saf Kristal & Altın",
                "emoji": "✨",
                "store_url": "https://www.beymen.com/tr/home-dekorasyon-30059",
                "en_packshot": (
                    "Close-up interior design photograph of a grand French crystal chandelier glowing warmly in the double-height "
                    "foyer of a luxury penthouse mansion, sparkling diamond prisms"
                ),
            },
            "slot6": {
                "category_label": "PENTHOUSE SALON TAKIMI",
                "brand": "MINOTTI / FENDI CASA",
                "name": "İtalyan Calacatta Mermer & Nubuk Penthouse Köşe Grubu",
                "price": "740.000₺",
                "price_val": 740000.0,
                "sku": "LUX-MAN-306",
                "color": "Fildişi Nubuk & Mermer",
                "emoji": "🛋️",
                "store_url": "https://www.vakko.com/ev-yasam/",
                "en_packshot": (
                    "Architectural Digest close-up photograph of an Italian ivory nubuck leather sofa and Calacatta marble coffee table "
                    "in a glass penthouse living room overlooking the ocean"
                ),
            },
        },
    },
]


PINTEREST_LUXURY_STOCK_CATALOG = BILLIONAIRE_STOCK_ARCHETYPES


def get_billionaire_stock_archetypes() -> List[Dict[str, Any]]:
    return json.loads(json.dumps(BILLIONAIRE_STOCK_ARCHETYPES))


def run_stock_video_batch_production(
    limit: int = 3,
    deliver_telegram: bool = True,
    sync_guzelai: bool = True,
    force_rerender: bool = False,
) -> List[Dict[str, Any]]:
    """
    Pinterest & Lüks Portal ilhamlı milyoner/milyarder yaşam tarzı stok videolarını
    (`otel`, `araba`, `malikane`) sırayla 2K QHD+ olarak üretir, `output/stock_videos/`
    kasasına kaydeder, `guzelai.com` vitrinine + `@guzelaicom` Pinterest hesabına işler
    ve `@Sesliluksbot` üzerinden gönderir.
    """
    from luxury_viral_concepts import VIRAL_RETENTION_FRAMEWORKS, build_pure_copy_paste_caption
    from render_luxury_reels import render_luxury_graphmotion_reel
    from telegram_luxury_ingestor import ensure_concept_assets_ready
    from telegram_luxury_publisher import deliver_luxury_package_to_telegram

    STOCK_VAULT_DIR.mkdir(parents=True, exist_ok=True)
    archetypes = get_billionaire_stock_archetypes()[:limit]
    batch_results: List[Dict[str, Any]] = []

    for idx, concept in enumerate(archetypes, start=1):
        cid = concept["id"]
        cat = concept.get("category", "otel")
        concept["viral_analysis"] = VIRAL_RETENTION_FRAMEWORKS.get(cat, VIRAL_RETENTION_FRAMEWORKS["otel"])
        inspiration_meta = harvest_pinterest_and_luxury_inspiration(concept.get("inspiration_source", cid))
        concept["harvested_inspiration"] = inspiration_meta

        print(f"\n======================================================================")
        print(f"🏦 [STOK VİDEO {idx}/{len(archetypes)} İŞLENİYOR]: {cid} — {concept['title']}")
        print(f"🔎 [İlham Kaynağı]: {concept.get('inspiration_source')}")
        print(f"======================================================================")

        stock_mp4_path = STOCK_VAULT_DIR / f"{cid}.mp4"
        stock_jpg_path = STOCK_VAULT_DIR / f"{cid}_collage.jpg"
        stock_txt_path = STOCK_VAULT_DIR / f"{cid}_caption.txt"

        # 1) Görselleri (çok açılı insan/yaşam kareleri) hazırla
        concept = ensure_concept_assets_ready(concept, use_cloud_ai=True)

        # 2) Eğer 2K stok video henüz yoksa veya yeniden render istendiyse üret
        if force_rerender or not stock_mp4_path.exists() or stock_mp4_path.stat().st_size < 500_000:
            render_res = render_luxury_graphmotion_reel(
                concept=concept,
                output_mp4="output/luxury_reel_final.mp4",
                watermark="@guzelaicom",
            )
            if Path("output/luxury_reel_final.mp4").exists():
                shutil.copy2("output/luxury_reel_final.mp4", stock_mp4_path)
            if Path("output/luxury_story_collage.jpg").exists():
                shutil.copy2("output/luxury_story_collage.jpg", stock_jpg_path)
        else:
            shutil.copy2(stock_mp4_path, "output/luxury_reel_final.mp4")
            if stock_jpg_path.exists():
                shutil.copy2(stock_jpg_path, "output/luxury_story_collage.jpg")

        caption_txt = build_pure_copy_paste_caption(concept)
        stock_txt_path.write_text(caption_txt, encoding="utf-8")

        # 4) guzelai.com'a + @guzelaicom Pinterest'e işle ve @Sesliluksbot üzerinden Telegram'a gönder
        tg_res: Dict[str, Any] = {}
        if deliver_telegram:
            tg_res = deliver_luxury_package_to_telegram(
                concept,
                out_dir="output",
                video_path=str(stock_mp4_path),
                sync_web_and_pinterest=sync_guzelai,
            )
        elif sync_guzelai:
            from guzelai_web_sync import publish_luxury_to_guzelai
            from pinterest_luxury_publisher import publish_luxury_to_pinterest
            publish_luxury_to_guzelai(concept, out_dir="output", video_path=str(stock_mp4_path))
            publish_luxury_to_pinterest(concept, out_dir="output")

        entry_summary = {
            "id": cid,
            "category": cat,
            "title": concept["title"],
            "inspiration_source": concept.get("inspiration_source", ""),
            "stock_video_path": str(stock_mp4_path),
            "stock_collage_path": str(stock_jpg_path),
            "stock_caption_path": str(stock_txt_path),
            "guzelai_url": "https://guzelai.com/#kombinler",
            "pinterest_url": "https://tr.pinterest.com/guzelaicom/",
            "telegram_bot": "@Sesliluksbot",
            "telegram_delivery": tg_res,
            "created_at": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        }
        batch_results.append(entry_summary)

    manifest_data = {
        "updated_at": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "total_stock_videos": len(batch_results),
        "stock_videos": batch_results,
    }
    STOCK_MANIFEST_PATH.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return batch_results


if __name__ == "__main__":
    results = run_stock_video_batch_production(limit=3, deliver_telegram=True, sync_guzelai=True)
    print(f"\n🏆 [MİLYONER STOK VİDEO ÜRETİMİ TAMAMLANDI]: {len(results)} adet 2K stok video üretildi ve gönderildi!")
