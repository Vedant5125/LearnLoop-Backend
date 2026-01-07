from youtube_transcript_api import YouTubeTranscriptApi
from ingest.chunker import chunk_text

def get_video_id(url: str) -> str:
    """
    Extract video ID from YouTube URL safely
    """
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id_with_params = url.split("youtu.be/")[1]
        return video_id_with_params.split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")


def load_youtube_transcript(url: str) -> str:
    video_id = get_video_id(url)

    yt_api = YouTubeTranscriptApi()
    transcript_list = yt_api.list(video_id)
    transcript = transcript_list.find_transcript(['en'])
    fetched = transcript.fetch()
    
    full_text = " ".join([entry.text for entry in fetched])
    return full_text
