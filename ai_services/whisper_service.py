"""Whisper API service for audio transcription."""
import os
from openai import OpenAI
from django.conf import settings


class WhisperService:
    """Service for transcribing audio files using OpenAI Whisper API."""

    def __init__(self):
        """Initialize OpenAI client with API key from settings."""
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in settings")
        self.client = OpenAI(api_key=api_key)

    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text using Whisper API.

        Args:
            audio_file_path: Path to audio file or file object

        Returns:
            str: Transcribed text

        Raises:
            Exception: If transcription fails
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Can be 'sw' for Swahili or auto-detect
                )
            return transcript.text
        except Exception as e:
            raise Exception(f"Whisper transcription failed: {str(e)}")

    def transcribe_from_file_field(self, file_field):
        """
        Transcribe audio from Django FileField.

        Args:
            file_field: Django FileField object

        Returns:
            str: Transcribed text
        """
        if not file_field:
            raise ValueError("No audio file provided")

        # Get the actual file path
        file_path = file_field.path
        return self.transcribe_audio(file_path)
