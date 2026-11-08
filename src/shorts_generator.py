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

        # 3. Preparar artes 4K oficiais e clipes múltiplos dinâmicos (evita repetição e cortes indevidos)
        art_keys = [
            "sr_palito_steeple.jpg",
            "sr_palito_cufflinks.jpg",
            "sr_palito_skyscraper.jpg",
            "sr_palito_blueprint.jpg"
        ]
        chosen_art = art_keys[(short_num - 1) % len(art_keys)]
        art_full_path = os.path.join(PROJECT_ROOT, "assets", "branding", chosen_art)
        if not os.path.exists(art_full_path):
            art_full_path = os.path.join(PROJECT_ROOT, "assets", "branding", "sr_palito_power.jpg")

        # 4. Biblioteca de múltiplos clipes por Short (cortes rápidos a cada ~3-4s sem repetição)
        day_specific_multiclips = {
            1: {
                1: [
                    "assets/broll_cache/napoleon_screaming.mp4",
                    "assets/broll_cache/talleyrand_calm_stare.mp4",
                    "assets/broll_cache/thomas_shelby_smoke.mp4",
                    "assets/broll_cache/talleyrand_smirk.mp4"
                ],
                2: [
                    "assets/broll_cache/musashi_samurai_duel.mp4",
                    "assets/broll_cache/napoleon_battle_anger.mp4",
                    "assets/broll_cache/samurai_strike_fast.mp4",
                    "assets/broll_cache/shelby_silence_stare.mp4"
                ],
                3: [
                    "assets/broll_cache/american_psycho_sweat.mp4",
                    "assets/broll_cache/hannibal_eye_contact.mp4",
                    "assets/broll_cache/logan_roy_stare.mp4",
                    "assets/broll_cache/fight_club_unreactive.mp4"
                ]
            },
            2: {
                1: [
                    "assets/broll_cache/feet_pointing_door.mp4",
                    "assets/broll_cache/interrogation_mirror.mp4",
                    "assets/broll_cache/eye_shift_nervous.mp4",
                    "assets/broll_cache/hannibal_eye_contact.mp4"
                ],
                2: [
                    "assets/broll_cache/logan_roy_stare.mp4",
                    "assets/broll_cache/godfather_door_close.mp4",
                    "assets/broll_cache/nervous_hands_fidget.mp4",
                    "assets/broll_cache/interrogation_mirror.mp4"
                ],
                3: [
                    "assets/broll_cache/talleyrand_smirk.mp4",
                    "assets/broll_cache/hannibal_eye_contact.mp4",
                    "assets/broll_cache/american_psycho_sweat.mp4",
                    "assets/broll_cache/shelby_silence_stare.mp4"
                ]
            }
        }

        day_clips = day_specific_multiclips.get(day, day_specific_multiclips[1])
        raw_clip_candidates = day_clips.get(short_num, day_clips[1])
        valid_clips = []
        for rc in raw_clip_candidates:
            p = os.path.join(PROJECT_ROOT, rc) if not os.path.isabs(rc) else rc
            if os.path.exists(p):
                valid_clips.append(p)

        badge_files = [
            "narrator_badge_thinking.png",
            "narrator_badge_official.png",
            "narrator_badge_power.png"
        ]
        badge_name = badge_files[(short_num - 1) % len(badge_files)]
        badge_path = os.path.join(PROJECT_ROOT, "assets", "branding", badge_name)

        anim_vertical_clips = []
        if valid_clips:
            narr_dur_1 = min(3.5, dur * 0.18)
            narr_dur_2 = min(3.0, dur * 0.15)
            sit_total_dur = max(4.0, dur - narr_dur_1 - narr_dur_2)
            per_clip_dur = sit_total_dur / len(valid_clips)

            # A. Narrador Abertura (Full-Screen 1080x1920 com fundo desfocado estético, sem cortar a imagem)
            anim_n1 = os.path.join(short_dir, "anim_narr_1.mp4")
            cmd_n1 = [
                "ffmpeg", "-y", "-loop", "1", "-i", art_full_path,
                "-t", f"{narr_dur_1:.3f}",
                "-filter_complex",
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.25[bg];"
                "[0:v]scale=1080:-1[fg];"
                "[bg][fg]overlay=0:(H-h)/2,fps=30[v_out]",
                "-map", "[v_out]",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                anim_n1
            ]
            r1 = subprocess.run(cmd_n1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if r1.returncode == 0 and os.path.exists(anim_n1):
                anim_vertical_clips.append(anim_n1)

            # B. Sequência de Múltiplos Clipes Variados (Sem cortar o vídeo e com badge no canto)
            for idx, c_path in enumerate(valid_clips):
                part_path = os.path.join(short_dir, f"sit_vert_{idx+1}.mp4")
                if os.path.exists(badge_path):
                    cmd_c = [
                        "ffmpeg", "-y", "-stream_loop", "3", "-i", c_path, "-i", badge_path,
                        "-t", f"{per_clip_dur:.3f}",
                        "-filter_complex",
                        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.25[bg];"
                        "[0:v]scale=1080:-1[fg];"
                        "[bg][fg]overlay=0:(H-h)/2[comp];"
                        "[1:v]scale=220:220[badge];"
                        "[comp][badge]overlay=W-w-35:H-h-240[v_out]",
                        "-map", "[v_out]",
                        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                        part_path
                    ]
                else:
                    cmd_c = [
                        "ffmpeg", "-y", "-stream_loop", "3", "-i", c_path,
                        "-t", f"{per_clip_dur:.3f}",
                        "-filter_complex",
                        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.25[bg];"
                        "[0:v]scale=1080:-1[fg];"
                        "[bg][fg]overlay=0:(H-h)/2,fps=30[v_out]",
                        "-map", "[v_out]",
                        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                        part_path
                    ]
                rc = subprocess.run(cmd_c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if rc.returncode == 0 and os.path.exists(part_path):
                    anim_vertical_clips.append(part_path)

            # C. Narrador Fechamento (Full-Screen 1080x1920 com fundo desfocado, sem corte)
            anim_n2 = os.path.join(short_dir, "anim_narr_2.mp4")
            cmd_n2 = [
                "ffmpeg", "-y", "-loop", "1", "-i", art_full_path,
                "-t", f"{narr_dur_2:.3f}",
                "-filter_complex",
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.25[bg];"
                "[0:v]scale=1080:-1[fg];"
                "[bg][fg]overlay=0:(H-h)/2,fps=30[v_out]",
                "-map", "[v_out]",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                anim_n2
            ]
            r2 = subprocess.run(cmd_n2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if r2.returncode == 0 and os.path.exists(anim_n2):
                anim_vertical_clips.append(anim_n2)
        else:
            anim_clip_path = os.path.join(short_dir, "anim_vert_fallback.mp4")
            cmd_anim = [
                "ffmpeg", "-y", "-loop", "1",
                "-i", art_full_path,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                "-t", f"{dur:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                anim_clip_path
            ]
            res = subprocess.run(cmd_anim, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0 and os.path.exists(anim_clip_path):
                anim_vertical_clips.append(anim_clip_path)

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
