import { getSubtitles } from 'youtube-captions-scraper';

interface Transcript {
  start: string;
  dur: string;
  text: string;
}

function getVideoId(url: string): string | null {
  const match = url.match(/(?:v=|\/)([0-9A-Za-z_-]{11}).*/);
  return match ? match[1] : null;
}

function formatTime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  const milliseconds = Math.floor((seconds % 1) * 1000);
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${milliseconds.toString().padStart(3, '0')}`;
}

async function youtubeToSrt(url: string): Promise<string> {
  const videoId = getVideoId(url);
  if (!videoId) {
    throw new Error('Invalid YouTube URL');
  }

  try {
    const transcript: Transcript[] = await getSubtitles({ videoID: videoId });
    let srtContent = '';
    transcript.forEach((entry, index) => {
      const startSeconds = parseFloat(entry.start);
      const durationSeconds = parseFloat(entry.dur);
      const startTime = formatTime(startSeconds);
      const endTime = formatTime(startSeconds + durationSeconds);
      srtContent += `${index + 1}\n${startTime} --> ${endTime}\n${entry.text}\n\n`;
    });
    return srtContent;
  } catch (error) {
    throw new Error(`Error fetching transcript: ${error.message}`);
  }
}

export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const youtubeUrl = url.searchParams.get('url');

    if (!youtubeUrl) {
      return new Response('Please provide a YouTube URL as a "url" query parameter.', { status: 400 });
    }

    try {
      const srtTranscript = await youtubeToSrt(youtubeUrl);
      return new Response(srtTranscript, {
        headers: { 'Content-Type': 'text/plain' },
      });
    } catch (error) {
      return new Response(error.message, { status: 500 });
    }
  },
};
