import asyncio
import sys
from player import AudioPlayer
from tts_core import TTSCore
from ui import TTSUI
from config import Config

def main():
    try:
        config = Config()
        player = AudioPlayer()
        tts_core = TTSCore(config)
        voice_options = asyncio.run(tts_core.get_voice_options())
        
        if not voice_options:
            print("No voice options available. Please check your configuration.")
            sys.exit(1)
            
        app = TTSUI(voice_options, player, tts_core)
        app.run()
        
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
