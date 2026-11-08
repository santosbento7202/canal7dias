"""src/audio_ambient.py - Gerador procedural de trilha sonora dark ambient para o canal Código Social.

Gera uma trilha de fundo sutil, cinematográfica e imersiva:
- Frequências graves quentes (55Hz, 110Hz, 165Hz) com modulação lenta (0.08Hz).
- Textura analógica sutil (ruído rosa filtrado) sem competir com a voz.
- Nível de mixagem masterizado a -26 dBFS para não abafar a narração neural.
"""

import os
import wave
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "assets", "audio")
DEFAULT_BGM_PATH = os.path.join(AUDIO_DIR, "dark_ambient_drone.wav")


def ensure_dark_ambient_bgm(duration_sec: float = 120.0, out_path: str = DEFAULT_BGM_PATH) -> str:
    """Gera proceduralmente a trilha dark ambient cinematográfica se não existir."""
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        return out_path

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    sample_rate = 44100
    n_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    # 1. Harmônicos graves fundamentais (A1 = 55Hz, A2 = 110Hz, E3 = 164.8Hz)
    lfo1 = 0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t)  # Modulação lenta de 14 segundos
    lfo2 = 0.5 + 0.5 * np.cos(2 * np.pi * 0.04 * t)  # Modulação lenta de 25 segundos

    tone_55 = np.sin(2 * np.pi * 55.0 * t) * (0.6 + 0.4 * lfo1)
    tone_110 = np.sin(2 * np.pi * 110.0 * t + 0.5) * (0.5 + 0.5 * lfo2)
    tone_165 = np.sin(2 * np.pi * 164.81 * t + 1.2) * (0.35 + 0.35 * lfo1)
    tone_220 = np.sin(2 * np.pi * 220.0 * t + 2.0) * (0.2 + 0.2 * lfo2)

    synth_drone = tone_55 + tone_110 + tone_165 + tone_220

    # 2. Textura sutil de fundo (filtro passa-baixa em ruído)
    noise = np.random.normal(0, 0.05, n_samples)
    # Suavização simples (média móvel) para cortar agudos e deixar quente
    window_size = 120
    kernel = np.ones(window_size) / window_size
    # Aplicar convolução rápida em blocos ou aproximação IIR
    alpha = 0.03
    filtered_noise = np.zeros(n_samples)
    acc = 0.0
    for i in range(min(n_samples, 44100 * 5)):  # aquece nos primeiros segundos
        acc = acc + alpha * (noise[i] - acc)
        filtered_noise[i] = acc
    # replicar padrão suavizado para economizar tempo
    if n_samples > len(filtered_noise):
        repeats = int(np.ceil(n_samples / len(filtered_noise)))
        filtered_noise = np.tile(filtered_noise[:44100 * 5], repeats)[:n_samples]

    # 3. Mixagem do drone e da textura
    mix = 0.75 * synth_drone + 0.25 * filtered_noise

    # 4. Fade in (3s) e Fade out (3s)
    fade_len = int(3.0 * sample_rate)
    if n_samples > 2 * fade_len:
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        mix[:fade_len] *= fade_in
        mix[-fade_len:] *= fade_out

    # 5. Normalizar para -26 dBFS (para ficar no fundo sem atrapalhar a voz humana)
    target_amp = 10 ** (-26.0 / 20.0)  # ~0.050
    current_max = np.max(np.abs(mix))
    if current_max > 0:
        mix = (mix / current_max) * target_amp

    int16_data = np.int16(mix * 32767)

    # Gravar arquivo WAV estéreo
    with wave.open(out_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int16_data.tobytes())

    return out_path


if __name__ == "__main__":
    p = ensure_dark_ambient_bgm(60.0)
    print(f"BGM dark ambient criada com sucesso em: {p}")
