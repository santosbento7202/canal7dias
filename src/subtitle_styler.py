"""src/subtitle_styler.py - Gerador de legendas cinéticas de alta retenção (.ass) para FFmpeg.

Gera legendas dinâmicas no estilo viral (Alex Hormozi / Aperture / Dark Psychology):
- Formatação ASS estilizada com fonte bold e borda preta espessa.
- Destaque em ouro (#FFD700) para palavras-chave de poder psicológico.
- Quebra de frases longas em blocos dinâmicos de 3 a 5 palavras.
"""

import os
import re
from typing import List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(PROJECT_ROOT, "assets", "fonts")

HIGHLIGHT_KEYWORDS = {
    "respeito", "pausa", "silêncio", "silenciosas", "regras", "regra",
    "comando", "autoridade", "coragem", "dominância", "valor", "controle",
    "erro", "fatal", "espelho", "firme", "calma", "insegurança", "presença",
    "zero", "olhar", "submissão", "psicologia", "sete", "90%"
}


def time_to_ass(time_str: str) -> str:
    """Converte formato SRT (00:00:01,234) para ASS (0:00:01.23)."""
    time_str = time_str.strip().replace(",", ".")
    parts = time_str.split(":")
    if len(parts) == 3:
        hrs = int(parts[0])
        mins = int(parts[1])
        secs = float(parts[2])
        return f"{hrs}:{mins:02d}:{secs:05.2f}"
    return "0:00:00.00"


def highlight_text(text: str) -> str:
    """Aplica cor dourada (&H0000D7FF&) às palavras de poder e branco (&H00FFFFFF&) ao restante."""
    words = text.split()
    styled_words = []
    for w in words:
        clean_w = re.sub(r"[^\w%]", "", w).lower()
        if clean_w in HIGHLIGHT_KEYWORDS:
            styled_words.append(r"{\c&H0000D7FF&}" + w.upper() + r"{\c&H00FFFFFF&}")
        else:
            styled_words.append(w.upper())
    return " ".join(styled_words)


def srt_to_dynamic_ass(srt_path: str, ass_path: str, is_vertical: bool = False) -> str:
    """Converte um arquivo SRT para legendas estilizadas .ASS para renderização no FFmpeg."""
    if not os.path.exists(srt_path):
        return ""

    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"\n\s*\n", content.strip())
    dialogues = []

    res_x = 1080 if is_vertical else 1920
    res_y = 1920 if is_vertical else 1080
    font_size = 64 if is_vertical else 46
    margin_v = 450 if is_vertical else 100

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            time_match = re.search(r"(\d\d:\d\d:\d\d[,\.]\d+)\s*-->\s*(\d\d:\d\d:\d\d[,\.]\d+)", lines[1])
            if time_match:
                start_raw = time_match.group(1)
                end_raw = time_match.group(2)
                start_ass = time_to_ass(start_raw)
                end_ass = time_to_ass(end_raw)
                raw_text = " ".join(lines[2:]).strip()

                # Quebrar em pequenos blocos de até 5 palavras para ritmo dinâmico
                words = raw_text.split()
                if len(words) <= 5:
                    styled = highlight_text(raw_text)
                    dialogues.append(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{styled}")
                else:
                    chunk_size = 4
                    n_chunks = (len(words) + chunk_size - 1) // chunk_size
                    # Calcular tempos proporcionais
                    t_start_s = parse_ass_seconds(start_ass)
                    t_end_s = parse_ass_seconds(end_ass)
                    t_dur = max(0.5, t_end_s - t_start_s)
                    step_dur = t_dur / n_chunks

                    for c_idx in range(n_chunks):
                        sub_words = words[c_idx * chunk_size : (c_idx + 1) * chunk_size]
                        sub_text = " ".join(sub_words)
                        c_start = format_seconds_to_ass(t_start_s + c_idx * step_dur)
                        c_end = format_seconds_to_ass(t_start_s + (c_idx + 1) * step_dur)
                        styled = highlight_text(sub_text)
                        dialogues.append(f"Dialogue: 0,{c_start},{c_end},Default,,0,0,0,,{styled}")

    ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {res_x}
PlayResY: {res_y}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Anton,{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,4,3,2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    full_ass = ass_header + "\n".join(dialogues) + "\n"
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(full_ass)

    return ass_path


def parse_ass_seconds(t_str: str) -> float:
    parts = t_str.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    return 0.0


def format_seconds_to_ass(secs: float) -> str:
    hrs = int(secs // 3600)
    mins = int((secs % 3600) // 60)
    s = secs % 60
    return f"{hrs}:{mins:02d}:{s:05.2f}"
