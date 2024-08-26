from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    # Extract video ID from YouTube URL
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def format_time(seconds):
    # Convert seconds to SRT time format
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

# Example usage
if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    srt_transcript = youtube_to_srt(url)
    print(srt_transcript)
    
    # Optionally, save to file
    with open("transcript.srt", "w", encoding="utf-8") as f:
        f.write(srt_transcript)