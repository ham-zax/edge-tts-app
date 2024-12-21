# Edge TTS GUI Player

A cross-platform desktop application for text-to-speech conversion using Microsoft Edge's TTS engine and MPV player for audio playback. It provides a user-friendly interface built with Python and web technologies to easily convert text to speech using a variety of English voices.

## Features
- Text-to-speech conversion powered by Microsoft Edge TTS
- Multiple English voice options
- Simple playback controls (play, pause, stop)
- Visual progress indication
- Cross-platform support (Windows, Linux, macOS)
- Clean and intuitive interface

## Requirements

### Python
- Python 3.7 or higher
- Required Python packages (installed automatically):
  - edge-tts>=6.1.7
  - pywin32>=306 (Windows only)

### MPV Player
MPV must be installed and accessible in your system PATH.

#### Windows Installation
1. Using package managers (recommended):
   ```bash
   # Using Chocolatey
   choco install mpv
   # OR using Scoop
   scoop install mpv
   ```
2. Manual installation:
   - Download MPV player from [MPV's official website](https://mpv.io/installation/)
   - Extract to a folder (e.g., `C:\Program Files\mpv`)
   - Add to PATH:
     1. Open System Properties > Advanced > Environment Variables
     2. Under System Variables, find and select "Path"
     3. Click "Edit" and add the MPV folder path
     4. Click "OK" to save changes

#### Linux Installation
```
   # Using apt (Debian/Ubuntu)
   sudo apt install mpv
   # OR using pacman (Arch Linux)
   sudo pacman -S mpv
   # OR using dnf (Fedora)
   sudo dnf install mpv
```

#### macOS Installation
```bash
   # Using brew
   brew install mpv
```

## Architecture

The application follows a modular design with the following key components:

- **`main.py`**: One of the main entry points for the application, responsible for initializing the core components (`Config`, `AudioPlayer`, `TTSCore`) and starting the user interface (`TTSUI`). It includes error handling for cases where voice options are not available or the application fails to start.
- **`tts_app.py`**: Another main entry point for the application, providing similar initialization of core components and starting the user interface.
- **`config.py`**: Handles application configuration (currently minimal).
- **`tts_core.py`**: Implements the text-to-speech functionality using the `edge-tts` library. It provides methods to list available voices and generate audio files.
- **`ui.py`**: Manages the user interface using the `webview` library. It sets up a local web server to serve the HTML frontend (`templates/index.html`) and handles communication between the frontend and backend using HTTP requests.
- **`player.py`**: Handles audio playback using the MPV player. It manages the MPV process and provides methods to play, pause, and stop audio.
- **`templates/index.html`**: The HTML frontend for the application, providing the user interface elements and interacting with the Python backend via API calls.

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python tts_app.py
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.
