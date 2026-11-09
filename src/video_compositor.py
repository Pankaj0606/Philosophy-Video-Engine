"""
Master Video Compositor:
Coordinates audio generation, bespoke visual fetching, typography cards,
and multi-axis FFmpeg camera motion into the final documentary video.
"""

import os
import asyncio
import subprocess
import edge_tts
from src.typography import create_chapter_card, create_quote_card
from src.visual_engine import fetch_clean_artwork, get_cinematic_filtergraph

VOICE = "en-IN-PrabhatNeural"
RATE = "-4%"


async def synthesize_chunk(text: str, output_path: str):
    """Synthesizes speech narration for a segment."""
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch="-1Hz")
    await communicate.save(output_path)


def render_scene(image_path: str, audio_path: str, output_clip: str, motion_mode: str):
    """Combines an image and an audio clip into an animated MP4 scene."""
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


async def produce_full_documentary(doc_blueprint: dict, session_id: str) -> str:
    """Builds all chapters, scenes, cards, and concatenates the master video."""
    work_dir = f"output/{session_id}"
    os.makedirs(f"{work_dir}/audio", exist_ok=True)
    os.makedirs(f"{work_dir}/images", exist_ok=True)
    os.makedirs(f"{work_dir}/clips", exist_ok=True)

    clip_paths = []
    clip_counter = 1

    chapters = doc_blueprint.get("chapters", [])
    total_chapters = len(chapters)

    for ch_idx, ch in enumerate(chapters, start=1):
        roman = ch.get("roman_numeral", f"Chapter {ch_idx}")
        title = ch.get("chapter_title", "")
        print(f"\n📽️ Processing [{roman}: {title}] ({ch_idx}/{total_chapters})...")

        # 1. Chapter Title Card
        print("  ├── 🎨 Generating Chapter Title Card...")
        card_img = f"{work_dir}/images/ch_{ch_idx}_card.jpg"
        create_chapter_card(roman, title, card_img)

        card_audio = f"{work_dir}/audio/ch_{ch_idx}_title_audio.mp3"
        await synthesize_chunk(f"{roman}. {title}.", card_audio)

        card_clip = f"{work_dir}/clips/clip_{clip_counter:03d}.mp4"
        render_scene(card_img, card_audio, card_clip, motion_mode="wide_reveal")
        clip_paths.append(card_clip)
        clip_counter += 1

        # 2. Sanskrit/Philosophy Quote Card (if present)
        quote_data = ch.get("quote", {})
        if quote_data.get("has_quote") and quote_data.get("original_verse"):
            print("  ├── 📜 Creating Ancient Verse Quote Plate...")
            q_img = f"{work_dir}/images/ch_{ch_idx}_quote.jpg"
            create_quote_card(
                sanskrit_verse=quote_data["original_verse"],
                english_trans=quote_data.get("english_translation", ""),
                attribution=quote_data.get("attribution", "Ancient Sutra"),
                output_path=q_img
            )

            q_audio = f"{work_dir}/audio/ch_{ch_idx}_quote_audio.mp3"
            quote_narration = f"As recorded in the ancient texts: {quote_data.get('english_translation', '')}"
            await synthesize_chunk(quote_narration, q_audio)

            q_clip = f"{work_dir}/clips/clip_{clip_counter:03d}.mp4"
            render_scene(q_img, q_audio, q_clip, motion_mode="cinematic_push_in")
            clip_paths.append(q_clip)
            clip_counter += 1

        # 3. Spoken Narrative & Visual Artwork Scenes
        spoken_script = ch.get("spoken_script", "")
        scenes = ch.get("visual_scenes", [])
        if not scenes:
            scenes = [{"camera_motion": "diagonal_dolly", "art_prompt": f"classical detailed oil painting of {title}"}]

        # Divide narration text among the scenes in this chapter
        words = spoken_script.split()
        chunk_size = max(1, len(words) // len(scenes))

        for sc_idx, scene in enumerate(scenes, start=1):
            sc_words = words[(sc_idx - 1) * chunk_size : sc_idx * chunk_size] if sc_idx < len(scenes) else words[(sc_idx - 1) * chunk_size :]
            scene_text = " ".join(sc_words)
            if not scene_text.strip():
                continue

            print(f"  ├── 🎨 Generating Artwork Scene ({sc_idx}/{len(scenes)})...")
            art_img = f"{work_dir}/images/ch_{ch_idx}_art_{sc_idx}.jpg"
            fetch_clean_artwork(prompt=scene.get("art_prompt", title), output_path=art_img, seed=ch_idx * 100 + sc_idx)

            art_audio = f"{work_dir}/audio/ch_{ch_idx}_narr_{sc_idx}.mp3"
            await synthesize_chunk(scene_text, art_audio)

            art_clip = f"{work_dir}/clips/clip_{clip_counter:03d}.mp4"
            motion = scene.get("camera_motion", "diagonal_dolly")
            render_scene(art_img, art_audio, art_clip, motion_mode=motion)
            clip_paths.append(art_clip)
            clip_counter += 1

    # 4. Master Concatenation
    print("\n🎞️ Stitching all chapters and scenes into master documentary...")
    abs_work_dir = os.path.abspath(work_dir)
    concat_manifest = os.path.join(abs_work_dir, "manifest.txt")

    with open(concat_manifest, "w") as f:
        for c in clip_paths:
            abs_clip = os.path.abspath(c)
            f.write(f"file '{abs_clip}'\n")

    abs_final_output = os.path.abspath(f"output/{session_id}_documentary.mp4")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_manifest,
        "-c", "copy",
        abs_final_output
    ]
    subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return abs_final_output