"""
Complete Cinematic Test:
Tests Chapter Title Intro + Living Motion Art Scene + Sanskrit Verse Card.
"""

import asyncio
import os
import subprocess
import edge_tts
from src.typography import create_chapter_card, create_quote_card
from src.visual_engine import fetch_clean_artwork, get_cinematic_filtergraph

VOICE = "en-IN-PrabhatNeural"
RATE = "-4%"

SCRIPT_SCENE_1 = "Chapter One. The Rebel Materialists of Ancient India."
SCRIPT_SCENE_2 = (
    "In the vibrant debates of ancient Magadha, while the Vedic priests spoke of sacrificial rituals "
    "and heavenly rewards, the Charvakas posed a radical counter-challenge: show us proof, or remain silent."
)
SCRIPT_SCENE_3 = "As the Brihaspati Sutra boldly proclaims: while life remains, let a man live happily. Drink melted butter, even if you must borrow money to do so."

OUTPUT_DIR = "output/cinematic_demo"
os.makedirs(f"{OUTPUT_DIR}/audio", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/images", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/clips", exist_ok=True)


async def synthesize_audio(text: str, filename: str) -> str:
    path = f"{OUTPUT_DIR}/audio/{filename}.mp3"
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch="-1Hz")
    await communicate.save(path)
    return path


def render_scene_clip(image_path: str, audio_path: str, output_clip: str, motion_mode: str = "cinematic_push_in"):
    filtergraph = get_cinematic_filtergraph(motion_mode)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-vf", filtergraph,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_clip
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


async def main():
    print("🎬 Generating Cinematic Documentary Suite...")

    # 1. Generate Voiceovers
    print("🎙️ Synthesizing narration with en-IN-PrabhatNeural...")
    a1 = await synthesize_audio(SCRIPT_SCENE_1, "audio_1")
    a2 = await synthesize_audio(SCRIPT_SCENE_2, "audio_2")
    a3 = await synthesize_audio(SCRIPT_SCENE_3, "audio_3")

    # 2. Generate Visual Assets
    print("🎨 Creating Chapter Title Card...")
    img_chapter = f"{OUTPUT_DIR}/images/chapter_card.jpg"
    create_chapter_card("Chapter I", "The Rebel Materialists", img_chapter)

    print("🎨 Generating Bespoke Flux Artwork...")
    img_art = f"{OUTPUT_DIR}/images/flux_art.jpg"
    fetch_clean_artwork(
        prompt="cinematic dark oil painting of ancient Indian philosophical assembly in royal courtyard, twilight torches, chiaroscuro, 4k masterpiece",
        output_path=img_art,
        seed=108
    )

    print("🎨 Creating Sanskrit Quote Card...")
    img_quote = f"{OUTPUT_DIR}/images/sanskrit_quote.jpg"
    create_quote_card(
        sanskrit_verse="यावज्जीवेत् सुखं जीवेत् ऋणं कृत्वा घृतं पिबेत् ।",
        english_trans="While life remains, let one live happily; drink ghee even if by taking debt.",
        attribution="Brihaspati Sutra (Charvaka Darshana)",
        output_path=img_quote
    )

    # 3. Render 3 Distinct Clips with Different Motion Modes
    print("🎥 Rendering Scene 1 (Title Card with Wide Reveal)...")
    clip1 = f"{OUTPUT_DIR}/clips/clip_1.mp4"
    render_scene_clip(img_chapter, a1, clip1, motion_mode="wide_reveal")

    print("🎥 Rendering Scene 2 (Living Artwork with Diagonal Dolly Drift)...")
    clip2 = f"{OUTPUT_DIR}/clips/clip_2.mp4"
    render_scene_clip(img_art, a2, clip2, motion_mode="diagonal_dolly")

    print("🎥 Rendering Scene 3 (Sanskrit Quote Card with Subtle Push-In)...")
    clip3 = f"{OUTPUT_DIR}/clips/clip_3.mp4"
    render_scene_clip(img_quote, a3, clip3, motion_mode="cinematic_push_in")

    # 4. Concatenate clips into final preview video
    print("🎞️ Stitching complete documentary segment...")
    concat_list = f"{OUTPUT_DIR}/clips.txt"
    with open(concat_list, "w") as f:
        f.write(f"file 'clips/clip_1.mp4'\nfile 'clips/clip_2.mp4'\nfile 'clips/clip_3.mp4'\n")

    final_video = f"{OUTPUT_DIR}/cinematic_showcase.mp4"
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        final_video
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print("\n" + "="*70)
    print("🏆 SHOWCASE COMPLETE! Watch the result on your Mac:")
    print(f"   Run: open {final_video}")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())