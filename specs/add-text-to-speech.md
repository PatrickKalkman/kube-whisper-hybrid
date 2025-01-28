# Transcript Analytics v0 Specification

## High-Level Objective

- Create a class ElevenLabsSpeaker that is responsible for converting text to speech using the elevenlabs API.

## Mid-Level Objective
- It should be stored in a file called elevenlabs_speaker.py in the src/kube_whisper/audio directory
- The class should have an speak function that converts text to speech and either streams it or returns the audio stream, see example 1
- It should accept an Eleven Labs API key in the initializer, see example 1

## Implementation Notes
- No need to import any external libraries see pyproject.toml for dependencies.
- Comment every function.
- Use type hints 
- Carefully review each example for context and inspiration

## Context

### Beginning context
- `pyproject.toml` (readonly)

### Ending context
- `pyproject.toml` (readonly)
- `src/kube_whisper/audio/elevenlabs_speaker.py`

## Low-Level Examples
> Ordered from start to finish
### Example 1
import os
from typing import Optional
from elevenlabs.client import ElevenLabs
from elevenlabs import stream

class ElevenLabsSpeaker:
    """
    A class for converting text to speech using the ElevenLabs API.
    
    Attributes:
        client (ElevenLabs): The ElevenLabs client instance
        default_voice_id (str): Default voice ID to use for synthesis
        default_model_id (str): Default model ID to use for synthesis
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        default_voice_id: str = "9BWtsMINqrJLrRacOk9x",
        default_model_id: str = "eleven_multilingual_v2"
    ):
        """
        Initialize the ElevenLabsSpeaker.
        
        Args:
            api_key: ElevenLabs API key. If None, will try to get from environment variable
            default_voice_id: Default voice ID to use
            default_model_id: Default model ID to use
        """
        self.client = ElevenLabs(
            api_key=api_key or os.environ.get("ELEVENLABS_API_KEY")
        )
        self.default_voice_id = default_voice_id
        self.default_model_id = default_model_id
        
    def speak(
        self, 
        text: str,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
        stream_audio: bool = True
    ) -> None:
        """
        Convert text to speech and either stream it or return the audio stream.
        
        Args:
            text: The text to convert to speech
            voice_id: Optional voice ID to override the default
            model_id: Optional model ID to override the default
            stream_audio: Whether to stream the audio immediately (True) or return the stream (False)
            
        Returns:
            None if stream_audio is True, otherwise returns the audio stream
        """
        audio_stream = self.client.text_to_speech.convert_as_stream(
            text=text,
            voice_id=voice_id or self.default_voice_id,
            model_id=model_id or self.default_model_id
        )
        
        if stream_audio:
            stream(audio_stream)
            return None
        return audio_stream
    
    def speak_to_file(
        self,
        text: str,
        output_path: str,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None
    ) -> None:
        """
        Convert text to speech and save it to a file.
        
        Args:
            text: The text to convert to speech
            output_path: Path where the audio file should be saved
            voice_id: Optional voice ID to override the default
            model_id: Optional model ID to override the default
        """
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=voice_id or self.default_voice_id,
            model_id=model_id or self.default_model_id
        )
        
        with open(output_path, 'wb') as f:
            f.write(audio)