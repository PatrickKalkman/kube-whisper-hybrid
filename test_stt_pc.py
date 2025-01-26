# /// script
# dependencies = [
#   "mlx-whisper",
#   "sounddevice",
#   "numpy"
# ]
# ///

import sounddevice as sd
import numpy as np
import mlx_whisper

try:
    while True:
        # Record 5 seconds of audio
        audio_data = sd.rec(int(16000 * 5), samplerate=16000, channels=1)
        sd.wait()  # Wait for recording to complete

        # Normalize audio
        audio_data = audio_data.flatten().astype(np.float32)

        result = mlx_whisper.transcribe(
            audio_data, path_or_hf_repo="mlx-community/whisper-large-v3-turbo"
        )["text"]

        print(result)

except KeyboardInterrupt:
    print("Stopped listening.")
