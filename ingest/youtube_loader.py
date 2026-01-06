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


if __name__ == "__main__":
    urls = [
        "https://youtu.be/Ec19ljjvlCI?list=TLGG6f3IQWMbfUswNDExMjAyNQ",
        "https://www.youtube.com/watch?v=Z_S0VA4jKes&t=3s"
    ]

    all_text = []

    for url in urls:
        text = load_youtube_transcript(url)
        all_text.append(text)

    combined_content = "\n\n--- NEW TOPIC ---\n\n".join(all_text)

    chunks = chunk_text(combined_content)

    print(f"Total chunks created: {len(chunks)}")
    print("/n************************************************/n")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
    print("/n************************************************/n")
    print("\nDone")

