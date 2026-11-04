"""
Luxury Life AI (@Luxurylifeaibot) — Telifsiz 44.1kHz Stereo Lüks Ses & Atmosfer Sentezleyici
--------------------------------------------------------------------------------------------
Her lüks kategori ('taki', 'makyaj', 'kombin', 'otel', 'araba') için 11.5 saniyelik
Monte Carlo Deep Lounge, Velvet Strings ve Golden Hour bas armonisi üretir.
"""
import os
import wave
import numpy as np


def generate_luxury_soundtrack(output_wav: str, duration: float = 11.5, category: str = "kombin") -> str:
    os.makedirs(os.path.dirname(output_wav) or ".", exist_ok=True)
    sr = 44100
    n_samples = int(duration * sr)
    t = np.linspace(0.0, duration, n_samples, endpoint=False)

    # Kategoriye göre lüks akor frekansları (Am9 / Fm9 / Dm9 / Gm9 Old Money Lounge)
    chord_map = {
        "taki": [220.0, 261.63, 329.63, 392.00, 493.88],      # Am9 Kristal & Arp
        "makyaj": [196.0, 246.94, 293.66, 369.99, 440.00],    # Gmaj9 Paris Vanity Lounge
        "kombin": [146.83, 174.61, 220.00, 261.63, 329.63],   # Dm9 Milano Runway Deep House
        "otel": [174.61, 220.00, 261.63, 329.63, 392.00],     # Fmaj9 Como & Bosphorus Chill
        "araba": [130.81, 155.56, 196.00, 233.08, 293.66],    # Cm9 Monaco Midnight Bass
    }
    freqs = chord_map.get(category, chord_map["kombin"])

    # 1. Katman: İpek sıcak pad ve yaylı armonisi
    left = np.zeros_like(t)
    right = np.zeros_like(t)
    for idx, f in enumerate(freqs):
        detune = 1.0015 if idx % 2 == 0 else 0.9985
        lfo = 0.85 + 0.15 * np.sin(2 * np.pi * (0.35 + idx * 0.08) * t)
        wave_l = np.sin(2 * np.pi * f * t) * lfo / len(freqs)
        wave_r = np.sin(2 * np.pi * (f * detune) * t + 0.35) * lfo / len(freqs)
        left += wave_l * 0.42
        right += wave_r * 0.42

    # 2. Katman: 116 BPM Lüks Podyum Nabzı (Sub-bass & yumuşak kick)
    bpm = 116.0 if category in ("kombin", "araba") else 104.0
    beat_period = 60.0 / bpm
    beat_phase = (t % beat_period) / beat_period
    kick_env = np.exp(-16.0 * beat_phase)
    kick_freq = 52.0 + 68.0 * np.exp(-28.0 * beat_phase)
    kick = np.sin(2 * np.pi * kick_freq * (t % beat_period)) * kick_env * 0.36

    # 3. Katman: GraphMotion Parça Girişlerinde (t=0.10, 0.65, 1.20, 1.75, 2.30, 2.85) Kristal Parıltı Çanı
    chime_times = [0.10, 0.65, 1.20, 1.75, 2.30, 2.85, 5.40]
    chime_l = np.zeros_like(t)
    chime_r = np.zeros_like(t)
    for idx, ct in enumerate(chime_times):
        mask = t >= ct
        dt = np.zeros_like(t)
        dt[mask] = t[mask] - ct
        env = np.zeros_like(t)
        env[mask] = np.exp(-5.5 * dt[mask])
        c_freq = freqs[idx % len(freqs)] * 2.0
        chime_l += np.sin(2 * np.pi * c_freq * dt) * env * 0.14
        chime_r += np.sin(2 * np.pi * (c_freq * 1.5) * dt) * env * 0.14

    left_mix = left + kick + chime_l
    right_mix = right + kick + chime_r

    # Yumuşak fade-in (0.2s) ve seamless loop fade-out (0.4s)
    fade_in = np.clip(t / 0.20, 0.0, 1.0)
    fade_out = np.clip((duration - t) / 0.40, 0.0, 1.0)
    master_env = fade_in * fade_out

    left_mix = np.clip(left_mix * master_env, -0.95, 0.95)
    right_mix = np.clip(right_mix * master_env, -0.95, 0.95)

    stereo = np.empty((n_samples * 2,), dtype=np.int16)
    stereo[0::2] = (left_mix * 32767).astype(np.int16)
    stereo[1::2] = (right_mix * 32767).astype(np.int16)

    with wave.open(output_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())

    return output_wav
