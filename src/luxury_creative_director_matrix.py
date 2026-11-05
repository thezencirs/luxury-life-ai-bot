"""
Luxury Life AI (@Luxurylifeaibot) — Viral Retention & Luxury Creative Director Matrix
=====================================================================================
Saf Beyaz Fotoğraf Stüdyosu (#FFFFFF White Cyclorama Studio) içerisinde:
1) SAHNE 1 (KOLDA, BİLEKTE VE YÜZDE MİKRO-SERGİ — 85mm/90mm/100mm Macro Close-Up):
   Saat, bileklik, yüzük, küpe, kolye, gözlük ve rujun doğrudan süpermodelin bileğinde,
   boynunda, kulağında ve yüzünde sergilendiği yüksek tutuşlu (watch-time) açılış sahnesi.
2) SAHNE 2 (MANKEN ÜZERİNDE BÜTÜNSEL LÜKS DURUŞ — 50mm/85mm Mid-Full Editorial Lookbook):
   6 lüks parçanın zengin ve asil süpermodel üzerinde birbiriyle kusursuz renk/materyal uyumu.
3) SAHNE 3 (YÜRÜRKEN FARK EDİLEN ZENGİN & LÜKS HAREKET — 35mm/50mm Dynamic Catwalk Motion):
   Süpermodelin saf beyaz fotoğraf stüdyosunda (#FFFFFF) kameraya doğru özgüvenle yürürken
   saçlarının, ipek/kaşmir kumaşın ve bilekteki/boyundaki mücevherlerin hareket halinde parlaması.

Tüm şablonlar %100 fotogerçekçi insan süpermodel (`is_3d_avatar: False`) standardındadır ve
doğrulanmış Türkiye lüks mağaza linkleri içerir.
"""
import copy
from typing import Any, Dict, List, Optional

EXTENDED_STUDIO_ONBODY_ARCHETYPES: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. TAKI & YÜKSEK SAATÇİLİK (taki) — Audemars Piguet & Zümrüt/Pırlanta
    # =========================================================================
    {
        "id": "lux_taki_audemars_emerald_studio_02",
        "category": "taki",
        "gender_segment": "kadin",
        "is_3d_avatar": False,
        "title": "Haute Horlogerie Beyaz Stüdyo: 18K Pembe Altın Saat, Zümrüt Kesim Pırlanta & Bilek Sanatı ✨",
        "cover_kicker": "» YÜKSEK SAATÇİLİK & MÜCEVHER • SAF BEYAZ STÜDYO REJİSİ «",
        "cover_headline": "KOLDA, BİLEKTE VE YÜZDE SERVET GÖSTEREN 6 MÜCEVHER KURALI",
        "spoken_hook_text": "Gerçek mücevher ve yüksek saatçilik vitrinde değil; bilekte, boyunda ve yürürken yakaladığı ışık kırılmasıyla kendini belli eder!",
        "viral_hook": "💎 Kolda 18K pembe altın saat, bilekte baget kelepçe, boyunda ve yüzde pırlanta ışıltısının yürürken yarattığı kusursuz aura! Kaydetmeyi unutma 👇✨",
        "location_name": "Haute Joaillerie Saf Beyaz Sonsuz Fon Fotoğraf Stüdyosu (#FFFFFF White Cyclorama Studio)",
        "camera_spec": "Hasselblad H6D-100c • 100mm f/2.8 Macro On-Wrist + 85mm f/1.4 On-Model + 35mm f/1.4 Catwalk Motion",
        "act1_beat": "SAHNE 1 (KOLDA & YÜZDE MİKRO-SERGİ): Süpermodelin bileğindeki 18K pembe altın saat, pırlanta kelepçe ve yüzündeki küpe/kolye uyumu.",
        "act2_beat": "SAHNE 2 (MANKEN ÜZERİNDE BÜTÜNSEL DURUŞ): Zümrüt yeşili ipek elbise üzerinde 6 mücevherin kusursuz renk ve altın oran dengesi.",
        "act3_twist": "SAHNE 3 (YÜRÜRKEN FARK EDİLEN LÜKS): Beyaz stüdyoda yürürken bilekte ve boyunda parlayan sessiz servet • Hemen KAYDET!",
        "model_prompt_en": (
            "Ultra-photorealistic luxury jewelry and watch campaign photograph shot on Hasselblad H6D-100c with 85mm f/1.4 lens "
            "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background, Profoto beauty dish and softbox lighting), "
            "stunning adult female supermodel with natural skin pores and sleek dark hair, wearing a deep emerald-green silk satin evening gown, "
            "posing gracefully to exhibit an 18k rose gold octagonal luxury wristwatch and diamond tennis bracelet on her wrist, "
            "emerald-cut diamond ring on her finger, diamond drop earrings on her ears, and a delicate diamond pendant necklace on her collarbone, "
            "zero 3D, zero cartoon, 8k Vogue & Haute Joaillerie studio lookbook"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic macro close-up luxury jewelry portrait shot on Hasselblad H6D-100c 100mm f/2.8 macro lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background, crisp Profoto specular studio lighting), "
                "real adult female supermodel with natural skin micro-texture raising her slender wrist and hand gracefully beside her jawline and collarbone, "
                "clearly exhibiting an 18k rose gold octagonal luxury wristwatch on her wrist alongside a stacked baguette diamond cuff bracelet, "
                "an emerald-cut solitaire diamond ring on her finger, sparkling pear-cut diamond drop earrings on her ear, "
                "and an 18k rose gold diamond pendant resting on her collarbone, zero 3D, zero cartoon, 8k Haute Horlogerie close-up"
            ),
            (
                "Ultra-photorealistic medium-full luxury studio lookbook photograph shot on Hasselblad H6D-100c 85mm f/1.4 prime lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white background and floor), "
                "wealthy real adult female supermodel standing in a poised three-quarter editorial stance wearing a deep emerald-green silk satin bias-cut evening gown, "
                "her left arm angled across her waist so the 18k rose gold wristwatch, diamond tennis bracelet, and emerald-cut ring are in razor-sharp focus, "
                "harmonizing with the diamond drop earrings and collarbone necklace, natural skin texture, zero 3D, zero cartoon, 8k editorial photography"
            ),
            (
                "Ultra-photorealistic full-body dynamic catwalk motion photograph shot on Hasselblad H6D-100c 35mm f/1.4 lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background with soft floor reflection), "
                "real adult female supermodel walking confidently forward toward the camera mid-stride in a flowing deep emerald-green silk evening gown, "
                "her wrist and hand swinging naturally in foreground catching bright studio highlights on her 18k rose gold wristwatch and stacked diamond bracelets, "
                "diamond necklace and earrings gleaming on her neck and face as she walks with effortless billionaire elegance, zero 3D, zero cartoon, 8k runway motion"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "Kolda 18K Rose Gold Saat",
                "emoji": "⌚",
                "brand": "AUDEMARS PIGUET STİLİ / BEYMEN SAAT",
                "name": "Royal Oak Siluetli 18K Pembe Altın Tonlu Sekizgen Bezel Lüks Kadın Kol Saati",
                "price": "38.950₺",
                "price_val": 38950.0,
                "sku": "LUX-TAK-201",
                "color": "18K Pembe Altın / Sedef Kadran",
                "store_url": "https://www.beymen.com/tr/kadin-saat-10126",
                "en_packshot": "macro studio photograph of an 18k rose gold octagonal bezel luxury wristwatch with mother-of-pearl dial worn on a female supermodel slender wrist in a pure solid white studio #FFFFFF",
            },
            "slot2": {
                "category_label": "Bilekte Pırlanta Su Yolu",
                "emoji": "✨",
                "brand": "ZEN PIRLANTA",
                "name": "3.00 Karat Görünümlü Baget & Yuvarlak Kesim Pırlanta Su Yolu Bileklik",
                "price": "42.500₺",
                "price_val": 42500.0,
                "sku": "LUX-TAK-202",
                "color": "Beyaz Altın / Pırlanta",
                "store_url": "https://www.zenpirlanta.com/pirlanta-bileklikler",
                "en_packshot": "macro studio photograph of a sparkling baguette and round-cut diamond tennis bracelet stacked next to a rose gold cuff worn on a female model wrist in a pure solid white studio #FFFFFF",
            },
            "slot3": {
                "category_label": "Boyunda Zümrüt & Pırlanta Kolye",
                "emoji": "📿",
                "brand": "ATASAY / ZEN PIRLANTA",
                "name": "18K Pembe Altın Zincirli Zümrüt & Pırlanta Hale Kolye",
                "price": "26.900₺",
                "price_val": 26900.0,
                "sku": "LUX-TAK-203",
                "color": "Zümrüt Yeşili / Pembe Altın",
                "store_url": "https://www.atasay.com/altin-kolye",
                "en_packshot": "macro studio photograph of an 18k rose gold chain necklace with an emerald-cut green emerald and diamond halo pendant worn on a female supermodel collarbone and neck in a pure solid white studio #FFFFFF",
            },
            "slot4": {
                "category_label": "Yüzde Damla Pırlanta Küpe",
                "emoji": "💎",
                "brand": "SWAROVSKI / ATASAY",
                "name": "Armut & Baget Kesim Kristal Pırlanta Sallantılı Lüks Küpe",
                "price": "8.450₺",
                "price_val": 8450.0,
                "sku": "LUX-TAK-204",
                "color": "Kristal Beyaz / Rose Gold",
                "store_url": "https://www.swarovski.com/tr-TR/c-0103/Categories/Jewelry/Earrings/",
                "en_packshot": "macro studio photograph of pear-shaped and baguette diamond drop earrings worn on a female supermodel ear beside her sculpted jawline in a pure solid white studio #FFFFFF",
            },
            "slot5": {
                "category_label": "Elde Zümrüt Kesim Yüzük",
                "emoji": "💍",
                "brand": "ZEN PIRLANTA",
                "name": "Emerald Kesim Tektaş & Yanları Baget Pırlanta 18K Altın Yüzük",
                "price": "34.900₺",
                "price_val": 34900.0,
                "sku": "LUX-TAK-205",
                "color": "18K Altın / D-Color Pırlanta",
                "store_url": "https://www.zenpirlanta.com/pirlanta-tektas-yuzukler",
                "en_packshot": "macro studio photograph of an emerald-cut diamond ring with tapered baguette side stones worn on a female supermodel slender finger in a pure solid white studio #FFFFFF",
            },
            "slot6": {
                "category_label": "Mankende Zümrüt İpek Elbise",
                "emoji": "💚",
                "brand": "VAKKO COUTURE",
                "name": "Zümrüt Yeşili %100 Saf İpek Saten Verev Kesim Gece Elbisesi",
                "price": "21.500₺",
                "price_val": 21500.0,
                "sku": "LUX-TAK-206",
                "color": "Zümrüt Yeşili",
                "store_url": "https://www.vakko.com/kadin-elbise/",
                "en_packshot": "editorial studio photograph of a deep emerald-green pure silk satin bias-cut evening gown worn on a female supermodel body in a pure solid white photography studio #FFFFFF",
            },
        },
        "hashtags": "#mücevher #lükssaat #pırlanta #altınbileklik #oldmoneyjewelry #quietluxury #luxurylife #reklam #işbirliğiyoktur",
    },

    # =========================================================================
    # 2. LÜKS MAKYAJ, GÜZELLİK & NİŞ PARFÜM (makyaj) — Chanel Velvet & Pearl Skin
    # =========================================================================
    {
        "id": "lux_makyaj_chanel_velvet_pearl_studio_02",
        "category": "makyaj",
        "gender_segment": "kadin",
        "is_3d_avatar": False,
        "title": "Vogue Beauty Beyaz Stüdyo: 'Pearl Glass Skin', Kadife Dudak & Bilekte İpek Parfüm Ritüeli 💄",
        "cover_kicker": "» LÜKS GÜZELLİK & PARFÜM • BEYAZ BEAUTY STÜDYO REJİSİ «",
        "cover_headline": "YÜZDE İNCİ IŞILTISI VE BİLEKTE PARFÜM İMZASI YARATAN 6 ÜRÜN",
        "spoken_hook_text": "Gerçek zenginlik cildin porselen ışıltısında, dudaktaki kadife dokunuşta ve yürürken bilekten yayılan niş parfüm izinde saklıdır!",
        "viral_hook": "💄 Saf beyaz beauty stüdyosunda süpermodelin yüzünde, dudaklarında ve bileğinde sergilenen 6 parçalık 'Pearl Skin & Velvet Lip' formülü! Kaydet 👇✨",
        "location_name": "Vogue Beauty Saf Beyaz Sonsuz Fon Fotoğraf Stüdyosu (#FFFFFF White Cyclorama Beauty Studio)",
        "camera_spec": "Hasselblad H6D-100c • 90mm f/2.8 Macro On-Face/Wrist + 85mm f/1.4 Beauty Portrait + 50mm f/1.4 Runway Walk",
        "act1_beat": "SAHNE 1 (YÜZDE VE BİLEKTE MİKRO-SERGİ): Süpermodelin elmacık kemiğinde inci aydınlatıcı, dudağında kadife ruj ve bileğinde altın bileklikle parfüm dokunuşu.",
        "act2_beat": "SAHNE 2 (MANKEN ÜZERİNDE BÜTÜNSEL DURUŞ): Şampanya ipek elbise içinde cam cilt dokusu ve 6 güzellik ikonu bir arada.",
        "act3_twist": "SAHNE 3 (YÜRÜRKEN FARK EDİLEN GÜZELLİK): Yürürken ışıkla parlayan porselen cilt ve ipeksi saçlar • Sephora & Beymen linklerini KAYDET!",
        "model_prompt_en": (
            "Ultra-photorealistic luxury beauty and fragrance campaign photograph shot on Hasselblad H6D-100c with 85mm f/1.4 lens "
            "inside a pure solid white cyclorama beauty studio (#FFFFFF seamless white background, Profoto beauty dish and ring light), "
            "gorgeous adult female supermodel with luminous pearl glass skin and natural skin pores, wearing an ivory champagne silk halter gown and gold cuff bracelet on her wrist, "
            "applying a gold-cased velvet rosewood lipstick to her lips while holding a crystal niche perfume bottle near her collarbone, "
            "zero 3D, zero cartoon, 8k Vogue Beauty studio editorial"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic macro beauty close-up portrait shot on Hasselblad H6D-100c 90mm f/2.8 macro lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white background, Profoto beauty dish lighting), "
                "real adult female supermodel with dewy pearl glass skin and visible natural skin pores raising her slender wrist and hand to her face, "
                "wearing an 18k gold cuff bracelet on her wrist while holding a luxury gold lipstick bullet against her rich velvet rose-berry lips, "
                "champagne pearl highlighter gleaming on her cheekbones and collarbone, zero 3D, zero cartoon, 8k Vogue Beauty close-up"
            ),
            (
                "Ultra-photorealistic medium-full luxury beauty lookbook photograph shot on Hasselblad H6D-100c 85mm f/1.4 prime lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background), "
                "wealthy real adult female supermodel dressed in a draped champagne-ivory silk satin gown, "
                "gracefully misting a crystal gold niche perfume bottle onto her inner wrist and neck, "
                "showcasing her radiant glass skin complexion, sculpted bronze cheekbones, velvet lips, and gold wrist jewelry in perfect harmony, "
                "zero 3D, zero cartoon, 8k editorial beauty photography"
            ),
            (
                "Ultra-photorealistic full-body dynamic catwalk motion beauty photograph shot on Hasselblad H6D-100c 50mm f/1.4 lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background and floor), "
                "real adult female supermodel walking confidently forward toward the camera mid-stride in a flowing champagne-ivory silk gown, "
                "voluminous glossy waves moving naturally in the studio breeze, her luminous glass skin, velvet lipstick, and gold bracelet on her wrist "
                "catching the crisp studio light in motion, zero 3D, zero cartoon, 8k runway beauty campaign"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "Yüzde İnci Işıltılı Fondöten",
                "emoji": "✨",
                "brand": "CHANEL BEAUTY / SEPHORA",
                "name": "Sublimage Le Teint & Les Beiges Işıltı Veren İpek Fondöten",
                "price": "3.450₺",
                "price_val": 3450.0,
                "sku": "LUX-MKJ-201",
                "color": "B20 Ivory Pearl Glow",
                "store_url": "https://www.sephora.com.tr/markalar/chanel/",
                "en_packshot": "macro studio photograph of luminous pearl glass skin foundation texture on a female supermodel cheekbone with the luxury glass foundation bottle held by her hand in a pure solid white studio #FFFFFF",
            },
            "slot2": {
                "category_label": "Dudakta Kadife Ruj",
                "emoji": "💄",
                "brand": "CHANEL / DIOR BEAUTY",
                "name": "Rouge Allure Velvet Altın Kılıflı İkonik Kadife Mat Ruj",
                "price": "2.390₺",
                "price_val": 2390.0,
                "sku": "LUX-MKJ-202",
                "color": "Bois de Rose / Velvet Berry",
                "store_url": "https://www.sephora.com.tr/markalar/dior/",
                "en_packshot": "macro studio photograph of a gold-cased velvet rosewood lipstick held by a female model slender fingers right next to her plush velvet-matte lips in a pure solid white studio #FFFFFF",
            },
            "slot3": {
                "category_label": "Elmacık Kemiğinde Aydınlatıcı",
                "emoji": "🌸",
                "brand": "GUERLAIN / SEPHORA",
                "name": "Terracotta Luminizer & Météorites Şampanya İnci Aydınlatıcı Pudra",
                "price": "2.950₺",
                "price_val": 2950.0,
                "sku": "LUX-MKJ-203",
                "color": "Champagne Pearl",
                "store_url": "https://www.sephora.com.tr/markalar/guerlain/",
                "en_packshot": "macro studio photograph of a gold compact champagne-pearl highlighter held at a female supermodel glowing cheekbone in a pure solid white studio #FFFFFF",
            },
            "slot4": {
                "category_label": "Bilekte & Boyunda Niş Parfüm",
                "emoji": "👑",
                "brand": "PARFUMS DE MARLY / BEYMEN",
                "name": "Delina Exclusif & Valaya Kristal Şişe Eau de Parfum (75 ml)",
                "price": "13.750₺",
                "price_val": 13750.0,
                "sku": "LUX-MKJ-204",
                "color": "Pudra Pembe & Altın",
                "store_url": "https://www.beymen.com/tr/kozmetik-parfum-10179",
                "en_packshot": "macro studio photograph of a luxury sculpted perfume flacon being misted onto a female supermodel inner wrist and neck in a pure solid white studio #FFFFFF",
            },
            "slot5": {
                "category_label": "Yüzde Altın Bakım Serumu",
                "emoji": "🧴",
                "brand": "LA MER / BEYMEN KOZMETİK",
                "name": "The Concentrate & Renewal Oil Hücresel Yenileyici Işıltı İksiri",
                "price": "9.850₺",
                "price_val": 9850.0,
                "sku": "LUX-MKJ-205",
                "color": "24K Altın İksir",
                "store_url": "https://www.beymen.com/tr/kozmetik-cilt-bakimi-10180",
                "en_packshot": "macro studio photograph of a luxury glass dropper applying golden radiance facial serum onto a female supermodel skin in a pure solid white studio #FFFFFF",
            },
            "slot6": {
                "category_label": "Bilekte İnce Altın Kelepçe",
                "emoji": "💛",
                "brand": "ATASAY / BEYMEN",
                "name": "14K Altın İtalyan Tasarım Beauty & Zarafet Bilekliği",
                "price": "15.900₺",
                "price_val": 15900.0,
                "sku": "LUX-MKJ-206",
                "color": "14K Sarı Altın",
                "store_url": "https://www.atasay.com/altin-bileklik",
                "en_packshot": "macro studio photograph of a sleek 18k yellow gold cuff bracelet worn on a female supermodel moisturized glowing wrist in a pure solid white studio #FFFFFF",
            },
        },
        "hashtags": "#lüksmakyaj #glassskin #nişparfüm #sephoratürkiye #beymenbeauty #oldmoneybeauty #luxurylife #reklam #işbirliğiyoktur",
    },

    # =========================================================================
    # 3. OLD MONEY & QUIET LUXURY KOMBİN (kombin) — Loro Piana Ivory & Cashmere Walk
    # =========================================================================
    {
        "id": "lux_kombin_loro_piana_ivory_walk_02",
        "category": "kombin",
        "gender_segment": "kadin",
        "is_3d_avatar": False,
        "title": "Loro Piana Estetiği Beyaz Stüdyo: Fildişi Kaşmir, Konyak Deri & Yürürken Konuşan Asalet 🧥",
        "cover_kicker": "» QUIET LUXURY KOMBİN • SAF BEYAZ PODYUM REJİSİ «",
        "cover_headline": "MANKEN ÜZERİNDE VE YÜRÜRKEN FARK EDİLEN 6 PARÇA SESSİZ LÜKS",
        "spoken_hook_text": "Sessiz lüks askıda dururken değil; mankenin üzerinde, bileğindeki saatle ve yürürken kumaşın aldığı kusursuz dalgayla anlaşılır!",
        "viral_hook": "🧥 Saf beyaz fotoğraf stüdyosunda kolda, yüzde ve yürürken sergilenen 6 parçalık 'Loro Piana Ivory & Cognac' kombin formülü! Kaydet 👇✨",
        "location_name": "Milano High-Fashion Saf Beyaz Sonsuz Fon Fotoğraf Stüdyosu (#FFFFFF White Cyclorama Studio)",
        "camera_spec": "Hasselblad H6D-100c • 85mm f/1.4 On-Wrist/Face + 50mm f/1.4 Full Lookbook + 35mm f/1.4 Runway Motion",
        "act1_beat": "SAHNE 1 (KOLDA VE YÜZDE MİKRO-SERGİ): Süpermodelin yüzünde kemik güneş gözlüğü, bileğinde deri kayışlı altın saat ve kaşmir kaban yakası.",
        "act2_beat": "SAHNE 2 (MANKEN ÜZERİNDE BÜTÜNSEL DURUŞ): Fildişi kaşmir kaban, ipek gömlek, palazzo pantolon ve konyak deri çantanın tam boy uyumu.",
        "act3_twist": "SAHNE 3 (YÜRÜRKEN FARK EDİLEN ZENGİNLİK): Kameraya doğru yürürken dalgalanan kaşmir kaban ve süet loafer adımı • Hemen KAYDET!",
        "model_prompt_en": (
            "Ultra-photorealistic full-body high-fashion lookbook photograph shot on Hasselblad H6D-100c with 50mm f/1.4 lens "
            "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background, Profoto parabolic lighting), "
            "wealthy adult female supermodel with natural skin texture, wearing an ivory double-faced cashmere trench coat over a champagne silk blouse, "
            "tailored cream wide-leg wool trousers, tortoiseshell sunglasses on her face, gold tank wristwatch on her wrist, "
            "carrying a cognac leather gold-lock handbag and stepping in cognac suede loafers, zero 3D, zero cartoon, 8k Loro Piana & Vogue studio lookbook"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic close-up fashion editorial portrait shot on Hasselblad H6D-100c 85mm f/1.4 lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white background, soft Profoto beauty dish light), "
                "real adult female supermodel with natural skin pores raising her hand to lightly touch her tortoiseshell oval sunglasses on her face, "
                "clearly showcasing a rectangular 18k gold tank watch with brown alligator strap on her wrist, gold hoop earrings on her ear, "
                "and the plush texture of an ivory cashmere coat lapel and champagne silk collar on her neck, zero 3D, zero cartoon, 8k close-up"
            ),
            (
                "Ultra-photorealistic medium-full fashion lookbook photograph shot on Hasselblad H6D-100c 50mm f/1.4 prime lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background), "
                "wealthy real adult female supermodel standing poised in a complete 6-piece quiet luxury ensemble: "
                "ivory double-faced cashmere coat draped over her shoulders, champagne silk button-down shirt, cream pleated wool trousers, "
                "structured cognac leather handbag held on her forearm next to her gold wristwatch, and cognac suede loafers, zero 3D, zero cartoon, 8k editorial"
            ),
            (
                "Ultra-photorealistic full-body dynamic catwalk motion photograph shot on Hasselblad H6D-100c 35mm f/1.4 lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background and floor), "
                "real adult female supermodel walking briskly and confidently forward toward the camera mid-stride, "
                "her ivory cashmere coat and wide-leg wool trousers flowing with natural kinetic movement, "
                "cognac leather handbag and gold wristwatch gleaming on her moving arm while her suede loafers step across the white studio floor, "
                "zero 3D, zero cartoon, 8k Milan runway photography"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "Mankende Fildişi Kaşmir Kaban",
                "emoji": "🧥",
                "brand": "MASSIMO DUTTI STUDIO / VAKKO",
                "name": "Fildişi Ekru Çift Yüzlü (Double-Faced) Yün & Kaşmir Kuşaklı Kaban",
                "price": "12.950₺",
                "price_val": 12950.0,
                "sku": "LUX-KMB-201",
                "color": "Fildişi Ekru",
                "store_url": "https://www.massimodutti.com/tr/kadin/palto-ve-trenckot-n1434",
                "en_packshot": "editorial studio photograph of an ivory double-faced wool cashmere coat worn draped over a female supermodel shoulders and torso in a pure solid white studio #FFFFFF",
            },
            "slot2": {
                "category_label": "Kolda Deri Kayışlı Altın Saat",
                "emoji": "⌚",
                "brand": "CARTIER TANK STİLİ / BEYMEN",
                "name": "18K Altın Kasalı & Taba Kroko Deri Kayışlı Dikdörtgen Klasik Saat",
                "price": "22.500₺",
                "price_val": 22500.0,
                "sku": "LUX-KMB-202",
                "color": "Altın / Konyak Deri",
                "store_url": "https://www.beymen.com/tr/kadin-saat-10126",
                "en_packshot": "macro studio photograph of a rectangular 18k gold tank wristwatch with cognac alligator leather strap worn on a female supermodel wrist beside a cashmere cuff in a pure solid white studio #FFFFFF",
            },
            "slot3": {
                "category_label": "Yüzde Kemik Güneş Gözlüğü",
                "emoji": "🕶️",
                "brand": "CELINE / BEYMEN EYEWEAR",
                "name": "Havana Kaplumbağa Desenli Gold Logolu Oval Güneş Gözlüğü",
                "price": "15.250₺",
                "price_val": 15250.0,
                "sku": "LUX-KMB-203",
                "color": "Havana Tortoiseshell / Gold",
                "store_url": "https://www.beymen.com/tr/kadin-aksesuar-gunes-gozlugu-10105",
                "en_packshot": "macro studio photograph of luxury Havana tortoiseshell oval sunglasses with gold temple hinge worn on a female supermodel face in a pure solid white studio #FFFFFF",
            },
            "slot4": {
                "category_label": "Mankende İpek Gömlek & Pantolon",
                "emoji": "👖",
                "brand": "VAKKO",
                "name": "Şampanya İpek Gömlek & Yüksek Bel Krem İtalyan Yün Palazzo Pantolon",
                "price": "8.950₺",
                "price_val": 8950.0,
                "sku": "LUX-KMB-204",
                "color": "Şampanya & Krem",
                "store_url": "https://www.vakko.com/kadin-pantolon/",
                "en_packshot": "editorial studio photograph of high-waisted cream pleated wool palazzo trousers and champagne silk blouse worn on a walking female supermodel in a pure solid white studio #FFFFFF",
            },
            "slot5": {
                "category_label": "Kolda Konyak Deri Çanta",
                "emoji": "👜",
                "brand": "BEYMEN COLLECTION",
                "name": "Konyak Taba Altın Kilitli Yapısal Hakiki Deri El & Kol Çantası",
                "price": "9.450₺",
                "price_val": 9450.0,
                "sku": "LUX-KMB-205",
                "color": "Konyak Taba / Gold",
                "store_url": "https://www.beymen.com/tr/kadin-canta-10014",
                "en_packshot": "macro studio photograph of a structured cognac tan leather top-handle handbag with gold clasp carried on a female supermodel wrist and forearm in a pure solid white studio #FFFFFF",
            },
            "slot6": {
                "category_label": "Ayakta Süet Summer Walk Loafer",
                "emoji": "👞",
                "brand": "LORO PIANA STİLİ / BEYMEN",
                "name": "Konyak Süet Deri Beyaz Kauçuk Tabanlı Yürüyüş Loafer Ayakkabı",
                "price": "6.850₺",
                "price_val": 6850.0,
                "sku": "LUX-KMB-206",
                "color": "Konyak Süet / Krem Taban",
                "store_url": "https://www.beymen.com/tr/kadin-ayakkabi-loafer-10042",
                "en_packshot": "close-up studio photograph of cognac suede slip-on loafers with cream soles worn on a female supermodel feet stepping mid-stride on a pure solid white studio floor #FFFFFF",
            },
        },
        "hashtags": "#oldmoneystyle #quietluxury #loropianastyle #kombinönerileri #kaşmirkaban #luxurylife #reklam #işbirliğiyoktur",
    },

    # =========================================================================
    # 4. ULTRA LÜKS OTEL & RESORT STİLİ (otel) — Lake Como & Bodrum White Resort
    # =========================================================================
    {
        "id": "lux_otel_como_villa_white_resort_02",
        "category": "otel",
        "gender_segment": "kadin",
        "is_3d_avatar": False,
        "title": "Villa d'Este & Bodrum Beyaz Resort Stüdyosu: Tatil Süiti, Bilekte Kelepçe & Resort Yürüyüşü 🌅",
        "cover_kicker": "» ULTRA LÜKS OTEL & RESORT STİLİ • BEYAZ STÜDYO REJİSİ «",
        "cover_headline": "5 YILDIZLI RESORT TATİLİNDE BİLEKTE VE ÜZERİNDE TAŞINAN 6 LÜKS DETAY",
        "spoken_hook_text": "Beş yıldızlı bir kraliyet süitinde tatil yaparken, elindeki kristal kadeh kadar bileğindeki altın kelepçe ve keten gömleğinin yürüyüşü konuşulur!",
        "viral_hook": "🌅 Ultra lüks tatil rotası ve saf beyaz stüdyoda kolda, yüzde ve yürürken sergilenen 6 parçalık 'Villa Resort' kombin & aksesuar linkleri! Kaydet 👇✨",
        "location_name": "Villa d'Este & Mandarin Oriental Saf Beyaz Resort Fotoğraf Stüdyosu (#FFFFFF White Studio)",
        "camera_spec": "Hasselblad H6D-100c • 85mm f/1.4 On-Wrist/Face + 50mm f/1.4 Resort Lookbook + 35mm f/1.4 Resort Catwalk",
        "act1_beat": "SAHNE 1 (KOLDA VE YÜZDE MİKRO-SERGİ): Kristal şampanya kadehi tutan bilekte altın/deri kelepçe, boyunda inci kolye ve yüzde güneş gözlüğü.",
        "act2_beat": "SAHNE 2 (MANKEN ÜZERİNDE BÜTÜNSEL DURUŞ): İtalyan beyaz keten resort takım, rafya deri çanta ve altın takıların süpermodel üzerindeki uyumu.",
        "act3_twist": "SAHNE 3 (YÜRÜRKEN FARK EDİLEN RESORT LÜKSÜ): Yürürken uçuşan saf keten gömlek ve parlayan bileklikler • Otel ve ürün linklerini KAYDET!",
        "model_prompt_en": (
            "Ultra-photorealistic luxury resort fashion and five-star hotel lifestyle photograph shot on Hasselblad H6D-100c with 50mm f/1.4 lens "
            "inside a bright pure solid white cyclorama photography studio (#FFFFFF seamless white background, sun-kissed Profoto studio lighting), "
            "wealthy adult female supermodel with radiant sun-kissed skin texture, wearing an unbuttoned crisp white Italian linen resort shirt over a silk bandeau, "
            "flowing ivory linen wide-leg resort trousers, gold and leather cuff bracelets on her wrist, baroque pearl necklace on her neck, "
            "holding a chilled crystal champagne flute and woven raffia leather tote bag, zero 3D, zero cartoon, 8k Conde Nast Traveler & Vogue Resort studio"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic macro close-up luxury resort portrait shot on Hasselblad H6D-100c 85mm f/1.4 lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white background, bright studio lighting), "
                "real adult female supermodel with glowing skin raising a chilled crystal champagne glass near her collarbone, "
                "clearly exhibiting an 18k gold cuff bracelet and turquoise-gold chain bracelet on her wrist, "
                "a natural baroque pearl necklace around her neck, and gold-rimmed resort sunglasses on her face, zero 3D, zero cartoon, 8k resort close-up"
            ),
            (
                "Ultra-photorealistic medium-full luxury resort lookbook photograph shot on Hasselblad H6D-100c 50mm f/1.4 prime lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white background), "
                "wealthy real adult female supermodel standing poised in a complete 5-star resort outfit: "
                "crisp white Italian linen resort shirt, ivory linen palazzo trousers, tan leather-trimmed raffia tote bag held on her arm, "
                "stacked gold cuff bracelets on her wrist, and baroque pearl jewelry on her neck, zero 3D, zero cartoon, 8k Vogue Resort lookbook"
            ),
            (
                "Ultra-photorealistic full-body dynamic resort catwalk motion photograph shot on Hasselblad H6D-100c 35mm f/1.4 lens "
                "inside a pure solid white cyclorama photography studio (#FFFFFF seamless white studio background and floor), "
                "real adult female supermodel walking effortlessly forward toward the camera mid-stride, "
                "her white Italian linen shirt and wide-leg resort trousers billowing softly in motion, "
                "stacked 18k gold bracelets gleaming on her moving wrist and leather resort sandals stepping forward, zero 3D, zero cartoon, 8k runway motion"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "Lüks Villa & Süit Otel",
                "emoji": "🏨",
                "brand": "MANDARIN ORIENTAL / LUXURY RESORT",
                "name": "Özel Sonsuzluk Havuzlu & Panoramik Teraslı Kraliyet Resort Villa Süiti",
                "price": "Gecelik Özel Süit",
                "price_val": 54000.0,
                "sku": "LUX-OTL-201",
                "color": "Beyaz Mermer & Turkuaz",
                "store_url": "https://www.booking.com/country/tr.tr.html",
                "en_packshot": "editorial studio showcase of a female supermodel holding a luxury hotel suite keycard and crystal champagne flute with stacked gold bracelets on her wrist in a pure solid white studio #FFFFFF",
            },
            "slot2": {
                "category_label": "Bilekte Altın & Deri Kelepçe",
                "emoji": "✨",
                "brand": "HERMÈS STİLİ / BEYMEN",
                "name": "Taba Deri & 18K Altın Kaplama Tokalı Resort Kelepçe Bileklik",
                "price": "17.450₺",
                "price_val": 17450.0,
                "sku": "LUX-OTL-202",
                "color": "Taba Deri / 18K Gold",
                "store_url": "https://www.beymen.com/tr/kadin-aksesuar-taki-10108",
                "en_packshot": "macro studio photograph of a tan leather and 18k gold hardware cuff bracelet stacked on a female supermodel sun-kissed wrist in a pure solid white studio #FFFFFF",
            },
            "slot3": {
                "category_label": "Boyunda Barok İnci Kolye",
                "emoji": "📿",
                "brand": "ATASAY / SWAROVSKI",
                "name": "Doğal Barok İnci & 14K Altın Deniz Kabuğu Detaylı Resort Kolye",
                "price": "11.950₺",
                "price_val": 11950.0,
                "sku": "LUX-OTL-203",
                "color": "Sedef İnci / Altın",
                "store_url": "https://www.atasay.com/altin-kolye",
                "en_packshot": "macro studio photograph of a natural baroque pearl and 18k yellow gold necklace worn on a female supermodel collarbone and neck in a pure solid white studio #FFFFFF",
            },
            "slot4": {
                "category_label": "Mankende İtalyan Keten Takım",
                "emoji": "🤍",
                "brand": "MASSIMO DUTTI / VAKKO MARE",
                "name": "%100 Saf İtalyan Keten Beyaz Oversize Gömlek & Palazzo Pantolon Resort Takım",
                "price": "7.450₺",
                "price_val": 7450.0,
                "sku": "LUX-OTL-204",
                "color": "Kırık Beyaz Keten",
                "store_url": "https://www.massimodutti.com/tr/kadin/gomlekler-ve-bluzlar-n1395",
                "en_packshot": "editorial studio photograph of a crisp white pure Italian linen resort shirt and wide-leg linen trousers worn on a female supermodel body in a pure solid white studio #FFFFFF",
            },
            "slot5": {
                "category_label": "Kolda Rafya & Deri Resort Çanta",
                "emoji": "👜",
                "brand": "BEYMEN CLUB / VAKKO",
                "name": "Doğal Rafya Örgü & Taba Deri Saplı Lüks Plaj ve Yacht Çantası",
                "price": "8.950₺",
                "price_val": 8950.0,
                "sku": "LUX-OTL-205",
                "color": "Doğal Rafya & Taba",
                "store_url": "https://www.beymen.com/tr/kadin-canta-10014",
                "en_packshot": "macro studio photograph of a woven natural raffia and cognac leather resort tote bag carried on a female supermodel arm beside her gold wrist bracelets in a pure solid white studio #FFFFFF",
            },
            "slot6": {
                "category_label": "Yüzde Gold Resort Gözlük",
                "emoji": "🕶️",
                "brand": "CHLOÉ / BEYMEN EYEWEAR",
                "name": "İnce Altın Çerçeveli & Degrade Kehribar Camlı Resort Güneş Gözlüğü",
                "price": "13.950₺",
                "price_val": 13950.0,
                "sku": "LUX-OTL-206",
                "color": "Altın / Sıcak Kehribar",
                "store_url": "https://www.beymen.com/tr/kadin-aksesuar-gunes-gozlugu-10105",
                "en_packshot": "macro studio photograph of gold-rimmed gradient amber resort sunglasses worn on a female supermodel face in a pure solid white photography studio #FFFFFF",
            },
        },
        "hashtags": "#luxuryhotels #resortstyle #tatilrotaları #oldmoneyvacation #bodrum #lakecomo #luxurylife #reklam #işbirliğiyoktur",
    },

    # =========================================================================
    # 5. SÜPER SPOR OTOMOBİL & SÜRÜŞ STİLİ (araba) — Ferrari Roma Spider & Gran Turismo Walk
    # =========================================================================
    {
        "id": "lux_araba_ferrari_roma_white_studio_02",
        "category": "araba",
        "gender_segment": "erkek",
        "is_3d_avatar": False,
        "title": "VIP Beyaz Otomotiv Stüdyosu: Süper Spor GT, Kolda Kronograf & Yürürken Centilmen Aurası 🏎️",
        "cover_kicker": "» SÜPER SPOR OTOMOBİL & SÜRÜŞ STİLİ • BEYAZ STÜDYO REJİSİ «",
        "cover_headline": "DİREKSİYONDA, BİLEKTE VE YÜRÜRKEN FARK EDİLEN 6 PARÇA CENTİLMEN LÜKSÜ",
        "spoken_hook_text": "Bir süper spor otomobilin gerçek ağırlığı sadece kaputun altında değil; sürücünün bileğindeki kronografta ve yürürken yaydığı özgüvende gizlidir!",
        "viral_hook": "🏎️ Saf beyaz otomotiv stüdyosunda kolda kronograf saat, yüzde sürüş gözlüğü ve yürürken sergilenen 6 parçalık 'Gran Turismo' stili! Kaydet 👇✨",
        "location_name": "VIP Saf Beyaz Sonsuz Fon Otomotiv Fotoğraf Stüdyosu (#FFFFFF White Cyclorama Car Studio)",
        "camera_spec": "Hasselblad H6D-100c • 85mm f/1.4 On-Wrist Chronograph + 50mm f/1.4 Car & Model + 35mm f/1.4 Dynamic Walk",
        "act1_beat": "SAHNE 1 (KOLDA VE YÜZDE MİKRO-SERGİ): Mankenin bileğinde titanyum kronograf saat, elinde süet ceket dokusu ve yüzünde polarize sürüş gözlüğü.",
        "act2_beat": "SAHNE 2 (MANKEN ÜZERİNDE BÜTÜNSEL DURUŞ): Süper spor GT otomobilin yanında lacivert süet ceket, fildişi kaşmir triko ve İtalyan loafer uyumu.",
        "act3_twist": "SAHNE 3 (YÜRÜRKEN FARK EDİLEN LÜKS): Otomobilin önünden kameraya doğru özgüvenle yürürken parlayan saat ve ceket • Hemen KAYDET!",
        "model_prompt_en": (
            "Ultra-photorealistic luxury automotive and menswear campaign photograph shot on Hasselblad H6D-100c with 50mm f/1.4 lens "
            "inside a massive pure solid white cyclorama automotive photography studio (#FFFFFF seamless white studio background and floor), "
            "charismatic adult male supermodel with natural skin pores and sharp jawline standing beside a silver-grey metallic Italian V8 Gran Turismo sports car, "
            "wearing a midnight-navy suede bomber jacket over an ivory cashmere polo knit, tailored stone-beige wool trousers, "
            "gold-bridge aviator sunglasses on his face, rose-gold chronograph wristwatch on his wrist, and cognac suede driving loafers, "
            "zero 3D, zero cartoon, 8k GQ & Architectural Digest automotive studio"
        ),
        "scene_prompts_en": [
            (
                "Ultra-photorealistic macro close-up gentleman driver portrait shot on Hasselblad H6D-100c 85mm f/1.4 lens "
                "inside a pure solid white cyclorama automotive photography studio (#FFFFFF seamless white studio background), "
                "charismatic real adult male supermodel with natural skin texture raising his wrist near his jawline to adjust his tortoiseshell-and-gold aviator sunglasses, "
                "clearly showcasing a luxury rose-gold and slate-blue dial mechanical chronograph wristwatch and braided leather bracelet on his wrist, "
                "midnight-navy suede jacket collar and ivory cashmere knit visible on his neck, zero 3D, zero cartoon, 8k watch & eyewear close-up"
            ),
            (
                "Ultra-photorealistic medium-full automotive fashion lookbook photograph shot on Hasselblad H6D-100c 50mm f/1.4 prime lens "
                "inside a pure solid white cyclorama automotive studio (#FFFFFF seamless white background), "
                "wealthy real adult male supermodel leaning with poised confidence beside the sculpted fender of a silver-grey Italian GT sports car, "
                "harmonizing all 6 luxury items on his body: midnight-navy suede driving jacket, ivory cashmere knit, rose-gold chronograph on his wrist, "
                "aviator sunglasses on his face, woven leather weekender bag in hand, and suede driving loafers, zero 3D, zero cartoon, 8k editorial"
            ),
            (
                "Ultra-photorealistic full-body dynamic motion photograph shot on Hasselblad H6D-100c 35mm f/1.4 lens "
                "inside a pure solid white cyclorama automotive photography studio (#FFFFFF seamless white background and floor), "
                "charismatic real adult male supermodel walking powerfully and confidently forward toward the camera mid-stride in front of the silver-grey GT sports car, "
                "his midnight-navy suede jacket open in motion over the ivory cashmere knit, the rose-gold chronograph watch gleaming on his swinging wrist "
                "and cognac suede loafers stepping across the white studio floor, zero 3D, zero cartoon, 8k runway motion"
            ),
        ],
        "items": {
            "slot1": {
                "category_label": "Stüdyoda Süper Spor GT",
                "emoji": "🏎️",
                "brand": "PORSCHE / GRAN TURISMO",
                "name": "Gümüş Metalik (GT Silver) Süper Spor Coupe & Taba Deri Kokpit Paketi",
                "price": "Özel Konfigürasyon",
                "price_val": 31500000.0,
                "sku": "LUX-ARB-201",
                "color": "GT Silver Metalik",
                "store_url": "https://www.porsche.com.tr/modeller/911/",
                "en_packshot": "editorial studio photograph of a male supermodel resting his hand with a chronograph watch on the sculpted silver-grey fender of a luxury GT sports car in a pure solid white studio #FFFFFF",
            },
            "slot2": {
                "category_label": "Kolda Rose Gold Kronograf",
                "emoji": "⌚",
                "brand": "VACHERON / BEYMEN SAAT",
                "name": "18K Pembe Altın Tonlu & Lacivert Kadranlı Otomatik Kronograf Sürüş Saati",
                "price": "92.500₺",
                "price_val": 92500.0,
                "sku": "LUX-ARB-202",
                "color": "Rose Gold / Lacivert Kadran",
                "store_url": "https://www.beymen.com/tr/erkek-aksesuar-saat-10075",
                "en_packshot": "macro studio photograph of an 18k rose-gold automatic chronograph wristwatch with navy tachymeter dial worn on a male supermodel wrist in a pure solid white studio #FFFFFF",
            },
            "slot3": {
                "category_label": "Mankende Lacivert Süet Ceket",
                "emoji": "🧥",
                "brand": "MASSIMO DUTTI STUDIO",
                "name": "Gece Laciverti %100 Hakiki İtalyan Süet Deri Sürüş & Bomber Ceket",
                "price": "15.950₺",
                "price_val": 15950.0,
                "sku": "LUX-ARB-203",
                "color": "Gece Laciverti Süet",
                "store_url": "https://www.massimodutti.com/tr/erkek/deri-ceketler-n1379",
                "en_packshot": "editorial studio photograph of a midnight-navy Italian suede bomber jacket worn over an ivory cashmere polo on a male supermodel torso in a pure solid white studio #FFFFFF",
            },
            "slot4": {
                "category_label": "Yüzde Polarize Sürüş Gözlüğü",
                "emoji": "🕶️",
                "brand": "CARTIER / PERSOL EYEWEAR",
                "name": "Altın Köprü Detaylı Kemik Çerçeve Polarize Sürüş Güneş Gözlüğü",
                "price": "16.450₺",
                "price_val": 16450.0,
                "sku": "LUX-ARB-204",
                "color": "Havana / Altın Köprü",
                "store_url": "https://www.beymen.com/tr/erkek-aksesuar-gunes-gozlugu-10073",
                "en_packshot": "macro studio photograph of luxury tortoiseshell and gold-bridge aviator driving sunglasses worn on a male supermodel face in a pure solid white studio #FFFFFF",
            },
            "slot5": {
                "category_label": "Elde Deri Weekender Çanta",
                "emoji": "💼",
                "brand": "BEYMEN COLLECTION",
                "name": "İtalyan Dokuma Deri (Intrecciato) Kokpit & Hafta Sonu Seyahat Çantası",
                "price": "14.500₺",
                "price_val": 14500.0,
                "sku": "LUX-ARB-205",
                "color": "Espresso Kahve Deri",
                "store_url": "https://www.beymen.com/tr/erkek-canta-10064",
                "en_packshot": "macro studio photograph of an espresso woven leather weekender bag held by a male supermodel hand with his wristwatch visible on his wrist in a pure solid white studio #FFFFFF",
            },
            "slot6": {
                "category_label": "Ayakta Süet Sürüş Loafer",
                "emoji": "👞",
                "brand": "VAKKO / SANTONI STİLİ",
                "name": "Konyak Süet Deri Esnek Kauçuk Tabanlı İtalyan Driving Loafer",
                "price": "9.750₺",
                "price_val": 9750.0,
                "sku": "LUX-ARB-206",
                "color": "Konyak Taba Süet",
                "store_url": "https://www.vakko.com/erkek-ayakkabi/",
                "en_packshot": "close-up studio photograph of cognac suede Italian driving loafers worn on a male supermodel feet stepping forward mid-stride on a pure solid white studio floor #FFFFFF",
            },
        },
        "hashtags": "#supercars #ferrariroma #porsche911 #oldmoneymen #gentlemanstyle #luxurycars #luxurylife #reklam #işbirliğiyoktur",
    },
]


def validate_studio_onbody_archetype(archetype: Dict[str, Any]) -> bool:
    """
    Şablonun %100 fotogerçekçi insan (`is_3d_avatar == False`), 3 aşamalı beyaz stüdyo
    sahne dizilimine (`scene_prompts_en` len == 3) ve 6 adet giyilebilir/manken üzeri
    pakete (`slot1`..`slot6`) sahip olduğunu doğrular.
    """
    if not isinstance(archetype, dict):
        return False
    if archetype.get("is_3d_avatar") is not False:
        return False
    prompts = archetype.get("scene_prompts_en")
    if not isinstance(prompts, list) or len(prompts) != 3:
        return False
    for p in prompts:
        if not isinstance(p, str) or "#FFFFFF" not in p or "zero 3D" not in p:
            return False
    items = archetype.get("items")
    if not isinstance(items, dict) or len(items) < 6:
        return False
    for idx in range(1, 7):
        slot = items.get(f"slot{idx}")
        if not isinstance(slot, dict):
            return False
        if not str(slot.get("store_url", "")).startswith("https://"):
            return False
        if "#FFFFFF" not in str(slot.get("en_packshot", "")):
            return False
    return True


def get_extended_studio_archetypes(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Saf Beyaz Fotoğraf Stüdyosu (#FFFFFF) Kolda, Bilekte, Yüzde ve Yürürken Lüks
    şablonlarının derin kopyasını (deep copy) döndürür.
    """
    all_items = copy.deepcopy(EXTENDED_STUDIO_ONBODY_ARCHETYPES)
    if category and category != "otomatik":
        return [a for a in all_items if a.get("category") == category]
    return all_items


def get_archetype_by_id(archetype_id: str) -> Optional[Dict[str, Any]]:
    """
    Verilen ID'ye göre şablonu bulur (yazım boşluğu toleranslı).
    """
    norm_target = (archetype_id or "").replace(" ", "").strip()
    for arch in EXTENDED_STUDIO_ONBODY_ARCHETYPES:
        if arch.get("id", "").replace(" ", "") == norm_target:
            return copy.deepcopy(arch)
    return None
