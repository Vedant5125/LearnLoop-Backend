from langchain_text_splitters import TokenTextSplitter

def chunk_text(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150
):
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_text(text)
    return chunks
