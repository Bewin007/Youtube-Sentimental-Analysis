import io
from pytube import YouTube
import whisper
from better_profanity import profanity
import os
import uuid

def download_audio(video_url, output_path):
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    unique_filename = str(uuid.uuid4()) + ".mp3"
    audio_file_path = os.path.join(output_path, unique_filename)
    
    audio_stream.download(output_path=output_path, filename=unique_filename)
    
    return audio_file_path

def audio_to_text(param):
    model = whisper.load_model("tiny")
    result = model.transcribe(param)

    transcribed_text = result["text"]
    sentences = [sentence.strip() for sentence in transcribed_text.split('.') + transcribed_text.split('?')]
    
    transcribed_text_variable = ""
    for sentence in sentences:
        if sentence:
            print(sentence)
            transcribed_text_variable += sentence + '\n'
    return transcribed_text_variable


def calculate_profanity_percentage(text):
    total_words = 0
    total_profane_words = 0
    sentences = text.split('\n')
    for line in sentences:
        words = line.split()
        total_words += len(words)
        total_profane_words += sum(profanity.contains_profanity(word) for word in words)
    if total_words == 0:
        return 0
    profanity_percentage = (total_profane_words / total_words) * 100
    return profanity_percentage


if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=78Ok52tMB30'
    location = download_audio(video_url, '.')

    transcribed_text = audio_to_text(location)
    
    percent = calculate_profanity_percentage(transcribed_text)
    print(percent)
