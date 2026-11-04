"""
Luxury Life AI (@Luxurylifeaibot) — Anlık Telegram -> GitHub Actions Tetikleme Köprüsü
--------------------------------------------------------------------------------------
Telegram'dan (@Luxurylifeaibot) bir fotoğraf, ürün linki veya komut gönderildiği anda
saniyeler içinde yakalar, GitHub kuyruğuna yazar ve `workflow_dispatch` ile GitHub Actions'ı
anında ateşler (böylece 5-10 dakika içinde 2K Reels videosu hazır olup Telegram'a düşer).
"""
import argparse
import time
from telegram_luxury_ingestor import (
    load_tg_queue,
    poll_and_enqueue_telegram_requests,
    trigger_github_workflow_dispatch,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--poll-seconds", type=int, default=0, help="Belirtilen süre boyunca anlık dinle (0 = tek sefer)")
    args = parser.parse_args()

    if args.poll_seconds <= 0:
        q = poll_and_enqueue_telegram_requests(acknowledge=True)
        if q:
            cat = q[0].get("category", "otomatik")
            dispatched = trigger_github_workflow_dispatch(category=cat)
            print(f"🚀 [GitHub Actions Anlık Tetikleme]: Kuyruk={len(q)} | Kategori={cat} | Tetiklendi={dispatched}")
        return

    end_t = time.time() + args.poll_seconds
    while time.time() < end_t:
        before_len = len(load_tg_queue())
        q = poll_and_enqueue_telegram_requests(acknowledge=True)
        if len(q) > before_len:
            cat = q[-1].get("category", "otomatik")
            dispatched = trigger_github_workflow_dispatch(category=cat)
            print(f"🚀 [Anlık Telegram Tetikleme]: Kategori={cat} -> GitHub Actions={dispatched}")
        time.sleep(3)


if __name__ == "__main__":
    main()
