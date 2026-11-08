"""src/character_prompt.py - Definição e gerador do prompt oficial do Sr. Palito (Mr. Stick)."""

OFFICIAL_SR_PALITO_PROMPT_TEMPLATE = """Create the exact same recurring mascot character, known as "Mr. Stick" (Sr. Palito), maintaining consistent character design in every generation.

A hyper-charismatic minimalist stick figure mascot with a perfectly round solid white head, sleek black facial area, intensely expressive white glowing eyes, sharp mischievous eyebrows and a confident, calculating smirk.

His body is a minimalist stick figure with thick, crisp, glowing white neon outlines and a premium futuristic appearance.

He always wears a razor-sharp crimson red bow tie (#FF2A2A).

Floating directly above his head is a magnificent holographic golden brain (#FFD700), with intricate glowing neural connections, crowned by a small, elegant, sharp-pointed golden royal crown.

His personality is intelligent, strategic, charismatic, dominant, mysterious and slightly mischievous.

Visual identity:
- Pure black background (#000000).
- Electric white neon outlines.
- Crimson red and electric gold rim lighting.
- High contrast, cinematic lighting.
- Premium cyberpunk minimalist aesthetic.
- Clean, polished, recognizable silhouette.
- Consistent proportions and facial features.

Character consistency is extremely important: Never change his head shape, eyes, facial expression style, bow tie, golden brain or crown. He must always be recognizable as the exact same character.

Pose and body language: {action_or_pose}.

Full-body character, centered composition, professional digital illustration, ultra-detailed, 4K quality.

No text, no letters, no watermark, no additional characters."""


def get_sr_palito_prompt(action_or_pose: str = "standing confident with hands on hips, looking directly at the viewer") -> str:
    """Retorna o prompt oficial e padronizado do Sr. Palito para geração de imagem ou instrução de IA."""
    return OFFICIAL_SR_PALITO_PROMPT_TEMPLATE.format(action_or_pose=action_or_pose)
