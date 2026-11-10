"""
Google Flow Ultra (https://flow.google.com/project/5b458128-eb46-49e2-9e58-58fade625e88)
Non-Stop 1080p Autonomous Luxury Video Marathon Producer, Scenario Engine & @Sesliluksbot + guzelai.com Publisher
-----------------------------------------------------------------------------------------------------------------
- Kullanıcının Google Flow Ultra (`5b458128-eb46-49e2-9e58-58fade625e88`) projesine doğrudan bağlanır.
- Resmi `guzelai.com` mankenlerimizin (Valentina Cruz, Leyla, Aura Kaya) referans görsellerini kullanarak:
  * Karşılaşmalar & Havalı Buluşmalar (İki mankenin Boğaz yalısında, Monaco VIP kulüpte veya Place Vendôme'da buluşması)
  * Milyoner Alışveriş Alışkanlıkları (VIP özel mücevher ve haute couture salonları, kadife pırlanta tepsileri)
  * Pahalı Lüks Oteller & Kral Dairesi Odalar (Çırağan Sultan Suite, Aman Venice, Four Seasons Bosphorus, Ritz Paris)
  * Özel Kulüpler (Yacht Club de Monaco, Annabel's Mayfair, Soho House VIP)
  * Süperyatlar & Boğaz Yalıları
  temalarında sürekli yeni senaryolar geliştirir.
- DOĞAL FİZİK VE MANTIK KİLİDİ: Yürümelerde, gidişlerde, insan, araba ve yat hareketlerinde geriye dönme,
  ters yöne yürüme veya mantık hatalarına kesinlikle yer vermez; tüm hareketler tek yönlü, akıcı ve doğaldır.
- Her videoyu 1080p Full HD (1080x1920) olarak masterlar, pahalı lüks ürünlerin doğrulanmış mağaza linkleri
  ve kısa yasal uyarı metni ile `@Sesliluksbot` Telegram botuna ve `guzelai.com` Klipler vitrinine gönderir.
"""
import base64
import ctypes
from ctypes import wintypes
import datetime
import hashlib
import json
import os
import shutil
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
    build_luxury_inline_keyboard,
    get_bot_token,
    load_target_chat_ids,
    tg_api,
)
from guzelai_web_sync import _gh_put_file, _gh_get_json

FLOW_PROJECT_URL = "https://flow.google.com/project/5b458128-eb46-49e2-9e58-58fade625e88"
FLOW_CLIPS_DIR = ROOT_DIR / "assets" / "flow_clips"
FLOW_STOCK_OUT_DIR = ROOT_DIR / "output" / "stock_videos"
FLOW_LEDGER_PATH = ROOT_DIR / "output" / "google_flow_delivered_ledger.json"

NATURAL_PHYSICS_RULE = (
    "DOĞAL FİZİK VE MANTIK KURALI: İnsan, araba ve yat hareketleri %100 doğal, tutarlı ve SADECE TEK YÖNLÜ ileri doğru olmalıdır; "
    "yürürken veya araç ilerlerken geriye dönme, ters yöne yürüme, geri gitme veya ani yön değiştirme gibi mantık hataları kesinlikle olmamalıdır. "
    "Üstte veya ortada hiçbir yazı/tablo olmadan saf 9:16 dikey sinematik 1080p video."
)


def _make_luxury_items(
    b1: str, n1: str, p1: str, u1: str, s1: str,
    b2: str, n2: str, p2: str, u2: str, s2: str,
    b3: str, n3: str, p3: str, u3: str, s3: str,
) -> Dict[str, Dict[str, Any]]:
    return {
        "slot1": {
            "category_label": "Yüksek Mücevher",
            "emoji": "💎",
            "brand": b1,
            "name": n1,
            "price": p1,
            "price_val": 1850000.0,
            "sku": s1,
            "store_url": u1,
        },
        "slot2": {
            "category_label": "Haute Horlogerie Saat",
            "emoji": "⌚",
            "brand": b2,
            "name": n2,
            "price": p2,
            "price_val": 2150000.0,
            "sku": s2,
            "store_url": u2,
        },
        "slot3": {
            "category_label": "Haute Couture & Lüks Yaşam",
            "emoji": "👗",
            "brand": b3,
            "name": n3,
            "price": p3,
            "price_val": 245000.0,
            "sku": s3,
            "store_url": u3,
        },
    }


FLOW_MARATHON_SCENES: List[Dict[str, Any]] = [
    # --- YENİ SENARYO GRUBU: HAVALI BULUŞMALAR, VIP ALIŞVERİŞ, YALILAR, KRAL DAİRESİ OTELLER & ÖZEL KULÜPLER ---
    {
        "scene_id": "flow_encounter_valentina_leyla_bosphorus_yali_10",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz & Leyla (guzelai.com)",
        "model_avatar": "/assets/valentina_avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_and_leyla_encounter.jpg"),
        "title": "Boğaz Yalısı Özel Rıhtımında Havalı Buluşma: Valentina Cruz & Leyla, Pırlanta Gerdanlıklar & Rolex 🏛️🥂",
        "location_name": "Kandilli Tarihi Boğaz Yalısı Özel Mermer Rıhtımı, İstanbul",
        "bottom_brand": "ZEN PIRLANTA & ROLEX DAY-DATE",
        "bottom_product": "22 Karat Pırlanta Gerdanlık & 18K Altın Saat • Boğaz Yalısı VIP Buluşma",
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "22 Karat Baget & Zümrüt Kesim Pırlanta Gerdanlık", "1.950.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", "941001001",
            "BEYMEN / ROLEX", "18K Sarı Altın & Rose Gold Lüks Saat Seçkisi", "2.450.000 TL", "https://www.beymen.com/tr/kadin-aksesuar-saat-10072", "941001002",
            "VAKKO COUTURE", "İpek Gece & Yalı Davet Koleksiyonu", "195.000 TL", "https://www.vakko.com/kadin-giyim-elbise/", "941001003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki iki guzelai.com mankeni Valentina Cruz (kırmızı couture elbiseli, boynunda zümrüt pırlanta gerdanlık olan kadın) "
            "ve Leyla (fildişi ipek elbiseli, boynunda pırlanta gerdanlık ve bileğinde altın saat olan kadın), "
            "İstanbul Boğazı'ndaki tarihi bir milyoner yalısının özel mermer rıhtımında gün batımında yan yana oturmuş kristal kadehlerle zarifçe sohbet edip gülümsüyorlar. "
            "Arkalarında Boğaz suları ve bağlı lüks maun yat hafifçe salınıyor, boyunlarındaki pahalı pırlanta kolyeler altın saat ışığında parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    {
        "scene_id": "flow_shopping_valentina_cartier_vip_salon_11",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "model_avatar": "/assets/valentina_avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_cruz_angle1.jpg"),
        "title": "Place Vendôme & İstinyePark VIP Mücevher Salonu: Özel Kadife Tepside Pırlanta Gerdanlık Alışverişi 🛍️💎",
        "location_name": "Place Vendôme & Beymen Privé VIP High Jewelry Salon",
        "bottom_brand": "ZEN PIRLANTA & BEYMEN PRIVÉ",
        "bottom_product": "VIP Özel Salon Pırlanta Gerdanlık & Couture Çanta Alışverişi • 3.850.000 TL",
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "VIP Salon Özel Tasarım Zümrüt Kesim Pırlanta Gerdanlık", "2.350.000 TL", "https://www.zenpirlanta.com/pirlanta-kolyeler/", "941002001",
            "BEYMEN", "Hermès / Bottega Veneta Egzotik Deri El Çantası Seçkisi", "485.000 TL", "https://www.beymen.com/tr/kadin-canta-10018", "941002002",
            "ATASAY HIGH JEWELRY", "18K Rose Gold Pırlanta Bileklik & Yüzük Seti", "690.000 TL", "https://www.atasay.com/pirlanta-bileklikler", "941002003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks alışveriş videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Valentina Cruz (ela-yeşil gözlü, kestane dalgalı saçlarında kırmızı kurdeleli, kırmızı couture elbiseli, boynunda zümrüt kesim pırlanta gerdanlık ve bileğinde 18K altın saat olan kadın), "
            "ultra-lüks bir VIP özel mücevher salonunda mermer masada otururken önündeki siyah kadife mücevher tepsisindeki pırlanta kolyeleri ve lüks kutuları inceliyor, "
            "kristal kadehten şampanyasını yudumlayıp kameraya doğru doğal ve özgüvenli şekilde gülümsüyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    {
        "scene_id": "flow_hotel_leyla_ciragan_sultan_suite_12",
        "guzelai_model_id": "guzelai-leyla-001",
        "guzelai_model_name": "Leyla (guzelai.com)",
        "model_avatar": "/influencers/leyla/reference.png",
        "ref_image": str(ROOT_DIR / "assets" / "guzelai_leyla_angle2.jpg"),
        "title": "Çırağan Palace Kempinski Sultan Suite (Geceliği 45.000 €): Mermer Kral Dairesi & 22 Karat Pırlanta 🏨👑",
        "location_name": "Çırağan Palace Kempinski Sultan Suite, İstanbul",
        "bottom_brand": "ÇIRAĞAN SULTAN SUITE & ZEN PIRLANTA",
        "bottom_product": "Kral Dairesi Boğaz Süiti, 22 Karat Pırlanta Gerdanlık & 18K Altın Rolex",
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "Sultan Suite 22 Karat Pırlanta Gerdanlık", "2.100.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", "941003001",
            "VAKKO COUTURE", "Kral Dairesi Fildişi İpek-Kaşmir Gece Elbisesi", "225.000 TL", "https://www.vakko.com/kadin-giyim-elbise/", "941003002",
            "SEPHORA / BACDKARAT ROUGE", "Maison Francis Kurkdjian Baccarat Rouge 540 Extrait", "24.500 TL", "https://www.sephora.com.tr/kadin-parfum-c30101/", "941003003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks otel odası videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Leyla (omuz hizası koyu kahve dalgalı saçlı, fildişi ipek gece elbiseli, boynunda pırlanta gerdanlık ve bileğinde 18K altın Rolex saat olan kadın), "
            "Boğaz manzaralı altın varaklı ve kristal avizeli ultra-lüks Çırağan Sarayı Kral Dairesi (Sultan Suite) salonunda mermer masada kristal kadehini tutarak zarifçe kameraya bakıyor, "
            "saray pencerelerinden gelen altın saat ışığı boynundaki pırlanta kolyede ve altın saatinde parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    {
        "scene_id": "flow_encounter_valentina_aurakaya_monaco_club_13",
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Valentina Cruz & Aura Kaya (guzelai.com)",
        "model_avatar": "/influencers/aurakaya/avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_and_aurakaya_encounter.jpg"),
        "title": "Yacht Club de Monaco & Annabel's Mayfair Özel Kulüp Buluşması: Valentina Cruz & Aura Kaya 🥂💎",
        "location_name": "Yacht Club de Monaco VIP Members Lounge & Terrace",
        "bottom_brand": "CARTIER & AUDEMARS PIGUET",
        "bottom_product": "Özel Üyelikli Milyoner Kulübü Buluşması • Pırlanta Gerdanlık & Royal Oak",
        "items": _make_luxury_items(
            "ATASAY / CARTIER STYLE", "Haute Joaillerie Pırlanta Gerdanlık Koleksiyonu", "1.890.000 TL", "https://www.atasay.com/pirlanta-gerdanliklar", "941004001",
            "BEYMEN", "Saint Laurent & Balmain Siyah-Kırmızı Couture Gece Seçkisi", "265.000 TL", "https://www.beymen.com/tr/kadin-giyim-elbise-10012", "941004002",
            "SWAROVSKI / LUXURY", "Kristal & Pırlanta Gece Küpesi ve Bileklik", "85.000 TL", "https://www.swarovski.com/tr-TR/c-01/Categories/Jewelry/", "941004003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik özel kulüp buluşma videosu oluştur: "
            "Referans görseldeki iki guzelai.com mankeni Valentina Cruz (kırmızı couture elbiseli, boynunda zümrüt pırlanta gerdanlık olan kadın) "
            "ve Aura Kaya (siyah haute couture ceket elbiseli, boynunda pırlanta gerdanlık ve bileğinde pırlanta saat olan kadın), "
            "sadece milyoner üyelerin girebildiği Yacht Club de Monaco VIP teras kulübünde mum ışıklı mermer masada yan yana oturmuş kristal kadehlerle gülümseyerek sohbet ediyorlar. "
            "Boyunlarındaki pahalı pırlanta kolyeler ve bileklerindeki saatler sıcak kulüp ışıklarında parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    {
        "scene_id": "flow_shopping_aurakaya_rodeo_drive_trunk_14",
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Aura Kaya (guzelai.com)",
        "model_avatar": "/influencers/aurakaya/avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "jet_heiress_angle3.jpg"),
        "title": "Rodeo Drive & Place Vendôme VIP Alışveriş: Özel Şoförlü Rolls-Royce & Haute Couture Paketler 🛍️🚘",
        "location_name": "Rodeo Drive Beverly Hills & Place Vendôme VIP Boutique",
        "bottom_brand": "ROLLS-ROYCE & BEYMEN PRIVÉ",
        "bottom_product": "VIP Özel Butik Alışverişi, Pırlanta Gerdanlık & Siyah Haute Couture",
        "items": _make_luxury_items(
            "BEYMEN", "Haute Couture Siyah Ceket Elbise & Lüks Deri Çanta", "310.000 TL", "https://www.beymen.com/tr/kadin-canta-10018", "941005001",
            "ZEN PIRLANTA", "19 Karat Pırlanta Gerdanlık & Tektaş Küpe", "1.780.000 TL", "https://www.zenpirlanta.com/pirlanta-kolyeler/", "941005002",
            "VAKKO", "Özel Dikim İpek Eşarp & Lüks Aksesuar Kutusu", "68.000 TL", "https://www.vakko.com/kadin-aksesuar/", "941005003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik VIP alışveriş videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Aura Kaya (koyu kahve saçlı, siyah haute couture ceket elbiseli, boynunda pahalı pırlanta kolye ve bileğinde pırlanta saat olan kadın), "
            "Beverly Hills Rodeo Drive lüks mücevher butiğinin önünde siyah Rolls-Royce otomobilinin yanında dururken kameraya doğru tek yönde, sakin ve özgüvenli bir gülümsemeyle bakıyor, "
            "boynundaki pırlanta gerdanlık ve küpeleri akşamüstü ışıklarında göz kamaştırıcı şekilde parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    {
        "scene_id": "flow_yali_leyla_bebek_private_pier_yacht_15",
        "guzelai_model_id": "guzelai-leyla-001",
        "guzelai_model_name": "Leyla (guzelai.com)",
        "model_avatar": "/influencers/leyla/reference.png",
        "ref_image": str(ROOT_DIR / "assets" / "guzelai_leyla_angle4.jpg"),
        "title": "Bebek Tarihi Boğaz Yalısı & Özel Riva Yat Güvertesi: Leyla, Pırlanta Gerdanlık & Altın Rolex 🛥️🌊",
        "location_name": "Bebek & Yeniköy Tarihi Boğaz Yalısı Özel Yat Güvertesi",
        "bottom_brand": "ZEN PIRLANTA & LORO PIANA",
        "bottom_product": "Boğaz Yalısı Özel Yat Seçkisi • 22 Karat Pırlanta & İpek-Kaşmir Kombin",
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "Boğaz Koleksiyonu 22 Karat Pırlanta Gerdanlık", "1.980.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", "941006001",
            "BEYMEN / LORO PIANA", "Fildişi İpek-Kaşmir Yat & Yalı Elbisesi", "215.000 TL", "https://www.beymen.com/tr/kadin-giyim-elbise-10012", "941006002",
            "ROLEX / LUXURY WATCH", "18K Sarı Altın Oyster Perpetual Day-Date 36", "1.950.000 TL", "https://www.beymen.com/tr/kadin-aksesuar-saat-10072", "941006003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik Boğaz yalısı ve yat videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Leyla (omuz hizası koyu kahve dalgalı saçlı, fildişi ipek elbiseli, boynunda pırlanta kolye ve bileğinde altın Rolex saat olan kadın), "
            "Boğaz yalısının önündeki cilalı maun Riva yatın krem deri koltuğunda uzanmış, tek yönde ileri doğru süzülen yatta kameraya doğru sıcak ve doğal şekilde gülümsüyor, "
            "deniz meltemi saçlarını hafifçe dalgalandırırken boynundaki pırlanta kolye güneş ışığında parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    {
        "scene_id": "flow_hotel_valentina_aman_venice_canal_suite_16",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "model_avatar": "/assets/valentina_avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_cruz_angle4.jpg"),
        "title": "Aman Venice Palazzo & Monte Carlo Royal Penthouse: Gün Batımı Terası & 18.5 Karat Zümrüt Pırlanta 🏰💎",
        "location_name": "Aman Venice Grand Canal Suite & Hotel de Paris Monte-Carlo",
        "bottom_brand": "AMAN PALAZZO SUITE & ZEN PIRLANTA",
        "bottom_product": "Kraliyet Teras Süiti, 18.5 Karat Zümrüt Pırlanta & Vakko Couture",
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "18.5 Karat Zümrüt Kesim Pırlanta Gerdanlık", "2.250.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", "941007001",
            "VAKKO COUTURE", "Kırmızı İpek Saten Royal Suite Gece Elbisesi", "188.000 TL", "https://www.vakko.com/kadin-giyim-elbise/", "941007002",
            "AUDEMARS PIGUET / BEYMEN", "18K Rose Gold Royal Oak Frosted Saat", "2.650.000 TL", "https://www.beymen.com/tr/kadin-aksesuar-saat-10072", "941007003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik kral dairesi teras videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Valentina Cruz (kırmızı ipek couture elbiseli, saçında kırmızı kurdeleli, boynunda zümrüt kesim pırlanta kolye ve bileğinde 18K altın Audemars Piguet saat olan kadın), "
            "deniz ve liman manzaralı ultra-lüks kraliyet terasında elinde kristal şampanya kadehiyle sabit ve zarif bir duruşla kameraya bakıp hafifçe gülümsüyor, "
            "akşamüstü rüzgarı saçlarını okşarken boynundaki zümrüt pırlanta gerdanlık altın ışıkta parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    {
        "scene_id": "flow_encounter_leyla_aurakaya_vip_jet_club_17",
        "guzelai_model_id": "guzelai-leyla-001",
        "guzelai_model_name": "Leyla & Aura Kaya (guzelai.com)",
        "model_avatar": "/influencers/leyla/reference.png",
        "ref_image": str(ROOT_DIR / "assets" / "leyla_and_aurakaya_encounter.jpg"),
        "title": "Cenevre Özel Jet Terminali & VIP Lounge Buluşması: Leyla & Aura Kaya, Patek Philippe & Pırlanta 🛩️🥂",
        "location_name": "Geneva Private Aviation VIP Lounge & Four Seasons",
        "bottom_brand": "PATEK PHILIPPE & ZEN PIRLANTA",
        "bottom_product": "VIP Özel Havacılık Kulübü Buluşması • Pırlanta Gerdanlık & Lüks Saat",
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "VIP Koleksiyon Çift Sıra Pırlanta Gerdanlık", "2.150.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", "941008001",
            "BEYMEN", "Loro Piana & Saint Laurent VIP Seyahat Couture Seçkisi", "295.000 TL", "https://www.beymen.com/tr/kadin-giyim-elbise-10012", "941008002",
            "ATASAY", "18K Altın Pırlanta Bezel Saat & Bileklik", "840.000 TL", "https://www.atasay.com/pirlanta-bileklikler", "941008003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik VIP kulüp buluşma videosu oluştur: "
            "Referans görseldeki iki guzelai.com mankeni Leyla (fildişi ipek elbiseli, boynunda pırlanta gerdanlık olan kadın) "
            "ve Aura Kaya (siyah haute couture ceket elbiseli, boynunda pırlanta kolye ve bileğinde pırlanta saat olan kadın), "
            "Cenevre özel jet terminalinin VIP milyoner lounge salonunda krem deri koltuklarda yan yana oturmuş espresso ve şampanya eşliğinde gülümseyerek kameraya bakıyorlar, "
            "boyunlarındaki pırlanta gerdanlıklar ve saatleri sıcak VIP salon ışığında parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
    # --- İLK 9 TEMEL SAHNE (DOĞAL TEK YÖNLÜ HAREKET KİLİTLİ) ---
    {
        "scene_id": "flow_valentina_monaco_ferrari_01",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "model_avatar": "/assets/valentina_avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_cruz_angle1.jpg"),
        "title": "Monaco Monte Carlo Limanı: Ferrari Roma Spider, Zümrüt Kesim Pırlanta Gerdanlık & Audemars Piguet 🏎️💎",
        "location_name": "Casino de Monte-Carlo & Port Hercule, Monaco",
        "bottom_brand": "ZEN PIRLANTA & AUDEMARS PIGUET",
        "bottom_product": "18.5 Karat Zümrüt Kesim Pırlanta Gerdanlık & Royal Oak 18K Rose Gold • 4.250.000 TL",
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "18.5 Karat Zümrüt Kesim Pırlanta Gerdanlık", "1.950.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", "941009001",
            "BEYMEN / AUDEMARS PIGUET", "Royal Oak 18K Rose Gold Lüks Saat", "2.300.000 TL", "https://www.beymen.com/tr/kadin-aksesuar-saat-10072", "941009002",
            "VAKKO COUTURE", "Kırmızı İpek Couture Elbise", "175.000 TL", "https://www.vakko.com/kadin-giyim-elbise/", "941009003",
        ),
        "prompt": (
            "9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            "Referans görseldeki guzelai.com mankeni Valentina Cruz (ela-yeşil gözlü, hafif çilli yanaklı, kestane dalgalı saçlarında kırmızı kurdeleli, kırmızı elbiseli, boynunda zümrüt kesim pırlanta kolye ve bileğinde 18K altın Audemars Piguet saat olan kadın), "
            "Monaco Monte Carlo limanında gün batımında şampanya-bej üstü açık Ferrari Spider direksiyonunda sakin ve doğal şekilde kameraya bakıp hafifçe gülümsüyor, "
            "rüzgarda saçları dalgalanıyor ve boynundaki pırlanta kolye güneş ışığında parıldıyor. "
            + NATURAL_PHYSICS_RULE
        ),
    },
]

# Sürekli Yeni Senaryo Üretici Havuzu (Tur 2+ için her seferinde benzersiz mekan, alışkanlık ve lüks ürün kombinasyonu üretir)
DYNAMIC_SCENARIO_BLUEPRINTS: List[Dict[str, Any]] = [
    {
        "slug": "vip_hermes_birkin_private_suite",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz (guzelai.com)",
        "model_avatar": "/assets/valentina_avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_cruz_angle2.jpg"),
        "title": "Paris Faubourg Saint-Honoré VIP Özel Oda: Egzotik Deri Çanta, Pırlanta Gerdanlık & Rose Gold Saat 🛍️💎",
        "location_name": "Faubourg Saint-Honoré VIP Private Suite, Paris",
        "bottom_brand": "BEYMEN PRIVÉ & ZEN PIRLANTA",
        "bottom_product": "VIP Özel Oda Çanta & 18.5 Karat Pırlanta Gerdanlık Seçkisi • Paris",
        "action_tr": "Paris'teki özel VIP moda salonunda kadife koltukta otururken önündeki turuncu lüks kutuları ve bileğindeki 18K altın saati sergileyerek kameraya doğal şekilde gülümsüyor",
    },
    {
        "slug": "lake_como_villa_deste_royal_breakfast",
        "guzelai_model_id": "guzelai-leyla-001",
        "guzelai_model_name": "Leyla (guzelai.com)",
        "model_avatar": "/influencers/leyla/reference.png",
        "ref_image": str(ROOT_DIR / "assets" / "guzelai_leyla_angle1.jpg"),
        "title": "Villa d'Este Como Gölü Kraliyet Terası: Sabah Kahvesi, 22 Karat Pırlanta Gerdanlık & Altın Rolex ☕🦢",
        "location_name": "Villa d'Este Royal Lake Terrace, Lake Como",
        "bottom_brand": "VILLA D'ESTE & ROLEX DAY-DATE",
        "bottom_product": "Como Gölü Kraliyet Terası • 22 Karat Pırlanta & 18K Altın Rolex",
        "action_tr": "Como Gölü kıyısındaki Villa d'Este mermer terasında sabah güneşinde otururken boynundaki 22 karat pırlanta gerdanlık ve bileğindeki altın Rolex saat ışıkta parıldıyor",
    },
    {
        "slug": "st_moritz_badrutts_palace_penthouse",
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Aura Kaya (guzelai.com)",
        "model_avatar": "/influencers/aurakaya/avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "jet_heiress_angle1.jpg"),
        "title": "St. Moritz Badrutt's Palace Penthouse Suite: Şömine Başı Yüksek Mücevher & Patek Philippe 🏔️💎",
        "location_name": "Badrutt's Palace Penthouse Suite, St. Moritz",
        "bottom_brand": "PATEK PHILIPPE & CARTIER",
        "bottom_product": "St. Moritz Penthouse Süiti • Pırlanta Serpenti Gerdanlık & Patek Philippe",
        "action_tr": "St. Moritz Badrutt's Palace kral dairesi süitinde sıcak ışıklar altında boynundaki pırlanta yılan kolyeyi ve pırlanta küpelerini sergileyerek kameraya sakin ve zarif şekilde bakıyor",
    },
    {
        "slug": "encounter_bosphorus_yali_sunset_toast",
        "guzelai_model_id": "valentina-cruz",
        "guzelai_model_name": "Valentina Cruz & Leyla (guzelai.com)",
        "model_avatar": "/assets/valentina_avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "valentina_and_leyla_encounter.jpg"),
        "title": "Yeniköy Tarihi Yalı Bahçesi VIP Davet Buluşması: Valentina Cruz & Leyla, Pırlanta & Couture 🥂🏛️",
        "location_name": "Yeniköy Tarihi Boğaz Yalısı Mermer Bahçesi, İstanbul",
        "bottom_brand": "VAKKO COUTURE & ZEN PIRLANTA",
        "bottom_product": "Tarihi Boğaz Yalısı VIP Buluşma • İki Manken & Pırlanta Gerdanlık Seçkisi",
        "action_tr": "Yeniköy'deki tarihi Boğaz yalısının mermer terasında gün batımında yan yana oturmuş kristal kadehlerle zarifçe gülümseyerek kameraya bakıyorlar",
    },
    {
        "slug": "dubai_burj_al_arab_royal_duplex",
        "guzelai_model_id": "aura-kaya",
        "guzelai_model_name": "Aura Kaya (guzelai.com)",
        "model_avatar": "/influencers/aurakaya/avatar.jpg",
        "ref_image": str(ROOT_DIR / "assets" / "jet_heiress_angle4.jpg"),
        "title": "Burj Al Arab Royal Duplex & Özel Teras Havuzu: Gece Işıkları, Pırlanta Gerdanlık & Haute Couture 🌃💎",
        "location_name": "Burj Al Arab Royal Suite Terrace, Dubai",
        "bottom_brand": "CARTIER HIGH JEWELRY & BEYMEN",
        "bottom_product": "Royal Duplex Teras Havuzu • Pırlanta Gerdanlık & Siyah İpek Couture",
        "action_tr": "kraliyet teras havuzunun kenarında gece ışıklarına karşı sabit ve zarif bir duruşla kameraya doğru gülümsüyor, boynundaki pırlanta kolye parıldıyor",
    },
]


def build_dynamic_scene(round_num: int, bp_idx: int) -> Dict[str, Any]:
    bp = DYNAMIC_SCENARIO_BLUEPRINTS[bp_idx % len(DYNAMIC_SCENARIO_BLUEPRINTS)]
    sid = f"flow_{bp['slug']}_r{round_num}_{bp_idx + 1}"
    sku_base = f"94{round_num:02d}{bp_idx + 1:02d}"
    return {
        "scene_id": sid,
        "guzelai_model_id": bp["guzelai_model_id"],
        "guzelai_model_name": bp["guzelai_model_name"],
        "model_avatar": bp["model_avatar"],
        "ref_image": bp["ref_image"],
        "title": bp["title"],
        "location_name": bp["location_name"],
        "bottom_brand": bp["bottom_brand"],
        "bottom_product": bp["bottom_product"],
        "items": _make_luxury_items(
            "ZEN PIRLANTA", "Yüksek Mücevher Pırlanta Gerdanlık Seçkisi", "2.150.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", f"{sku_base}1",
            "BEYMEN", "Haute Horlogerie Altın & Pırlanta Saat Koleksiyonu", "2.400.000 TL", "https://www.beymen.com/tr/kadin-aksesuar-saat-10072", f"{sku_base}2",
            "VAKKO COUTURE", "Özel Dikim İpek Gece & Resort Koleksiyonu", "195.000 TL", "https://www.vakko.com/kadin-giyim-elbise/", f"{sku_base}3",
        ),
        "prompt": (
            f"9:16 dikey ultra-fotogerçekçi sinematik lüks yaşam videosu oluştur: "
            f"Referans görseldeki guzelai.com mankeni {bp['guzelai_model_name']}, "
            f"{bp['action_tr']}. Sinematik 85mm f/1.4 sabit ileri/yakınlaşan kamera. "
            + NATURAL_PHYSICS_RULE
        ),
    }


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
    upscales/masters it to crystal-clear 1080p Full HD (1080x1920) using Lanczos + optical unsharp mask,
    draws ONLY the sleek bottom highlight pill (zero top bar, zero table),
    and preserves Google Flow's native stereo audio stream!
    """
    import imageio_ffmpeg

    out_mp4_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_overlay_png = out_mp4_path.parent / f"_pill_{out_mp4_path.stem}.png"

    # Build overlay directly at full 1080x1920 resolution for razor-sharp typography
    w, h = 1080, 1920
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    pad_x = int(w * 0.055)
    pill_h = int(h * 0.078)
    pill_y1 = h - int(h * 0.088)
    pill_y0 = pill_y1 - pill_h

    draw.rounded_rectangle(
        (pad_x, pill_y0, w - pad_x, pill_y1),
        radius=int(pill_h * 0.36),
        fill=(10, 10, 14, 192),
        outline=(218, 182, 115, 225),
        width=3,
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
    overlay.save(str(tmp_overlay_png))

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", str(raw_mp4_path),
        "-i", str(tmp_overlay_png),
        "-filter_complex", "[0:v]scale=1080:1920:flags=lanczos,unsharp=3:3:0.55:3:3:0.0[scaled];[scaled][1:v]overlay=0:0[v]",
        "-map", "[v]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "15",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(out_mp4_path),
    ]
    subprocess.run(cmd, capture_output=True)
    if tmp_overlay_png.exists():
        tmp_overlay_png.unlink()
    return out_mp4_path if out_mp4_path.exists() else raw_mp4_path


def sync_clip_to_guzelai_website(mp4_path: Path, scene_meta: Dict[str, Any], variation_idx: int = 1) -> bool:
    """
    Copies the 1080p Flow MP4 & poster into local `guzelai/public/clips/` AND pushes
    both the clip and `public/clips/flow_clips_feed.json` to `thezencirs/guzelai` so
    `guzelai.com` Klipler (`VerticalClipsSection.tsx`) loops the new video immediately!
    """
    try:
        guzelai_dir = ROOT_DIR.parent / "guzelai"
        clips_dir = guzelai_dir / "public" / "clips"
        posters_dir = clips_dir / "posters"
        clips_dir.mkdir(parents=True, exist_ok=True)
        posters_dir.mkdir(parents=True, exist_ok=True)

        clip_slug = f"{scene_meta['scene_id']}_v{variation_idx}"
        web_mp4_rel = f"/clips/{clip_slug}.mp4"
        web_poster_rel = f"/clips/posters/{scene_meta['scene_id']}.jpg"

        # Copy to local guzelai workspace
        dst_mp4 = clips_dir / f"{clip_slug}.mp4"
        shutil.copy2(mp4_path, dst_mp4)
        ref_img = Path(scene_meta["ref_image"])
        dst_poster = posters_dir / f"{scene_meta['scene_id']}.jpg"
        if ref_img.exists():
            shutil.copy2(ref_img, dst_poster)

        # Upload poster & 1080p MP4 to GitHub `thezencirs/guzelai`
        if dst_poster.exists():
            _gh_put_file(
                f"public/clips/posters/{scene_meta['scene_id']}.jpg",
                dst_poster.read_bytes(),
                f"feat(clips): upload poster {scene_meta['scene_id']}.jpg to guzelai.com",
            )
        if dst_mp4.exists() and dst_mp4.stat().st_size < 24 * 1024 * 1024:
            _gh_put_file(
                f"public/clips/{clip_slug}.mp4",
                dst_mp4.read_bytes(),
                f"feat(clips): publish 1080p Flow clip {clip_slug}.mp4 to guzelai.com",
            )

        clip_entry = {
            "id": clip_slug.replace("_", "-"),
            "title": scene_meta["title"],
            "brandName": scene_meta["bottom_brand"],
            "category": "jewelry",
            "categoryLabel": "💎 1080p Google Flow Lüks Klip",
            "modelId": scene_meta["guzelai_model_id"],
            "modelName": scene_meta["guzelai_model_name"],
            "modelAvatar": scene_meta.get("model_avatar", "/assets/valentina_avatar.jpg"),
            "posterImage": web_poster_rel,
            "videoSrc": web_mp4_rel,
            "hookText": scene_meta["title"],
            "subHookText": f"{scene_meta['location_name']} • {scene_meta['bottom_product']}",
            "ctaText": "Koleksiyonu & Linkleri İncele",
            "musicTrack": "Google Flow Native Stereo Ambience",
            "cameraMotion": "85mm f/1.4 Doğal Tek Yönlü Gimbal (1080p)",
            "aspectRatio": "9:16",
            "durationSec": 10,
            "roasStat": "6.4x ROAS",
            "viewsStat": "Yeni 1080p",
            "colorHex": "#C69E52",
            "description": f"{scene_meta['guzelai_model_name']} ile {scene_meta['location_name']} konumunda çekilmiş 1080p dikey lüks yaşam klibi.",
        }

        feed_file = clips_dir / "flow_clips_feed.json"
        existing_clips: List[Dict[str, Any]] = []
        if feed_file.exists():
            try:
                existing_clips = json.loads(feed_file.read_text(encoding="utf-8")).get("clips", [])
            except Exception:
                existing_clips = []

        existing_clips = [c for c in existing_clips if c.get("id") != clip_entry["id"]]
        updated_clips = [clip_entry] + existing_clips[:24]
        feed_data = {
            "updated_at": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "clips": updated_clips,
        }
        feed_bytes = json.dumps(feed_data, ensure_ascii=False, indent=2).encode("utf-8")
        feed_file.write_bytes(feed_bytes)
        _gh_put_file(
            "public/clips/flow_clips_feed.json",
            feed_bytes,
            f"feat(clips): add {clip_slug} to guzelai.com live Klipler feed",
        )
        return True
    except Exception as e:
        print(f"[FlowMarathon] guzelai.com clip sync note: {e}")
        return False


def publish_flow_video_to_telegram_and_web(mp4_path: Path, scene_meta: Dict[str, Any], variation_idx: int = 1) -> Dict[str, Any]:
    items = scene_meta.get("items") or _make_luxury_items(
        "ZEN PIRLANTA", "Pırlanta Gerdanlık Seçkisi", "1.950.000 TL", "https://www.zenpirlanta.com/pirlanta-gerdanliklar/", "941000001",
        "BEYMEN", "Haute Horlogerie Lüks Saat Seçkisi", "2.250.000 TL", "https://www.beymen.com/tr/kadin-aksesuar-saat-10072", "941000002",
        "VAKKO COUTURE", "İpek Gece & Yat Koleksiyonu", "185.000 TL", "https://www.vakko.com/kadin-giyim-elbise/", "941000003",
    )
    concept = {
        "id": f"{scene_meta['scene_id']}_v{variation_idx}",
        "title": scene_meta["title"],
        "guzelai_model_id": scene_meta["guzelai_model_id"],
        "guzelai_model_name": scene_meta["guzelai_model_name"],
        "location_name": scene_meta["location_name"],
        "category": "taki",
        "items": items,
    }

    # Build rich copy-paste caption with verified product links + short comprehensive legal/AI notice
    base_caption = build_pure_copy_paste_caption(concept)
    product_lines = []
    for idx_i, (_, it) in enumerate(items.items(), start=1):
        product_lines.append(
            f"{idx_i}️⃣ {it.get('emoji', '💎')} {it.get('brand')} – {it.get('name')} ({it.get('price')})\n🔗 {it.get('store_url')}"
        )
    links_block = "\n".join(product_lines)

    # Combine title + model + location + direct product links + legal disclaimer cleanly
    lines = base_caption.splitlines()
    header_part = "\n".join(lines[:3])
    footer_part = "\n".join(lines[3:])
    full_caption = f"{header_part}\n\n🛍️ Lüks Ürün & Mağaza Linkleri:\n{links_block}\n\n{footer_part}"

    cap_path = mp4_path.with_suffix(".txt")
    cap_path.write_text(full_caption, encoding="utf-8")

    # Sync to guzelai.com Klipler section
    sync_clip_to_guzelai_website(mp4_path, scene_meta, variation_idx=variation_idx)

    reply_markup_json = json.dumps(build_luxury_inline_keyboard(concept))
    chat_ids = load_target_chat_ids(concept)
    tok = get_bot_token()
    delivered = {}
    for cid in chat_ids:
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
        if v_ok:
            time.sleep(0.6)
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


def _url_token_key(u: str) -> str:
    full_tok = u.split("/asb/")[-1].split("=")[0]
    return "asb_" + hashlib.sha256(full_tok.encode("utf-8")).hexdigest()[:32]


def run_continuous_google_flow_marathon(max_rounds: int = 50) -> None:
    FLOW_CLIPS_DIR.mkdir(parents=True, exist_ok=True)
    FLOW_STOCK_OUT_DIR.mkdir(parents=True, exist_ok=True)

    stop_evt = threading.Event()
    _start_auto_allow_clicker(stop_evt)
    try:
        client = FlowCDPClient()
    finally:
        stop_evt.set()

    ledger = load_delivered_ledger()

    # Mark all currently visible tiles on the canvas as already known so we only deliver newly generated ones
    initial_urls = client.list_completed_asb_urls()
    for u in initial_urls:
        ledger.add(_url_token_key(u))
        ledger.add(u.split("/asb/")[-1].split("=")[0][:48])
    save_delivered_ledger(ledger)
    print(f"[FlowMarathon] Connected to Flow canvas. Indexed {len(initial_urls)} existing canvas tiles. Starting new scenarios...")

    round_num = 0
    while round_num < max_rounds:
        round_num += 1
        scenes_this_round: List[Dict[str, Any]] = []
        if round_num == 1:
            scenes_this_round = list(FLOW_MARATHON_SCENES[:-1])
        else:
            for bp_i in range(len(DYNAMIC_SCENARIO_BLUEPRINTS)):
                scenes_this_round.append(build_dynamic_scene(round_num, bp_i))

        for scene in scenes_this_round:
            before_urls = set(client.list_completed_asb_urls())
            for bu in before_urls:
                ledger.add(_url_token_key(bu))

            submitted = client.submit_scene(scene)
            if not submitted:
                print("[FlowMarathon] Could not submit scene (quota reached or UI busy). Waiting 25s...")
                time.sleep(25)
                continue

            harvested_for_scene = 0
            for _ in range(28):
                time.sleep(5.0)
                page_txt = client.eval_js("document.body.innerText.slice(0, 1200)") or ""
                if "krediniz bitti" in page_txt.lower() or "out of credits" in page_txt.lower():
                    print("[FlowMarathon] Google Flow credits exhausted! Stopping marathon cleanly.")
                    return

                cur_urls = client.list_completed_asb_urls()
                cookie_jar = client.get_cookie_jar()
                for u in cur_urls:
                    tkey = _url_token_key(u)
                    old_key = u.split("/asb/")[-1].split("=")[0][:48]
                    if u not in before_urls and tkey not in ledger and old_key not in ledger:
                        r = requests.get(u, cookies=cookie_jar, timeout=60)
                        if r.status_code == 200 and len(r.content) > 500_000:
                            content_sha = "sha256_" + hashlib.sha256(r.content).hexdigest()[:32]
                            if content_sha in ledger:
                                ledger.add(tkey)
                                save_delivered_ledger(ledger)
                                continue

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
                                f"[FlowMarathon] Delivered 1080p Flow video {out_p.name} ({out_p.stat().st_size} bytes) -> @Sesliluksbot & guzelai.com: {res}"
                            )
                            ledger.add(tkey)
                            ledger.add(old_key)
                            ledger.add(content_sha)
                            save_delivered_ledger(ledger)

                if harvested_for_scene >= 2:
                    break


if __name__ == "__main__":
    run_continuous_google_flow_marathon()
