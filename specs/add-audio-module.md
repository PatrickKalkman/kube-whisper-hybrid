# Transcript Analytics v0 Specification

## High-Level Objective

- Create a class WhisperTranscriber that is responsible for transcribing voice to text using the mlx-whisper package

## Mid-Level Objective
- It should be stored in a file called whisper_transcriber.py in the src/kube_whisper/audio directory
- The class should have a function to listen to the sound from the microphone and transscribe
- The function should use a callback to make it maintainable and usable from other places, see example 1
- It should also be possible to listen to computer audio, see example 2

## Implementation Notes
- No need to import any external libraries see pyproject.toml for dependencies.
- Comment every function.
- Use type hints 
- Carefully review each low-level task for exact code changes.

## Context

### Beginning context
- `pyproject.toml` (readonly)

### Ending context
- `pyproject.toml` (readonly)
- `src/kube_whisper/audio/whisper_transcriber.py`

## Low-Level Examples
> Ordered from start to finish
### Example 1
import sounddevice as sd
import numpy as np
import mlx_whisper
from typing import Optional

class WhisperTranscriber:
    def __init__(self, 
                 model_path: str = "mlx-community/whisper-large-v3-turbo",
                 sample_rate: int = 16000,
                 channels: int = 1,
                 recording_duration: float = 5.0):
        """Initialize the WhisperTranscriber.
        
        Args:
            model_path: Path or HuggingFace repo for the Whisper model
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels
            recording_duration: Duration of each recording in seconds
        """
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording_duration = recording_duration
        self._is_listening = False

    def record_audio(self) -> np.ndarray:
        """Record audio using sounddevice.
        
        Returns:
            Normalized audio data as numpy array
        """
        samples = int(self.sample_rate * self.recording_duration)
        audio_data = sd.rec(samples, 
                          samplerate=self.sample_rate,
                          channels=self.channels)
        sd.wait()  # Wait for recording to complete
        return audio_data.flatten().astype(np.float32)

    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        """Transcribe audio data using Whisper.
        
        Args:
            audio_data: Normalized audio data as numpy array
            
        Returns:
            Transcribed text
        """
        result = mlx_whisper.transcribe(
            audio_data, 
            path_or_hf_repo=self.model_path
        )
        return result["text"]

    def start_listening(self, callback: Optional[callable] = None) -> None:
        """Start continuous listening and transcription.
        
        Args:
            callback: Optional callback function to process transcribed text
        """
        self._is_listening = True
        try:
            while self._is_listening:
                audio_data = self.record_audio()
                transcribed_text = self.transcribe_audio(audio_data)
                
                if callback:
                    callback(transcribed_text)
                else:
                    print(transcribed_text)
                    
        except KeyboardInterrupt:
            self.stop_listening()

    def stop_listening(self) -> None:
        """Stop the continuous listening loop."""
        self._is_listening = False
        print("Stopped listening.")

# Example usage:
if __name__ == "__main__":
    transcriber = WhisperTranscriber()
    
    # Option 1: Simple usage with default print
    transcriber.start_listening()
    
    # Option 2: With custom callback
    # def process_text(text: str):
    #     print(f"Transcribed: {text}")
    # transcriber.start_listening(callback=process_text)

### Example 2
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
