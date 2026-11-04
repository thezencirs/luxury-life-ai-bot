---
name: universal-reels-telegram-engine
description: Concept-independent 2K QHD+ (1440x2560 @ 30fps, 22 Mbps CRF 12) Remotion-physics Reels engine, 100% photorealistic AI visual standard (zero 3D/cartoon), atomic Zero-Repeat Double-Lock (Local + GitHub API), Pure Net Copy-Paste Telegram publisher, and Multi-User Telegram ingestor. Trigger whenever starting or running a social media / Reels / Telegram automation in ANY concept or niche.
---

# Universal 2K Remotion Reels & Telegram Automation Blueprint (`universal-reels-telegram-engine`)

Bu yetenek **konseptten bağımsızdır** (Moda, Lüks Yaşam, Otomobil, Emlak, Teknoloji, Takı/Saat, Gurme, Seyahat vb. her konseptte çalışır). Yeni bir konuşmada farklı bir konseptle başlandığında aynı teknik altyapıyı sıfır tekrarla uygular:

## 1. %100 Fotogerçekçi Görsel Standardı (Sıfır Animasyon / Sıfır 3D Karakter)
- Hangi konsept olursa olsun **3D CGI, Pixar, animasyon, çizgi film veya yapay avatar (`is_3d_avatar = True`) kullanımı kesinlikle yasaktır.**
- İnsan veya sahne üretimlerinde her zaman **Hasselblad H6D-100c 85mm f/1.4** editöryal fotoğrafçılık kalitesi, doğal cilt/materyal mikro-dokusu ve gerçekçi ışık fiziği kullanılır.

## 2. 2K QHD+ (1440×2560 @ 30fps) & Remotion Sinema Fiziği
- **Çözünürlük & Bitrate:** `1440x2560` (9:16 Dikey 2K QHD+), `30 fps`, H.264 `High@L5.1`, `-crf 12`, `-b:v 22M`, `-maxrate 30M`, `-bufsize 45M`, `-vf "unsharp=5:5:0.75:3:3:0.0"`, `44.1 kHz 320 kbps AAC` stereo ses.
- **Remotion Yay Fiziği (`_remotion_spring`):** Kart girişleri, HUD bantları ve kamera geçişlerinde doğrusal (`linear`) kayma yerine sönümlü harmonik yay fiziği (`damping=14, stiffness=120, mass=0.8`) kullanılır.
- **Optik Kare Geçişi & Film Light-Leak:** Çoklu sahne/kare geçişlerinde 180° shutter yönlü hareket bulanıklığı (`motion blur`), optik kare harmanlama (`cross-blend`) ve sıcak anamorfik film ışık sızıntısı (`light leak`) uygulanır.
- **Gündem & Öneri HUD Bandı:** Videonun üst ve alt sinematik HUD bantlarında o konseptin güncel trendi ve izleyiciye somut fayda sağlayan 1 cümlelik uzman önerisi yer alır.

## 3. Sıfır-Tekrar Çift Kilit (Zero-Repeat Double-Lock)
- Daha önce paylaşılan hiçbir içerik (`id`) veya görsel karesi tekrar paylaşılmaz.
- `output/zero_repeat_ledger.json` hem yerel diske hem de `GH_TOKEN` ile GitHub Contents API (`PUT .../contents/output/zero_repeat_ledger.json`) üzerinden anında buluta yazılır.
- GitHub Actions (`daily_reels.yml`) içinde `git add` asla tek satırda çoklu opsiyonel dosyayla çağrılmaz; `for f in ...; do [ -e "$f" ] && git add -f "$f"; done` döngüsü kullanılır.

## 4. Telegram Botunda Sadece Net Kopyala-Yapıştır Metin
- Telegram'a gönderilen açıklama mesajında `"📋 [KOPYALA-YAPIŞTIR 3/3]"`, `"👇 Aşağıdaki metni kopyalayın:"`, `"Kopyalanacak metin:"`, `"💬 Sabit Yorum:"` gibi **hiçbir ekstra başlık veya sarmalayıcı metin bulunmaz**.
- Mesaj **%100 saf paylaşım metninden** (Viral Hook + Gündem/Uzman Önerisi + Numaralı Liste/Linkler + Hashtagler) oluşur; tek dokunuşla kopyalanıp doğrudan Instagram/TikTok/YouTube'a yapıştırılır.

## 5. Çoklu Kullanıcı Telegram İçerik/Link İşleme
- Botu kullanan yönetici veya **herhangi bir Telegram kullanıcısı (`requester_chat_id`)** bota link, fotoğraf veya konsept/içerik talebi attığında:
  1. `cid` kısıtlaması olmadan kabul edilir ve `output/telegram_pending_queue.json` içine alınır.
  2. Soğuma süresi (`cooldown`) otomatik olarak bypass edilir.
  3. İçerik kategorisi otomatik algılanarak %100 fotogerçekçi görsel/model ile 2K Reels hazırlanır ve hem gönderen kullanıcıya (`requester_chat_id`) hem yöneticiye teslim edilir.
