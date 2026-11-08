"""src/gif_situations.py - Coletor e processador de GIFs/clipes de filmes e situações reais.

Pesquisa e baixa clipes MP4 de alta relevância (Tenor) para ilustrar exatamente o que o Narrador está falando:
- Cenas de filmes históricos (Napoleão, Júlio César, Samurais).
- Expressões e linguagem corporal (olhar frio de Thomas Shelby, The Godfather, silêncio tenso).
- Ajuste automático de resolução para 1920x1080 H.264 30fps.
"""

import os
import re
import subprocess
import requests
from typing import Optional, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(PROJECT_ROOT, "assets", "broll_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def search_and_download_gif_clip(
    query: str,
    output_filename: str,
    target_width: int = 1920,
    target_height: int = 1080,
    duration_sec: float = 6.0
) -> Optional[str]:
    """Busca um clipe de situação/filme e converte para MP4 1080p padronizado."""
    clean_name = re.sub(r"[^\w\-]", "_", output_filename) + ".mp4"
    final_path = os.path.join(CACHE_DIR, clean_name)

    # Se já foi baixado e tem tamanho válido, reaproveitar cache
    if os.path.exists(final_path) and os.path.getsize(final_path) > 20000:
        return final_path

    # 1. Buscar no Tenor Web
    slug_query = re.sub(r"\s+", "-", query.strip().lower())
    search_url = f"https://tenor.com/search/{slug_query}-gifs"

    mp4_urls = []
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=8)
        if resp.status_code == 200:
            # Capturar links diretos de mídia mp4
            found = re.findall(r'https://media\.tenor\.com/[^"\'\s]+\.mp4', resp.text)
            # Priorizar clipes de tamanho completo (geralmente terminam com AAP1 ou AAPo)
            for u in found:
                if u not in mp4_urls:
                    mp4_urls.append(u)
    except Exception as e:
        print(f"[GIF] Erro ao buscar '{query}': {e}")

    if not mp4_urls:
        print(f"[GIF] Nenhum clipe encontrado para '{query}'.")
        return None

    # 2. Baixar o primeiro clipe válido
    raw_temp = os.path.join(CACHE_DIR, f"temp_{clean_name}")
    downloaded = False
    for candidate_url in mp4_urls[:4]:
        try:
            r = requests.get(candidate_url, headers=HEADERS, timeout=12)
            if r.status_code == 200 and len(r.content) > 10000:
                with open(raw_temp, "wb") as f:
                    f.write(r.content)
                downloaded = True
                break
        except Exception:
            continue

    if not downloaded or not os.path.exists(raw_temp):
        return None

    # 3. Padronizar via FFmpeg: loop se for curto, crop centralizado para target_width x target_height, 30 fps
    vf = (
        f"scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
        f"crop={target_width}:{target_height},"
        f"fps=30"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "3",
        "-i", raw_temp,
        "-t", f"{duration_sec:.2f}",
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-an",
        final_path
    ]

    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if os.path.exists(raw_temp):
            try: os.remove(raw_temp)
            except Exception: pass
        if os.path.exists(final_path) and os.path.getsize(final_path) > 10000:
            print(f"[GIF] Clipe '{query}' processado com sucesso: {final_path}")
            return final_path
    except Exception as e:
        print(f"[GIF] Erro no processamento FFmpeg ({e})")

    return None


if __name__ == "__main__":
    # Teste rápido com Napoleão
    p = search_and_download_gif_clip("napoleon angry", "napoleon_screaming", 1920, 1080, 5.0)
    print("Resultado do teste:", p)
