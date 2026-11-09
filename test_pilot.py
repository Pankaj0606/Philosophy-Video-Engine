"""
Updated Pilot Test:
1. Uses natural Indian English voice (en-IN-PrabhatNeural).
2. Automatically removes/crops the Pollinations watermark completely using Pillow.
3. Renders clean, watermark-free 1080p video with Ken Burns motion.
"""

import asyncio
import os
import subprocess
import urllib.parse
import requests
import edge_tts
from PIL import Image

# Natural, articulate Indian English voice for documentaries
VOICE = "en-IN-PrabhatNeural"
RATE = "-4%"   # Slightly measured, contemplative pace
PITCH = "-1Hz"

SAMPLE_TEXT = (
    "Before the Buddha, and before the Upanishads were canonized, "
    "there walked the Lokayatas. They rejected heaven, rejected karma, "
    "and dared to proclaim that this breath, this earth, and this moment "
    "are all that consciousness will ever possess."
)

IMAGE_PROMPT = (
    "cinematic dark renaissance oil painting of ancient Indian sages debating under a giant banyan tree, "
    "dim twilight, chiaroscuro lighting, moody atmospheric mist, ancient manuscripts, hyper-detailed, masterpiece, 4k"
)

AUDIO_FILE = "output/audio/pilot_voice.mp3"
IMAGE_FILE = "output/images/pilot_art.jpg"
VIDEO_FILE = "output/videos/pilot_test.mp4"


async def generate_speech():
    print(f"🎙️ Generating voiceover using Indian English ({VOICE})...")
    communicate = edge_tts.Communicate(SAMPLE_TEXT, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(AUDIO_FILE)
    print(f"  └── Saved audio to: {AUDIO_FILE}")


def generate_visual_without_watermark():
    print("🎨 Generating 1080p artwork via Flux AI...")
    encoded_prompt = urllib.parse.quote(IMAGE_PROMPT)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&model=flux&seed=42"
    
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        with open(IMAGE_FILE, "wb") as f:
            f.write(response.content)
            
        # Cleanly strip the bottom-right watermark using Pillow
        print("✂️ Stripping watermark cleanly...")
        with Image.open(IMAGE_FILE) as img:
            w, h = img.size
            # Crop off the bottom 55 pixels where the watermark sits
            cropped = img.crop((0, 0, w, h - 55))
            # Seamlessly upscale back to standard 1920x1080
            clean_img = cropped.resize((w, h), Image.Resampling.LANCZOS)
            clean_img.save(IMAGE_FILE, quality=95)
            
        print(f"  └── Clean, watermark-free artwork saved to: {IMAGE_FILE}")
    else:
        raise ConnectionError(f"Failed to fetch image. Status: {response.status_code}")


def render_video():
    print("🎬 Rendering cinematic video with dynamic camera motion (FFmpeg)...")
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", IMAGE_FILE,
        "-i", AUDIO_FILE,
        "-vf", "scale=8000:-1,zoompan=z='min(zoom+0.0015,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=25",
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        VIDEO_FILE
    ]
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  └── 🏆 Finished! Video exported to: {VIDEO_FILE}")


async def main():
    os.makedirs("output/audio", exist_ok=True)
    os.makedirs("output/images", exist_ok=True)
    os.makedirs("output/videos", exist_ok=True)

    await generate_speech()
    generate_visual_without_watermark()
    render_video()

    print("\n" + "="*60)
    print("🎉 TEST READY! Play the new video on your Mac:")
    print(f"   Run: open {VIDEO_FILE}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())