"""
Luxury Life AI (@Luxurylifeaibot) — 7/24 Kesintisiz Telegram Otomatik Tetikleme Daemon'u
----------------------------------------------------------------------------------------
Kullanıcının Telegram'dan (@Luxurylifeaibot) yazdığı HER MESAJI ve gönderdiği HER GÖRÜNTÜYÜ
(fotoğraf, video, ürün linki, düzeltme notu) birkaç saniye içinde yakalar:
- Kullanıcının peş peşe yazdığı mesajları (örn. fotoğraf + 'İsmini düzelt') bekleyip tek pakette birleştirir (4 sn debounce).
- Anında 2K GraphMotion Plus Reels videosunu kullanıcının kendi görüntüsüyle üretir ve 3 mesaj halinde Telegram'a teslim eder.
- Aynı zamanda GitHub Actions bulut kuyruğunu da senkronize tutar.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from telegram_luxury_ingestor import (
    BASE_DIR,
    load_tg_queue,
    poll_and_enqueue_telegram_requests,
    trigger_github_workflow_dispatch,
)


def run_daemon() -> None:
    print("💎 [@Sesliluksbot 7/24 Canlı Tetikleme Daemon'u Başlatıldı] Mesaj ve görüntüler dinleniyor...", flush=True)
    py_exe = sys.executable

    while True:
        try:
            q = poll_and_enqueue_telegram_requests(acknowledge=True)
            if q:
                # Kullanıcının fotoğrafın hemen ardından "İsmini düzelt" gibi ek bir mesaj yazabilmesi için 5 saniye bekle ve tekrar yokla
                time.sleep(5)
                q = poll_and_enqueue_telegram_requests(acknowledge=False)
                cat = q[-1].get("category", "otomatik") if q else "otomatik"
                trigger_github_workflow_dispatch(category=cat)
                print(f"🚀 [Canlı Tetikleme Yakalandı] Kuyrukta {len(q)} mesaj/görüntü var. GitHub Actions ve yerel 2K Reels üretimi başlatılıyor...", flush=True)
                subprocess.run(
                    [py_exe, str(BASE_DIR / "src" / "main.py"), "--output", str(BASE_DIR / "output" / "luxury_reel_final.mp4")],
                    cwd=str(BASE_DIR),
                    check=False,
                )
        except Exception as e:
            print(f"[Daemon Uyarısı]: {e}")
        time.sleep(3)


if __name__ == "__main__":
    run_daemon()
