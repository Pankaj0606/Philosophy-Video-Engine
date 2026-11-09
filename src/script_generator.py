"""
Multi-Act Script & Scene Generator via Groq LLM:
Generates structured documentary scripts (20-40 mins) with:
- Chapter headings (for title cards)
- Sanskrit / Greek primary quotes
- Vivid, luminous scene-by-scene visual prompts
"""

import os
import json
import re
import sys
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def call_llm(prompt: str) -> dict:
    """Calls Groq with JSON format enforcement and fallback models."""
    client = Groq(api_key=GROQ_API_KEY)
    candidate_models = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile"]

    for model in candidate_models:
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a master historical documentary writer. Output only a valid raw JSON object. Do not wrap in markdown fences."},
                    {"role": "user", "content": prompt}
                ],
                model=model,
                response_format={"type": "json_object"},
                max_tokens=6000,
                temperature=0.3
            )
            raw = response.choices[0].message.content
            if "<think>" in raw and "</think>" in raw:
                raw = raw[raw.find("</think>") + 8:].strip()
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1:
                return json.loads(raw[start:end+1])
        except Exception:
            continue
    raise RuntimeError("All LLM models failed to generate valid script.")


def generate_documentary_structure(topic: str, tradition: str, target_mins: int = 25) -> dict:
    """
    Generates a full documentary blueprint containing 5 distinct narrative chapters,
    complete with spoken text, visual image prompts, and original philosophical verses.
    """
    print(f"🧠 Designing {target_mins}-minute documentary blueprint for: {topic}...")
    
    prompt = f"""
Create a comprehensive historical documentary script about:
Topic: {topic}
Tradition: {tradition}
Target Video Duration: ~{target_mins} minutes

Design exactly 5 progressive narrative chapters:
1. The Existential Hook & Historical Rebellion
2. The Epistemology (How they determine truth)
3. The Core Metaphysics & Worldview
4. The Great Philosophical Debates & Clashes with Rivals
5. The Modern Crisis & What This Means For Us Today

Return a single JSON object strictly matching this schema:
{{
  "main_title": "Epic Main Title (e.g. CHARVAKA)",
  "main_subtitle": "Sub-heading (e.g. The Lost Materialists of Ancient India)",
  "chapters": [
    {{
      "roman_numeral": "Chapter I",
      "chapter_title": "Evocative Title for this chapter",
      "spoken_script": "Deep, meditative narration text (minimum 250 words per chapter) written in clear, articulate documentary prose.",
      "quote": {{
        "has_quote": true,
        "original_verse": "Sanskrit verse in Devanagari script (or Greek/Latin if Western philosophy)",
        "english_translation": "Clear English translation of the verse",
        "attribution": "Ancient Text / Author source"
      }},
      "visual_scenes": [
        {{
          "camera_motion": "diagonal_dolly",
          "art_prompt": "Vivid, luminous description of scene, warm sunlight, ancient temple/agora, scholars debating, detailed oil painting"
        }},
        {{
          "camera_motion": "cinematic_push_in",
          "art_prompt": "Close-up of ancient palm leaf manuscripts, oil lamps, warm golden lighting, detailed historical artifacts"
        }}
      ]
    }}
  ]
}}
"""
    return call_llm(prompt)