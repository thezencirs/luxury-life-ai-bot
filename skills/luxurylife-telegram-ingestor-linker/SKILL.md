---
name: luxurylife-telegram-ingestor-linker
description: Telegram (@Luxurylifeaibot) raw material & product link ingestor, exact store/collaboration link resolver, and 3-message publisher (Explanatory Guide + Pure Copy-Paste Caption + Pure Copy-Paste Links with mandatory Turkish #reklam #işbirliğiyoktur legal disclosure).
---

# Luxury Life AI — Telegram Ingestor, Exact Product Linker & 3-Message Publisher Skill (`luxurylife-telegram-ingestor-linker`)

## Core Mandate
1. **Telegram Bot Identity & Fast Cloud Trigger (`@Luxurylifeaibot`):**
   - **Bot Username:** `@Luxurylifeaibot`
   - **Bot Token:** `9244899175:AAGEkK0KD_sMxMB_wJaS_4Mlrjh8IGLgr7c`
   - **Workflow Turnaround:** Triggered immediately via GitHub Actions (`workflow_dispatch`, local watcher bridge, or 5-minute fast queue poll `*/5 * * * *`) so that any material sent by the user on Telegram is rendered into a 2K Reels video and delivered back to Telegram within **5 to 10 minutes**.

2. **Exact Product Matching & Brand Collaboration Links:**
   - Whenever the user sends product URLs, product names, photos, or raw clips (jewelry, makeup, outfits, hotels, cars):
     - Scrape exact metadata (Brand, Product Name, Price, SKU, Image) from provided URLs.
     - For items identified from photos/text, resolve direct, verified clickable store & collaboration links (Beymen, Sephora Türkiye, Vakko, Swarovski, Atasay, Zen Pırlanta, Trendyol Luxury/Designer, Zara, Massimo Dutti, Mandarin Oriental, Four Seasons, Porsche, Mercedes-Benz, Chrono24).

3. **Strict 3-Message Telegram Delivery + Mandatory Legal Notice:**
   After sending the visual assets (`hook_cover.jpg`, `luxury_story_collage.jpg`, and `luxury_reel_final.mp4`), send **3 separate text messages**:
   - **Message 1 (Açıklayıcı Reji & Viral Analiz Notu — Copy-Paste Harici):** Detailed breakdown of why this concept achieves high save rates, camera angle/lens choice, location/model setup, and posting instructions.
   - **Message 2 (Açıklama Copy-Paste — Pure Instagram Caption):** 100% pure copy-paste caption text (ZERO wrapper headers like `"Kopyalanacak metin:"`). Must include the mandatory legal notice:
     `⚖️ Yasal Uyarı: Bu paylaşım herhangi bir ticari iş birliği veya sponsorluk içermez; tamamen lüks yaşam/stil önerisi ve bilgilendirme amaçlıdır. Markalar göründüğü için yasal zorunluluk gereği #reklam #işbirliğiyoktur`
   - **Message 3 (Linkler Copy-Paste — Pure Product & Collaboration Links):** 100% pure copy-paste link list (1️⃣..6️⃣ Brand, Model, Price, Code & Direct Link) plus the mandatory `#reklam #işbirliğiyoktur` legal notice.
