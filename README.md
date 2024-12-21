# Edge TTS GUI Player

A cross-platform graphical user interface for text-to-speech conversion using Microsoft Edge's TTS engine and MPV player.

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
