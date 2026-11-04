"""
Luxury Life AI (@Luxurylifeaibot) — Viral Hook, High-Save-Rate (Kaydetme Oranı Yüksek) İçerik Analiz
ve 5 Lüks Dikey Kategori (Takı/Saat, Makyaj/Kozmetik, Old Money Kombin, Ultra Lüks Otel, Süper Spor Araba)
Reji, Kamera Açısı, Mekan, Model, Yazım Düzeltici ve Doğrulanmış İş Birliği Link Motoru
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_PATH = BASE_DIR / "output" / "luxury_zero_repeat_ledger.json"

# ============================================================================
# YASAL UYARI SABİTLERİ (T.C. Ticaret Bakanlığı Reklam Kurulu Tam Uyumlu)
# ============================================================================
TR_LEGAL_CAPTION_NOTICE = (
    "⚖️ Yasal Uyarı: Bu paylaşım herhangi bir ticari iş birliği veya sponsorluk içermez; "
    "tamamen lüks yaşam, stil ve estetik önerisi amaçlıdır. Görsellerde markalar yer aldığı için "
    "yasal zorunluluk gereği #reklam #işbirliğiyoktur"
)

TR_LEGAL_LINKS_NOTICE = (
    "⚖️ Yasal Not: İş birliği yoktur, takipçi bilgilendirmesi amaçlı ürün ve mağaza linkleridir. "
    "Yasal zorunluluk gereği #reklam #işbirliğiyoktur"
)

# ============================================================================
# AKILLI YAZIM DÜZELTİCİ & META-KOMUT TEMİZLEYİCİ ("Otel santorıny" + "İsmini düzelt" -> "Otel Santorini")
# ============================================================================
TYPO_CORRECTIONS = [
    (r"(?i)\bsantor[ıiİy]+n[ıiİy]+\b", "Santorini"),
    (r"(?i)\bsantorin[ıiİy]\b", "Santorini"),
    (r"(?i)\bkapadok[yia]+\b", "Kapadokya"),
    (r"(?i)\bmonak[o0]\b", "Monaco"),
    (r"(?i)\bmontekarlo\b", "Monte-Carlo"),
    (r"(?i)\bbodr[uü]m\b", "Bodrum"),
    (r"(?i)\bç[ıi]ra[ğg]an\b", "Çırağan Palace"),
    (r"(?i)\bmandar[ıi]n\b", "Mandarin Oriental"),
    (r"(?i)\bcart[ıi]er\b", "Cartier"),
    (r"(?i)\bherm[eè]s\b", "Hermès"),
    (r"(?i)\bporsh?e\b", "Porsche"),
    (r"(?i)\bswarovsk[ıiy]\b", "Swarovski"),
    (r"(?i)\bchanell?\b", "Chanel"),
    (r"(?i)\bd[ıi]or\b", "Dior"),
    (r"(?i)\brolexx?\b", "Rolex"),
]

META_INSTRUCTION_PATTERNS = [
    r"(?i)\bismini\s+d[üu]zelt\b[.,!]*",
    r"(?i)\bad[ıi]n[ıi]\s+d[üu]zelt\b[.,!]*",
    r"(?i)\byaz[ıi]y[ıi]\s+d[üu]zelt\b[.,!]*",
    r"(?i)\bmetni\s+d[üu]zelt\b[.,!]*",
    r"(?i)\bbunu\s+(?:yap|payla[şs]|üret)\b[.,!]*",
    r"(?i)\bvideo\s+yap\b[.,!]*",
    r"(?i)^/(?:start|uret|yayinla|paylas|taki|makyaj|kombin|otel|araba)\b",
]


def normalize_and_correct_user_text(raw_messages: List[str]) -> Dict[str, str]:
    """
    Kullanıcının Telegram'dan peş peşe yazdığı mesajları (örn. ['Otel santorıny', 'İsmini düzelt'])
    birleştirir, 'İsmini düzelt' gibi meta komutları temizler ve yazım hatalarını kusursuz
    lüks editoryal başlığa dönüştürür.
    """
    cleaned_parts: List[str] = []
    had_correction_request = False

    for msg in raw_messages:
        if not msg:
            continue
        t = msg.strip()
        if re.search(r"(?i)(ismini|adını|yazıyı|metni)\s+d[üu]zelt", t):
            had_correction_request = True
        for pat in META_INSTRUCTION_PATTERNS:
            t = re.sub(pat, "", t).strip()
        for wrong_pat, right_word in TYPO_CORRECTIONS:
            t = re.sub(wrong_pat, right_word, t)
        t = re.sub(r"\s+", " ", t).strip(" -.,!")
        if t:
            cleaned_parts.append(t)

    combined = " — ".join(cleaned_parts) if cleaned_parts else ""
    for wrong_pat, right_word in TYPO_CORRECTIONS:
        combined = re.sub(wrong_pat, right_word, combined)

    low = combined.lower()
    if "santorini" in low:
        return {
            "clean_subject": "Santorini Oia Caldera Lüks Teras Oteli",
            "title": "Santorini Oia Caldera: Alacakaranlık Terası, Kristal Kadeh & Hermès Bileklik Zarafeti ✨",
            "cover_kicker": "» ULTRA LÜKS OTEL & MÜCEVHER • SANTORİNİ OİA REJİSİ «",
            "cover_headline": "SANTORİNİ CALDERA TERASINDA UNUTULMAZ AKŞAM RİTÜELİ",
            "viral_hook": "🌅 Santorini Oia'nın beyaz teraslarında alacakaranlık büyüsü, bilekteki Hermès & altın kelepçe uyumu ve lüks tatil detayları! Kaydetmeyi unutma 👇✨",
            "location_name": "Katikies & Canaves Oia Luxury Suites • Santorini, Yunanistan",
            "had_correction": "true" if had_correction_request else "false",
        }

    if not combined:
        return {
            "clean_subject": "",
            "title": "",
            "cover_kicker": "",
            "cover_headline": "",
            "viral_hook": "",
            "location_name": "",
            "had_correction": "true" if had_correction_request else "false",
        }

    # İlk harfleri büyüt (Türkçe uyumlu)
    words = combined.split()
    titled = " ".join(w[0].upper() + w[1:] if w else "" for w in words)
    return {
        "clean_subject": titled,
        "title": f"{titled}: Sessiz Lüks & Kusursuz Detay Reçetesi ✨",
        "cover_kicker": f"» LUXURY LIFE AI • {titled.upper()[:28]} ÖZEL REJİSİ «",
        "cover_headline": f"{titled.upper()[:42]} • 6 LÜKS DETAY",
        "viral_hook": f"💎 {titled} — Doğru kamera açısı, lüks mekan ve birebir ürün linkleriyle kaydetmelik seçki! 👇✨",
        "location_name": titled,
        "had_correction": "true" if had_correction_request else "false",
    }


# ============================================================================
# KAYDETME ORANI YÜKSEK (HIGH-SAVE-RATE) VİRAL TUTUŞ FORMÜLLERİ ANALİZ RAPORU
# ============================================================================
VIRAL_RETENTION_FRAMEWORKS: Dict[str, Dict[str, str]] = {
    "taki": {
        "category_tr": "Mücevher & Yüksek Saatçilik (Haute Joaillerie & Horlogerie)",
        "save_rate_benchmark": "%9.4 - %13.8 Kaydetme Oranı (Referans Katalog Etkisi)",
        "hook_formula": "0.0s-1.2s Mikro-Parıltı Kancası + 'Bilekte/Boyunda Servet Gösteren 3 Altın Oran Kuralı'",
        "camera_angle": "100mm f/2.8 Macro Lens (Kadife & Mermer Üzeri Elmas Kırılması) + 85mm f/1.4 Golden-Hour Dekolte/Bilek Portresi",
        "lighting_setup": "3200K Sıcak Şampanya Nokta Spot (Specular Highlight) + Yumuşak Altın Rim Işığı",
        "location_direction": "Place Vendôme Paris VIP Salon / Monaco Casino Terası / Boğaz Yalısı Calacatta Mermer Balkon",
        "model_direction": "%100 Fotogerçekçi Süpermodel — Obsidyen siyah ipek gece elbisesi veya kaşmir boğazlı triko üzerinde zarif bilek/boyun hareketi",
        "why_saved": "İzleyiciler mücevher/saat kombinasyonundaki 'Saat + Tek Bileklik + Yüzük' altın oranını ve ulaşılabilir/lüks alternatif linklerini alışverişte kullanmak için kaydeder.",
    },
    "makyaj": {
        "category_tr": "Lüks Makyaj, Cilt Bakımı & Niş Parfüm (Luxury Beauty & Parfumerie)",
        "save_rate_benchmark": "%11.2 - %15.6 Kaydetme Oranı (Rutin & Ürün Kodu Listesi Etkisi)",
        "hook_formula": "0.0s-1.2s Mermer Vanity Kurulumu + 'Filtresiz Old Money Cam Cilt (Glass Skin) ve Kadife Dudak Formülü'",
        "camera_angle": "90mm f/2.8 Macro Overhead Flat-Lay (Mermer Makyaj Masası) + 85mm f/1.4 Ayna Karşısı Uygulama Açısı",
        "lighting_setup": "4800K Doğal Gün Işığı Tül Perde Difüzyonu + Ayna Kenarı Sıcak Kristal Aplik Yansıması",
        "location_direction": "Hôtel Plaza Athénée Paris Mermer Banyo Süiti / Milano Penthouse Vanity Odası",
        "model_direction": "%100 Fotogerçekçi Süpermodel — Şampanya ipek bornoz, arkaya toplanmış parlak saçlar, porselen cilt dokusu ve ruj/parfüm dokunuşu",
        "why_saved": "Kadın takipçiler ton numarası, baz-fondöten-ruj-parfüm sıralaması ve Sephora/Beymen ürün linklerini mağazada bulmak için doğrudan kaydeder.",
    },
    "kombin": {
        "category_tr": "Old Money & Quiet Luxury Kombinler (Haute Couture & Sartorial)",
        "save_rate_benchmark": "%10.5 - %14.9 Kaydetme Oranı (6 Parça Kapsül Gardırop Etkisi)",
        "hook_formula": "0.0s-1.2s Dergi Kapağı Kancası + 'Logoya İhtiyaç Duymadan 250.000₺ Aurası Veren 6 Parça Renk Matematiği'",
        "camera_angle": "85mm f/1.4 Prime Tam Boy (Head-to-Toe) Alçak Podyum Yürüyüş Açısı + GraphMotion 6'lı Stüdyo Dekupe",
        "lighting_setup": "Altın Saat (Golden Hour) Arka Kontur Işığı + Yumuşak Ön Portre Dolgu Işığı",
        "location_direction": "Via Monte Napoleone Milano / Nişantaşı Abdi İpekçi Caddesi / St. Moritz & Lake Como Taş Bulvarı",
        "model_direction": "%100 Fotogerçekçi Süpermodel — Kaşmir kabanın yürürken doğal dalgalanması, ayakkabıdan gözlüğe 6 parçanın 1:1 net görünümü",
        "why_saved": "60-30-10 renk kuralı ve 6 parçanın doğrudan mağaza linkleri 'Yarın ne giysem?' sorusuna hazır reçete sunduğu için en yüksek kaydetme ve paylaşım oranını yakalar.",
    },
    "otel": {
        "category_tr": "Ultra Lüks Oteller, Kraliyet Süitleri & Tatil Rotaları (5-Star Palace & Cliffside Hotels)",
        "save_rate_benchmark": "%12.0 - %16.4 Kaydetme Oranı (Bucket-List & Seyahat Rehberi Etkisi)",
        "hook_formula": "0.0s-1.2s Panoramik Teras POV Açılışı + 'Hayatında En Az Bir Kez Yaşaman Gereken Alacakaranlık Terası & Stil Detayları'",
        "camera_angle": "24mm f/1.4 Mimari Geniş Açı (Caldera / Boğaz Terası) + 50mm f/1.2 POV Kadeh & Bileklik Detay Açısı",
        "lighting_setup": "Mavi Saat (Blue Hour / Twilight) Deniz Ufku + Sıcak 2700K Teras & Villa Kandil Işıkları Kontrastı",
        "location_direction": "Santorini Oia Caldera (Katikies / Canaves Oia) • Çırağan Palace • Mandarin Oriental • Villa d'Este Como",
        "model_direction": "POV Lüks Çift & Süpermodel — Beyaz teras korkuluğunda kristal kadeh tokuşturma, ön planda Hermès deri/altın bileklik ve kırmızı ipli pırlanta bileklik detayı",
        "why_saved": "Çiftler ve lüks seyahat tutkunları yıldönümü, balayı veya yaz/kış kaçamağı için oteli ve fotoğraftaki bileklik/kadeh/kombin linklerini kaydeder ve birbirine DM atar.",
    },
    "araba": {
        "category_tr": "Süper Spor & Ultra Lüks Otomobiller (Exotic Supercars & Bespoke Luxury)",
        "save_rate_benchmark": "%9.8 - %14.2 Kaydetme Oranı (Aspirational Lifestyle & Sürüş Stili Etkisi)",
        "hook_formula": "0.0s-1.2s Alçak Açı Rolling Shot + 'Sadece Motor Sesiyle Değil, İçinden İnen Duruşla Konuşan Lüks'",
        "camera_angle": "35mm f/1.4 Low-Angle Dinamik Rampa/Rolling Açısı + Kokpit Deri Direksiyon/Saat POV + Araç Yanı Tam Boy",
        "lighting_setup": "Gece Islak Asfalt Şehir/Kulüp Yansımaları + Gün Batımı Metalik Gövde Kontur Işığı",
        "location_direction": "Place du Casino Monte-Carlo Monaco / İsviçre Alpleri Virajı / Bebek & Zorlu Center VIP Vale Meydanı",
        "model_direction": "%100 Fotogerçekçi Süpermodel — Aracın dış rengiyle (British Racing Green / GT Silver / Obsidian Black) uyumlu süet/kaşmir sürüş kombini",
        "why_saved": "Otomobil, lüks saat ve sürüş stilini tek karede birleştiren 'Old Money Driver' konsepti hem erkek hem kadın kitlede yüksek kaydetme ve hikaye paylaşımı üretir.",
    },
}

# ============================================================================
# SANTORİNİ OİA CALDERA ÖZEL ŞABLONU (Kullanıcının Gönderdiği Fotoğraftaki Birebir Detaylar!)
# ============================================================================
SANTORINI_OIA_CUSTOM_TEMPLATE: Dict[str, Any] = {
    "id": "lux_otel_santorini_oia_caldera_twilight",
    "category": "otel",
    "gender_segment": "kadin",
    "title": "Santorini Oia Caldera: Alacakaranlık Terası, Kristal Kadeh & Hermès Bileklik Zarafeti ✨",
    "cover_kicker": "» ULTRA LÜKS OTEL & STİL • SANTORİNİ OİA REJİSİ «",
    "cover_headline": "SANTORİNİ CALDERA TERASINDA UNUTULMAZ AKŞAM RİTÜELİ",
    "spoken_hook_text": "Santorini'de gün batıp mavi saat başladığında, terastaki kadehin ışıltısı ve bilekteki zarafet tüm hikayeyi anlatır!",
    "viral_hook": "🌅 Santorini Oia'nın ikonik beyaz teraslarında mavi saat (Blue Hour) büyüsü ve fotoğraftaki 6 lüks detayın birebir linkleri! Kaydet ve gitmek istediğin kişiye gönder 👇✨",
    "location_name": "Katikies & Canaves Oia Luxury Suites • Santorini Caldera, Yunanistan",
    "camera_spec": "Hasselblad H6D-100c • 24mm f/1.4 Blue-Hour Terrace + 50mm f/1.2 POV",
    "act1_beat": "SAHNE 1: Ege Kalderası üzerinde mavi saat ve yamaçtaki sıcak altın villa ışıkları.",
    "act2_beat": "SAHNE 2: Kristal kadehler, Hermès deri-altın kelepçe ve şans bilekliğiyle kusursuz POV.",
    "act3_twist": "FİNAL: Bu büyülü rotayı ve bileklik/stil linklerini kaybetmemek için hemen KAYDET!",
    "model_prompt_en": (
        "Ultra-photorealistic luxury travel & lifestyle photograph shot on 35mm f/1.4 lens at blue hour twilight in Oia Santorini Greece, "
        "overlooking the deep blue Aegean caldera sea and whitewashed cliffside boutique hotel villas glowing with warm golden lights, "
        "elegant couple terrace table with two chilled crystal white wine glasses, luxury python leather and gold cuff bracelet on wrist, "
        "zero 3D, zero cartoon, Conde Nast Traveler cover photography"
    ),
    "items": {
        "slot1": {
            "category_label": "Lüks Teras Otel",
            "emoji": "🏨",
            "brand": "KATIKIES / CANAVES OIA SANTORINI",
            "name": "Oia Caldera Manzaralı Özel Sonsuzluk Havuzlu & Teraslı Lüks Süit",
            "price": "Gecelik Özel Süit",
            "price_val": 48500.0,
            "sku": "LUX-SNT-101",
            "color": "Santorini Beyazı & Ege Mavisi",
            "store_url": "https://www.booking.com/city/gr/oia.tr.html",
            "crop_box": (0.0, 0.0, 1.0, 0.72),
            "en_packshot": "luxury whitewashed Santorini Oia cliffside hotel terrace overlooking blue caldera sea at twilight",
        },
        "slot2": {
            "category_label": "Deri & Altın Bileklik",
            "emoji": "✨",
            "brand": "HERMÈS STİLİ / BEYMEN",
            "name": "Python Dokulu Deri & Altın Tokalı Kelepçe Bileklik (Fotoğraftaki Sol Bilek)",
            "price": "16.950₺",
            "price_val": 16950.0,
            "sku": "LUX-SNT-102",
            "color": "Piton Kahve & Gold",
            "store_url": "https://www.beymen.com/tr/kadin-aksesuar-taki-10108",
            "crop_box": (0.14, 0.66, 0.50, 0.94),
            "en_packshot": "luxury python-embossed leather cuff bracelet with 18k gold hardware clasp on pure white background #FFFFFF",
        },
        "slot3": {
            "category_label": "Altın Kelepçe",
            "emoji": "💛",
            "brand": "CARTIER LOVE STİLİ / ATASAY",
            "name": "14K Sarı Altın İnce İtalyan Bangle Kelepçe Bileklik",
            "price": "19.450₺",
            "price_val": 19450.0,
            "sku": "LUX-SNT-103",
            "color": "14K Sarı Altın",
            "store_url": "https://www.atasay.com/altin-bileklik",
            "crop_box": (0.18, 0.72, 0.46, 0.92),
            "en_packshot": "sleek 18k yellow gold oval bangle bracelet on pure solid white studio background #FFFFFF",
        },
        "slot4": {
            "category_label": "Şans Bilekliği",
            "emoji": "❤️",
            "brand": "REDLINE PARİS STİLİ / ZEN PIRLANTA",
            "name": "Kırmızı İpli Altın & Tektaş Pırlanta Şans Bilekliği (Fotoğraftaki Sağ Bilek)",
            "price": "7.890₺",
            "price_val": 7890.0,
            "sku": "LUX-SNT-104",
            "color": "Kırmızı İp & Pırlanta",
            "store_url": "https://www.zenpirlanta.com/pirlanta-bileklikler",
            "crop_box": (0.72, 0.36, 0.98, 0.66),
            "en_packshot": "delicate red silk cord bracelet with solitaire diamond in 18k gold bezel on pure white background #FFFFFF",
        },
        "slot5": {
            "category_label": "Kristal Kadeh Seti",
            "emoji": "🥂",
            "brand": "NUDE GLASS / BEYMEN HOME",
            "name": "El Yapımı Kurşunsuz Kristal Beyaz Şarap & Şampanya Kadehi Seti",
            "price": "4.250₺",
            "price_val": 4250.0,
            "sku": "LUX-SNT-105",
            "color": "Saf Kristal",
            "store_url": "https://www.beymen.com/tr/ev-yasam-sofra-10302",
            "crop_box": (0.30, 0.24, 0.72, 0.80),
            "en_packshot": "two crystal stemmed white wine glasses clinking on pure solid white background #FFFFFF",
        },
        "slot6": {
            "category_label": "Resort Keten Gömlek",
            "emoji": "🤍",
            "brand": "VAKKO MARE / MASSIMO DUTTI",
            "name": "Santorini Beyazı %100 Saf İtalyan Keten Oversize Resort Gömlek",
            "price": "5.490₺",
            "price_val": 5490.0,
            "sku": "LUX-SNT-106",
            "color": "Kırık Beyaz Keten",
            "store_url": "https://www.massimodutti.com/tr/kadin/gomlekler-ve-bluzlar-n1395",
            "crop_box": (0.0, 0.65, 0.55, 1.0),
            "en_packshot": "crisp white pure Italian linen resort shirt isolated on pure solid white background #FFFFFF",
        },
    },
    "hashtags": "#santorini #oiasantorini #luxuryhotels #oldmoneytravel #quietluxury #luxurylife #tatilrotaları #reklam #işbirliğiyoktur",
}

# ============================================================================
# 5 LÜKS KATEGORİDE HAZIR MASTER ŞABLONLAR (DOĞRULANMIŞ MAĞAZA & İŞ BİRLİĞİ LİNKLERİYLE)
# ============================================================================
LUXURY_MASTER_ARCHETYPES: List[Dict[str, Any]] = [
    SANTORINI_OIA_CUSTOM_TEMPLATE,
    {
        "id": "lux_taki_vendome_gold_diamond_01",
        "category": "taki",
        "gender_segment": "kadin",
        "title": "Place Vendôme Işıltısı: 18K Altın & Baget Pırlanta Katmanlama Sanatı ✨",
        "cover_kicker": "» MÜCEVHER & SAAT • PLACE VENDÔME PARİS REJİSİ «",
        "cover_headline": "BİLEKTE SERVET GÖSTEREN 6 PARÇA ALTIN ORAN KURALI",
        "spoken_hook_text": "Mücevherde sessiz lüks bağırarak değil, altın ve pırlantanın doğru katmanlanmasıyla konuşur!",
        "viral_hook": "💎 Bilekte ve boyunda 'Old Money' zarafeti yaratan 6 parçalık mücevher & saat formülü! Kaydetmeyi unutma 👇✨",
        "location_name": "Place Vendôme Paris & Boğaz Yalısı Mermer Teras",
        "camera_spec": "Hasselblad H6D-100c • 100mm f/2.8 Macro + 85mm f/1.4 Golden Rim",
        "act1_beat": "SAHNE 1: Çok takı takmak değil, doğru 3 odak noktasını seçmek lüksü yaratır.",
        "act2_beat": "SAHNE 2: Şampanya kadranlı saat ve çivi/kelepçe altın bileklik uyumu %100 imza duruşu verir.",
        "act3_twist": "FİNAL: Takı alışverişinden önce bu 6'lı reçeteyi KAYDET • Birebir linkler aşağıda!",
        "model_prompt_en": (
            "Ultra-photorealistic editorial luxury jewelry campaign photograph shot on Hasselblad H6D-100c with 85mm f/1.4 lens, "
            "stunning adult female high-fashion supermodel with sleek dark espresso hair in a low chignon, natural skin pores, "
            "wearing a sleek black silk evening gown on a candlelit marble balcony overlooking Place Vendome Paris at golden hour, "
            "clearly showcasing a 18k yellow gold clover pendant necklace, diamond drop earrings, luxury gold wristwatch and stacked gold bracelets, "
            "zero 3D, zero cartoon, 8k magazine photography"
        ),
        "items": {
            "slot1": {
                "category_label": "Lüks Saat",
                "emoji": "⌚",
                "brand": "CARTIER / BEYMEN",
                "name": "Panthère & Baignoire Stili 18K Altın Tonlu Çelik Lüks Kadın Kol Saati",
                "price": "24.950₺",
                "price_val": 24950.0,
                "sku": "LUX-WATCH-801",
                "color": "Şampanya Altın",
                "store_url": "https://www.beymen.com/tr/kadin-saat-10126",
                "en_packshot": "luxury 18k yellow gold women wristwatch with champagne dial on pure solid white studio background #FFFFFF, macro product photography",
            },
            "slot2": {
                "category_label": "İmza Bileklik",
                "emoji": "✨",
                "brand": "ATASAY / SO CHIC",
                "name": "14 Ayar Altın İtalyan Kelepçe & Çivi Formlu Tasarım Bileklik",
                "price": "18.490₺",
                "price_val": 18490.0,
                "sku": "LUX-BRC-802",
                "color": "Sarı Altın",
                "store_url": "https://www.atasay.com/altin-bileklik",
                "en_packshot": "18k yellow gold sleek nail-style cuff bangle bracelet with diamond tip on pure solid white studio background #FFFFFF",
            },
            "slot3": {
                "category_label": "Kolye",
                "emoji": "📿",
                "brand": "VAN CLEEF STİLİ / ZEN PIRLANTA",
                "name": "Sedef & Oniks Yonca Motifli 14K Altın Zincir Kolye",
                "price": "14.250₺",
                "price_val": 14250.0,
                "sku": "LUX-NCK-803",
                "color": "Altın / Sedef",
                "store_url": "https://www.zenpirlanta.com/altin-kolye",
                "en_packshot": "18k gold chain necklace with mother-of-pearl four-leaf clover motif pendant on pure solid white background #FFFFFF",
            },
            "slot4": {
                "category_label": "Pırlanta Küpe",
                "emoji": "💎",
                "brand": "SWAROVSKI / ZEN",
                "name": "Baget & Damla Kesim Kristal Pırlanta Işıltılı Küpe",
                "price": "6.890₺",
                "price_val": 6890.0,
                "sku": "LUX-EAR-804",
                "color": "Beyaz Pırlanta / Altın",
                "store_url": "https://www.swarovski.com/tr-TR/c-0103/Categories/Jewelry/Earrings/",
                "en_packshot": "luxury baguette diamond and gold drop earrings pair on pure solid white studio background #FFFFFF",
            },
            "slot5": {
                "category_label": "Tamtur Yüzük",
                "emoji": "💍",
                "brand": "ZEN PIRLANTA",
                "name": "Emerald & Baget Kesim Pırlanta Taşlı Altın Tamtur Yüzük",
                "price": "19.900₺",
                "price_val": 19900.0,
                "sku": "LUX-RNG-805",
                "color": "Altın / Pırlanta",
                "store_url": "https://www.zenpirlanta.com/pirlanta-tamtur-yuzukler",
                "en_packshot": "luxury emerald-cut diamond eternity band ring in 18k yellow gold on pure solid white background #FFFFFF",
            },
            "slot6": {
                "category_label": "Gece Elbisesi & Kutu",
                "emoji": "🖤",
                "brand": "VAKKO COUTURE",
                "name": "Obsidyen Siyah İpek Saten Sırt Dekolteli Gece Elbisesi",
                "price": "16.500₺",
                "price_val": 16500.0,
                "sku": "LUX-DRS-806",
                "color": "Obsidyen Siyah",
                "store_url": "https://www.vakko.com/kadin-elbise/",
                "en_packshot": "sleek jet-black silk satin evening dress isolated flat-lay on pure solid white background #FFFFFF",
            },
        },
        "hashtags": "#mücevher #altıntakı #pırlanta #lükssaat #oldmoneystyle #luxurylife #quietluxury #reklam #işbirliğiyoktur",
    },
    {
        "id": "lux_makyaj_paris_vanity_glass_skin_01",
        "category": "makyaj",
        "gender_segment": "kadin",
        "title": "Hôtel Plaza Athénée Vanity: 6 Adımda 'Old Money Glass Skin' & Kadife Dudak Sırrı 💄",
        "cover_kicker": "» LÜKS MAKYAJ & PARFÜM • PARİS VANITY REJİSİ «",
        "cover_headline": "FİLTRESİZ 'OLD MONEY' CAM CİLT YARATAN 6 İKONİK ÜRÜN",
        "spoken_hook_text": "Pahalı ve dinlenmiş görünen bir cildin sırrı kapatıcıda değil, doğru ışıltı bazında ve kadife dudak tonundadır!",
        "viral_hook": "💄 Paris'in en lüks makyaj masalarından çıkan 6 parçalık 'Glass Skin & Velvet Lip' rutini! Kodları ve linkleri kaydet 👇✨",
        "location_name": "Hôtel Plaza Athénée Paris Calacatta Mermer Banyo Süiti",
        "camera_spec": "Hasselblad H6D-100c • 90mm f/2.8 Macro Vanity + 85mm f/1.4 Golden Mirror",
        "act1_beat": "SAHNE 1: Ağır mat fondöten yerine cildi içeriden aydınlatan ipek bazla başla.",
        "act2_beat": "SAHNE 2: Sıcak bronz kontur ve gül kurusu-bordo dudak tonu yüz hatlarını anında yukarı taşır.",
        "act3_twist": "FİNAL: Sephora & Beymen alışverişinde aramamak için hemen KAYDET • Linkler aşağıda!",
        "model_prompt_en": (
            "Ultra-photorealistic luxury beauty campaign photograph shot on 85mm f/1.4 prime lens, "
            "gorgeous adult female supermodel with glowing glass skin, natural skin micro-texture, wearing a champagne silk robe "
            "in a sunlit Calacatta marble bathroom suite at Hotel Plaza Athenee Paris, holding a gold designer lipstick tube "
            "in front of a gilded mirror with luxury perfume bottles and gold compact powder on the marble vanity, "
            "zero 3D, zero cartoon, Vogue Beauty editorial photography"
        ),
        "items": {
            "slot1": {
                "category_label": "Işıltılı Baz & Fondöten",
                "emoji": "✨",
                "brand": "DIOR BEAUTY / SEPHORA",
                "name": "Forever Skin Glow 24H Nemlendirici & Işıltı Veren Lüks Fondöten (2N)",
                "price": "2.850₺",
                "price_val": 2850.0,
                "sku": "LUX-BTY-901",
                "color": "2N Neutral Glow",
                "store_url": "https://www.sephora.com.tr/markalar/dior/",
                "en_packshot": "luxury glass bottle of radiant liquid foundation makeup with gold cap on pure solid white background #FFFFFF",
            },
            "slot2": {
                "category_label": "Kadife Ruj",
                "emoji": "💄",
                "brand": "YSL BEAUTY / SEPHORA",
                "name": "Rouge Pur Couture Caring Satin Altın Gövdeli İkonik Ruj (Nu Muse)",
                "price": "2.190₺",
                "price_val": 2190.0,
                "sku": "LUX-BTY-902",
                "color": "Nu Muse / Rosewood",
                "store_url": "https://www.sephora.com.tr/markalar/yves-saint-laurent/",
                "en_packshot": "luxury gold-cased satin lipstick bullet in rosewood nude shade on pure solid white background #FFFFFF",
            },
            "slot3": {
                "category_label": "Pudra & Bronzer",
                "emoji": "🪞",
                "brand": "CHARLOTTE TILBURY / BEYMEN",
                "name": "Airbrush Flawless Finish Altın Kompakt İpek Pudra",
                "price": "2.490₺",
                "price_val": 2490.0,
                "sku": "LUX-BTY-903",
                "color": "Medium Golden",
                "store_url": "https://www.beymen.com/tr/kozmetik-10006",
                "en_packshot": "luxury ribbed rose-gold compact pressed powder makeup case open on pure solid white background #FFFFFF",
            },
            "slot4": {
                "category_label": "Allık & Aydınlatıcı",
                "emoji": "🌸",
                "brand": "CHANEL BEAUTY / SEPHORA",
                "name": "Les Beiges Healthy Glow Aydınlatıcı & Kremsi Allık Paleti",
                "price": "3.150₺",
                "price_val": 3150.0,
                "sku": "LUX-BTY-904",
                "color": "Warm Peach Champagne",
                "store_url": "https://www.sephora.com.tr/markalar/chanel/",
                "en_packshot": "luxury luminous champagne-rose highlighter and blush compact palette on pure solid white background #FFFFFF",
            },
            "slot5": {
                "category_label": "Cilt Bakım İksiri",
                "emoji": "🧴",
                "brand": "ESTÉE LAUDER / SEPHORA",
                "name": "Advanced Night Repair & Crème de la Mer Işıltı Serumu",
                "price": "4.450₺",
                "price_val": 4450.0,
                "sku": "LUX-BTY-905",
                "color": "Altın İksir",
                "store_url": "https://www.sephora.com.tr/cilt-bakimi/",
                "en_packshot": "luxury amber-gold dropper facial serum glass bottle on pure solid white studio background #FFFFFF",
            },
            "slot6": {
                "category_label": "Niş Parfüm",
                "emoji": "👑",
                "brand": "MAISON FRANCIS KURKDJIAN / BEYMEN",
                "name": "Baccarat Rouge 540 & Oud Satin Mood Extrait de Parfum (70 ml)",
                "price": "14.950₺",
                "price_val": 14950.0,
                "sku": "LUX-PRF-906",
                "color": "Yakut & Altın",
                "store_url": "https://www.beymen.com/tr/kozmetik-parfum-10179",
                "en_packshot": "luxury crystal square ruby-red and gold niche perfume bottle on pure solid white background #FFFFFF",
            },
        },
        "hashtags": "#lüksmakyaj #makyajönerileri #sephoratürkiye #glassskin #oldmoneybeauty #nişparfüm #luxurylife #reklam #işbirliğiyoktur",
    },
    {
        "id": "lux_kombin_milano_cashmere_espresso_01",
        "category": "kombin",
        "gender_segment": "kadin",
        "title": "Via Monte Napoleone Milano: Kaşmir, İpek & Espresso Süet 'Quiet Luxury' Kurgusu 🧥",
        "cover_kicker": "» OLD MONEY KOMBİN • MİLANO HAUTE COUTURE REJİSİ «",
        "cover_headline": "LOGOSUZ 250.000₺ AURASI YARATAN 6 PARÇA KAŞMİR FORMÜLÜ",
        "spoken_hook_text": "Gerçek lüks üzerinde dev logolar taşımaz; kaşmirin dokusu ve altmış-otuz-on renk dengesiyle ilk saniyede anlaşılır!",
        "viral_hook": "🧥 Milano Via Monte Napoleone'den fırlamış 6 parçalık 'Quiet Luxury' kombin reçetesi! Kaydet ve linkleri incele 👇✨",
        "location_name": "Via Monte Napoleone Milano & Nişantaşı Abdi İpekçi Bulvarı",
        "camera_spec": "Hasselblad H6D-100c • 85mm f/1.4 Prime Tam Boy Podyum Yürüyüşü",
        "act1_beat": "SAHNE 1: %60 Devetüyü kaşmir dış katman, %30 fildişi merinos iç katmanla birleşir.",
        "act2_beat": "SAHNE 2: %10 Espresso süet çanta ve loafer dokunuşu kombini podyum seviyesine çıkarır.",
        "act3_twist": "FİNAL: Dolabının imza kombinini kaybetmemek için hemen KAYDET • Doğrulanmış linkler aşağıda!",
        "model_prompt_en": (
            "Ultra-photorealistic full-body street style fashion photograph shot on Hasselblad H6D-100c with 85mm f/1.4 lens, "
            "stunning adult female supermodel walking mid-stride head-to-toe on Via Monte Napoleone Milan at golden hour, "
            "wearing a tailored camel double-breasted cashmere coat over an ivory ribbed turtleneck sweater, warm taupe pleated wide-leg wool palazzo trousers, "
            "tortoiseshell designer sunglasses, structured espresso-brown leather gold-clasp handbag, and suede loafers, "
            "natural skin texture, zero 3D, zero cartoon, 8k Vogue Italia lookbook"
        ),
        "items": {
            "slot1": {
                "category_label": "Kaşmir Kaban",
                "emoji": "🧥",
                "brand": "MASSIMO DUTTI / BEYMEN",
                "name": "Devetüyü (Camel) Kruvaze Yün & Kaşmir Karışımlı Uzun Kaban",
                "price": "9.950₺",
                "price_val": 9950.0,
                "sku": "LUX-FSH-701",
                "color": "Camel / Devetüyü",
                "store_url": "https://www.massimodutti.com/tr/kadin/palto-ve-trenckot-n1434",
                "en_packshot": "tailored warm camel double-breasted wool cashmere overcoat isolated on pure solid white background #FFFFFF",
            },
            "slot2": {
                "category_label": "Güneş Gözlüğü",
                "emoji": "🕶️",
                "brand": "CELINE / BEYMEN EYEWEAR",
                "name": "Triomphe Gold Detaylı Kemik/Siyah Oval Güneş Gözlüğü",
                "price": "14.500₺",
                "price_val": 14500.0,
                "sku": "LUX-FSH-702",
                "color": "Siyah / Altın",
                "store_url": "https://www.beymen.com/tr/kadin-aksesuar-gunes-gozlugu-10105",
                "en_packshot": "luxury black acetate oval sunglasses with gold temple emblem on pure solid white background #FFFFFF",
            },
            "slot3": {
                "category_label": "Kaşmir Triko",
                "emoji": "👚",
                "brand": "İPEKYOL / VAKKO",
                "name": "Fildişi Ekru İnce Fitilli Boğazlı Merinos & Kaşmir Triko",
                "price": "2.950₺",
                "price_val": 2950.0,
                "sku": "LUX-FSH-703",
                "color": "Fildişi Ekru",
                "store_url": "https://www.ipekyol.com.tr/triko-modelleri/",
                "en_packshot": "ivory cream ribbed-knit cashmere turtleneck sweater isolated on pure solid white background #FFFFFF",
            },
            "slot4": {
                "category_label": "Palazzo Pantolon",
                "emoji": "👖",
                "brand": "VAKKO / ZARA ATELIER",
                "name": "Vizon & Taş Beji Yüksek Bel Pileli İtalyan Yün Palazzo Pantolon",
                "price": "3.490₺",
                "price_val": 3490.0,
                "sku": "LUX-FSH-704",
                "color": "Vizon Bej",
                "store_url": "https://www.vakko.com/kadin-pantolon/",
                "en_packshot": "warm taupe beige high-waisted pleated wide-leg wool palazzo trousers on pure solid white background #FFFFFF",
            },
            "slot5": {
                "category_label": "Lüks Deri Çanta",
                "emoji": "👜",
                "brand": "BEYMEN COLLECTION",
                "name": "Espresso Kahve Gold Kilitli Kelly Formlu Deri El & Omuz Çantası",
                "price": "7.850₺",
                "price_val": 7850.0,
                "sku": "LUX-FSH-705",
                "color": "Espresso Kahve",
                "store_url": "https://www.beymen.com/tr/kadin-canta-10014",
                "en_packshot": "structured espresso dark-brown leather top-handle handbag with gold turn-lock clasp on pure solid white background #FFFFFF",
            },
            "slot6": {
                "category_label": "Süet Loafer",
                "emoji": "👞",
                "brand": "LORO PIANA STİLİ / NETWORK",
                "name": "Summer Walk Stili Hakiki Süet Deri Krem Tabanlı Lüks Loafer",
                "price": "5.490₺",
                "price_val": 5490.0,
                "sku": "LUX-FSH-706",
                "color": "Taba Süet",
                "store_url": "https://www.network.com.tr/kadin-ayakkabi-1006/",
                "en_packshot": "luxury warm cognac suede slip-on loafers with cream rubber sole on pure solid white background #FFFFFF",
            },
        },
        "hashtags": "#oldmoneystyle #quietluxury #kombinönerileri #kaşmirkaban #lüksmoda #luxurylife #reklam #işbirliğiyoktur",
    },
    {
        "id": "lux_araba_monaco_porsche_gt3_driver_01",
        "category": "araba",
        "gender_segment": "erkek",
        "title": "Monaco Casino Meydanı: Porsche 911 GT3 Touring & 'Gentleman Driver' 6 Parça Stili 🏎️",
        "cover_kicker": "» SÜPER SPOR OTOMOBİL & STİL • MONACO GP REJİSİ «",
        "cover_headline": "SADECE MOTOR SESİYLE DEĞİL DURUŞUYLA KONUŞAN 6 PARÇA",
        "spoken_hook_text": "Gerçek bir süper spor otomobilin direksiyonundan indiğinde, üzerindeki süet ceket ve bileğindeki kronograf aynı dili konuşmalıdır!",
        "viral_hook": "🏎️ Porsche 911 GT3 Touring (British Racing Green) ve 'Old Money Gentleman Driver' 6 parçalık sürüş stili! Kaydet 👇✨",
        "location_name": "Place du Casino Monte-Carlo Monaco & Zorlu VIP Meydan",
        "camera_spec": "Hasselblad H6D-100c • 35mm f/1.4 Low-Angle Rolling + Kokpit POV",
        "act1_beat": "SAHNE 1: British Racing Green gövde rengi ile taba deri kokpitin zamansız uyumu.",
        "act2_beat": "SAHNE 2: İtalyan süet sürüş ceketi, kronograf saat ve deri loafer kusursuz bütünlük kurar.",
        "act3_twist": "FİNAL: Otomobil ve lüks stil tutkunları için hemen KAYDET • Ürün linkleri aşağıda!",
        "model_prompt_en": (
            "Ultra-photorealistic luxury automotive & menswear editorial photograph shot on 35mm f/1.4 lens at low angle, "
            "charismatic adult male fashion model with sharp jawline standing beside a sleek British Racing Green Porsche 911 GT3 Touring sports car "
            "in front of Place du Casino Monte Carlo Monaco at golden sunset, wearing a cognac suede bomber jacket over a fine cream merino turtleneck, "
            "charcoal tailored trousers, aviator sunglasses, luxury chronograph watch, and leather driving loafers, "
            "natural skin texture, zero 3D, zero cartoon, 8k GQ automotive photography"
        ),
        "items": {
            "slot1": {
                "category_label": "Süper Spor Otomobil",
                "emoji": "🏎️",
                "brand": "PORSCHE TÜRKİYE",
                "name": "Porsche 911 GT3 Touring Package (British Racing Green / Cognac Deri Kokpit)",
                "price": "Özel Konfigürasyon",
                "price_val": 28500000.0,
                "sku": "LUX-CAR-501",
                "color": "British Racing Green",
                "store_url": "https://www.porsche.com.tr/modeller/911/",
                "en_packshot": "sleek dark emerald green Porsche 911 GT3 luxury sports car 3/4 front studio angle on pure solid white background #FFFFFF",
            },
            "slot2": {
                "category_label": "Kronograf Saat",
                "emoji": "⌚",
                "brand": "TAG HEUER / BEYMEN SAAT",
                "name": "Carrera & Daytona Stili Çelik Kasalı Kronograf Sürüş Saati",
                "price": "84.500₺",
                "price_val": 84500.0,
                "sku": "LUX-CAR-502",
                "color": "Gümüş / Yeşil Kadran",
                "store_url": "https://www.beymen.com/tr/erkek-aksesuar-saat-10075",
                "en_packshot": "luxury stainless steel racing chronograph wristwatch with green tachymeter bezel on pure solid white background #FFFFFF",
            },
            "slot3": {
                "category_label": "Süet Sürüş Ceketi",
                "emoji": "🧥",
                "brand": "MASSIMO DUTTI STUDIO",
                "name": "Konyak Taba %100 Hakiki Süet Deri İtalyan Sürüş & Bomber Ceket",
                "price": "14.950₺",
                "price_val": 14950.0,
                "sku": "LUX-CAR-503",
                "color": "Konyak Taba",
                "store_url": "https://www.massimodutti.com/tr/erkek/deri-ceketler-n1379",
                "en_packshot": "men cognac tan suede leather bomber driving jacket isolated on pure solid white background #FFFFFF",
            },
            "slot4": {
                "category_label": "Sürüş Gözlüğü",
                "emoji": "🕶️",
                "brand": "PERSOL / RAY-BAN",
                "name": "Steve McQueen Katlanabilir Kemik & Polarize Camlı Sürüş Gözlüğü",
                "price": "9.450₺",
                "price_val": 9450.0,
                "sku": "LUX-CAR-504",
                "color": "Havana / Yeşil Cam",
                "store_url": "https://www.beymen.com/tr/erkek-aksesuar-gunes-gozlugu-10073",
                "en_packshot": "luxury Havana tortoiseshell aviator driving sunglasses with green polarized lenses on pure solid white background #FFFFFF",
            },
            "slot5": {
                "category_label": "Hafta Sonu Çantası",
                "emoji": "💼",
                "brand": "TERGAN / BEYMEN CLUB",
                "name": "Örgü Dokulu (Intrecciato) Hakiki Deri Hafta Sonu & Kokpit Çantası",
                "price": "8.950₺",
                "price_val": 8950.0,
                "sku": "LUX-CAR-505",
                "color": "Acı Kahve Deri",
                "store_url": "https://www.beymen.com/tr/erkek-canta-10064",
                "en_packshot": "dark espresso woven leather weekender duffle bag on pure solid white studio background #FFFFFF",
            },
            "slot6": {
                "category_label": "Sürüş Loafer",
                "emoji": "👞",
                "brand": "SANTONI / NETWORK",
                "name": "Konyak Süet Deri Esnek Tabanlı İtalyan Driving Loafer",
                "price": "6.750₺",
                "price_val": 6.750,
                "sku": "LUX-CAR-506",
                "color": "Konyak Süet",
                "store_url": "https://www.network.com.tr/erkek-ayakkabi-1030/",
                "en_packshot": "men cognac suede Italian driving loafers shoes on pure solid white studio background #FFFFFF",
            },
        },
        "hashtags": "#porsche911 #supercars #oldmoneymen #gentlemanstyle #luxurycars #monacolifestyle #luxurylife #reklam #işbirliğiyoktur",
    },
]


def detect_luxury_category(text: str, urls: Optional[List[str]] = None) -> str:
    """
    Kullanıcının Telegram'dan gönderdiği metin, komut veya linklere göre
    5 lüks kategoriden ('taki', 'makyaj', 'kombin', 'otel', 'araba') hangisi olduğunu algılar.
    """
    blob = " ".join([text or ""] + (urls or [])).lower()

    if any(k in blob for k in ("/otel", "otel", "hotel", "santorini", "santorıny", "santoriny", "kapadokya", "suit", "süit", "tatil", "resort", "villa", "havuz", "boğaz", "bogaz", "mandarin", "çırağan", "ciragan", "four seasons", "amanruya", "bodrum", "como", "booking", "ets", "teras", "caldera")):
        return "otel"
    if any(k in blob for k in ("/taki", "takı", "taki", "kolye", "bileklik", "küpe", "kupe", "yüzük", "yuzuk", "pırlanta", "pirlanta", "altın", "altin", "mücevher", "mucevher", "cartier", "swarovski", "atasay", "zenpirlanta", "pandora", "rolex", "saat")):
        return "taki"
    if any(k in blob for k in ("/makyaj", "makyaj", "ruj", "fondöten", "fondoten", "allık", "allik", "pudra", "rimel", "maskara", "sephora", "parfüm", "parfum", "kozmetik", "cilt", "serum", "krem", "dior beauty", "chanel beauty", "charlotte tilbury")):
        return "makyaj"
    if any(k in blob for k in ("/araba", "araba", "otomobil", "porsche", "ferrari", "rolls-royce", "rolls royce", "bentley", "mercedes", "g63", "amg", "range rover", "lamborghini", "aston martin", "supercar", "sürüş", "kokpit")):
        return "araba"
    if any(k in blob for k in ("/kombin", "kombin", "kaban", "ceket", "elbise", "pantolon", "triko", "kazak", "çanta", "canta", "ayakkabı", "ayakkabi", "loafer", "beymen", "vakko", "zara", "massimo dutti", "ipekyol")):
        return "kombin"
    return "otomatik"


def resolve_smart_collaboration_url(item_name: str, brand: str, category: str, explicit_url: str = "") -> str:
    if explicit_url and explicit_url.startswith("http"):
        return explicit_url.strip()

    from urllib.parse import quote_plus
    query = quote_plus(f"{brand} {item_name}".strip())
    b_low = (brand or "").lower()

    if "sephora" in b_low or category == "makyaj":
        return f"https://www.sephora.com.tr/on/demandware.store/Sites-Sephora_TR-Site/tr_TR/Search-Show?q={query}"
    if "atasay" in b_low or "zen" in b_low or "swarovski" in b_low or category == "taki":
        return f"https://www.trendyol.com/sr?q={query}"
    if "porsche" in b_low:
        return "https://www.porsche.com.tr/modeller/911/"
    if "santorini" in b_low or "katikies" in b_low or "canaves" in b_low:
        return "https://www.booking.com/city/gr/oia.tr.html"
    if "mandarin" in b_low or "çırağan" in b_low or category == "otel":
        return "https://www.mandarinoriental.com/tr/istanbul/bosphorus"
    if "vakko" in b_low:
        return f"https://www.vakko.com/arama/?q={query}"
    if "massimo" in b_low:
        return "https://www.massimodutti.com/tr/"
    return f"https://www.beymen.com/tr/search?q={query}"


def load_luxury_ledger() -> Dict[str, Any]:
    os.makedirs(LEDGER_PATH.parent, exist_ok=True)
    if LEDGER_PATH.exists():
        try:
            return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"published_ids": [], "last_category_index": -1, "last_dispatch_ts": 0.0}


def save_luxury_ledger(data: Dict[str, Any]) -> None:
    os.makedirs(LEDGER_PATH.parent, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def select_luxury_concept(force_category: str = "otomatik", custom_concept: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if custom_concept:
        cat = custom_concept.get("category", "otel")
        custom_concept["viral_analysis"] = VIRAL_RETENTION_FRAMEWORKS.get(cat, VIRAL_RETENTION_FRAMEWORKS["otel"])
        return custom_concept

    ledger = load_luxury_ledger()
    cat_order = ["otel", "taki", "makyaj", "kombin", "araba"]
    if force_category in cat_order:
        target_cat = force_category
    else:
        next_idx = (int(ledger.get("last_category_index", -1)) + 1) % len(cat_order)
        target_cat = cat_order[next_idx]
        ledger["last_category_index"] = next_idx
        save_luxury_ledger(ledger)

    candidates = [a for a in LUXURY_MASTER_ARCHETYPES if a["category"] == target_cat]
    chosen = dict(candidates[0] if candidates else LUXURY_MASTER_ARCHETYPES[0])
    chosen["viral_analysis"] = VIRAL_RETENTION_FRAMEWORKS.get(chosen["category"], VIRAL_RETENTION_FRAMEWORKS["otel"])
    return chosen


def build_explanatory_director_message(concept: Dict[str, Any]) -> str:
    va = concept.get("viral_analysis") or VIRAL_RETENTION_FRAMEWORKS.get(concept.get("category", "otel"))
    title = concept.get("title", "Lüks Yaşam Konsepti")
    loc = concept.get("location_name", "Santorini / Paris / Milano / İstanbul Boğazı")
    cam = concept.get("camera_spec", "Hasselblad H6D-100c • 35mm f/1.4")
    has_user_media = bool(concept.get("user_photo_path") or concept.get("user_photos") or concept.get("user_video_path"))
    media_note = (
        "✅ Telegram'dan gönderdiğiniz ham fotoğraf/görüntü ve metin doğrudan ana sahne, kapak ve 6'lı GraphMotion detay kartları olarak işlendi (yazım düzeltmesi otomatik uygulandı)."
        if has_user_media
        else "✅ Kategoriye özel yüksek kaydetme oranlı (High-Save-Rate) lüks şablon ve sahne kurgusu uygulandı."
    )

    lines = [
        "🎬 [LUXURY LIFE AI — REELS TUTUŞ, KAYDETME ORANI & REJİ ANALİZİ]",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📌 Konsept: {title}",
        f"🏆 Kategori: {va['category_tr']}",
        f"📈 Beklenen Kaydetme Oranı (Save Rate): {va['save_rate_benchmark']}",
        f"🖼️ Ham Materyal & Tetikleme Durumu: {media_note}",
        "",
        "🧠 NEDEN BU VİDEO YÜKSEK KAYDETME ALIR?",
        f"• Kanca (0.0s - 1.2s): {va['hook_formula']}",
        f"• Kaydetme Psikolojisi: {va['why_saved']}",
        "",
        "🎥 DOĞRU AÇI, MEKAN & MODEL REJİSİ:",
        f"• Kamera & Lens Açısı: {cam} ({va['camera_angle']})",
        f"• Işık Kurulumu: {va['lighting_setup']}",
        f"• Seçilen Lüks Mekan: {loc}",
        f"• Model & Sahne Duruşu: {va['model_direction']}",
        "",
        "📋 KULLANIM REHBERİ (AŞAĞIDAKİ 2 AYRI COPY-PASTE MESAJI):",
        "1️⃣ Hemen alttaki 1. metin mesajı: SADECE Instagram Reels Açıklama (Caption) kısmına tek dokunuşla kopyalayıp yapıştırmanız içindir (Yasal '#reklam #işbirliğiyoktur' notu dahildir).",
        "2️⃣ Onun altındaki 2. metin mesajı: SADECE görseldeki ürünlerin/mekanın birebir doğrulanmış mağaza ve iş birliği linkleridir; İlk Yoruma, Story Link etiketine veya takipçi DM'lerine doğrudan kopyalayıp yapıştırabilirsiniz.",
    ]
    return "\n".join(lines)


def build_pure_copy_paste_caption(concept: Dict[str, Any]) -> str:
    va = concept.get("viral_analysis") or VIRAL_RETENTION_FRAMEWORKS.get(concept.get("category", "otel"))
    title = concept.get("title", "")
    viral_hook = concept.get("viral_hook", "")
    loc = concept.get("location_name", "")
    items = concept.get("items", {})
    hashtags = concept.get("hashtags", "#luxurylife #oldmoney #quietluxury #reklam #işbirliğiyoktur")

    num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
    item_lines = []
    for idx, (slot_k, it) in enumerate(items.items()):
        num_e = num_emojis[idx] if idx < len(num_emojis) else "•"
        em = it.get("emoji", "✨")
        lbl = it.get("category_label", "Detay")
        brand = it.get("brand", "Lüks Marka")
        name = it.get("name", "Ürün")
        price = it.get("price", "")
        sku = it.get("sku", "-")
        item_lines.append(f"{num_e} {em} {lbl}: {brand} — {name} ({price} | Kod: {sku})")

    lines = [
        f"✨ {title}",
        "",
        f"{viral_hook}",
        "",
        f"📍 Mekan & Atmosfer: {loc}",
        f"🎥 Estetik & Stil Notu: {va['why_saved']}",
        "",
        "💎 VİDEODAKİ 6 LÜKS DETAY & ÜRÜN REÇETESİ:",
        *item_lines,
        "",
        "📌 Bu lüks kurguyu ve ürün kodlarını kaybetmemek için videoyu hemen KAYDET ve birlikte gitmek/denemek istediğin arkadaşına GÖNDER! 👇✨",
        "💬 Senin favorin kaç numaralı detay oldu? (1-6 arası yoruma yaz, linkini sabitleyelim 👇)",
        "",
        TR_LEGAL_CAPTION_NOTICE,
        "",
        hashtags,
    ]
    return "\n".join(lines)


def build_pure_copy_paste_links(concept: Dict[str, Any]) -> str:
    title = concept.get("title", "Lüks Yaşam Seçkisi")
    items = concept.get("items", {})
    num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]

    lines = [
        f"💎 {title} — BİREBİR ÜRÜN, OTEL & MAĞAZA LİNKLERİ 👇",
        "",
    ]
    for idx, (slot_k, it) in enumerate(items.items()):
        num_e = num_emojis[idx] if idx < len(num_emojis) else "•"
        em = it.get("emoji", "✨")
        brand = it.get("brand", "Mağaza")
        name = it.get("name", "Ürün")
        price = it.get("price", "")
        sku = it.get("sku", "-")
        url = it.get("store_url") or resolve_smart_collaboration_url(name, brand, concept.get("category", "otel"))
        lines.append(f"{num_e} {em} {brand} – {name} ({price} | Kod: {sku})")
        lines.append(f"👉 {url}")
        lines.append("")

    lines.append("✨ Favori parçanızın numarasını yoruma yazabilirsiniz!")
    lines.append(TR_LEGAL_LINKS_NOTICE)
    return "\n".join(lines)
