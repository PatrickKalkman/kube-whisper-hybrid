"""
Tests for the assistant module.
"""
import pytest
from src.kube_whisper.assistant import Assistant

def test_assistant_initialization():
    assistant = Assistant()
    assert assistant is not None
