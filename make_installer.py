import os
import sys
import subprocess
from pathlib import Path

def create_installer():
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Install required packages
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create spec file for PyInstaller
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['dropclear.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DropClear',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
    """
    
    # Create assets directory if it doesn't exist
    assets_dir = project_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Create spec file
    with open("dropclear.spec", "w") as f:
        f.write(spec_content.strip())
    
    # Create PyInstaller command
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "DropClear",
        "--clean",
        "--console",
        "dropclear.py"
    ]
    
    # If icon exists, add it to the command
    icon_path = assets_dir / "icon.ico"
    if icon_path.exists():
        pyinstaller_cmd.extend(["--icon", str(icon_path)])
    
    # Run PyInstaller
    subprocess.check_call(pyinstaller_cmd)
    
    # Create installer directory
    installer_dir = project_root / "installer"
    installer_dir.mkdir(exist_ok=True)
    
    # Move executable to installer directory
    exe_path = project_root / "dist" / "DropClear.exe"
    if exe_path.exists():
        new_exe_path = installer_dir / "DropClear.exe"
        exe_path.rename(new_exe_path)
        
        # Create autorun.bat
        with open(installer_dir / "autorun.bat", "w") as f:
            f.write("""@echo off
echo Installing DropClear...
echo.

REM Create start menu shortcut
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\DropClear.lnk'); $Shortcut.TargetPath = '%~dp0DropClear.exe'; $Shortcut.Save()"

REM Create desktop shortcut
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\DropClear.lnk'); $Shortcut.TargetPath = '%~dp0DropClear.exe'; $Shortcut.Save()"

echo Installation complete!
echo Shortcuts have been created on your desktop and start menu.
echo.
pause
start DropClear.exe
""")
        
        print("\nInstaller created successfully!")
        print(f"Installer location: {installer_dir}")
        print("\nTo distribute:")
        print("1. Zip the 'installer' folder")
        print("2. Share the zip file")
        print("\nUsers just need to:")
        print("1. Extract the zip")
        print("2. Run autorun.bat")
    else:
        print("Error: Failed to create executable")

if __name__ == "__main__":
    create_installer() 