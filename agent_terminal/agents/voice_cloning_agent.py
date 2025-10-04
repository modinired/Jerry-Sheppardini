"""An agent that clones a user's voice to respond to prompts."""

import asyncio
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import sounddevice as sd
import soundfile as sf

from .base import Agent
from .openai_agent import OpenAIAgent

if TYPE_CHECKING:
    from chatterbox.tts import ChatterboxTTS


class VoiceCloningAgent(Agent):
    """
    An agent that uses a voice sample to generate spoken responses.

    This agent first generates a text response using an OpenAI model and then
    synthesizes it into speech using the provided voice sample. The final
    output is the played audio.
    """

    def __init__(self, model: str, audio_path: str) -> None:
        """
        Initializes the VoiceCloningAgent.

        Args:
            model: The name of the OpenAI model to use for text generation.
            audio_path: The path to the audio file for voice cloning.
        """
        if not Path(audio_path).is_file():
            raise FileNotFoundError(f"Audio file not found at: {audio_path}")

        self.model = model
        self.audio_path = audio_path
        self.text_agent = OpenAIAgent(model=self.model)
        self.tts_model: "ChatterboxTTS | None" = None

    async def _lazy_load_model(self) -> None:
        """Load the TTS model on demand to avoid slow startup times."""
        if self.tts_model is None:
            import torch
            from chatterbox.tts import ChatterboxTTS

            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tts_model = ChatterboxTTS.from_pretrained(device=device)

    async def get_response(self, prompt: str) -> str:
        """
        Generates a text response and synthesizes it as spoken audio.

        Args:
            prompt: The user's input prompt.

        Returns:
            A message indicating that the audio response is being played.
        """
        await self._lazy_load_model()
        text_response = await self.text_agent.get_response(prompt)

        # Generate audio from the text response
        wav = self.tts_model.generate(
            text_response,
            audio_prompt_path=self.audio_path,
        )

        # Save the generated audio to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            sf.write(fp.name, wav.squeeze().cpu().numpy(), self.tts_model.sr)
            temp_audio_path = fp.name

        # Play the audio in a separate thread to avoid blocking
        asyncio.create_task(self._play_audio(temp_audio_path))

        return f"Playing audio response for: '{prompt}'"

    async def _play_audio(self, audio_path: str) -> None:
        """
        Plays the audio file at the given path.

        Args:
            audio_path: The path to the audio file to play.
        """
        try:
            data, fs = sf.read(audio_path, dtype="float32")
            sd.play(data, fs)
            sd.wait()
        finally:
            # Clean up the temporary file
            Path(audio_path).unlink()