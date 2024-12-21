import asyncio
import sys
import webview
from tkinter import messagebox
from player import AudioPlayer
from tts_core import TTSCore
from ui import TTSUI
from config import Config

def show_error_and_exit(message):
    messagebox.showerror("Error", message)
    sys.exit(1)

def main():
    try:
        config = Config()
        player = AudioPlayer()
        tts_core = TTSCore(config)
        
        try:
            voice_options = asyncio.run(tts_core.get_voice_options())
            if not voice_options:
                show_error_and_exit("No voice options available. Please check your configuration.")
        except Exception as e:
            show_error_and_exit(f"Failed to get voice options: {str(e)}")

        try:
            app = TTSUI(voice_options, player, tts_core)
            app.run()
        except Exception as e:
            show_error_and_exit(f"Failed to start application: {str(e)}")

    except Exception as e:
        show_error_and_exit(f"Application initialization failed: {str(e)}")

if __name__ == "__main__":
    main()
