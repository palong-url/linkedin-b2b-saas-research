"""
YouTube Transcript Downloader
Usage: python get_transcript.py <youtube_url_or_video_id>
Example: python get_transcript.py https://www.youtube.com/watch?v=abc123
"""

import sys
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url_or_id):
    # If it's already just an ID (no slashes or dots)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    # Extract from URL
    match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")

def download_transcript(url_or_id, output_folder="research/youtube-transcripts"):
    video_id = extract_video_id(url_or_id)
    print(f"Fetching transcript for video: {video_id}")

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Combine all text into readable paragraphs
    full_text = ""
    chunk = ""
    for entry in transcript:
        chunk += entry['text'] + " "
        # Break into paragraphs every ~500 characters
        if len(chunk) > 500:
            full_text += chunk.strip() + "\n\n"
            chunk = ""
    if chunk:
        full_text += chunk.strip()

    # Save to file
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{video_id}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Transcript: {video_id}\n")
        f.write(f"Source: https://www.youtube.com/watch?v={video_id}\n\n")
        f.write("---\n\n")
        f.write(full_text)

    print(f"Saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_transcript.py <youtube_url_or_video_id>")
        sys.exit(1)
    download_transcript(sys.argv[1])
