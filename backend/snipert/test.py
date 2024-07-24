from pydub import AudioSegment
import os

def convert_mp3_to_wav(mp3_file, wav_file):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file)
    
    # Export the audio to WAV format
    audio.export(wav_file, format="wav")

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)

    try:
        transcribed_text = recognizer.recognize_google(audio_data)
        return transcribed_text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

# Provide the correct file paths for the MP3 and WAV files
mp3_file = "C:\\Users\\MADHAN\\Documents\\Bewin\\baackend\\75ffbfff-e303-4730-b992-215ab58c488c.mp3"
wav_file = "C:\\Users\\MADHAN\\Documents\\Bewin\\baackend\\75ffbfff-e303-4730-b992-215ab58c488c.wav"

# Convert MP3 to WAV
convert_mp3_to_wav(mp3_file, wav_file)

# Transcribe the audio
transcribed_text = transcribe_audio(wav_file)
print(transcribed_text)

# Clean up the WAV file after transcription
os.remove(wav_file)
