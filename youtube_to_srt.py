import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys

def get_video_id(url):
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return video_id_match.group(1) if video_id_match else None

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

def youtube_to_srt(url):
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL"

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

    srt_content = ""
    for i, entry in enumerate(transcript, 1):
        start_time = format_time(entry['start'])
        end_time = format_time(entry['start'] + entry['duration'])
        srt_content += f"{i}\n{start_time} --> {end_time}\n{entry['text']}\n\n"

    return srt_content

def main():
    parser = argparse.ArgumentParser(description="Convert YouTube video subtitles to SRT format.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", help="Output file name (default: transcript.srt)")
    args = parser.parse_args()

    print("Fetching transcript...")
    srt_transcript = youtube_to_srt(args.url)
    
    if srt_transcript.startswith("Error") or srt_transcript == "Invalid YouTube URL":
        print(srt_transcript)
        sys.exit(1)

    output_file = args.output or "transcript.srt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt_transcript)
    
    print(f"Transcript saved to {output_file}")

if __name__ == "__main__":
    main()