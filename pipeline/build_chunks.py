from ingest.chunker import chunk_text
from ingest.youtube_loader import load_youtube_transcript
from ingest.pdf_loader import load_pdf


def get_all_chunks():
    all_chunks = []
    all_chunks.append("PDF started\n\n")

    pdf_text = load_pdf("economics.pdf")
    pdf_chunks = chunk_text(pdf_text)
    all_chunks.extend(pdf_chunks)

    all_chunks.append("PDF ended\n\n")

    yt_urls = [
        "https://youtu.be/Ec19ljjvlCI?list=TLGG6f3IQWMbfUswNDExMjAyNQ",
        "https://www.youtube.com/watch?v=Z_S0VA4jKes&t=3s"
    ]

    all_chunks.append("YouTube started\n\n")

    for url in yt_urls:
        yt_text = load_youtube_transcript(url)
        yt_chunks = chunk_text(yt_text)
        all_chunks.extend(yt_chunks)

    return all_chunks

if __name__ == "__main__":
    chunks = get_all_chunks()
    print(f"Total chunks created: {len(chunks)}")
    print("/n************************************************/n")
    print(chunks)

