"""
Luxury Life AI (@Luxurylifeaibot) — Ana Orkestrasyon Motoru
-----------------------------------------------------------
1) @Luxurylifeaibot Telegram kuyruğunu kontrol eder (kullanıcının gönderdiği takı, makyaj, kombin,
   otel, araba fotoğraf/video ve ürün linklerini yakalar).
2) Kaydetme oranı yüksek (High-Save-Rate) viral kanca, kamera açısı, mekan ve %100 gerçekçi model kurgusunu hazırlar.
3) 2K QHD+ (1440x2560 @ 30 FPS) GraphMotion Plus Reels videosunu ve kapak/story görsellerini üretir.
4) @Luxurylifeaibot üzerinden:
   - Mesaj 1: Copy-Paste Harici Açıklayıcı Reji & Kaydetme Oranı Analizi
   - Mesaj 2: Saf Instagram Açıklama Copy-Paste (#reklam #işbirliğiyoktur dahil)
   - Mesaj 3: Saf Birebir Ürün & İş Birliği Linkleri Copy-Paste (#reklam #işbirliğiyoktur dahil)
   olarak teslim eder.
"""
import argparse
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from luxury_viral_concepts import select_luxury_concept
from render_luxury_reels import render_luxury_graphmotion_reel
from system_health_auditor import audit_luxury_system_health
from telegram_luxury_ingestor import (
    ensure_concept_assets_ready,
    poll_and_enqueue_telegram_requests,
    pop_next_telegram_custom_concept,
)
from telegram_luxury_publisher import (
    configure_luxury_bot_profile,
    deliver_luxury_package_to_telegram,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default=os.environ.get("LUXURY_CATEGORY", "otomatik"))
    parser.add_argument("--output", default="output/luxury_reel_final.mp4")
    parser.add_argument("--only-if-telegram-pending", action="store_true", help="Sadece Telegram kuyruğunda yeni mesaj varsa üret")
    parser.add_argument("--setup-bot", action="store_true", help="@Luxurylifeaibot profil ve komutlarını yapılandır")
    parser.add_argument("--no-telegram-publish", action="store_true", help="Telegram gönderimini atla (yalnızca yerel test)")
    args = parser.parse_args()

    out_dir = os.path.dirname(args.output) or "output"
    os.makedirs(out_dir, exist_ok=True)

    if args.setup_bot:
        cfg = configure_luxury_bot_profile()
        print(f"🤖 [@Luxurylifeaibot Profil Yapılandırması]: {cfg}")

    # Önce @Luxurylifeaibot üzerinde bekleyen kullanıcı mesajı / fotoğrafı / ürün linki var mı bak
    custom_concept = pop_next_telegram_custom_concept()

    if args.only_if_telegram_pending and custom_concept is None:
        print("ℹ️ [Hızlı Telegram Kuyruk Kontrolü] @Luxurylifeaibot üzerinde bekleyen yeni talep yok, adım temiz şekilde tamamlandı.")
        return

    concept = select_luxury_concept(force_category=args.category, custom_concept=custom_concept)
    print(f"💎 [Seçilen Lüks Konsept]: {concept['id']} ({concept['category'].upper()}) — {concept['title']}")

    concept = ensure_concept_assets_ready(concept, use_cloud_ai=True)
    render_info = render_luxury_graphmotion_reel(concept, output_mp4=args.output, watermark="@luxurylifeaibot")
    print(f"🎬 [2K GraphMotion Plus Reels Hazır]: {render_info}")

    if not args.no_telegram_publish:
        deliver_luxury_package_to_telegram(concept, out_dir=out_dir)

    health = audit_luxury_system_health(out_dir=out_dir)
    print(f"🩺 [Sistem Sağlığı Skoru]: %{health['overall_health_score']} ({health['status']})")


if __name__ == "__main__":
    main()
