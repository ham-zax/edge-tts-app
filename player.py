import subprocess
import os
import tempfile
import socket
import json
import time

class AudioPlayer:
    def __init__(self):
        self.mpv_process = None
        self.audio_file = None
        self.ipc_socket = None
        self.is_playing = False
        self.is_paused = False
        self._cleanup_resources()

    def _cleanup_resources(self):
        """Clean up any leftover resources"""
        if self.ipc_socket and os.path.exists(self.ipc_socket):
            try:
                os.unlink(self.ipc_socket)
            except Exception as e:
                print(f"Warning: Failed to clean up socket {self.ipc_socket}: {e}")

    def check_mpv_installed(self):
        try:
            subprocess.run(['mpv', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            scoop_mpv = os.path.expanduser('~/scoop/apps/mpv/current/mpv.exe')
            if os.path.exists(scoop_mpv):
                os.environ['PATH'] = os.path.dirname(scoop_mpv) + os.pathsep + os.environ['PATH']
                return True
            return False

    def play(self, audio_file):
        if not self.check_mpv_installed():
            raise RuntimeError("MPV not found. Please ensure it is installed and in your PATH.")

        self._cleanup_resources()
        self.audio_file = audio_file

        try:
            self.ipc_socket = os.path.join(tempfile.gettempdir(), f'mpv-socket-{os.getpid()}')
            
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            startupinfo = subprocess.STARTUPINFO() if os.name == 'nt' else None
            if startupinfo:
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            self.mpv_process = subprocess.Popen([
                "mpv",
                "--no-terminal",
                "--no-video",
                "--no-audio-display",
                "--force-window=no",
                f"--input-ipc-server={self.ipc_socket}",
                "--input-ipc-client=",
                self.audio_file
            ], creationflags=creation_flags,
               startupinfo=startupinfo)
            
            # Wait briefly to ensure process started successfully
            time.sleep(0.1)
            if self.mpv_process.poll() is not None:
                raise RuntimeError("MPV process failed to start")
            
            self.is_playing = True
            self.is_paused = False

        except Exception as e:
            self._cleanup_resources()
            self.mpv_process = None
            raise RuntimeError(f"Failed to start playback: {str(e)}")

    def stop(self):
        try:
            if self.mpv_process:
                self.mpv_process.terminate()
                try:
                    self.mpv_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.mpv_process.kill()
                self.mpv_process = None
        finally:
            self.is_playing = False
            self.is_paused = False
            if self.audio_file:
                try:
                    os.remove(self.audio_file)
                except Exception as e:
                    print(f"Warning: Failed to remove audio file: {e}")
                self.audio_file = None
            self._cleanup_resources()

    def __del__(self):
        """Ensure resources are cleaned up"""
        self.stop()
