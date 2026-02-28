from pathlib import Path
from typing import Generator

import ffmpeg


def extract_audio_chunks(video_path: Path) -> Generator[bytes, None, None]:
    process = (
        ffmpeg
        .input(str(video_path))
        .output('pipe:', format='s16le', ac=1, ar=16000)
        .run_async(pipe_stdout=True)
    )
    chunk_samples = 16000
    chunk_size = chunk_samples * 2
    while True:
        chunk = process.stdout.read(chunk_size)
        if not chunk:
            break
        print(f"Chunk size: {len(chunk)} bytes")
        yield chunk
    process.wait()
