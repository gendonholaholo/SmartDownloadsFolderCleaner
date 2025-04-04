# DropClear

Smart CLI Cleaner for Windows Downloads Folder

![DropClear Banner](assets/dropbanner.png)

## Features

- **Smart Scanning**: Recursively scan your downloads folder and subfolders
- **Intelligent Cleaning**: Remove old and large files based on customizable criteria
- **File Archiving**: Automatically archive important files to keep them organized
- **Fuzzy Search**: Find files using fuzzy matching for more flexible searches
- **Customizable Settings**:
- Set minimum file size and age
- Exclude specific file extensions
- Exclude specific folders
- Customize archive location
- **Beautiful CLI Interface**: Modern and user-friendly terminal interface
- **Persistent Configuration**: Your settings are saved between sessions

## Installation

### Easy Install (Recommended)

1. Download the latest release (`DropClear-Installer.zip`)
2. Extract the zip file
3. Run `autorun.bat`
4. Shortcuts will be created on your desktop and start menu

### Manual Installation (For Developers)

```bash
# Clone the repository
git clone https://github.com/gendonholaholo/SmartDownloadsFolderCleaner.git
cd SmartDownloadsFolderCleaner

# Install dependencies
pip install -r requirements.txt

# Run the application
python dropclear.py
```

## Usage

### Main Menu

The application provides four main options:

1. **Scan Files**:

   - View files in your downloads folder
   - Filter by age, size, and name
   - See detailed folder structure

2. **Clean Files**:

   - Remove old or large files
   - Preview files before deletion
   - Get summary of cleaned folders

3. **Archive Files**:

   - Move specific file types to archive
   - Maintain folder structure
   - Get archive summary by type

4. **Configure Settings**:
   - Set downloads and archive paths
   - Configure size and age thresholds
   - Manage exclusion rules

### Configuration

You can configure:

- **Downloads Path**: Location to monitor
- **Archive Path**: Where to move archived files
- **Minimum Size**: Ignore files smaller than this
- **Maximum Age**: Focus on older files
- **Exclusions**:
  - File extensions to ignore
  - Folders to exclude from scanning

### Keyboard Shortcuts

- Use number keys (1-5) to navigate menus
- Press Enter to confirm selections
- Ctrl+C to exit at any time

## Building from Source

To create your own installer:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run the installer builder
python make_installer.py
```

The installer will be created in the `installer` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Uses [TheFuzz](https://github.com/seatgeek/thefuzz) for fuzzy matching
- Inspired by the need for a smarter downloads folder manager

---

Made with ❤️ for cleaner downloads folders
~ Mas Gendon
