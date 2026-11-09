"""
Master Execution Pipeline:
1. Connects to 'Philosophy_Videos' tab in 'DSA_Instagram_Automation' Google Sheet.
2. Fetches the first 'Pending' topic.
3. Generates the structured multi-chapter script & scene prompts.
4. Synthesizes Indian English narration, renders luminous artwork, and applies varied camera motions.
5. Renders the complete documentary MP4.
6. Marks the row as 'Completed' in Google Sheets.
"""

import asyncio
import os
import re
from src.sheets_manager import get_next_pending_topic, mark_topic_completed
from src.script_generator import generate_documentary_structure
from src.video_compositor import produce_full_documentary


def slugify(text: str) -> str:
    return re.sub(r'[\s_]+', '_', re.sub(r'[^\w\s]', '', text)).strip().lower()


async def main():
    print("📡 Connecting to Google Sheets: DSA_Instagram_Automation -> 'Philosophy_Videos'...")
    pending = get_next_pending_topic()
    if not pending:
        print("✓ All topics are completed! Add more pending topics in Google Sheets.")
        return

    row_num, data = pending
    topic_id = data.get("ID", 1)
    tradition = data.get("Tradition", "General")
    topic = data.get("Philosophy Topic", "Ancient Philosophy")
    target_mins = int(data.get("Target Mins", 25))

    print(f"\n🎯 Found Pending Topic #{topic_id} [{tradition}]: {topic}")
    print(f"⏱️ Target Duration: ~{target_mins} Minutes")

    session_id = f"doc_{topic_id}_{slugify(topic)[:20]}"

    # 1. Generate Script and Chapters
    doc_blueprint = generate_documentary_structure(topic, tradition, target_mins)

    # 2. Produce Full Video
    final_video = await produce_full_documentary(doc_blueprint, session_id)

    # 3. Mark Completed in Google Sheets
    mark_topic_completed(row_num)

    print("\n" + "="*70)
    print(f"🏆 DOCUMENTARY COMPLETED SUCCESSFULLY!")
    print(f"   Video File: {final_video}")
    print(f"   Launch with: open {final_video}")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())