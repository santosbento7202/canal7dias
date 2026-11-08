"""src/stickman_renderer.py - Stickman Premium Renderer.

Design specifications:
- Premium minimalist aesthetic: pure black (#000000) canvas with subtle spotlight (intensity <= 0.55).
- Supersampling (2x) for crisp, anti-aliased geometry and smooth glow.
- Stickman premium figures: thick white glowing stroke, grounded elliptical shadow,
  expressive faces (smile, fake_smile, smirk, angry, worried, calm, neutral),
  9 pose structures (confident, slouched, shouting, thinking, pointing, arms_wide, offer_left, cross, walking).
- Dynamic accessories: crown, xmark, arrow, dotted, scissors, mirror, marionette, phone, speech_bubble, lightning_eye.
- Typography: Bebas Neue or Anton (OFL) with fallback to DejaVu/Arial, high contrast text blocks with drop shadow and outline.
- Full support for 1920x1080 (landscape), 1080x1920 (Shorts portrait), and 1280x720 (YouTube Thumbnails).
"""

import math
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
FONTS_DIR = os.path.join(PROJECT_ROOT, "assets", "fonts")

# Typography lookup: prefer downloaded Anton or Bebas Neue, fallback to system DejaVu / Arial
def get_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        os.path.join(FONTS_DIR, "Anton-Regular.ttf"),
        os.path.join(FONTS_DIR, "BebasNeue-Regular.ttf"),
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "DejaVuSans-Bold.ttf",
        "arial.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

# Colors
COLOR_BG = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GOLD = (255, 215, 0)      # #FFD700
COLOR_RED = (255, 42, 42)       # #FF2A2A
COLOR_GRAY = (120, 120, 120)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_YELLOW = (255, 230, 0)

@dataclass
class Fig:
    x: float
    y: float  # Ground/feet y coordinate
    scale: float = 1.0
    pose: str = "confident"  # confident, slouched, shouting, thinking, pointing, arms_wide, offer_left, cross, walking
    expression: str = "calm"  # smile, fake_smile, smirk, angry, worried, calm, neutral
    color: Tuple[int, int, int] = COLOR_WHITE
    glow_color: Optional[Tuple[int, int, int, int]] = (255, 255, 255, 90)
    facing: int = 1  # 1: right, -1: left
    head_accessory: Optional[str] = None  # e.g. "crown"
    body_accessory: Optional[str] = None  # e.g. "xmark", "scissors", "mirror", "phone", "lightning_eye"

@dataclass
class Accessory:
    kind: str  # "arrow", "dotted", "marionette", "scissors", "mirror", "crown", "xmark", "speech_bubble"
    x1: float
    y1: float
    x2: float = 0.0
    y2: float = 0.0
    color: Tuple[int, int, int] = COLOR_GOLD
    extra: Dict[str, Any] = field(default_factory=dict)

class StickmanRenderer:
    def __init__(self, scale_factor: int = 2):
        self.sf = scale_factor

    def create_canvas(self, width: int, height: int, spotlight: Optional[Tuple[float, float, float]] = None) -> Image.Image:
        """Create a supersampled canvas with optional radial spotlight (intensity <= 0.55)."""
        w, h = width * self.sf, height * self.sf
        img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
        
        if spotlight:
            # spotlight = (center_x, center_y, intensity <= 0.55)
            cx, cy, intensity = spotlight
            intensity = min(0.55, max(0.05, intensity))
            cx_px, cy_px = int(cx * w), int(cy * h)
            max_r = int(min(w, h) * 0.75)
            
            spot = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            draw_spot = ImageDraw.Draw(spot)
            steps = 40
            for i in range(steps, 0, -1):
                r = int(max_r * (i / steps))
                alpha = int(255 * intensity * ((steps - i) / steps) ** 1.8)
                color = (255, 255, 255, alpha)
                draw_spot.ellipse([cx_px - r, cy_px - int(r * 0.6), cx_px + r, cy_px + int(r * 0.6)], fill=color)
            spot = spot.filter(ImageFilter.GaussianBlur(radius=int(25 * self.sf)))
            img = Image.alpha_composite(img, spot)
            
        return img

    def draw_shadow(self, draw: ImageDraw.ImageDraw, x: float, y: float, scale: float):
        """Ground shadow under stickman feet."""
        rx = int(45 * scale * self.sf)
        ry = int(12 * scale * self.sf)
        x_px, y_px = int(x * self.sf), int(y * self.sf)
        draw.ellipse([x_px - rx, y_px - ry, x_px + rx, y_px + ry], fill=(15, 15, 15, 180))

    def draw_face(self, draw: ImageDraw.ImageDraw, hx: float, hy: float, hr: float, expression: str, facing: int, color: Tuple[int, int, int]):
        """Render facial expression on stickman head."""
        f = facing
        eye_y = hy - hr * 0.15
        eye_spacing = hr * 0.35
        eye_r = max(2, int(2.5 * self.sf))
        
        left_eye_x = hx - eye_spacing * 0.5 + f * hr * 0.1
        right_eye_x = hx + eye_spacing * 0.5 + f * hr * 0.1
        mouth_y = hy + hr * 0.35
        
        # Eyes
        if expression == "angry":
            # Diagonal angled eyebrows
            draw.line([left_eye_x - 4 * self.sf, eye_y - 6 * self.sf, left_eye_x + 4 * self.sf, eye_y - 2 * self.sf], fill=color, width=int(2 * self.sf))
            draw.line([right_eye_x - 4 * self.sf, eye_y - 2 * self.sf, right_eye_x + 4 * self.sf, eye_y - 6 * self.sf], fill=color, width=int(2 * self.sf))
            draw.ellipse([left_eye_x - eye_r, eye_y - eye_r, left_eye_x + eye_r, eye_y + eye_r], fill=color)
            draw.ellipse([right_eye_x - eye_r, eye_y - eye_r, right_eye_x + eye_r, eye_y + eye_r], fill=color)
        elif expression == "worried":
            draw.line([left_eye_x - 4 * self.sf, eye_y - 2 * self.sf, left_eye_x + 4 * self.sf, eye_y - 6 * self.sf], fill=color, width=int(2 * self.sf))
            draw.line([right_eye_x - 4 * self.sf, eye_y - 6 * self.sf, right_eye_x + 4 * self.sf, eye_y - 2 * self.sf], fill=color, width=int(2 * self.sf))
            draw.ellipse([left_eye_x - eye_r, eye_y - eye_r, left_eye_x + eye_r, eye_y + eye_r], fill=color)
            draw.ellipse([right_eye_x - eye_r, eye_y - eye_r, right_eye_x + eye_r, eye_y + eye_r], fill=color)
        elif expression == "smirk":
            draw.line([right_eye_x - 4 * self.sf, eye_y - 6 * self.sf, right_eye_x + 4 * self.sf, eye_y - 4 * self.sf], fill=color, width=int(2 * self.sf))
            draw.ellipse([left_eye_x - eye_r, eye_y - eye_r, left_eye_x + eye_r, eye_y + eye_r], fill=color)
            draw.ellipse([right_eye_x - eye_r, eye_y - eye_r, right_eye_x + eye_r, eye_y + eye_r], fill=color)
        else:
            # Normal eyes
            draw.ellipse([left_eye_x - eye_r, eye_y - eye_r, left_eye_x + eye_r, eye_y + eye_r], fill=color)
            draw.ellipse([right_eye_x - eye_r, eye_y - eye_r, right_eye_x + eye_r, eye_y + eye_r], fill=color)

        # Mouth
        if expression == "smile":
            mx0, mx1 = hx - hr * 0.45 + f * 4 * self.sf, hx + hr * 0.45 + f * 4 * self.sf
            draw.arc([min(mx0, mx1), mouth_y - hr * 0.3, max(mx0, mx1), mouth_y + hr * 0.3], start=10, end=170, fill=color, width=int(2.5 * self.sf))
        elif expression == "fake_smile":
            # Exaggerated strained grin with teeth line
            draw.rectangle([hx - hr * 0.4, mouth_y - 3 * self.sf, hx + hr * 0.4, mouth_y + 4 * self.sf], outline=color, width=int(2 * self.sf))
            draw.line([hx - hr * 0.4, mouth_y, hx + hr * 0.4, mouth_y], fill=color, width=int(1.5 * self.sf))
        elif expression == "smirk":
            mx0 = hx - hr * 0.35 if f == 1 else hx - hr * 0.1
            mx1 = hx + hr * 0.5 if f == 1 else hx + hr * 0.35
            draw.arc([min(mx0, mx1), mouth_y - hr * 0.3, max(mx0, mx1), mouth_y + hr * 0.25], start=0, end=180, fill=color, width=int(2.5 * self.sf))
        elif expression == "angry":
            draw.line([hx - hr * 0.4, mouth_y + 3 * self.sf, hx + hr * 0.4, mouth_y - 1 * self.sf], fill=color, width=int(2.5 * self.sf))
        elif expression == "worried":
            draw.arc([hx - hr * 0.4, mouth_y, hx + hr * 0.4, mouth_y + hr * 0.4], start=190, end=350, fill=color, width=int(2.5 * self.sf))
        elif expression == "shouting":
            draw.ellipse([hx - hr * 0.3, mouth_y - hr * 0.2, hx + hr * 0.3, mouth_y + hr * 0.4], outline=color, fill=(0, 0, 0), width=int(2.5 * self.sf))
        else:  # calm / neutral
            draw.line([hx - hr * 0.3, mouth_y, hx + hr * 0.3, mouth_y], fill=color, width=int(2 * self.sf))

    def draw_figure(self, img: Image.Image, fig: Fig):
        """Draw single stickman with premium glow, shadow, pose, expression, accessories."""
        sf = self.sf
        x_px = fig.x * sf
        y_px = fig.y * sf
        scale = fig.scale * sf
        f = fig.facing
        c = fig.color
        stroke_w = max(3, int(6.0 * scale))
        glow_w = stroke_w + int(8 * scale)

        # 1. Ground shadow on base canvas
        shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw_shadow = ImageDraw.Draw(shadow_layer)
        self.draw_shadow(draw_shadow, fig.x, fig.y, fig.scale)
        img.paste(shadow_layer, (0, 0), shadow_layer)

        # 2. Key anatomical points calculated based on pose
        total_h = 240 * scale
        head_r = 26 * scale
        
        # Poses
        if fig.pose == "slouched":
            head_x = x_px + 25 * scale * f
            head_y = y_px - total_h + 30 * scale
            neck_x = x_px + 15 * scale * f
            neck_y = head_y + head_r
            pelvis_x = x_px - 10 * scale * f
            pelvis_y = y_px - 90 * scale
            left_hand = (x_px - 5 * scale, y_px - 95 * scale)
            right_hand = (x_px + 15 * scale * f, y_px - 85 * scale)
            left_foot = (x_px - 20 * scale, y_px)
            right_foot = (x_px + 10 * scale, y_px)
            chest_x, chest_y = (neck_x + pelvis_x) / 2, (neck_y + pelvis_y) / 2
        elif fig.pose == "shouting":
            head_x = x_px - 10 * scale * f
            head_y = y_px - total_h - 5 * scale
            neck_x = head_x
            neck_y = head_y + head_r
            pelvis_x = x_px
            pelvis_y = y_px - 95 * scale
            chest_x, chest_y = x_px + 5 * scale * f, (neck_y + pelvis_y) / 2
            left_hand = (chest_x + 50 * scale * f, chest_y - 25 * scale)
            right_hand = (chest_x + 40 * scale * f, chest_y + 10 * scale)
            left_foot = (x_px - 35 * scale, y_px)
            right_foot = (x_px + 25 * scale, y_px)
        elif fig.pose == "thinking":
            head_x = x_px
            head_y = y_px - total_h
            neck_x, neck_y = head_x, head_y + head_r
            pelvis_x, pelvis_y = x_px, y_px - 95 * scale
            chest_x, chest_y = x_px, (neck_y + pelvis_y) / 2
            # Hand to chin
            right_hand = (head_x + 12 * scale * f, head_y + head_r * 0.9)
            left_hand = (chest_x - 10 * scale * f, chest_y + 15 * scale)
            left_foot = (x_px - 15 * scale, y_px)
            right_foot = (x_px + 20 * scale, y_px)
        elif fig.pose == "pointing":
            head_x = x_px
            head_y = y_px - total_h
            neck_x, neck_y = head_x, head_y + head_r
            pelvis_x, pelvis_y = x_px, y_px - 95 * scale
            chest_x, chest_y = x_px, (neck_y + pelvis_y) / 2
            right_hand = (chest_x + 75 * scale * f, chest_y - 10 * scale)
            left_hand = (chest_x - 15 * scale * f, pelvis_y + 5 * scale)
            left_foot = (x_px - 18 * scale, y_px)
            right_foot = (x_px + 18 * scale, y_px)
        elif fig.pose == "arms_wide":
            head_x, head_y = x_px, y_px - total_h
            neck_x, neck_y = head_x, head_y + head_r
            pelvis_x, pelvis_y = x_px, y_px - 95 * scale
            chest_x, chest_y = x_px, (neck_y + pelvis_y) / 2
            left_hand = (chest_x - 65 * scale, chest_y - 30 * scale)
            right_hand = (chest_x + 65 * scale, chest_y - 30 * scale)
            left_foot = (x_px - 25 * scale, y_px)
            right_foot = (x_px + 25 * scale, y_px)
        elif fig.pose == "offer_left":
            head_x, head_y = x_px, y_px - total_h
            neck_x, neck_y = head_x, head_y + head_r
            pelvis_x, pelvis_y = x_px, y_px - 95 * scale
            chest_x, chest_y = x_px, (neck_y + pelvis_y) / 2
            left_hand = (chest_x - 55 * scale, chest_y + 10 * scale)
            right_hand = (chest_x + 20 * scale, pelvis_y)
            left_foot = (x_px - 15 * scale, y_px)
            right_foot = (x_px + 20 * scale, y_px)
        elif fig.pose == "cross":
            head_x, head_y = x_px, y_px - total_h
            neck_x, neck_y = head_x, head_y + head_r
            pelvis_x, pelvis_y = x_px, y_px - 95 * scale
            chest_x, chest_y = x_px, (neck_y + pelvis_y) / 2
            left_hand = (chest_x + 18 * scale, chest_y + 5 * scale)
            right_hand = (chest_x - 18 * scale, chest_y + 5 * scale)
            left_foot = (x_px - 15 * scale, y_px)
            right_foot = (x_px + 15 * scale, y_px)
        elif fig.pose == "walking":
            head_x = x_px + 10 * scale * f
            head_y = y_px - total_h
            neck_x, neck_y = head_x, head_y + head_r
            pelvis_x, pelvis_y = x_px, y_px - 95 * scale
            chest_x, chest_y = x_px + 5 * scale * f, (neck_y + pelvis_y) / 2
            left_hand = (chest_x - 30 * scale * f, chest_y + 10 * scale)
            right_hand = (chest_x + 30 * scale * f, chest_y - 15 * scale)
            left_foot = (x_px - 35 * scale * f, y_px)
            right_foot = (x_px + 35 * scale * f, y_px - 10 * scale)
        else:  # "confident" default
            head_x = x_px
            head_y = y_px - total_h
            neck_x, neck_y = head_x, head_y + head_r
            pelvis_x, pelvis_y = x_px, y_px - 95 * scale
            chest_x, chest_y = x_px, (neck_y + pelvis_y) / 2
            # Hands on hips
            left_hand = (x_px - 32 * scale, pelvis_y - 5 * scale)
            right_hand = (x_px + 32 * scale, pelvis_y - 5 * scale)
            left_foot = (x_px - 22 * scale, y_px)
            right_foot = (x_px + 22 * scale, y_px)

        # Draw Glow Layer
        glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw_glow = ImageDraw.Draw(glow_layer)
        glow_rgba = (c[0], c[1], c[2], 100)

        # Spine & limbs glow
        draw_glow.line([neck_x, neck_y, pelvis_x, pelvis_y], fill=glow_rgba, width=glow_w)
        draw_glow.line([chest_x, chest_y, left_hand[0], left_hand[1]], fill=glow_rgba, width=glow_w)
        draw_glow.line([chest_x, chest_y, right_hand[0], right_hand[1]], fill=glow_rgba, width=glow_w)
        draw_glow.line([pelvis_x, pelvis_y, left_foot[0], left_foot[1]], fill=glow_rgba, width=glow_w)
        draw_glow.line([pelvis_x, pelvis_y, right_foot[0], right_foot[1]], fill=glow_rgba, width=glow_w)
        draw_glow.ellipse([head_x - head_r, head_y - head_r, head_x + head_r, head_y + head_r], outline=glow_rgba, width=glow_w)
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=int(6 * scale)))
        img.paste(glow_layer, (0, 0), glow_layer)

        # Core crisp figure
        fig_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw_fig = ImageDraw.Draw(fig_layer)
        
        # Legs
        draw_fig.line([pelvis_x, pelvis_y, left_foot[0], left_foot[1]], fill=c, width=stroke_w)
        draw_fig.line([pelvis_x, pelvis_y, right_foot[0], right_foot[1]], fill=c, width=stroke_w)
        # Spine
        draw_fig.line([neck_x, neck_y, pelvis_x, pelvis_y], fill=c, width=stroke_w)
        # Arms
        if fig.pose == "confident":
            # Elbows bent outward
            left_elbow = (x_px - 40 * scale, chest_y + 10 * scale)
            right_elbow = (x_px + 40 * scale, chest_y + 10 * scale)
            draw_fig.line([chest_x, chest_y, left_elbow[0], left_elbow[1]], fill=c, width=stroke_w)
            draw_fig.line([left_elbow[0], left_elbow[1], left_hand[0], left_hand[1]], fill=c, width=stroke_w)
            draw_fig.line([chest_x, chest_y, right_elbow[0], right_elbow[1]], fill=c, width=stroke_w)
            draw_fig.line([right_elbow[0], right_elbow[1], right_hand[0], right_hand[1]], fill=c, width=stroke_w)
        else:
            draw_fig.line([chest_x, chest_y, left_hand[0], left_hand[1]], fill=c, width=stroke_w)
            draw_fig.line([chest_x, chest_y, right_hand[0], right_hand[1]], fill=c, width=stroke_w)

        # Head (filled black with thick glowing stroke)
        draw_fig.ellipse([head_x - head_r, head_y - head_r, head_x + head_r, head_y + head_r], fill=(0, 0, 0, 255), outline=c, width=stroke_w)
        
        # Expressive face
        self.draw_face(draw_fig, head_x, head_y, head_r, fig.expression, f, c)

        # Head Accessory (e.g. Floating Crown)
        if fig.head_accessory == "crown":
            self.draw_crown(draw_fig, head_x, head_y - head_r - 18 * scale, scale)

        # Body Accessory
        if fig.body_accessory == "xmark":
            # X mark on torso/side, NEVER covering face
            x_cx = chest_x + 40 * scale * f
            x_cy = chest_y + 10 * scale
            self.draw_xmark(draw_fig, x_cx, x_cy, scale)
        elif fig.body_accessory == "scissors":
            self.draw_scissors(draw_fig, right_hand[0] + 15 * scale, right_hand[1], scale)
        elif fig.body_accessory == "mirror":
            self.draw_mirror(draw_fig, right_hand[0] + 20 * scale * f, chest_y, scale)
        elif fig.body_accessory == "phone":
            self.draw_phone(draw_fig, right_hand[0], right_hand[1], scale)
        elif fig.body_accessory == "lightning_eye":
            self.draw_lightning_eye(draw_fig, head_x, head_y, f, scale)

        img.paste(fig_layer, (0, 0), fig_layer)

    def draw_crown(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Floating 3-pointed golden crown with jewels."""
        w = 34 * scale
        h = 22 * scale
        pts = [
            (cx - w, cy + h * 0.5),
            (cx - w * 0.9, cy - h * 0.5),
            (cx - w * 0.4, cy),
            (cx, cy - h * 0.8),
            (cx + w * 0.4, cy),
            (cx + w * 0.9, cy - h * 0.5),
            (cx + w, cy + h * 0.5)
        ]
        draw.polygon(pts, fill=COLOR_GOLD)
        # Gold glow jewels on peaks
        r = max(2, int(3 * scale))
        for px, py in [(cx - w * 0.9, cy - h * 0.5), (cx, cy - h * 0.8), (cx + w * 0.9, cy - h * 0.5)]:
            draw.ellipse([px - r, py - r, px + r, py + r], fill=COLOR_WHITE)

    def draw_xmark(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Red X mark with glow."""
        s = 24 * scale
        w = int(6 * scale)
        draw.line([cx - s, cy - s, cx + s, cy + s], fill=COLOR_RED, width=w)
        draw.line([cx - s, cy + s, cx + s, cy - s], fill=COLOR_RED, width=w)

    def draw_scissors(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Open red scissors."""
        w = int(4 * scale)
        s = 18 * scale
        draw.line([cx - s, cy - s, cx + s, cy + s], fill=COLOR_RED, width=w)
        draw.line([cx - s, cy + s, cx + s, cy - s], fill=COLOR_RED, width=w)
        draw.ellipse([cx - s - 6 * scale, cy - s - 6 * scale, cx - s + 6 * scale, cy - s + 6 * scale], outline=COLOR_RED, width=w)
        draw.ellipse([cx - s - 6 * scale, cy + s - 6 * scale, cx - s + 6 * scale, cy + s + 6 * scale], outline=COLOR_RED, width=w)

    def draw_mirror(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Mirror showing reflection waves."""
        rw = 18 * scale
        rh = 38 * scale
        draw.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], outline=COLOR_GOLD, width=int(3 * scale))
        # Handle
        draw.line([cx, cy + rh, cx, cy + rh + 20 * scale], fill=COLOR_GOLD, width=int(4 * scale))
        # Reflection light gleams
        draw.line([cx - rw * 0.5, cy - rh * 0.4, cx + rw * 0.3, cy + rh * 0.2], fill=COLOR_WHITE, width=int(2 * scale))

    def draw_phone(self, draw: ImageDraw.ImageDraw, cx: float, cy: float, scale: float):
        """Smartphone with glowing screen."""
        pw = 14 * scale
        ph = 26 * scale
        draw.rectangle([cx - pw, cy - ph, cx + pw, cy + ph], fill=(20, 20, 20), outline=COLOR_WHITE, width=int(2 * scale))
        draw.rectangle([cx - pw + 2 * scale, cy - ph + 4 * scale, cx + pw - 2 * scale, cy + ph - 4 * scale], fill=(0, 200, 255))

    def draw_lightning_eye(self, draw: ImageDraw.ImageDraw, hx: float, hy: float, facing: int, scale: float):
        """Laser / lightning shooting from eyes."""
        pts = [
            (hx + 10 * scale * facing, hy - 4 * scale),
            (hx + 50 * scale * facing, hy - 12 * scale),
            (hx + 40 * scale * facing, hy),
            (hx + 100 * scale * facing, hy - 8 * scale)
        ]
        draw.line(pts, fill=COLOR_RED, width=int(3 * scale))

    def draw_accessory(self, img: Image.Image, acc: Accessory):
        """Draw standalone accessory (e.g. arrow, dotted line, puppet strings)."""
        sf = self.sf
        draw = ImageDraw.Draw(img)
        x1, y1 = acc.x1 * sf, acc.y1 * sf
        x2, y2 = acc.x2 * sf, acc.y2 * sf

        if acc.kind == "arrow":
            # Arrow from (x1, y1) pointing to (x2, y2)
            draw.line([x1, y1, x2, y2], fill=acc.color, width=int(4 * sf))
            angle = math.atan2(y2 - y1, x2 - x1)
            arrow_len = 22 * sf
            p1 = (x2 - arrow_len * math.cos(angle - math.pi / 6), y2 - arrow_len * math.sin(angle - math.pi / 6))
            p2 = (x2 - arrow_len * math.cos(angle + math.pi / 6), y2 - arrow_len * math.sin(angle + math.pi / 6))
            draw.polygon([ (x2, y2), p1, p2 ], fill=acc.color)
        elif acc.kind == "dotted":
            # Dotted line
            dist = math.hypot(x2 - x1, y2 - y1)
            dots = max(3, int(dist / (14 * sf)))
            for i in range(dots + 1):
                t = i / dots
                px = x1 + (x2 - x1) * t
                py = y1 + (y2 - y1) * t
                r = int(3 * sf)
                draw.ellipse([px - r, py - r, px + r, py + r], fill=acc.color)
        elif acc.kind == "marionette":
            # Wooden cross at top with strings hanging down to figures
            cx = (x1 + x2) / 2 if x2 else x1
            cy = y1
            cw = 120 * sf
            ch = 20 * sf
            draw.rectangle([cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2], fill=COLOR_RED)
            draw.rectangle([cx - ch / 2, cy - cw / 3, cx + ch / 2, cy + cw / 3], fill=COLOR_RED)
            # 4 Strings hanging down
            for offset in [-cw * 0.45, -cw * 0.15, cw * 0.15, cw * 0.45]:
                draw.line([cx + offset, cy + ch / 2, cx + offset * 1.5, y2], fill=(200, 200, 200, 160), width=int(1.5 * sf))

    def render_scene(
        self,
        width: int,
        height: int,
        figures: List[Fig],
        accessories: Optional[List[Accessory]] = None,
        caption_text: str = "",
        spotlight_pos: Optional[Tuple[float, float, float]] = None
    ) -> Image.Image:
        """Render complete 1920x1080 or 1080x1920 scene with figures, accessories, and caption."""
        canvas = self.create_canvas(width, height, spotlight=spotlight_pos)
        
        # Draw accessories behind figures if any
        if accessories:
            for acc in accessories:
                self.draw_accessory(canvas, acc)

        # Draw figures
        for fig in figures:
            self.draw_figure(canvas, fig)

        # Draw caption if provided (in reserved bottom 25% area)
        if caption_text:
            self.draw_caption(canvas, caption_text, width, height)

        # Downsample supersampling with Lanczos
        return canvas.resize((width, height), Image.Resampling.LANCZOS)

    def draw_caption(self, canvas: Image.Image, text: str, orig_w: int, orig_h: int):
        """Render yellow highlighted caption in lower safe area."""
        sf = self.sf
        w, h = orig_w * sf, orig_h * sf
        draw = ImageDraw.Draw(canvas)
        
        font_size = int(28 * sf) if orig_w >= orig_h else int(34 * sf)
        font = get_font(font_size)
        
        # Word wrap if text is long
        words = text.split()
        lines = []
        cur = []
        for w_word in words:
            test_line = " ".join(cur + [w_word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > w * 0.8:
                lines.append(" ".join(cur))
                cur = [w_word]
            else:
                cur.append(w_word)
        if cur:
            lines.append(" ".join(cur))

        # Position in bottom 20%
        box_y = int(h * 0.82)
        line_h = font_size + int(10 * sf)
        start_y = box_y - (len(lines) - 1) * line_h // 2

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = (w - tw) // 2
            ty = start_y + i * line_h

            # Highlight pill box
            pad_x = int(14 * sf)
            pad_y = int(6 * sf)
            draw.rectangle([tx - pad_x, ty - pad_y, tx + tw + pad_x, ty + th + pad_y], fill=(0, 0, 0, 220), outline=COLOR_GOLD, width=int(2 * sf))
            draw.text((tx, ty), line, font=font, fill=COLOR_WHITE)

    def render_thumbnail(
        self,
        title: str,
        thumb_text: str,
        visual_type: str,
        out_path: str
    ) -> str:
        """Render YouTube 1280x720 thumbnail with high-contrast figures, impact accessory and 3-4 word text."""
        w, h = 1280, 720
        # Validate thumbnail text length
        words = thumb_text.strip().split()
        if len(words) > 4:
            raise ValueError(f"Thumbnail text has {len(words)} words, maximum allowed is 4.")

        # Determine figures and accessories based on visual_type description
        figures = []
        accessories = []

        if "vs" in visual_type or "curvado" in visual_type:
            # Day 1 style: Slouched with X vs confident with Crown
            fig_errado = Fig(
                x=320, y=520, scale=1.35, pose="slouched", expression="fake_smile",
                color=COLOR_GRAY, body_accessory="xmark", facing=1
            )
            fig_certo = Fig(
                x=960, y=520, scale=1.35, pose="confident", expression="calm",
                color=COLOR_WHITE, head_accessory="crown", facing=-1
            )
            figures = [fig_errado, fig_certo]
        elif "pés" in visual_type or "pes" in visual_type:
            # Day 2 style: liar smiling with arrow pointing to feet
            fig = Fig(
                x=640, y=520, scale=1.4, pose="confident", expression="smirk",
                color=COLOR_WHITE, facing=1
            )
            figures = [fig]
            accessories.append(Accessory(kind="arrow", x1=400, y1=450, x2=580, y2=520, color=COLOR_GOLD))
        elif "espelho" in visual_type:
            # Day 3 style: shouting figure vs calm with mirror
            fig1 = Fig(
                x=330, y=520, scale=1.35, pose="shouting", expression="angry",
                color=COLOR_RED, facing=1
            )
            fig2 = Fig(
                x=950, y=520, scale=1.35, pose="confident", expression="calm",
                color=COLOR_WHITE, body_accessory="mirror", facing=-1
            )
            figures = [fig1, fig2]
        elif "tesoura" in visual_type or "amigo" in visual_type:
            # Day 4 style: handshake with scissors behind back
            fig1 = Fig(
                x=420, y=520, scale=1.35, pose="offer_left", expression="fake_smile",
                color=COLOR_GRAY, body_accessory="scissors", facing=1
            )
            fig2 = Fig(
                x=860, y=520, scale=1.35, pose="offer_left", expression="calm",
                color=COLOR_WHITE, facing=-1
            )
            figures = [fig1, fig2]
        elif "vácuo" in visual_type or "vacuo" in visual_type or "correndo" in visual_type:
            # Day 5 style: figures chasing 1 confident figure
            f1 = Fig(x=200, y=530, scale=1.0, pose="walking", expression="worried", color=COLOR_GRAY, facing=1)
            f2 = Fig(x=340, y=530, scale=1.0, pose="walking", expression="worried", color=COLOR_GRAY, facing=1)
            f3 = Fig(x=480, y=530, scale=1.0, pose="walking", expression="worried", color=COLOR_GRAY, facing=1)
            leader = Fig(x=950, y=520, scale=1.35, pose="confident", expression="calm", color=COLOR_WHITE, head_accessory="crown", facing=1)
            figures = [f1, f2, f3, leader]
        elif "espelho" in visual_type or "fio" in visual_type:
            # Day 6 style: 2 identical figures synchronized with gold dotted line
            fig1 = Fig(x=360, y=520, scale=1.35, pose="confident", expression="calm", color=COLOR_WHITE, facing=1)
            fig2 = Fig(x=920, y=520, scale=1.35, pose="confident", expression="calm", color=COLOR_WHITE, facing=-1)
            figures = [fig1, fig2]
            accessories.append(Accessory(kind="dotted", x1=360, y1=380, x2=920, y2=380, color=COLOR_GOLD))
        elif "marionete" in visual_type or "fios" in visual_type:
            # Day 7 style: Puppet cross with stickman cutting threads
            hero = Fig(x=640, y=520, scale=1.4, pose="confident", expression="calm", color=COLOR_WHITE, body_accessory="scissors", facing=1)
            figures = [hero]
            accessories.append(Accessory(kind="marionette", x1=400, y1=80, x2=880, y2=450, color=COLOR_RED))
        else:
            # Default strong contrast
            fig1 = Fig(x=360, y=520, scale=1.35, pose="slouched", expression="worried", color=COLOR_GRAY, facing=1)
            fig2 = Fig(x=920, y=520, scale=1.35, pose="confident", expression="calm", color=COLOR_WHITE, head_accessory="crown", facing=-1)
            figures = [fig1, fig2]

        # Spotlight behind center
        canvas = self.create_canvas(w, h, spotlight=(0.5, 0.45, 0.45))

        for acc in accessories:
            self.draw_accessory(canvas, acc)
        for fig in figures:
            self.draw_figure(canvas, fig)

        # Draw Thumb Text at upper/middle banner area (large impact font in #FFD700 or #FF2A2A with black outline)
        sf = self.sf
        draw = ImageDraw.Draw(canvas)
        font = get_font(int(78 * sf))

        # Calculate bounding box
        bbox = draw.textbbox((0, 0), thumb_text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        tx = (w * sf - tw) // 2
        ty = int(80 * sf)

        # Render bold outline
        outline_w = int(8 * sf)
        for ox in range(-outline_w, outline_w + 1):
            for oy in range(-outline_w, outline_w + 1):
                if ox * ox + oy * oy <= outline_w * outline_w:
                    draw.text((tx + ox, ty + oy), thumb_text, font=font, fill=(0, 0, 0))

        # Main text fill in Gold #FFD700
        text_color = COLOR_RED if "PARE" in thumb_text or "CORTE" in thumb_text else COLOR_GOLD
        draw.text((tx, ty), thumb_text, font=font, fill=text_color)

        final_img = canvas.resize((w, h), Image.Resampling.LANCZOS)
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        final_img.save(out_path, format="PNG")
        return out_path


def put_transparent(stickman_img: Image.Image) -> Image.Image:
    """Helper to convert black background to transparency for backdrop overlay."""
    img = stickman_img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        # If very close to pure black, make transparent
        if item[0] < 8 and item[1] < 8 and item[2] < 8:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img


def stickman_over_backdrop(stickman_img: Image.Image, backdrop_img: Image.Image) -> Image.Image:
    """Composite stickman image with transparent background over a graded video backdrop."""
    stickman_trans = put_transparent(stickman_img)
    bg = backdrop_img.convert("RGBA").resize(stickman_img.size)
    return Image.alpha_composite(bg, stickman_trans)
