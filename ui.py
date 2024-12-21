import webview
import threading
import asyncio
import os
import http.server
import socketserver
import json
from pathlib import Path

class TTSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.voice_options = kwargs.pop('voice_options', [])
        self.tts_ui = kwargs.pop('tts_ui', None)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/voices':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Group voices by localization
            grouped_voices = {}
            for voice in self.voice_options:
                # Assuming voice format is "en-US-Standard-A"
                parts = voice.split('-')
                if len(parts) >= 2:
                    locale = f"{parts[0]}-{parts[1]}"  # e.g., "en-US"
                    voice_type = '-'.join(parts[2:])   # e.g., "Standard-A"
                    
                    if locale not in grouped_voices:
                        grouped_voices[locale] = []
                    grouped_voices[locale].append({
                        'id': voice,
                        'name': voice_type
                    })
            
            self.wfile.write(json.dumps(grouped_voices).encode())
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == '/tts':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            text = data.get('text', '')
            voice = data.get('voice', '')
            action = data.get('action', '')
            
            if action == 'play' and self.tts_ui:
                self.tts_ui.play_audio(text, voice)
                response = {'status': 'success'}
            elif action == 'stop' and self.tts_ui:
                self.tts_ui.stop_audio()
                response = {'status': 'success'}
            else:
                response = {'status': 'error', 'message': 'Invalid action'}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return
        
        self.send_response(404)
        self.end_headers()

    def translate_path(self, path):
        if path == '/':
            return os.path.join(os.getcwd(), 'templates', 'index.html')
        return super().translate_path(path)

class TTSUI:
    def __init__(self, voice_options, player, tts_core):
        self.player = player
        self.tts_core = tts_core
        self.voice_options = voice_options
        self.window = None
        self.is_playing = False
        self.is_closing = False
        self.server = None
        self.server_thread = None

    def start_server(self):
        handler = lambda *args: TTSRequestHandler(*args, voice_options=self.voice_options, tts_ui=self)
        self.server = socketserver.TCPServer(('localhost', 0), handler)
        port = self.server.server_address[1]
        
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        return f'http://localhost:{port}'

    def run(self):
        try:
            # Start local server
            url = self.start_server()
            
            # Create window pointing to local server
            self.window = webview.create_window(
                'Text-to-Speech Player',
                url=url
            )
            
            # Start webview
            webview.start(debug=True)
            
        except Exception as e:
            print(f"Error starting webview: {e}")
            if self.server:
                self.server.shutdown()
            raise
        
    def cleanup(self):
        try:
            if not self.is_closing:
                self.is_closing = True
                self.stop_audio()
                if self.player.ipc_socket and os.path.exists(self.player.ipc_socket):
                    try:
                        os.unlink(self.player.ipc_socket)
                    except Exception as e:
                        print(f"Error cleaning up socket: {e}")
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def on_closing(self):
        self.cleanup()
        return True


    def play_audio(self, text, voice):
        if not text:
            return

        if self.is_playing:
            self.stop_audio()

        self.window.evaluate_js('setButtonState("playButton", false)')
        self.window.evaluate_js('setButtonState("stopButton", true)')
        self.player.is_paused = False

        self.playback_thread = threading.Thread(target=self._play_audio_thread, args=(text, voice))
        self.playback_thread.start()
        self.is_playing = True

    def _play_audio_thread(self, text, voice):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            audio_file = loop.run_until_complete(self.tts_core.generate_audio(text, voice))
            self.player.play(audio_file)
            if self.player.mpv_process:
                self.player.mpv_process.wait()
        except Exception as e:
            print(f"Failed to play audio: {e}")
        finally:
            self.is_playing = False
            self.window.evaluate_js('setButtonState("playButton", true)')
            self.window.evaluate_js('setButtonState("stopButton", false)')
            self.window.evaluate_js('setProgress(0)')

    def stop_audio(self):
        self.player.stop()
        self.is_playing = False
        self.window.evaluate_js('setButtonState("playButton", true)')
        self.window.evaluate_js('setButtonState("stopButton", false)')
        self.window.evaluate_js('setProgress(0)')
