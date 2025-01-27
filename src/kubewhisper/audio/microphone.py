"""
Microphone handling and audio capture.
"""

import sounddevice as sd
import numpy as np


class Microphone:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def record(self, duration):
        """Record audio for specified duration"""
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
        )
        sd.wait()
        return recording
