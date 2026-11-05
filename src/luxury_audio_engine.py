"""
Luxury Life AI (@Luxurylifeaibot) — Telifsiz 44.1kHz Stereo Lüks Ses, Foley & Atmosfer Sentezleyici
---------------------------------------------------------------------------------------------------
Saf Beyaz Fotoğraf Stüdyosu (White Cyclorama) 2K GraphMotion Reels için:
1) 6 Bento Kartı Girişinde (0.35s, 0.65s, 0.95s, 1.25s, 1.55s, 1.85s) Mekanik Hasselblad Orta Format
   Deklanşör Sesi (Double-Action Leaf Shutter Click) + Profoto Stüdyo Flaş Patlaması (Soft Strobe Pop)
2) 3 Stüdyo Sahne Geçişinde (3.60s, 6.90s, 10.20s) Anamorfik Film Light-Leak & Kristal Parıltı Çanı
3) Sahne 3 (10.20s - 13.50s) Manken Yürüyüşünde 114 BPM Podyum Adım Sub-Bass Nabzı (Catwalk Stride Pulse)
4) Kategoriye ('taki', 'makyaj', 'kombin', 'otel', 'araba') Özel Sıcak Elektrik Piyano, İpek Pad & Sub-Bass
"""
import os
import wave
import numpy as np


def generate_luxury_soundtrack(wav_path: str, duration: float = 13.5, category: str = "kombin") -> str:
    os.makedirs(os.path.dirname(wav_path) or ".", exist_ok=True)
    sr = 44100
    n_samples = int(round(duration * sr))
    t = np.linspace(0.0, duration, n_samples, endpoint=False, dtype=np.float32)
    two_pi = np.float32(2.0 * np.pi)

    # Deterministik akustik doku (stüdyo flaş ve mekanik deklanşör mikro-transiyentleri için)
    rng = np.random.default_rng(seed=20261105)

    # Kategoriye göre lüks akor frekansları (Am9 / Gmaj9 / Dm9 / Fmaj9 / Cm9 Old Money & Paris Runway)
    chord_map = {
        "taki": [220.00, 261.63, 329.63, 392.00, 493.88],      # Am9 Kristal & Elmas Sergisi
        "makyaj": [196.00, 246.94, 293.66, 369.99, 440.00],    # Gmaj9 Paris Vanity & Beauty Studio
        "kombin": [146.83, 174.61, 220.00, 261.63, 329.63],    # Dm9 Milano & Paris Runway Deep Lounge
        "otel": [174.61, 220.00, 261.63, 329.63, 392.00],      # Fmaj9 Palace Suite & Bosphorus Chill
        "araba": [130.81, 155.56, 196.00, 233.08, 293.66],     # Cm9 Monaco Grand Tourer Bass
    }
    freqs = chord_map.get(category, chord_map["kombin"])
    root_freq = np.float32(freqs[0] * 0.5)

    # -------------------------------------------------------------------------
    # 1. KATMAN: Sıcak Elektrik Piyano (Rhodes) + İpek Stereo Pad + Derin Sub-Bass
    # -------------------------------------------------------------------------
    left = np.zeros(n_samples, dtype=np.float32)
    right = np.zeros(n_samples, dtype=np.float32)

    # Ortak stereo chorus LFO (sıcak ve hızlı vektörel sentez)
    lfo_l = 0.86 + 0.14 * np.sin(two_pi * 0.34 * t)
    lfo_r = 0.86 + 0.14 * np.cos(two_pi * 0.34 * t + 0.40)
    voice_gain = np.float32(0.34 / len(freqs))

    for idx, f_val in enumerate(freqs):
        f = np.float32(f_val)
        detune = np.float32(1.0014 if idx % 2 == 0 else 0.9986)
        fund_l = np.sin(two_pi * f * t)
        fund_r = np.sin(two_pi * (f * detune) * t + np.float32(0.32 + idx * 0.12))
        # Yumuşak 2. harmonik sıcak Rhodes tınısı (polinomik çift-harmonik doygunluk)
        harm2_l = 0.18 * (1.0 - 2.0 * fund_l * fund_l)
        harm2_r = 0.18 * (1.0 - 2.0 * fund_r * fund_r)
        left += (fund_l + harm2_l) * voice_gain
        right += (fund_r + harm2_r) * voice_gain

    left *= lfo_l
    right *= lfo_r

    # Derin, sıcak Sub-Bass (kök nota + hafif 2. harmonik sıcaklık)
    sub_lfo = 0.88 + 0.12 * np.sin(two_pi * 0.95 * t)
    sub_fund = np.sin(two_pi * root_freq * t)
    sub_bass = (0.22 * sub_fund + 0.07 * (1.0 - 2.0 * sub_fund * sub_fund)) * sub_lfo

    # Genel Lounge Nabzı (112 BPM yumuşak kalp atışı / deep lounge groove)
    base_bpm = np.float32(112.0)
    base_period = np.float32(60.0 / base_bpm)
    base_mod = t % base_period
    base_phase = base_mod / base_period
    lounge_kick_env = np.exp(-15.0 * base_phase)
    lounge_kick_freq = 48.0 + 58.0 * np.exp(-26.0 * base_phase)
    lounge_kick = np.sin(two_pi * lounge_kick_freq * base_mod) * lounge_kick_env * np.float32(0.24)

    # -------------------------------------------------------------------------
    # 2. KATMAN: 4 Kamera Açısı Geçişinde Mekanik Hasselblad Deklanşör + Flaş Pop
    #    Zamanlar: t = 0.08s, 3.38s, 6.75s, 10.12s
    # -------------------------------------------------------------------------
    bento_card_times = [0.08, 3.38, 6.75, 10.12]
    shutter_l = np.zeros(n_samples, dtype=np.float32)
    shutter_r = np.zeros(n_samples, dtype=np.float32)

    for idx, ct in enumerate(bento_card_times):
        s_idx = int(round(ct * sr))
        win_len = int(round(0.14 * sr))  # 140ms pencere
        e_idx = min(n_samples, s_idx + win_len)
        if s_idx >= n_samples or e_idx <= s_idx:
            continue

        seg_n = e_idx - s_idx
        dt = np.arange(seg_n, dtype=np.float32) / np.float32(sr)
        noise_burst = rng.standard_normal(seg_n).astype(np.float32)

        # (a) Birincil Hasselblad Yaprak Deklanşör (Leaf Shutter) Mekanik Klik (t + 0.000s)
        click1_env = np.exp(-260.0 * dt)
        click1_metal = (
            0.55 * np.sin(two_pi * 2450.0 * dt)
            + 0.35 * np.sin(two_pi * 4850.0 * dt + 0.4)
            + 0.40 * noise_burst * np.sin(two_pi * 3200.0 * dt)
        ) * click1_env

        # (b) İkincil Ayna / Mekanik Mandal Dönüşü "Ka-Chuk" (t + 0.026s)
        dt2 = np.maximum(np.float32(0.0), dt - np.float32(0.026))
        mask2 = (dt >= 0.026).astype(np.float32)
        click2_env = mask2 * np.exp(-195.0 * dt2)
        click2_body = (
            0.48 * np.sin(two_pi * 1680.0 * dt2)
            + 0.30 * np.sin(two_pi * 3420.0 * dt2)
            + 0.35 * np.sin(two_pi * 195.0 * dt2)
            + 0.25 * noise_burst
        ) * click2_env

        # (c) Profoto Stüdyo Flaş Kapasitör Boşalması (Soft Strobe Pop, t + 0.006s)
        dt_pop = np.maximum(np.float32(0.0), dt - np.float32(0.006))
        mask_pop = (dt >= 0.006).astype(np.float32)
        pop_env = mask_pop * np.exp(-52.0 * dt_pop)
        pop_freq = 56.0 + 95.0 * np.exp(-110.0 * dt_pop)
        strobe_pop = (
            0.55 * np.sin(two_pi * pop_freq * dt_pop) * pop_env
            + 0.14 * np.sin(two_pi * np.float32(freqs[idx % len(freqs)] * 2.0) * dt_pop) * np.exp(-18.0 * dt_pop) * mask_pop
        )

        combined_foley = np.float32(0.26) * (click1_metal + 0.82 * click2_body + 0.90 * strobe_pop)

        # Sol sütun kartları (#1, #3, #5) hafif sola, sağ sütun kartları (#2, #4, #6) hafif sağa panlanır
        pan_l = np.float32(1.12 if idx % 2 == 0 else 0.86)
        pan_r = np.float32(0.86 if idx % 2 == 0 else 1.12)
        shutter_l[s_idx:e_idx] += combined_foley * pan_l
        shutter_r[s_idx:e_idx] += combined_foley * pan_r

    # -------------------------------------------------------------------------
    # 3. KATMAN: 3 Stüdyo Sahne Geçişinde (3.60s, 6.90s, 10.20s) Anamorfik Film Light-Leak
    #    & Kristal Parıltı Çanları (Crystal Shimmer Chimes)
    # -------------------------------------------------------------------------
    scene_cut_times = [3.38, 6.75, 10.12]
    shimmer_l = np.zeros(n_samples, dtype=np.float32)
    shimmer_r = np.zeros(n_samples, dtype=np.float32)

    # Bento tamamlanma altın ışık dalgası (2.35s) için hafif kristal dokunuş
    if 2.35 < duration:
        s_b = int(round(2.35 * sr))
        e_b = min(n_samples, s_b + int(round(0.85 * sr)))
        dt_b = np.arange(e_b - s_b, dtype=np.float32) / np.float32(sr)
        env_b = np.sin(np.float32(np.pi) * np.clip(dt_b / 0.85, 0.0, 1.0)) * np.exp(-2.4 * dt_b)
        shimmer_l[s_b:e_b] += 0.09 * np.sin(two_pi * np.float32(freqs[2] * 2.0) * dt_b) * env_b
        shimmer_r[s_b:e_b] += 0.09 * np.sin(two_pi * np.float32(freqs[4] * 2.0) * dt_b + 0.5) * env_b

    # 3 Ana Stüdyo Sahne Kesmesi: 3.60s (Sahne 1), 6.90s (Sahne 2), 10.20s (Sahne 3)
    arp_ratios = [1.0, 1.25, 1.50, 2.0, 2.50, 3.0]
    for sc_idx, sc_t in enumerate(scene_cut_times):
        if sc_t >= duration:
            continue

        # (a) Anamorfik Film Light-Leak Sıcak Swell (kesmeden 0.16s önce başlar, 0.60s sürer)
        sw_start = max(0, int(round((sc_t - 0.16) * sr)))
        sw_end = min(n_samples, int(round((sc_t + 0.44) * sr)))
        if sw_end > sw_start:
            dt_sw = np.arange(sw_end - sw_start, dtype=np.float32) / np.float32(sr)
            sw_dur = np.float32((sw_end - sw_start) / float(sr))
            sw_env = np.sin(np.float32(np.pi) * np.clip(dt_sw / sw_dur, 0.0, 1.0)) ** 1.6
            base_f = np.float32(freqs[sc_idx % len(freqs)])
            sweep_f = base_f * (1.0 + 0.35 * (dt_sw / sw_dur))
            shimmer_l[sw_start:sw_end] += 0.11 * np.sin(two_pi * sweep_f * dt_sw) * sw_env
            shimmer_r[sw_start:sw_end] += 0.11 * np.sin(two_pi * (sweep_f * 1.008) * dt_sw + 0.6) * sw_env

        # (b) Kristal Arpej Çanları (Crystal Shimmer Chime Cascade)
        for n_i, ratio in enumerate(arp_ratios):
            note_t = sc_t + n_i * 0.038
            n_start = int(round(note_t * sr))
            n_end = min(n_samples, n_start + int(round(0.72 * sr)))
            if n_start >= n_samples or n_end <= n_start:
                continue
            dt_n = np.arange(n_end - n_start, dtype=np.float32) / np.float32(sr)
            chime_freq = np.float32(freqs[(sc_idx + n_i) % len(freqs)] * 2.0 * ratio)
            env_n = (1.0 - np.exp(-180.0 * dt_n)) * np.exp(-6.2 * dt_n)
            bell_wave = (
                np.sin(two_pi * chime_freq * dt_n)
                + 0.32 * np.sin(two_pi * (chime_freq * 2.0) * dt_n + 0.3)
            ) * env_n * np.float32(0.085)

            if n_i % 2 == 0:
                shimmer_l[n_start:n_end] += bell_wave * np.float32(1.15)
                shimmer_r[n_start:n_end] += bell_wave * np.float32(0.75)
            else:
                shimmer_l[n_start:n_end] += bell_wave * np.float32(0.75)
                shimmer_r[n_start:n_end] += bell_wave * np.float32(1.15)

    # -------------------------------------------------------------------------
    # 4. KATMAN: Sahne 3 (10.20s - 13.50s) Catwalk Stride Sub-Bass Pulse (114 BPM)
    # -------------------------------------------------------------------------
    catwalk_l = np.zeros(n_samples, dtype=np.float32)
    catwalk_r = np.zeros(n_samples, dtype=np.float32)
    walk_start_t = 10.20
    if duration > walk_start_t:
        w_start = int(round(walk_start_t * sr))
        dt_w = t[w_start:] - np.float32(walk_start_t)
        walk_bpm = np.float32(114.0)
        walk_period = np.float32(60.0 / walk_bpm)
        walk_mod = dt_w % walk_period
        walk_phase = walk_mod / walk_period

        # Güçlü, hipnotik 114 BPM podyum yürüyüş sub-bass vuruşu
        stride_env = np.exp(-12.5 * walk_phase)
        stride_freq = 46.0 + 64.0 * np.exp(-24.0 * walk_phase)
        stride_sub = np.sin(two_pi * stride_freq * walk_mod) * stride_env * np.float32(0.30)

        # Podyum topuk adımı (Tactile Heel Step Click) + off-beat ipek hi-hat dokunuşu
        heel_env = np.exp(-95.0 * walk_phase)
        heel_click = np.sin(two_pi * 920.0 * walk_mod) * heel_env * np.float32(0.07)

        off_phase = ((dt_w + walk_period * 0.5) % walk_period) / walk_period
        hat_env = np.exp(-48.0 * off_phase)
        hat_shimmer = np.sin(two_pi * 6400.0 * dt_w) * hat_env * np.float32(0.045)

        # Sahne 3 başında yumuşak devreye giriş zarfı
        walk_fade = np.clip(dt_w / 0.18, 0.0, 1.0)
        catwalk_l[w_start:] = (stride_sub + heel_click + hat_shimmer * 1.1) * walk_fade
        catwalk_r[w_start:] = (stride_sub + heel_click + hat_shimmer * 0.9) * walk_fade

        # Sahne 3'te ana lounge kick ile çakışmayı önlemek için 10.20s sonrasında lounge_kick'i yumuşakça azalt
        lounge_kick[w_start:] *= (1.0 - 0.75 * walk_fade)

    # -------------------------------------------------------------------------
    # 5. KATMAN: Sıcak Analog Stereo Mastering & Clipping Korumalı Normalizasyon
    # -------------------------------------------------------------------------
    left_mix = left + sub_bass + lounge_kick + shutter_l + shimmer_l + catwalk_l
    right_mix = right + sub_bass + lounge_kick + shutter_r + shimmer_r + catwalk_r

    # Yumuşak fade-in (0.18s) ve seamless loop fade-out (0.40s)
    fade_in = np.clip(t / 0.18, 0.0, 1.0)
    fade_out = np.clip((np.float32(duration) - t) / 0.40, 0.0, 1.0)
    master_env = fade_in * fade_out

    left_mix *= master_env
    right_mix *= master_env

    # Yumuşak analog-tipi doygunluk (soft saturation) + sıfır-clipping tepe normalizasyonu (-0.8 dBFS)
    left_mix = np.tanh(left_mix * np.float32(1.15))
    right_mix = np.tanh(right_mix * np.float32(1.15))

    peak = max(float(np.max(np.abs(left_mix))), float(np.max(np.abs(right_mix))), 1e-6)
    scale = np.float32(0.91 / peak)
    left_mix = np.clip(left_mix * scale, -0.98, 0.98)
    right_mix = np.clip(right_mix * scale, -0.98, 0.98)

    stereo = np.empty((n_samples * 2,), dtype=np.int16)
    stereo[0::2] = (left_mix * 32767.0).astype(np.int16)
    stereo[1::2] = (right_mix * 32767.0).astype(np.int16)

    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())

    return wav_path
