"""
Cinematic Visual & Motion FX Engine:
- Fetches bespoke 1080p Flux artwork (watermark-free)
- Alternates 4 distinct camera maneuvers
- Applies luminous documentary color grading (no dark shadow crushing)
"""

import os
import urllib.parse
import requests
import random
from PIL import Image

CAMERA_MODES = [
    "diagonal_dolly",    # Glides smoothly diagonally while slowly zooming
    "cinematic_push_in", # Deep focus zoom towards key subject
    "wide_reveal",       # Slow pull-back revealing the whole ancient scene
    "lateral_glide"      # Cinematic horizontal pan from left to right
]


def fetch_clean_artwork(prompt: str, output_path: str, seed: int = None) -> str:
    """Downloads bespoke 1080p artwork via Flux and removes all watermarks."""
    if seed is None:
        seed = random.randint(100, 999999)

    # Inject positive lighting cues to guarantee clear, vibrant imagery
    enhanced_prompt = (
        f"{prompt}, warm golden sunlight, sharp focus, vibrant colors, "
        f"detailed classical architectural background, 8k resolution, masterpiece oil painting"
    )
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&model=flux&seed={seed}"

    response = requests.get(url, timeout=40)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to generate artwork. Status: {response.status_code}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)

    # Cleanly strip watermark from bottom edge
    with Image.open(output_path) as img:
        w, h = img.size
        cropped = img.crop((0, 0, w, h - 55))
        clean_img = cropped.resize((w, h), Image.Resampling.LANCZOS)
        clean_img.save(output_path, quality=95)

    return output_path


def get_cinematic_filtergraph(mode: str) -> str:
    """
    Returns an advanced FFmpeg filtergraph:
    Multi-axis camera motion + warm cinematic documentary grade (clean, visible shadows).
    """
    if mode == "diagonal_dolly":
        motion = "scale=8000:-1,zoompan=z='min(zoom+0.0012,1.20)':x='(iw-iw/zoom)*(on/(25*10))':y='(ih-ih/zoom)*(on/(25*10))':d=1:s=1920x1080:fps=25"
    elif mode == "wide_reveal":
        motion = "scale=8000:-1,zoompan=z='max(1.22-0.0012*on,1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=25"
    elif mode == "lateral_glide":
        motion = "scale=8000:-1,zoompan=z='1.12':x='(iw-iw/zoom)*(on/(25*12))':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=25"
    else:  # cinematic_push_in
        motion = "scale=8000:-1,zoompan=z='min(zoom+0.0015,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=25"

    # Luminous, rich grade: slight contrast boost, warm saturation, very soft vignette
    effects = "vignette=PI/6,eq=contrast=1.04:brightness=0.02:saturation=1.15"

    return f"{motion},{effects}"