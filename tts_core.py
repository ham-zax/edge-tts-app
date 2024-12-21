import asyncio
import edge_tts
import tempfile

class TTSCore:
    def __init__(self, config):
        self.config = config
        # Potential future use of config:
        # print(f"Configuration loaded: {self.config.__dict__}")

    async def get_voice_options(self):
        voice_options = await edge_tts.list_voices()
        return [voice['ShortName'] for voice in voice_options if voice["Locale"].startswith('en-')]

    async def generate_audio(self, text, voice):
        communicate = edge_tts.Communicate(text, voice)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            await communicate.save(tmp_file.name)
            return tmp_file.name
