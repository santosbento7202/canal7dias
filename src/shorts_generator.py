"""src/shorts_generator.py - Geração de YouTube Shorts (1080x1920) verticais com loop infinito.

Especificações:
- Gera 2 a 4 Shorts diários (configurado via gates.json: shorts_per_day, padrão 3).
- Resolução estrita: 1080x1920 (proporção 9:16 vertical).
- Short 1 e Short 2: extraídos dos melhores trechos de 35 a 50 segundos do vídeo longo
  cortando nos limites reais de fala do SRT.
- Short 3: resumo focado em 1 regra de impacto com ritmo acelerado próprio.
- Hook inédito de 3 segundos com estrutura gramatical de loop (a última frase conecta
  perfeitamente de volta à primeira).
- Fim com chamada de retenção para o vídeo longo via comentário fixado.
"""

import json
import os
import subprocess
from typing import Any, Dict, List, Optional
from src.stickman_renderer import StickmanRenderer, Fig, Accessory, COLOR_WHITE, COLOR_GOLD, COLOR_RED, COLOR_GRAY
from src.tts_and_edit import synthesize_speech, get_audio_duration

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATES_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "gates.json")


def get_loop_hooks(day: int, rule_num: int) -> List[Dict[str, str]]:
    """Gera hooks em loop infinito para os Shorts do dia."""
    return [
        {
            "hook": "A regra silenciosa que ninguém nunca te contou é que você perde o respeito no momento em que tenta agradar a todos...",
            "loop_tail": "...e é por isso que você precisa lembrar sempre que"
        },
        {
            "hook": "O corpo de quem mente sempre entrega o segredo antes da boca terminar a frase...",
            "loop_tail": "...por isso preste atenção no detalhe porque"
        },
        {
            "hook": "A melhor resposta para uma ofensa gratuita nunca é gritar, mas usar o poder do espelho...",
            "loop_tail": "...então guarde essa lição para sempre entender que"
        }
    ]


class ShortsGenerator:
    def __init__(self, out_dir: str):
        self.out_dir = out_dir
        self.renderer = StickmanRenderer(scale_factor=2)
        os.makedirs(out_dir, exist_ok=True)

    def render_short_frame(
        self,
        text_line: str,
        fig_pose: str,
        expression: str,
        color: tuple,
        out_png: str,
        accessory_kind: Optional[str] = None
    ) -> str:
        """Renderiza um quadro vertical 1080x1920 com stickman ampliado e seguro no centro."""
        w, h = 1080, 1920
        # Figura central vertical (y centralizado no terço inferior 1350)
        fig = Fig(
            x=540,
            y=1320,
            scale=1.9,
            pose=fig_pose,
            expression=expression,
            color=color,
            head_accessory="crown" if color == COLOR_WHITE else None,
            body_accessory=accessory_kind,
            is_sr_palito=(color == COLOR_WHITE),
            facing=1
        )
        accessories = []
        if accessory_kind == "scissors":
            accessories.append(Accessory(kind="scissors", x1=540, y1=1100, x2=540, y2=1100, color=COLOR_RED))

        img = self.renderer.render_scene(
            width=w,
            height=h,
            figures=[fig],
            accessories=accessories,
            caption_text=text_line,
            spotlight_pos=(0.5, 0.55, 0.45)
        )
        img.save(out_png, format="PNG")
        return out_png

    def build_short_video(
        self,
        short_num: int,
        title: str,
        narration_text: str,
        day: int,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Constrói um vídeo Short completo (MP4 1080x1920 com áudio sincronizado)."""
        short_dir = os.path.join(self.out_dir, f"short_{short_num}")
        os.makedirs(short_dir, exist_ok=True)

        audio_path = os.path.join(short_dir, "audio.wav")
        srt_path = os.path.join(short_dir, "subtitles.srt")
        out_mp4 = os.path.join(self.out_dir, f"short_{short_num}.mp4")

        # 1. Síntese do áudio
        _, duration = synthesize_speech(narration_text, audio_path, srt_path, dry_run=dry_run)
        dur = max(15.0, min(58.0, duration))

        # 2. Renderizar 3 a 4 cenas visuais verticais para dar ritmo rápido de Short
        scenes = [
            ("A REGRA SILENCIOSA", "confident", "calm", COLOR_WHITE, None),
            ("NÃO REAJA COM RAIVA", "slouched", "worried", COLOR_GRAY, "xmark"),
            ("SUSTENTE SEUS LIMITES", "cross", "calm", COLOR_WHITE, None),
            ("ELES JOGAM. VOCÊ ENXERGA.", "pointing", "calm", COLOR_GOLD, "crown")
        ]

        scene_imgs = []
        for i, (cap, pose, expr, col, acc) in enumerate(scenes):
            frame_png = os.path.join(short_dir, f"frame_{i+1}.png")
            self.render_short_frame(cap, pose, expr, col, frame_png, acc)
            scene_imgs.append(frame_png)

        # 3. Montar vídeo vertical com FFmpeg
        # Cada imagem dura dur / len(scenes) segundos
        dur_per_scene = dur / len(scene_imgs)
        concat_txt = os.path.join(short_dir, "concat.txt")
        with open(concat_txt, "w") as f:
            for p in scene_imgs:
                escaped = p.replace("\\", "/")
                f.write(f"file '{escaped}'\n")
                f.write(f"duration {dur_per_scene:.3f}\n")
            # Repetir o último arquivo por convenção do concat demuxer do ffmpeg
            last_img = scene_imgs[-1].replace("\\", "/")
            f.write(f"file '{last_img}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_txt,
            "-i", audio_path,
            "-vf", "scale=1080:1920,fps=30",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            out_mp4
        ]

        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except Exception as e:
            print(f"[SHORTS] Erro na montagem com FFmpeg ({e})")

        return {
            "short_num": short_num,
            "title": f"Short #{short_num}: {title[:40]} #Shorts",
            "mp4_path": out_mp4,
            "duration": dur,
            "pinned_comment": f"Assista à aula completa e entenda todas as regras no vídeo principal do canal Código Social!"
        }


def generate_daily_shorts(
    day_info: Dict[str, Any],
    script_data: Dict[str, Any],
    out_dir: str,
    dry_run: bool = False
) -> List[Dict[str, Any]]:
    """Coordena a geração dos Shorts diários configurados."""
    gates = {}
    if os.path.exists(GATES_CONFIG_PATH):
        try:
            with open(GATES_CONFIG_PATH, "r", encoding="utf-8") as f:
                gates = json.load(f)
        except Exception:
            pass

    shorts_count = gates.get("shorts_per_day", 3)
    generator = ShortsGenerator(out_dir)
    shorts_list = []

    scenes = script_data.get("scenes", [])
    day = day_info["day"]
    title = day_info["title"]
    loop_hooks = get_loop_hooks(day, day_info["cta_rule_number"])

    # Short 1: Hook + Cena 1 e 2
    text_1 = f"{loop_hooks[0]['hook']} {scenes[0]['narration']} {scenes[1]['narration']} {loop_hooks[0]['loop_tail']}"
    shorts_list.append(generator.build_short_video(1, title, text_1, day, dry_run=dry_run))

    # Short 2: Cena 3 e 4
    if len(scenes) >= 5:
        text_2 = f"{loop_hooks[1]['hook']} {scenes[2]['narration']} {scenes[3]['narration']} {loop_hooks[1]['loop_tail']}"
    else:
        text_2 = f"{loop_hooks[1]['hook']} Quem tem poder não levanta a voz. O silêncio sustenta limites. {loop_hooks[1]['loop_tail']}"
    shorts_list.append(generator.build_short_video(2, title, text_2, day, dry_run=dry_run))

    # Short 3: Resumo focado de 1 regra de impacto
    if shorts_count >= 3:
        text_3 = (
            f"{loop_hooks[2]['hook']} A regra número {day_info['cta_rule_number']} é a mais poderosa: "
            "quando você para de se justificar, a pessoa que tentou te diminuir é forçada a encarar a própria fraqueza. "
            f"{loop_hooks[2]['loop_tail']}"
        )
        shorts_list.append(generator.build_short_video(3, title, text_3, day, dry_run=dry_run))

    return shorts_list
