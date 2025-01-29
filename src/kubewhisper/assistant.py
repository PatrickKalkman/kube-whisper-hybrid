"""
Main assistant implementation combining speech, LLM, and Kubernetes functionality.
"""

import logging
from typing import Optional, Callable, Literal
from kubewhisper.llm.deepseek import DeepSeekLLM
from kubewhisper.audio.whisper_transcriber import WhisperTranscriber
from kubewhisper.audio.elevenlabs_speaker import ElevenLabsSpeaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Assistant:
    """
    Main assistant class that combines speech recognition, LLM processing,
    and Kubernetes operations.
    """

    def __init__(
        self,
        model_path: str = "mlx-community/whisper-large-v3-turbo",
        input_device: Optional[int] = None,
        recording_duration: float = 5.0,
        output_mode: Literal["text", "voice"] = "text",
        elevenlabs_api_key: Optional[str] = None,
    ):
        """
        Initialize the assistant with speech recognition and LLM components.

        Args:
            model_path: Path to the Whisper model
            input_device: Audio input device index
            recording_duration: Duration of each recording in seconds
        """
        logger.info("Initializing Kubernetes Assistant...")

        self.output_mode = output_mode

        # Initialize LLM
        self.llm = DeepSeekLLM()

        # Initialize speech components
        self.speaker = ElevenLabsSpeaker(api_key=elevenlabs_api_key) if output_mode == "voice" else None
        self.transcriber = WhisperTranscriber(
            model_path=model_path, input_device=input_device, recording_duration=recording_duration
        )

        self._is_running = False
        logger.info("Assistant initialized successfully")

    async def process_query(self, query: str) -> dict:
        """
        Process a text query through the LLM and execute any resulting function calls.

        Args:
            query: The user's question or command

        Returns:
            The processed response including any function execution results
        """
        logger.info(f"Processing query: {query}")

        # Get LLM response
        response = await self.llm.ask_question(query)

        # If response contains a function call, execute it
        if isinstance(response, dict) and "type" in response and response["type"] == "function":
            execution_result = await self.llm.execute_function_call(response)

            if "error" in execution_result:
                logger.error(f"Function execution failed: {execution_result['error']}")
                return execution_result

            if "formatted_response" in execution_result:
                return {"response": execution_result["formatted_response"]}

            return execution_result

        return response

    async def process_speech(self, audio_data) -> dict:
        """
        Process speech input through transcription and LLM.

        Args:
            audio_data: Raw audio data to process

        Returns:
            The processed response
        """
        # Transcribe audio to text
        transcribed_text = self.transcriber.transcribe_audio(audio_data)
        logger.info(f"Transcribed text: {transcribed_text}")

        # Process the transcribed text
        return await self.process_query(transcribed_text)

    def start_voice_interaction(self, callback: Optional[Callable[[dict], None]] = None) -> None:
        """
        Start continuous voice interaction mode.

        Args:
            callback: Optional function to handle responses
        """
        logger.info("Starting voice interaction mode...")
        self._is_running = True

        async def process_speech_callback(transcribed_text: str):
            if not transcribed_text.strip():
                return

            response = await self.process_query(transcribed_text)
            if callback:
                callback(response)
            else:
                response_text = response.get("response", response)
                if self.output_mode == "voice" and self.speaker:
                    self.speaker.speak(response_text)
                else:
                    print(f"Assistant: {response_text}")

        def sync_callback(transcribed_text: str):
            if self._is_running:  # Only process if still running
                import asyncio
                asyncio.run(process_speech_callback(transcribed_text))

        try:
            self.transcriber.start_listening(callback=sync_callback)
        except KeyboardInterrupt:
            self.stop_voice_interaction()

    def stop_voice_interaction(self) -> None:
        """Stop the voice interaction mode."""
        logger.info("Stopping voice interaction...")
        self._is_running = False
        self.transcriber.stop_listening()

    def set_input_device(self, device_index: int) -> None:
        """
        Set the audio input device.

        Args:
            device_index: Index of the audio input device
        """
        self.transcriber.set_input_device(device_index)
        logger.info(f"Set input device to index: {device_index}")
