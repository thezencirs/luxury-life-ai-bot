"""
Luxury Life AI (@Luxurylifeaibot) — 2K QHD+ (1440x2560 @ 30 FPS) GraphMotion Plus & Sinema Reels Motoru
-------------------------------------------------------------------------------------------------------
Standart düz kolajın ötesine geçen GraphMotion Plus akışı:
1) Act I (0.0s - 0.45s): Dergi Kapağı Scroll-Stopper Hook (hook_cover.jpg)
2) Act II (0.45s - 5.20s): Obsidian & Champagne Gold Glassmorphism Bento + Specular Işık Dalgası + Yaylanmalı (Spring) 6'lı Ürün/Detay Akışı
3) Act III (5.20s - 11.00s): 3 Adımlı Gimbal Parallax Fotogerçekçi Model / Mekan / Otomobil Sinema Sahnesi + Kamera Açısı & Kaydetme Kancası HUD
"""
import math
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from luxury_audio_engine import generate_luxury_soundtrack
from realistic_cinema_optics import (
    apply_organic_camera_breathing,
    apply_studio_contact_shadow_card,
    enhance_frame_with_real_optics,
)

W, H = 1440, 2560
SCALE = W / 1080.0
FPS = 30


def S(val: float) -> int:
    return int(round(val * SCALE))


def _remotion_spring(
    t: float,
    damping: float = 14.0,
    stiffness: float = 120.0,
    mass: float = 0.8,
) -> float:
    """
    Remotion `spring({ frame, fps, config: { damping: 14, stiffness: 120, mass: 0.8 } })`
    fizik motorunun birebir harmonik salınım denklemi.
    """
    if t <= 0.0:
        return 0.0
    omega0 = math.sqrt(stiffness / max(0.001, mass))
    zeta = damping / (2.0 * math.sqrt(stiffness * max(0.001, mass)))
    if zeta < 1.0:
        omega_d = omega0 * math.sqrt(1.0 - zeta * zeta)
        env = math.exp(-zeta * omega0 * t)
        val = 1.0 - env * (
            math.cos(omega_d * t) + (zeta / math.sqrt(1.0 - zeta * zeta)) * math.sin(omega_d * t)
        )
    else:
        val = 1.0 - (1.0 + omega0 * t) * math.exp(-omega0 * t)
    return float(max(0.0, min(1.12, val)))


def _apply_180deg_shutter_blur(card_im: Image.Image, speed_px: float) -> Image.Image:
    """
    180° Shutter Angle sinematik hareket bulanıklığı (Motion Blur):
    Kart yüksek hızla sahneye girerken hız vektörüne orantılı yumuşak bulanıklık uygular.
    """
    if speed_px < 18.0:
        return card_im
    radius = min(4.5, speed_px / 65.0)
    return card_im.filter(ImageFilter.GaussianBlur(radius=radius))


def _apply_film_light_leak(
    frame_rgb: Image.Image,
    intensity: float,
    sweep_pos: float = 0.5,
) -> Image.Image:
    """
    Sahne geçişlerinde (Act II -> Act III ve 3 adımlı Gimbal kesmelerinde)
    sıcak kehribar/şampanya altın Anamorfik Film Light-Leak (Işık Sızıntısı) uygular.
    """
    if intensity <= 0.01:
        return frame_rgb
    arr = np.array(frame_rgb, dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = xx / float(W)
    ny = yy / float(H)

    diag = nx * 0.78 + ny * 0.22
    band = np.exp(-((diag - sweep_pos) ** 2) / 0.032)
    corner_glow = np.exp(-(((nx - 0.12) ** 2 + (ny - 0.18) ** 2) / 0.11))

    leak = np.clip(band * 0.85 + corner_glow * 0.45, 0.0, 1.0) * float(intensity)
    arr[:, :, 0] = np.clip(arr[:, :, 0] + leak * 245.0, 0.0, 255.0)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + leak * 182.0, 0.0, 255.0)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + leak * 92.0, 0.0, 255.0)
    return Image.fromarray(arr.astype(np.uint8), mode="RGB")


def ease_out_back(t: float) -> float:
    return _remotion_spring(t * 0.55, damping=14.0, stiffness=120.0, mass=0.8)


def ease_in_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2


def get_ffmpeg_exe() -> str:
    sys_ff = shutil.which("ffmpeg")
    if sys_ff:
        return sys_ff
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def get_font(size_1080: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    size = S(size_1080)
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def enhance_luxury_micro_contrast(img: Image.Image, is_cutout: bool = False) -> Image.Image:
    has_alpha = img.mode == "RGBA"
    if has_alpha:
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
    else:
        rgb = img.convert("RGB")

    rgb = ImageEnhance.Contrast(rgb).enhance(1.08 if is_cutout else 1.10)
    rgb = ImageEnhance.Color(rgb).enhance(1.09 if is_cutout else 1.12)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.5, percent=135, threshold=2))

    if has_alpha:
        r2, g2, b2 = rgb.split()
        return Image.merge("RGBA", (r2, g2, b2, a))
    return rgb


def _tr_upper(s: str) -> str:
    return (s or "").replace("i", "İ").replace("ı", "I").upper()


def _draw_pill(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill_rgba: tuple,
    text_rgba: tuple,
    pad_x: int,
    pad_y: int,
    radius: int,
    outline_rgba: tuple = None,
    outline_width: int = 0,
) -> None:
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except Exception:
        tw = int(len(text) * S(16))
        th = S(28)
    half_w = min((W - S(44)) // 2, (tw // 2) + pad_x)
    half_h = (th // 2) + pad_y
    rect = (cx - half_w, cy - half_h, cx + half_w, cy + half_h)
    draw.rounded_rectangle(rect, radius=radius, fill=fill_rgba, outline=outline_rgba, width=outline_width)
    draw.text((cx, cy), text, fill=text_rgba, font=font, anchor="mm")


def create_obsidian_gold_stage(watermark_text: str = "@luxurylifeaibot") -> Image.Image:
    """
    2K (1440x2560) çözünürlükte Saf Beyaz Sonsuz Fon (Pure White Cyclorama #FFFFFF) &
    Profoto Softbox + 18K Şampanya Altın Çerçeveli Fotoğraf Stüdyosu sahnesi oluşturur.
    """
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx - W * 0.5) / (W * 0.62)
    ny = (yy - H * 0.44) / (H * 0.58)
    dist = np.clip(np.sqrt(nx * nx + ny * ny), 0.0, 1.35) / 1.35
    smooth = dist * dist * (3.0 - 2.0 * dist)

    # Merkezde saf beyaz stüdyo spotu (255, 255, 255) -> Kenarlarda yumuşak stüdyo sonsuz fon (244, 241, 235)
    r_ch = (255.0 - 11.0 * smooth).astype(np.uint8)
    g_ch = (255.0 - 14.0 * smooth).astype(np.uint8)
    b_ch = (255.0 - 20.0 * smooth).astype(np.uint8)
    a_ch = np.full((H, W), 255, dtype=np.uint8)
    bg = Image.fromarray(np.dstack([r_ch, g_ch, b_ch, a_ch]), mode="RGBA")

    draw = ImageDraw.Draw(bg)
    # Çift katmanlı 18K Şampanya Altın Fotoğraf Stüdyosu Çerçevesi (Filigransız tertemiz beyaz stüdyo)
    draw.rounded_rectangle(
        (S(16), S(16), W - S(16), H - S(16)),
        radius=S(28),
        outline=(198, 160, 88, 240),
        width=S(3),
    )
    draw.rounded_rectangle(
        (S(26), S(26), W - S(26), H - S(26)),
        radius=S(22),
        outline=(198, 160, 88, 130),
        width=S(1),
    )
    return bg


def _wrap_headline_lines(text: str, max_chars: int = 22) -> List[str]:
    clean = _tr_upper(text or "SESSİZ LÜKSÜN 6 ALTIN KURALI")
    words = clean.split()
    lines: List[str] = []
    cur: List[str] = []
    for w in words:
        if sum(len(x) for x in cur) + len(cur) + len(w) <= max_chars:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            if len(lines) == 3:
                cur = []
                break
            cur = [w]
    if cur and len(lines) < 3:
        lines.append(" ".join(cur))
    return lines[:3] or ["SESSİZ LÜKSÜN", "6 ALTIN KURALI"]


def generate_hook_cover_and_story_collage(
    concept: Dict[str, Any],
    scene_frames: List[Image.Image],
    prepared_cards: List[Dict[str, Any]],
    out_dir: str,
) -> Image.Image:
    """
    1) output/hook_cover.jpg (Saf Beyaz Stüdyo Estetikli Reels Kapak Fotoğrafı)
    2) output/luxury_story_collage.jpg (Saf Beyaz Fotoğraf Stüdyosu 9:16 Story & Moodboard Lookbook Kolajı)
    üretir.
    """
    base = scene_frames[0].copy().convert("RGBA") if scene_frames else create_obsidian_gold_stage()

    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    for y in range(S(380)):
        alpha = int(165 * (1.0 - (y / float(S(380)))) ** 1.35)
        gdraw.line([(0, y), (W, y)], fill=(255, 255, 255, alpha))
    for y in range(H - S(820), H):
        prog = (y - (H - S(820))) / float(S(820))
        alpha = int(215 * (prog ** 1.2))
        gdraw.line([(0, y), (W, y)], fill=(252, 250, 246, alpha))
    base = Image.alpha_composite(base, grad)
    draw = ImageDraw.Draw(base)

    f_crest = get_font(18, bold=True)
    f_kicker = get_font(22, bold=True)
    f_big = get_font(42, bold=True)
    f_sub = get_font(22, bold=True)
    f_mini = get_font(18, bold=True)

    _draw_pill(
        draw, W // 2, S(178),
        "LUXURY LIFE AI • WHITE STUDIO EDITION",
        f_crest, (255, 255, 255, 245), (22, 18, 24, 255),
        S(26), S(9), S(16), (198, 160, 88, 240), S(2),
    )
    kicker = _tr_upper(concept.get("cover_kicker", "» SAF BEYAZ FOTOĞRAF STÜDYOSU REJİSİ «"))[:48]
    _draw_pill(
        draw, W // 2, S(238),
        kicker,
        f_kicker, (255, 255, 255, 248), (154, 114, 42, 255),
        S(30), S(13), S(24), (198, 160, 88, 245), S(2),
    )

    # Sağ dikey sütunda 4 Saf Beyaz Stüdyo Önizleme Kartı
    card_w, card_h = S(190), S(205)
    card_x = W - card_w - S(34)
    start_y = S(335)
    gap_y = S(220)
    for idx_c, p_card in enumerate(prepared_cards[:4]):
        cy = start_y + idx_c * gap_y
        draw.rounded_rectangle(
            (card_x, cy, card_x + card_w, cy + card_h),
            radius=S(24),
            fill=(255, 255, 255, 248),
            outline=(198, 160, 88, 245),
            width=S(3),
        )
        thumb = p_card["cutout"].copy()
        thumb.thumbnail((card_w - S(24), card_h - S(56)), Image.Resampling.LANCZOS)
        tx = card_x + (card_w - thumb.width) // 2
        ty = cy + S(10) + (card_h - S(56) - thumb.height) // 2
        base.paste(thumb, (tx, ty), thumb)

        draw.rounded_rectangle(
            (card_x + S(10), cy + S(10), card_x + S(52), cy + S(36)),
            radius=S(9),
            fill=(198, 160, 88, 255),
        )
        draw.text((card_x + S(31), cy + S(23)), f"#{idx_c + 1}", fill=(255, 255, 255, 255), font=f_crest, anchor="mm")

        price_txt = str(p_card["data"].get("price", ""))[:14]
        draw.rounded_rectangle(
            (card_x + S(10), cy + card_h - S(42), card_x + card_w - S(10), cy + card_h - S(8)),
            radius=S(10),
            fill=(246, 242, 234, 255),
            outline=(198, 160, 88, 180),
            width=S(1),
        )
        draw.text((card_x + card_w // 2, cy + card_h - S(25)), price_txt, fill=(22, 18, 24, 255), font=f_mini, anchor="mm")

    # Alt-Merkez Saf Beyaz Dergi Kapağı Hook Kutusu
    box_top, box_bot = S(1305), S(1685)
    draw.rounded_rectangle(
        (S(46), box_top, W - S(46), box_bot),
        radius=S(36),
        fill=(255, 255, 255, 246),
        outline=(198, 160, 88, 250),
        width=S(3),
    )
    loc_short = _tr_upper(concept.get("location_name", "SAF BEYAZ FOTOĞRAF STÜDYOSU (#FFFFFF)"))[:42]
    _draw_pill(
        draw, W // 2, box_top + S(46),
        f"» {loc_short} «",
        f_kicker, (198, 160, 88, 255), (255, 255, 255, 255),
        S(26), S(11), S(18),
    )

    h_lines = _wrap_headline_lines(concept.get("cover_headline", concept.get("title", "")), max_chars=22)
    line_start_y = box_top + S(122) if len(h_lines) == 3 else box_top + S(145)
    for i_ln, ln_txt in enumerate(h_lines):
        draw.text((W // 2, line_start_y + i_ln * S(60)), ln_txt, fill=(18, 16, 20, 255), font=f_big, anchor="mm")

    _draw_pill(
        draw, W // 2, box_bot - S(46),
        "» KAYDET & BİREBİR ÜRÜN LİNKLERİNİ İNCELE «",
        f_sub, (18, 16, 20, 255), (242, 214, 158, 255),
        S(28), S(12), S(20),
    )

    rgb_cover = base.convert("RGB")
    cover_path = os.path.join(out_dir, "hook_cover.jpg")
    rgb_cover.save(cover_path, "JPEG", quality=97, subsampling=0)

    # Ayrıca 9:16 Saf Beyaz Stüdyo Story Moodboard Kolajı (luxury_story_collage.jpg) üret
    story = create_obsidian_gold_stage("@luxurylifeaibot")
    sdraw = ImageDraw.Draw(story)
    _draw_pill(
        sdraw, W // 2, S(95),
        "LUXURY LIFE AI • SAF BEYAZ STÜDYO 6'LI LÜKS SEÇKİ",
        f_kicker, (198, 160, 88, 255), (255, 255, 255, 255),
        S(30), S(12), S(20),
    )
    _draw_pill(
        sdraw, W // 2, S(162),
        _tr_upper(concept.get("title", ""))[:46],
        f_sub, (255, 255, 255, 248), (22, 18, 24, 255),
        S(26), S(10), S(18), (198, 160, 88, 220), S(2),
    )
    grid_coords = [
        (S(55), S(230)), (S(555), S(230)),
        (S(55), S(740)), (S(555), S(740)),
        (S(55), S(1250)), (S(555), S(1250)),
    ]
    cw_box, ch_box = S(470), S(470)
    for idx_g, p_card in enumerate(prepared_cards[:6]):
        gx, gy = grid_coords[idx_g]
        sdraw.rounded_rectangle(
            (gx, gy, gx + cw_box, gy + ch_box),
            radius=S(28),
            fill=(255, 255, 255, 252),
            outline=(198, 160, 88, 235),
            width=S(3),
        )
        im_c = p_card["cutout"].copy()
        im_c.thumbnail((cw_box - S(50), ch_box - S(120)), Image.Resampling.LANCZOS)
        story.paste(im_c, (gx + (cw_box - im_c.width) // 2, gy + S(24) + (ch_box - S(120) - im_c.height) // 2), im_c)

        it_d = p_card["data"]
        b_txt = _tr_upper(str(it_d.get("brand", "LUXURY")))[:22]
        p_txt = f"{it_d.get('price', '')} • KOD: {it_d.get('sku', '-')}"
        sdraw.rounded_rectangle(
            (gx + S(16), gy + ch_box - S(86), gx + cw_box - S(16), gy + ch_box - S(14)),
            radius=S(16),
            fill=(248, 244, 236, 255),
            outline=(198, 160, 88, 190),
            width=S(1),
        )
        sdraw.text((gx + cw_box // 2, gy + ch_box - S(62)), f"#{idx_g + 1} {b_txt}", fill=(18, 16, 20, 255), font=f_mini, anchor="mm")
        sdraw.text((gx + cw_box // 2, gy + ch_box - S(32)), p_txt, fill=(154, 114, 42, 255), font=f_crest, anchor="mm")

    _draw_pill(
        sdraw, W // 2, S(1815),
        "» TÜM ÜRÜN LİNKLERİ AÇIKLAMADA & İLK YORUMDA «",
        f_sub, (18, 16, 20, 255), (242, 214, 158, 255),
        S(32), S(14), S(22),
    )
    story_path = os.path.join(out_dir, "luxury_story_collage.jpg")
    story.convert("RGB").save(story_path, "JPEG", quality=96)

    return rgb_cover


def render_luxury_graphmotion_reel(
    concept: Dict[str, Any],
    output_mp4: str,
    watermark: str = "@luxurylifeaibot",
) -> Dict[str, Any]:
    out_dir = os.path.dirname(output_mp4) or "output"
    os.makedirs(out_dir, exist_ok=True)
    frames_dir = os.path.join(out_dir, "_lux_frames")
    os.makedirs(frames_dir, exist_ok=True)

    bg_stage = create_obsidian_gold_stage(watermark)

    # 6 Bento Kartının GraphMotion Plus Koordinat ve Hızlı Yaylanma (Spring) Zamanlaması
    slot_configs = [
        {"slot": "slot1", "box": (S(50), S(245), S(470), S(470)), "start_xy": (S(-520), S(180)), "t_in": 0.35},
        {"slot": "slot2", "box": (S(560), S(245), S(470), S(470)), "start_xy": (S(1180), S(180)), "t_in": 0.65},
        {"slot": "slot3", "box": (S(50), S(755), S(470), S(470)), "start_xy": (S(-520), S(755)), "t_in": 0.95},
        {"slot": "slot4", "box": (S(560), S(755), S(470), S(470)), "start_xy": (S(1180), S(755)), "t_in": 1.25},
        {"slot": "slot5", "box": (S(50), S(1265), S(470), S(470)), "start_xy": (S(-520), S(1420)), "t_in": 1.55},
        {"slot": "slot6", "box": (S(560), S(1265), S(470), S(470)), "start_xy": (S(1180), S(1420)), "t_in": 1.85},
    ]

    f_mini = get_font(16, bold=True)
    f_crest = get_font(18, bold=True)
    f_kicker = get_font(22, bold=True)
    f_title = get_font(25, bold=True)
    f_brand = get_font(20, bold=True)
    f_price = get_font(19, bold=True)

    items_dict = concept.get("items", {})
    prepared_cards: List[Dict[str, Any]] = []
    for idx, scfg in enumerate(slot_configs, start=1):
        it_data = items_dict.get(scfg["slot"]) or list(items_dict.values())[idx - 1]
        c_path = it_data.get("cutout_path", "")
        if c_path and os.path.exists(c_path):
            cut_im = Image.open(c_path).convert("RGBA")
        else:
            cut_im = Image.new("RGBA", (400, 400), (255, 255, 255, 255))
        cut_im = enhance_luxury_micro_contrast(cut_im, is_cutout=True)

        # Önceden hazır Saf Beyaz Stüdyo Bento Kart görüntüsü oluştur (#FFFFFF + 18K Gold)
        _, _, bw, bh = scfg["box"]
        card_im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        cdraw = ImageDraw.Draw(card_im)
        cdraw.rounded_rectangle(
            (0, 0, bw - 1, bh - 1),
            radius=S(28),
            fill=(255, 255, 255, 252),
            outline=(198, 160, 88, 240),
            width=S(3),
        )
        # İç altın çerçeve
        cdraw.rounded_rectangle(
            (S(8), S(8), bw - S(9), bh - S(9)),
            radius=S(22),
            outline=(198, 160, 88, 110),
            width=S(1),
        )
        thumb = cut_im.copy()
        thumb.thumbnail((bw - S(56), bh - S(128)), Image.Resampling.LANCZOS)
        card_im.paste(
            thumb,
            ((bw - thumb.width) // 2, S(26) + (bh - S(128) - thumb.height) // 2),
            thumb,
        )
        # Sol üst altın numara rozeti
        cdraw.rounded_rectangle(
            (S(14), S(14), S(68), S(46)),
            radius=S(10),
            fill=(198, 160, 88, 255),
        )
        cdraw.text((S(41), S(30)), f"#{idx}", fill=(255, 255, 255, 255), font=f_crest, anchor="mm")

        # Sağ üst kategori etiketi
        cat_lbl = _tr_upper(str(it_data.get("category_label", "LÜKS")))[:16]
        cdraw.rounded_rectangle(
            (bw - S(185), S(14), bw - S(14), S(46)),
            radius=S(10),
            fill=(248, 244, 236, 255),
            outline=(198, 160, 88, 190),
            width=S(1),
        )
        cdraw.text((bw - S(100), S(30)), cat_lbl, fill=(142, 104, 36, 255), font=f_crest, anchor="mm")

        # Alt marka + fiyat + kod şeridi (Saf Beyaz / Krem Editoryal Şerit)
        cdraw.rounded_rectangle(
            (S(14), bh - S(86), bw - S(14), bh - S(14)),
            radius=S(16),
            fill=(248, 244, 236, 255),
            outline=(198, 160, 88, 185),
            width=S(1),
        )
        b_name = _tr_upper(str(it_data.get("brand", "LUXURY")))[:22]
        p_info = f"{it_data.get('price', '')}  |  {it_data.get('sku', '-')}"
        cdraw.text((bw // 2, bh - S(62)), b_name, fill=(18, 16, 20, 255), font=f_brand, anchor="mm")
        cdraw.text((bw // 2, bh - S(32)), p_info, fill=(154, 114, 42, 255), font=f_price, anchor="mm")
        card_im = apply_studio_contact_shadow_card(card_im, elevation_px=S(10))

        prepared_cards.append({
            **scfg,
            "data": it_data,
            "cutout": cut_im,
            "card_im": card_im,
        })

    # Sahne karelerini 2K kalitesinde yükle
    scene_frames: List[Image.Image] = []
    for fp in concept.get("model_frames", []):
        if os.path.exists(fp):
            im = Image.open(fp).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
            im = enhance_luxury_micro_contrast(im, is_cutout=False)
            scene_frames.append(im)
    if not scene_frames:
        scene_frames = [bg_stage.convert("RGB")] * 3

    hook_cover_rgb = generate_hook_cover_and_story_collage(concept, scene_frames, prepared_cards, out_dir)

    total_duration = 13.5
    total_frames = int(total_duration * FPS)
    bento_end_sec = 3.60

    for f_idx in range(total_frames):
        t = f_idx / float(FPS)

        # ACT I (0.00s - 0.35s): Scroll-Stopper Dergi Kapağı Kancası
        if t < 0.35:
            frame_rgb = hook_cover_rgb.copy()
        # ACT II (0.35s - 3.60s): Saf Beyaz Fotoğraf Stüdyosu 6'lı Bento & Remotion Yay Fiziği (Sadece Ön Plana Çıkan 6 Ürün Kartı)
        elif t < bento_end_sec:
            canvas = bg_stage.copy()

            # 6 Bento Kartının Remotion Yay Fiziği (_remotion_spring) + 180° Shutter Motion Blur ile Yerleşimi
            for p_card in prepared_cards:
                t_in = p_card["t_in"]
                if t < t_in:
                    continue
                dt = t - t_in
                dt_prev = max(0.0, dt - (1.0 / float(FPS)))
                sp_now = _remotion_spring(dt, damping=14.0, stiffness=120.0, mass=0.8)
                sp_prev = _remotion_spring(dt_prev, damping=14.0, stiffness=120.0, mass=0.8)

                tx, ty, bw, bh = p_card["box"]
                sx, sy = p_card["start_xy"]
                cur_x = int(round(sx + (tx - sx) * sp_now))
                cur_y = int(round(sy + (ty - sy) * sp_now))
                prev_x = int(round(sx + (tx - sx) * sp_prev))
                prev_y = int(round(sy + (ty - sy) * sp_prev))

                speed_px = math.hypot(cur_x - prev_x, cur_y - prev_y)
                card_visual = _apply_180deg_shutter_blur(p_card["card_im"], speed_px)
                canvas.paste(card_visual, (cur_x, cur_y), card_visual)

            frame_rgb = canvas.convert("RGB")

            # Bento tamamlandığında (2.30s - 3.45s) Specular Champagne Gold Işık Dalgası
            if 2.30 <= t <= 3.45:
                shimmer_p = (t - 2.30) / 1.15
                frame_rgb = _apply_film_light_leak(frame_rgb, intensity=0.22 * math.sin(shimmer_p * math.pi), sweep_pos=shimmer_p)

        # ACT III (3.60s - 13.50s): Manken Çıktığı Anda Ekstra Yazı/Sahne Başlığı Olmadan Sadece Altta Ön Plana Çıkan 2 Ürün Kartı!
        else:
            scene_dur = (total_duration - bento_end_sec) / 3.0
            rel_t = t - bento_end_sec
            stage_idx = min(2, int(rel_t // scene_dur))
            stage_local_t = rel_t - (stage_idx * scene_dur)

            cur_frame_im = scene_frames[min(stage_idx, len(scene_frames) - 1)]
            if stage_idx < len(scene_frames) - 1 and stage_local_t > (scene_dur - 0.38):
                blend_p = ease_in_out_cubic((stage_local_t - (scene_dur - 0.38)) / 0.38)
                base_sc = Image.blend(cur_frame_im, scene_frames[stage_idx + 1], blend_p)
            else:
                base_sc = cur_frame_im.copy()

            # Sahneye Özel Organik El Kamerası Nefes Alma Salınımı + Gerçek Elmas/Altın Optik Parıltıları + Kodak Portra 35mm Sensör Dokusu
            breathed_sc = apply_organic_camera_breathing(
                base_sc,
                t=stage_local_t,
                stage_idx=stage_idx,
                is_walking=(stage_idx == 2),
            )
            optical_sc = enhance_frame_with_real_optics(
                breathed_sc,
                t=t,
                frame_idx=f_idx,
                stage_idx=stage_idx,
                enable_glints=True,
            )
            cropped = optical_sc.convert("RGBA")

            # Manken Sahnelerinde Üst Yazı/Sahne Başlığı YOK — Sadece Altta Ön Plana Çıkarılan 2 Ürün Kartı (Örn. Zen Pırlanta & Vakko Couture)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            odraw = ImageDraw.Draw(ov)

            hud_spring = min(1.0, _remotion_spring(stage_local_t, damping=14.0, stiffness=120.0, mass=0.8))
            y_offset_hud = int(round((1.0 - hud_spring) * S(130)))
            hud_top = H - S(285) + y_offset_hud

            pair_start = stage_idx * 2
            pair_cards = prepared_cards[pair_start:pair_start + 2]
            for p_i, p_item in enumerate(pair_cards):
                item_num = pair_start + p_i + 1
                box_w = S(486)
                box_h = S(182)
                bx = S(48) + p_i * (box_w + S(12))
                by = hud_top

                odraw.rounded_rectangle(
                    (bx, by, bx + box_w, by + box_h),
                    radius=S(22),
                    fill=(255, 255, 255, 246),
                    outline=(198, 160, 88, 240),
                    width=S(3),
                )
                mini_im = p_item["cutout"].copy()
                mini_im.thumbnail((S(142), S(142)), Image.Resampling.LANCZOS)
                ov.paste(
                    mini_im,
                    (bx + S(14) + (S(142) - mini_im.width) // 2, by + (box_h - mini_im.height) // 2),
                    mini_im,
                )

                it_d = p_item["data"]
                lbl_t = _tr_upper(f"#{item_num} {it_d.get('category_label', 'LÜKS DETAY')}")[:20]
                br_t = _tr_upper(str(it_d.get("brand", "LUXURY")).split("/")[0].strip())[:18]
                nm_t = str(it_d.get("name", ""))[:22]
                pr_t = f"{it_d.get('price', '')} • {it_d.get('sku', '')}"[:22]

                tx_left = bx + S(168)
                odraw.text((tx_left, by + S(34)), lbl_t, fill=(154, 114, 42, 255), font=f_mini, anchor="lm")
                odraw.text((tx_left, by + S(74)), br_t, fill=(18, 16, 20, 255), font=f_brand, anchor="lm")
                odraw.text((tx_left, by + S(112)), nm_t, fill=(62, 56, 50, 255), font=f_mini, anchor="lm")
                odraw.text((tx_left, by + S(148)), pr_t, fill=(142, 104, 36, 255), font=f_crest, anchor="lm")

            frame_rgb = Image.alpha_composite(cropped, ov).convert("RGB")

        # Sahne Geçişlerinde Anamorfik Film Light-Leak (Işık Sızıntısı) Geçiş Efekti
        if 0.28 <= t <= 0.44:
            lp = (t - 0.28) / 0.16
            frame_rgb = _apply_film_light_leak(frame_rgb, intensity=0.55 * math.sin(lp * math.pi), sweep_pos=lp)
        elif 3.42 <= t <= 3.82:
            lp = (t - 3.42) / 0.40
            frame_rgb = _apply_film_light_leak(frame_rgb, intensity=0.72 * math.sin(lp * math.pi), sweep_pos=lp)
        elif 6.72 <= t <= 7.08:
            lp = (t - 6.72) / 0.36
            frame_rgb = _apply_film_light_leak(frame_rgb, intensity=0.46 * math.sin(lp * math.pi), sweep_pos=lp)
        elif 10.02 <= t <= 10.38:
            lp = (t - 10.02) / 0.36
            frame_rgb = _apply_film_light_leak(frame_rgb, intensity=0.46 * math.sin(lp * math.pi), sweep_pos=1.0 - lp)

        # Üst Kenar 6px Şampanya Altın İzlenme Tutma (Retention) İlerleme Çubuğu
        top_draw = ImageDraw.Draw(frame_rgb)
        prog_w = max(S(12), int(W * (t / total_duration)))
        top_draw.rectangle((0, 0, prog_w, S(6)), fill=(238, 204, 142))

        frame_path = os.path.join(frames_dir, f"frame_{f_idx:04d}.jpg")
        frame_rgb.save(frame_path, "JPEG", quality=95)

    wav_path = os.path.join(out_dir, "luxury_soundtrack.wav")
    generate_luxury_soundtrack(wav_path, duration=total_duration, category=concept.get("category", "kombin"))

    ffmpeg_exe = get_ffmpeg_exe()
    cmd = [
        ffmpeg_exe,
        "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%04d.jpg"),
        "-i", wav_path,
        "-vf", "unsharp=5:5:0.75:3:3:0.0,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "slow",
        "-profile:v", "high",
        "-level:v", "5.1",
        "-crf", "12",
        "-b:v", "22M",
        "-maxrate", "30M",
        "-bufsize", "45M",
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "44100",
        "-ac", "2",
        "-shortest",
        "-movflags", "+faststart",
        output_mp4,
    ]
    subprocess.run(cmd, check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)

    return {
        "video_path": output_mp4,
        "hook_cover_path": os.path.join(out_dir, "hook_cover.jpg"),
        "story_collage_path": os.path.join(out_dir, "luxury_story_collage.jpg"),
        "duration_sec": total_duration,
        "resolution": f"{W}x{H}",
        "fps": FPS,
        "video_codec": "libx264 (CRF 12, 22 Mbps, BT.709)",
        "physics": "Remotion Spring (damping=14, stiffness=120, mass=0.8) + 180deg Shutter Blur + Film Light-Leak",
    }
