"""src/generate_branding.py - Gera avatar e banner oficiais do canal Código Social.

Identidade visual:
- Canal: Código Social
- Handle: @CodigoSocialOficial
- Avatar 800x800: Fundo #000000, anel dourado #FFD700 de 14px, stickman confiante com coroa dourada.
- Banner 2560x1440: Fundo #000000, safe area 1546x423 central, título em branco, subtítulo em #FFD700, dois bonecos ligados por linha pontilhada #FF2A2A.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PIL import Image, ImageDraw
from src.stickman_renderer import (
    StickmanRenderer, Fig, Accessory, get_font,
    COLOR_GOLD, COLOR_WHITE, COLOR_RED, COLOR_BG
)
BRANDING_DIR = os.path.join(PROJECT_ROOT, "assets", "branding")


def generate_avatar(out_path: str) -> str:
    """Gera avatar 800x800 com anel dourado de 14px e stickman confiante coroado."""
    w, h = 800, 800
    renderer = StickmanRenderer(scale_factor=2)
    canvas = renderer.create_canvas(w, h, spotlight=(0.5, 0.45, 0.45))
    sf = renderer.sf

    # Sr. Palito centralizado
    fig = Fig(
        x=400,
        y=610,
        scale=1.6,
        pose="confident",
        expression="smirk",
        color=COLOR_WHITE,
        head_accessory="crown",
        is_sr_palito=True,
        facing=1
    )
    renderer.draw_figure(canvas, fig)

    # Anel dourado #FFD700 de 14px nas bordas seguras
    draw = ImageDraw.Draw(canvas)
    ring_width = int(14 * sf)
    margin = int(24 * sf)
    draw.ellipse(
        [margin, margin, w * sf - margin, h * sf - margin],
        outline=COLOR_GOLD,
        width=ring_width
    )

    final_img = canvas.resize((w, h), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    final_img.save(out_path, format="PNG")
    print(f"Avatar gerado: {out_path} (dimensões: {final_img.size})")
    return out_path


def generate_banner(out_path: str) -> str:
    """Gera banner 2560x1440 com safe area central 1546x423."""
    w, h = 2560, 1440
    renderer = StickmanRenderer(scale_factor=2)
    canvas = renderer.create_canvas(w, h, spotlight=(0.5, 0.5, 0.5))
    sf = renderer.sf

    # Safe Area central: 1546 x 423
    safe_w = 1546
    safe_h = 423
    safe_x1 = (w - safe_w) // 2  # 507
    safe_y1 = (h - safe_h) // 2  # 508.5 -> 508
    safe_x2 = safe_x1 + safe_w   # 2053
    safe_y2 = safe_y1 + safe_h   # 931
    safe_cy = (safe_y1 + safe_y2) // 2

    # Dois stickmans nas laterais da safe area (Sr. Palito à esquerda)
    fig_left = Fig(
        x=safe_x1 + 180,
        y=safe_y2 - 30,
        scale=1.15,
        pose="confident",
        expression="smirk",
        color=COLOR_WHITE,
        head_accessory="crown",
        is_sr_palito=True,
        facing=1
    )
    fig_right = Fig(
        x=safe_x2 - 180,
        y=safe_y2 - 30,
        scale=1.2,
        pose="slouched",
        expression="smirk",
        color=(140, 140, 140),
        body_accessory="scissors",
        facing=-1
    )

    # Linha pontilhada vermelha #FF2A2A conectando os dois
    acc_dotted = Accessory(
        kind="dotted",
        x1=safe_x1 + 180,
        y1=safe_cy - 10,
        x2=safe_x2 - 180,
        y2=safe_cy - 10,
        color=COLOR_RED
    )

    renderer.draw_accessory(canvas, acc_dotted)
    renderer.draw_figure(canvas, fig_left)
    renderer.draw_figure(canvas, fig_right)

    # Tipografia no centro da Safe Area
    draw = ImageDraw.Draw(canvas)
    title_font = get_font(int(84 * sf))
    subtitle_font = get_font(int(36 * sf))

    title_text = "CÓDIGO SOCIAL"
    sub_text = "ELES JOGAM. VOCÊ ENXERGA."

    # Título centralizado
    t_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    t_w = t_bbox[2] - t_bbox[0]
    t_x = (w * sf - t_w) // 2
    t_y = int((safe_cy - 65) * sf)

    # Sombra do título
    draw.text((t_x + 3 * sf, t_y + 3 * sf), title_text, font=title_font, fill=(0, 0, 0, 200))
    draw.text((t_x, t_y), title_text, font=title_font, fill=COLOR_WHITE)

    # Subtítulo centralizado em #FFD700
    s_bbox = draw.textbbox((0, 0), sub_text, font=subtitle_font)
    s_w = s_bbox[2] - s_bbox[0]
    s_x = (w * sf - s_w) // 2
    s_y = int((safe_cy + 35) * sf)

    draw.text((s_x + 2 * sf, s_y + 2 * sf), sub_text, font=subtitle_font, fill=(0, 0, 0, 200))
    draw.text((s_x, s_y), sub_text, font=subtitle_font, fill=COLOR_GOLD)

    final_img = canvas.resize((w, h), Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    final_img.save(out_path, format="PNG")
    print(f"Banner gerado: {out_path} (dimensões: {final_img.size})")
    return out_path


def main():
    avatar_path = os.path.join(BRANDING_DIR, "avatar_800x800.png")
    banner_path = os.path.join(BRANDING_DIR, "banner_2560x1440.png")

    generate_avatar(avatar_path)
    generate_banner(banner_path)

    # Validar dimensões exatas via PIL
    im_av = Image.open(avatar_path)
    im_ba = Image.open(banner_path)
    assert im_av.size == (800, 800), f"Avatar tamanho inválido: {im_av.size}"
    assert im_ba.size == (2560, 1440), f"Banner tamanho inválido: {im_ba.size}"
    print(f"[OK] Identidade visual validada com sucesso! Avatar: {im_av.size}, Banner: {im_ba.size}")


if __name__ == "__main__":
    main()
