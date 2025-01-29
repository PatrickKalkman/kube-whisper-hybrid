import sounddevice as sd
import numpy as np
from typing import Optional, Callable
import mlx_whisper
from pynput import keyboard


class WhisperTranscriber:
    def __init__(
        self,
        model_path: str = "mlx-community/whisper-large-v3-turbo",
        sample_rate: int = 16000,
        channels: int = 1,
        recording_duration: float = 5.0,
        input_device: Optional[int] = None,
    ):
        """Initialize the WhisperTranscriber.

        Args:
            model_path: Path or HuggingFace repo for the Whisper model.
            sample_rate: Audio sample rate in Hz.
            channels: Number of audio channels.
            recording_duration: Duration of each recording in seconds.
            input_device: Device index for audio input. None for default microphone.
        """
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording_duration = recording_duration
        self.input_device = input_device
        self._is_recording = False
        self._is_listening = False

    def record_audio(self) -> np.ndarray:
        """Record audio from the specified input device.

        Returns:
            Normalized audio data as a NumPy array.
        """
        samples = int(self.sample_rate * self.recording_duration)
        print("Recording... (Press and hold spacebar)")
        audio_data = sd.rec(samples, samplerate=self.sample_rate, channels=self.channels, device=self.input_device)
        sd.wait()
        print("Recording finished")
        return audio_data.flatten().astype(np.float32)

    def on_press(self, key):
        """Handle key press events."""
        try:
            if key == keyboard.Key.space and not self._is_recording:
                self._is_recording = True
                # Suppress the spacebar output
                return False
                audio_data = self.record_audio()
                transcribed_text = self.transcribe_audio(audio_data)
                if self._callback:
                    self._callback(transcribed_text)
                else:
                    print(transcribed_text)
        except Exception as e:
            print(f"Error during recording: {e}")

    def on_release(self, key):
        """Handle key release events."""
        if key == keyboard.Key.space:
            self._is_recording = False
        elif key == keyboard.Key.esc:
            self._is_listening = False
            # Stop listener
            return False

    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        """Transcribe audio data using mlx-whisper.

        Args:
            audio_data: Normalized audio data as a NumPy array.

        Returns:
            Transcribed text.
        """
        result = mlx_whisper.transcribe(audio_data, path_or_hf_repo=self.model_path)
        return result["text"]

    def start_listening(self, callback: Optional[Callable[[str], None]] = None) -> None:
        """Start listening for keyboard events to trigger recording.

        Args:
            callback: Optional function to process transcribed text.
        """
        self._is_listening = True
        self._callback = callback
        print("Listening for input... (Press and hold spacebar to record, ESC to quit)")

        # Set up keyboard listener
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def stop_listening(self) -> None:
        """Stop the continuous listening loop."""
        self._is_listening = False
        print("Stopped listening.")

    def set_input_device(self, device_index: int) -> None:
        """Set the audio input device by its index.

        Args:
            device_index: Index of the audio input device.
        """
        self.input_device = device_index
