import subprocess
import os
import tempfile
import socket
import json

class AudioPlayer:
    def __init__(self):
        self.mpv_process = None
        self.audio_file = None
        self.ipc_socket = None
        self.is_playing = False
        self.is_paused = False

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
            print("MPV Error: MPV not found. Please ensure it is installed and in your PATH.")
            return

        self.audio_file = audio_file
        try:
            self.ipc_socket = os.path.join(tempfile.gettempdir(), f'mpv-socket-{os.getpid()}')
            if os.path.exists(self.ipc_socket):
                os.unlink(self.ipc_socket)

            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
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
               startupinfo=(subprocess.STARTUPINFO() if os.name == 'nt' else None))
            self.is_playing = True
        except FileNotFoundError:
            print("Error: mpv not found. Please ensure it is installed and in your PATH.")
        except Exception as e:
            print(f"Error playing audio with mpv: {e}")

    def stop(self):
        if self.mpv_process:
            self.mpv_process.terminate()
            self.mpv_process = None
        self.is_playing = False
        self.is_paused = False
        if self.audio_file:
            os.remove(self.audio_file)
            self.audio_file = None
        if self.ipc_socket:
            try:
                if os.path.exists(self.ipc_socket):
                    os.unlink(self.ipc_socket)
            finally:
                self.ipc_socket = None

    def pause_resume(self):
        if self.mpv_process and self.ipc_socket and os.path.exists(self.ipc_socket):
            try:
                if os.name == 'nt':
                    import win32file
                    handle = win32file.CreateFile(
                        self.ipc_socket,
                        win32file.GENERIC_WRITE,
                        0, None,
                        win32file.OPEN_EXISTING,
                        0, None
                    )
                    command = json.dumps({"command": ["cycle", "pause"]}) + '\n'
                    win32file.WriteFile(handle, command.encode())
                    win32file.CloseHandle(handle)
                else:
                    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                        client.connect(self.ipc_socket)
                        command = {"command": ["cycle", "pause"]}
                        client.sendall((json.dumps(command) + '\n').encode())
                self.is_paused = not self.is_paused
            except (FileNotFoundError, ConnectionRefusedError) as e:
                print(f"Error sending pause command: {e}")
