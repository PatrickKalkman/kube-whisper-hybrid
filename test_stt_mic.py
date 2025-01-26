# /// script
# dependencies = [
#   "SpeechRecognition",
#   "mlx-whisper",
#   "pyaudio",
# ]
# ///

import speech_recognition as sr
import numpy as np
import mlx_whisper

r = sr.Recognizer()
mic = sr.Microphone(sample_rate=16000)

print("Listening...")

try:
    with mic as source:
        r.adjust_for_ambient_noise(source)
        while True:
            audio = r.listen(source)
            # Convert audio to numpy array
            audio_data = (
                np.frombuffer(audio.get_raw_data(), dtype=np.int16).astype(np.float32)
                / 32768.0
            )

            # Process audio with Apple MLXWhisper model
            result = mlx_whisper.transcribe(
                audio_data, path_or_hf_repo="mlx-community/whisper-large-v3-turbo"
            )["text"]

            # Print the transcribed text
            print(result)

except KeyboardInterrupt:
    print("Stopped listening.")
