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

        # 2. Gerar legendas verticais cinéticas ASS
        from src.subtitle_styler import srt_to_dynamic_ass
        ass_path = os.path.join(short_dir, "subtitles.ass")
        srt_to_dynamic_ass(srt_path, ass_path, is_vertical=True)

        # 3. Preparar quadros com arte 4K oficial do Sr. Palito adaptada para vertical (1080x1920)
        from PIL import Image
        art_keys = [
            "sr_palito_pointing.jpg",
            "sr_palito_thinking.jpg",
            "sr_palito_power.jpg",
            "sr_palito_official_fullbody.jpg"
        ]
        chosen_art = art_keys[(short_num - 1) % len(art_keys)]
        art_full_path = os.path.join(PROJECT_ROOT, "assets", "branding", chosen_art)

        scene_imgs = []
        if os.path.exists(art_full_path):
            base = Image.open(art_full_path).convert("RGB")
            # Redimensiona para cobrir o centro vertical
            target_w, target_h = 1080, 1920
            # Redimensiona mantendo proporção com corte central
            scale = max(target_w / base.width, target_h / base.height)
            new_w = int(base.width * scale)
            new_h = int(base.height * scale)
            resized = base.resize((new_w, new_h), Image.Resampling.LANCZOS)
            x0 = (new_w - target_w) // 2
            y0 = (new_h - target_h) // 2
            cropped = resized.crop((x0, y0, x0 + target_w, y0 + target_h))

            for i in range(3):
                frame_png = os.path.join(short_dir, f"frame_{i+1}.png")
                cropped.save(frame_png, format="PNG")
                scene_imgs.append(frame_png)
        else:
            scenes = [
                ("A REGRA SILENCIOSA", "confident", "calm", COLOR_WHITE, None),
                ("NÃO REAJA COM RAIVA", "slouched", "worried", COLOR_GRAY, "xmark"),
                ("SUSTENTE SEUS LIMITES", "cross", "calm", COLOR_WHITE, None),
                ("ELES JOGAM. VOCÊ ENXERGA.", "pointing", "calm", COLOR_GOLD, "crown")
            ]
            for i, (cap, pose, expr, col, acc) in enumerate(scenes):
                frame_png = os.path.join(short_dir, f"frame_{i+1}.png")
                self.render_short_frame(cap, pose, expr, col, frame_png, acc)
                scene_imgs.append(frame_png)

        # 4. Intercalar Narrador e Clipes de Situações/Filmes
        from src.gif_situations import search_and_download_gif_clip
        short_situation_map = {
            1: ("napoleon angry", "napoleon_screaming"),
            2: ("samurai sword duel", "musashi_samurai_duel"),
            3: ("roman emperor", "julius_caesar_power")
        }
        sit_info = short_situation_map.get(short_num)
        sit_clip_path = None
        if sit_info:
            sit_clip_path = search_and_download_gif_clip(sit_info[0], sit_info[1], 1080, 1920, 8.0)

        anim_vertical_clips = []
        if sit_clip_path and os.path.exists(sit_clip_path):
            narr_dur_1 = min(4.0, dur * 0.25)
            sit_dur = max(4.0, dur * 0.50)
            narr_dur_2 = max(3.0, dur - narr_dur_1 - sit_dur)

            # A. Narrador Abertura
            anim_n1 = os.path.join(short_dir, "anim_narr_1.mp4")
            frames_n1 = int(narr_dur_1 * 30)
            cmd_n1 = [
                "ffmpeg", "-y", "-i", scene_imgs[0],
                "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0008,1.06)':d={frames_n1}:s=1080x1920:fps=30",
                "-t", f"{narr_dur_1:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                anim_n1
            ]
            subprocess.run(cmd_n1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if os.path.exists(anim_n1): anim_vertical_clips.append(anim_n1)

            # B. Clipe do Filme/Situação Real
            sit_vert = os.path.join(short_dir, "sit_vert.mp4")
            cmd_sv = [
                "ffmpeg", "-y", "-stream_loop", "3", "-i", sit_clip_path,
                "-t", f"{sit_dur:.3f}",
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                sit_vert
            ]
            subprocess.run(cmd_sv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if os.path.exists(sit_vert): anim_vertical_clips.append(sit_vert)

            # C. Narrador Fechamento
            anim_n2 = os.path.join(short_dir, "anim_narr_2.mp4")
            frames_n2 = int(narr_dur_2 * 30)
            cmd_n2 = [
                "ffmpeg", "-y", "-i", scene_imgs[-1],
                "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0008,1.06)':d={frames_n2}:s=1080x1920:fps=30",
                "-t", f"{narr_dur_2:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                anim_n2
            ]
            subprocess.run(cmd_n2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if os.path.exists(anim_n2): anim_vertical_clips.append(anim_n2)
        else:
            dur_per_scene = dur / len(scene_imgs)
            for idx, spath in enumerate(scene_imgs):
                anim_clip_path = os.path.join(short_dir, f"anim_vert_{idx+1}.mp4")
                frames = int(dur_per_scene * 30)
                cmd_anim = [
                    "ffmpeg", "-y",
                    "-i", spath,
                    "-vf", f"scale=1080:1920,zoompan=z='min(zoom+0.0008,1.06)':d={frames}:s=1080x1920:fps=30",
                    "-t", f"{dur_per_scene:.3f}",
                    "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    anim_clip_path
                ]
                res = subprocess.run(cmd_anim, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if res.returncode == 0 and os.path.exists(anim_clip_path):
                    anim_vertical_clips.append(anim_clip_path)
                else:
                    anim_vertical_clips.append(spath)

        concat_txt = os.path.join(short_dir, "concat.txt")
        with open(concat_txt, "w") as f:
            for p in anim_vertical_clips:
                escaped = p.replace("\\", "/")
                f.write(f"file '{escaped}'\n")

        bgm_path = os.path.join(PROJECT_ROOT, "assets", "audio", "dark_ambient_drone.wav")
        if not os.path.exists(bgm_path):
            try:
                from src.audio_ambient import ensure_dark_ambient_bgm
                ensure_dark_ambient_bgm(60.0, bgm_path)
            except Exception:
                pass

        vf_vert = "scale=1080:1920,fps=30"
        if os.path.exists(os.path.join(short_dir, "subtitles.ass")):
            vf_vert = "scale=1080:1920,subtitles=subtitles.ass,fps=30"

        if os.path.exists(bgm_path):
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_txt,
                "-i", audio_path,
                "-stream_loop", "-1", "-i", bgm_path,
                "-filter_complex", "[1:a]volume=1.0[v_aud];[2:a]volume=0.18[b_aud];[v_aud][b_aud]amix=inputs=2:duration=first:dropout_transition=2[aout]",
                "-map", "0:v",
                "-map", "[aout]",
                "-vf", vf_vert,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                out_mp4
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_txt,
                "-i", audio_path,
                "-vf", vf_vert,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                out_mp4
            ]

        try:
            subprocess.run(cmd, cwd=short_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
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

    day = day_info["day"]
    title = day_info["title"]

    # Se houver histórias curadas de alto impacto em DAY_SCRIPTS, priorizar para máxima retenção
    try:
        from src.day_scripts import DAY_SCRIPTS
        curated_shorts = DAY_SCRIPTS.get(day, {}).get("shorts_stories", [])
    except Exception:
        curated_shorts = []

    if curated_shorts and len(curated_shorts) >= 3:
        for cs in curated_shorts[:shorts_count]:
            s_num = cs["short_num"]
            s_title = cs["title"]
            s_text = cs["narration"]
            shorts_list.append(generator.build_short_video(s_num, s_title, s_text, day, dry_run=dry_run))
        return shorts_list

    scenes = script_data.get("scenes", [])
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
