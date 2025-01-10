from __future__ import unicode_literals
import youtube_dl
import click
import whisperx
from openai import OpenAI
import torch
import os
# import markdown_pdf

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@click.command()
@click.argument("youtube_link", required=True)
@click.argument("language", required=False, default="en")
def cli(youtube_link: str, language: str) -> None:
    """
    Entrypoint for the CLI.

    Returns None
    """
    ydl_opts = {
        'format': 'mp4',
        "outtmpl": "videos/%(id)s.%(ext)s",
        'writesubtitles': True
    }
    youtube_id = youtube_link.split("v=")[1]
    if (youtube_id+".mp4") not in os.listdir("videos/"):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_link])
            print(f"Downloaded the video from {youtube_link} :)")

    transcript = get_transcript(youtube_id, language)
    print(f"Transcript: {transcript}")

    # Retrieve the pattern!
    pattern = get_pattern(transcript)
    print(pattern)
    # pdf_bytes = markdown_pdf.markdown_to_pdf(pattern)

    # with open(f"pattern/{youtube_id}.pdf", "wb") as f:
    #     f.write(pdf_bytes)
    # return transcript


def get_transcript(youtube_id: str, language: str = "en") -> str:
    """
    Get the transcript of the video.

    Returns the transcript of the video.
    """
    # Get the transcript of the video
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    audio_file = f"videos/{youtube_id}.mp4"
    batch_size = 16 # reduce if low on GPU mem
    compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)

    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("large", device='cpu', compute_type=compute_type, language=language)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    transcription = "".join([x["text"] for x in result["segments"]])
    return transcription

def get_pattern(transcript: str) -> str:
    """
    Get the pattern of the video.

    Returns the pattern of the video.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are well-versed in writing knitting patterns and are able to pick out mistakes to improve and correct them."},
            {
                "role": "user",
                "content": "Can you clean the transcription and help to extract key instructions to make the knit item in markdown format? Feel free to modify the pattern that would make the pattern more correct and accurate. \n " + transcript
            }
            ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    cli()
