---
name: luxurylife-viral-save-analyzer
description: Analyzes top-performing, high-save-rate (kaydetme oranı yüksek) Instagram Luxury Reels across 5 verticals (Jewelry/Watches, Luxury Makeup/Beauty, Quiet Luxury Outfits, 5-Star Palace Hotels, Exotic Supercars) and generates scroll-stopping hooks, camera angles, luxury locations, and 3-act screenplays for @Luxurylifeaibot.
---

# Luxury Life AI — Viral Hook & High-Save-Rate Reels Analyzer Skill (`luxurylife-viral-save-analyzer`)

## Core Mandate
1. **High-Save-Rate (Kaydetme Oranı Yüksek) Psychological Triggers:**
   Every Reel produced for `@Luxurylifeaibot` is engineered around the 4 proven Instagram algorithm signals (**Save Rate > 8%**, **Watch-Time Retention > 110%**, **DM Share Rate**, **Comment Velocity**):
   - **Reference Value Trigger (Kaydetme Kancası):** Give structured, concrete luxury blueprints (exact 6-item breakdown, brand + model + price + SKU, lens/angle recipe, or suite/location checklist) so viewers *must* tap **Save (Kaydet)** to reference later.
   - **0.0s – 1.2s Scroll-Stopper Visual & Verbal Hook:** Open with a bold magazine cover hook (`hook_cover.jpg`) and a curiosity-gap headline (e.g., *"Nişantaşı ve Place Vendôme’da %1’lik Dilimin Asla Söylemediği 6 Detay"*, *"Servet Harcamadan 500.000₺’lik Old Money Aurası Yaratan Renk ve Materyal Formülü"*).
   - **Seamless Loop Architecture:** The final 1.2 seconds resolves back into the opening frame’s color/audio cadence with a prompt that encourages re-watching (*"3. parçadaki detayı kaçırdıysan başa sar"*).

2. **5 Core Luxury Life Verticals & Ideal Camera / Location / Model Direction:**
   Whenever the user sends raw material or triggers a post on `@Luxurylifeaibot`, automatically classify and apply the exact cinematic recipe:

   | Kategori Kodu | Lüks Dikey Alan | İdeal Kamera & Lens Açısı | İkonik Lüks Mekanlar | Model & Sahne Rejisi |
   | :--- | :--- | :--- | :--- | :--- |
   | **`taki`** | Mücevher & Yüksek Saatçilik (Jewelry & Watches) | `100mm f/2.8 Macro` kadife ışık kırılması + `85mm f/1.4` altın saat boyun/bilek portresi | Place Vendôme Paris, Monaco Casino Terası, Boğaz Yalısı Mermer Salon | İpek siyah/şampanya gece elbisesi veya kaşmir boğazlı triko üzerinde pırlanta/altın parıltısı |
   | **`makyaj`** | Lüks Makyaj, Kozmetik & Niş Parfüm (Luxury Beauty) | `90mm f/2.8 Macro` mermer vanity doku/swatch + `85mm f/1.4` ayna karşısı golden-hour | Hôtel Plaza Athénée Paris Mermer Banyo, Milano Penthouse Vanity | İpek bornoz veya haute couture hazırlık sahnesi, cam cilt (glass skin) ve kadife dudak dokusu |
   | **`kombin`** | Old Money & Quiet Luxury Kombinler (Haute Couture) | `85mm f/1.4 Prime` tam boy (head-to-toe) yürüyüş + alçak podyum (low-angle street) | Via Monte Napoleone Milano, Nişantaşı Abdi İpekçi, St. Moritz, Lake Como | %100 fotogerçekçi insan süpermodel, 6 parçanın 1:1 dekupe kartlarıyla birebir eşleşen yürüyüşü |
   | **`otel`** | Ultra Lüks Oteller, Süitler & Tatil Rotaları (5-Star Hotels) | `24mm f/1.4 Tilt-Shift` mimari sonsuzluk havuzu/teras + `50mm f/1.2` POV yürüyüş | Amanruya Bodrum, Çırağan Palace, Mandarin Oriental Bosphorus, Villa d'Este Como | Boğaz veya İtalyan gölü manzaralı terasta sabah kahvaltısı / gün batımı şampanya terası |
   | **`araba`** | Süper Spor & Ultra Lüks Otomobiller (Supercars) | `35mm f/1.4 Low-Angle Rolling` dinamik rampa + kokpit deri/saat POV + dış cephe | Monaco Grand Prix Virajı, İsviçre Alpleri, Bebek-Zorlu Gece Işıkları | Aracın dış renk paletiyle (British Racing Green, GT Silver, Nero Daytona) uyumlu Old Money kombinli model |

3. **Mandatory 3-Part Telegram Output Structure:**
   - **Part 1 (Explanatory Analysis — Non-Copy-Paste):** Explains the viral concept, why its save rate is high, the chosen camera angle, lighting, location, and model direction.
   - **Part 2 (Pure Copy-Paste Instagram Caption):** Ready to paste in one tap with hook, luxury breakdown, save CTA, hashtags, and mandatory legal notice (`#reklam #işbirliğiyoktur`).
   - **Part 3 (Pure Copy-Paste Product & Collaboration Links):** Ready to paste in First Comment / Story / DM with exact validated store links and mandatory legal notice (`#reklam #işbirliğiyoktur`).
