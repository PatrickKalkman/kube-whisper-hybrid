"""
Command-line interface for the Kubernetes Assistant.
"""

import argparse
import asyncio
import logging
from typing import Optional
from kubewhisper.k8s import k8s_tools  # noqa: F401
from kubewhisper.assistant import Assistant


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity level.

    Args:
        verbose: If True, set logging level to DEBUG
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def run_text_mode(assistant: Assistant, query: str) -> None:
    """Run the assistant in text mode with a single query.

    Args:
        assistant: Initialized Assistant instance
        query: Text query to process
    """
    response = await assistant.process_query(query)
    print(f"Assistant: {response.get('response', response)}")


def run_voice_mode(assistant: Assistant, duration: float, device_index: Optional[int]) -> None:
    """Run the assistant in voice interaction mode.

    Args:
        assistant: Initialized Assistant instance
        duration: Recording duration in seconds
        device_index: Audio input device index
    """
    if device_index is not None:
        assistant.set_input_device(device_index)

    try:
        assistant.start_voice_interaction()
    except KeyboardInterrupt:
        print("\nStopping voice interaction...")
    finally:
        assistant.stop_voice_interaction()


def main():
    parser = argparse.ArgumentParser(
        description="Kubernetes Voice Assistant CLI", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # General options
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("-t", "--text", help="Run in text mode with the provided query")
    mode_group.add_argument("--voice", action="store_true", help="Run in voice interaction mode")

    # Voice mode options
    parser.add_argument(
        "--model", default="mlx-community/whisper-large-v3-turbo", help="Path or name of the Whisper model to use"
    )
    parser.add_argument("--duration", type=float, default=5.0, help="Recording duration in seconds for voice mode")
    parser.add_argument("--device", type=int, help="Audio input device index")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Initialize assistant
    assistant = Assistant(model_path=args.model, input_device=args.device, recording_duration=args.duration)

    # Run in selected mode
    try:
        if args.text:
            asyncio.run(run_text_mode(assistant, args.text))
        else:  # voice mode
            run_voice_mode(assistant, args.duration, args.device)
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
