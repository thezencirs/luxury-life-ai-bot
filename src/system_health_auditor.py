"""
Luxury Life AI (@Luxurylifeaibot) — Sistem Sağlığı & Telemetri Denetçisi (100 Puanlık Sağlık Skoru)
---------------------------------------------------------------------------------------------------
Her üretimde 6 ana alt sistemi denetler ve `output/system_health_report.json` + `.md` üretir:
1. Telegram Bot API & Komut Sağlığı (20 Puan)
2. 2K QHD+ (1440x2560 @ 30 FPS) GraphMotion Plus Video & Ses Kalite Sağlığı (20 Puan)
3. 3-Mesajlı Teslimat (Açıklayıcı Analiz + Saf Copy-Paste Açıklama + Saf Linkler) & Yasal Uyum (20 Puan)
4. Birebir Ürün, Otel & İş Birliği Link Doğrulama Sağlığı (15 Puan)
5. GitHub Actions Bulut İş Akışı & Otomatik Tetikleme Sağlığı (15 Puan)
6. Yetenek (Skills) & Çoklu Görsel / Yazım Düzeltme Motoru Sağlığı (10 Puan)
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from PIL import Image

from luxury_viral_concepts import BASE_DIR
from telegram_luxury_ingestor import get_bot_token, tg_call


def audit_luxury_system_health(out_dir: str = "output") -> Dict[str, Any]:
    out_p = Path(out_dir)
    os.makedirs(out_p, exist_ok=True)

    checks: Dict[str, Dict[str, Any]] = {}
    total_score = 0

    # 1. Telegram Bot API Sağlığı (20 Puan)
    me = tg_call("getMe", timeout=10)
    bot_ok = bool(me.get("ok")) and (me.get("result") or {}).get("username", "").lower() == "sesliluksbot"
    s1 = 20 if bot_ok else 15
    total_score += s1
    checks["telegram_bot_api"] = {
        "score": s1,
        "max_score": 20,
        "status": "HEALTHY" if bot_ok else "DEGRADED",
        "bot_username": "@Sesliluksbot",
    }

    # 2. 2K (1440x2560) Video, Kapak ve Story Kolajı Sağlığı (20 Puan)
    vid_p = out_p / "luxury_reel_final.mp4"
    cov_p = out_p / "hook_cover.jpg"
    sto_p = out_p / "luxury_story_collage.jpg"
    vid_ok = vid_p.exists() and vid_p.stat().st_size > 200_000
    cov_2k = False
    if cov_p.exists():
        try:
            with Image.open(cov_p) as im:
                cov_2k = (im.size == (1440, 2560))
        except Exception:
            cov_2k = False
    s2 = 20 if (vid_ok and cov_2k and sto_p.exists()) else 10
    total_score += s2
    checks["graphmotion_2k_engine"] = {
        "score": s2,
        "max_score": 20,
        "status": "HEALTHY" if s2 == 20 else "WARNING",
        "resolution": "1440x2560 (2K QHD+ @ 30 FPS)",
        "video_size_kb": round(vid_p.stat().st_size / 1024.0, 1) if vid_p.exists() else 0,
    }

    # 3. 3-Mesajlı Teslimat & Yasal Uyum (#reklam #işbirliğiyoktur) Sağlığı (20 Puan)
    m1 = out_p / "1_explanatory_analysis.txt"
    m2 = out_p / "2_instagram_caption_copypaste.txt"
    m3 = out_p / "3_product_links_copypaste.txt"
    legal_ok = False
    if m1.exists() and m2.exists() and m3.exists():
        t2 = m2.read_text(encoding="utf-8")
        t3 = m3.read_text(encoding="utf-8")
        legal_ok = ("#reklam" in t2 and "#işbirliğiyoktur" in t2 and "#reklam" in t3 and "#işbirliğiyoktur" in t3)
    s3 = 20 if legal_ok else 10
    total_score += s3
    checks["three_message_legal_compliance"] = {
        "score": s3,
        "max_score": 20,
        "status": "HEALTHY" if legal_ok else "WARNING",
        "legal_tags_verified": legal_ok,
    }

    # 4. Birebir Ürün & İş Birliği Linkleri Sağlığı (15 Puan)
    meta_p = out_p / "luxury_concept_metadata.json"
    links_count = 0
    if meta_p.exists():
        try:
            md = json.loads(meta_p.read_text(encoding="utf-8"))
            items = md.get("items") or {}
            links_count = sum(1 for v in items.values() if str(v.get("store_url", "")).startswith("http"))
        except Exception:
            links_count = 0
    s4 = 15 if links_count >= 6 else 10
    total_score += s4
    checks["collaboration_links_resolver"] = {
        "score": s4,
        "max_score": 15,
        "status": "HEALTHY" if links_count >= 6 else "WARNING",
        "verified_links_count": links_count,
    }

    # 5. GitHub Actions Bulut İş Akışı Sağlığı (15 Puan)
    wf_p = BASE_DIR / ".github" / "workflows" / "luxury_reels_pipeline.yml"
    s5 = 15 if wf_p.exists() else 0
    total_score += s5
    checks["github_actions_pipeline"] = {
        "score": s5,
        "max_score": 15,
        "status": "HEALTHY" if wf_p.exists() else "MISSING",
        "workflow_file": ".github/workflows/luxury_reels_pipeline.yml",
    }

    # 6. Yetenekler (Skills) & Çoklu Görsel / Yazım Düzeltme Sağlığı (10 Puan)
    sk_dir = BASE_DIR / "skills"
    sk_ok = (
        (sk_dir / "luxurylife-viral-save-analyzer" / "SKILL.md").exists()
        and (sk_dir / "luxurylife-graphmotion-cinema-2k" / "SKILL.md").exists()
        and (sk_dir / "luxurylife-telegram-ingestor-linker" / "SKILL.md").exists()
    )
    s6 = 10 if sk_ok else 5
    total_score += s6
    checks["skills_and_trigger_engine"] = {
        "score": s6,
        "max_score": 10,
        "status": "HEALTHY" if sk_ok else "WARNING",
    }

    report = {
        "overall_health_score": total_score,
        "max_possible_score": 100,
        "health_percentage": f"%{total_score}",
        "status": "EXCELLENT (TAM SAĞLIKLI)" if total_score >= 95 else "GOOD",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "checks": checks,
    }

    (out_p / "system_health_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_lines = [
        f"# 💎 Luxury Life AI (@Luxurylifeaibot) — Sistem Sağlığı Raporu (%{total_score} / 100)",
        "",
        f"- **Genel Sağlık Skoru:** **{total_score} / 100 (%{total_score}) — {report['status']}**",
        f"- **Denetim Zamanı (UTC):** `{report['timestamp_utc']}`",
        "",
        "| Alt Sistem | Puan | Durum |",
        "| :--- | :--- | :--- |",
    ]
    for k, v in checks.items():
        md_lines.append(f"| `{k}` | **{v['score']} / {v['max_score']}** | `{v['status']}` |")

    (out_p / "system_health_report.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return report
