import json
import os
from pathlib import Path
from typing import Dict, Any
from rich.console import Console

console = Console()

class Config:
    @staticmethod
    def get_default_downloads_path() -> str:
        """Get the default Downloads folder path for the current user"""
        # Try to get from environment variables first
        user_profile = os.environ.get('USERPROFILE')
        if user_profile:
            downloads_path = Path(user_profile) / "Downloads"
            if downloads_path.exists():
                return str(downloads_path)
        
        # Fallback to home directory
        downloads_path = Path.home() / "Downloads"
        if downloads_path.exists():
            return str(downloads_path)
        
        # If all else fails, return a default path
        return str(Path.home() / "Downloads")
    
    @staticmethod
    def get_default_archive_path() -> str:
        """Get the default Archive folder path for the current user"""
        # Try to get from environment variables first
        user_profile = os.environ.get('USERPROFILE')
        if user_profile:
            archive_path = Path(user_profile) / "Documents" / "Arsip"
            if archive_path.exists() or not archive_path.parent.exists():
                return str(archive_path)
        
        # Fallback to home directory
        archive_path = Path.home() / "Documents" / "Arsip"
        return str(archive_path)
    
    DEFAULT_CONFIG = {
        "downloads_path": get_default_downloads_path.__func__(),
        "min_size_mb": 50,
        "max_age_days": 30,
        "exclude_extensions": ["zip", "mp4", "exe"],
        "exclude_folders": ["node_modules", ".git", "venv"],  # Default folders to exclude
        "archive_path": get_default_archive_path.__func__()
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        
        # Validate paths
        self._validate_paths()
    
    def _validate_paths(self) -> None:
        """Validate that the configured paths exist or can be created"""
        # Check downloads path
        downloads_path = Path(self.config['downloads_path'])
        if not downloads_path.exists():
            # Try to find the Downloads folder
            default_path = self.get_default_downloads_path()
            if default_path != self.config['downloads_path']:
                console.print(f"[yellow]Warning: Downloads path '{downloads_path}' not found. Using default: '{default_path}'[/yellow]")
                self.config['downloads_path'] = default_path
                self._save_config(self.config)
        
        # Check archive path
        archive_path = Path(self.config['archive_path'])
        if not archive_path.exists():
            # Create the archive directory if it doesn't exist
            try:
                archive_path.mkdir(parents=True, exist_ok=True)
                console.print(f"[green]Created archive directory: {archive_path}[/green]")
            except Exception as e:
                # If creation fails, use default path
                default_path = self.get_default_archive_path()
                if default_path != self.config['archive_path']:
                    console.print(f"[yellow]Warning: Could not create archive path '{archive_path}'. Using default: '{default_path}'[/yellow]")
                    self.config['archive_path'] = default_path
                    self._save_config(self.config)
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Validate config structure
                for key in self.DEFAULT_CONFIG:
                    if key not in config:
                        console.print(f"[yellow]Warning: Missing '{key}' in config file. Using default value.[/yellow]")
                        config[key] = self.DEFAULT_CONFIG[key]
                return config
        except FileNotFoundError:
            console.print(f"[yellow]Config file not found. Creating new config file: {self.config_file}[/yellow]")
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG
        except json.JSONDecodeError:
            console.print(f"[red]Error: Invalid JSON in config file. Using default configuration.[/red]")
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        try:
            # Ensure the parent directory exists
            config_path = Path(self.config_file)
            if config_path.parent != Path('.'):
                config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save with pretty formatting
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving config file: {e}[/red]")
            console.print("[yellow]Changes will not persist after application closes.[/yellow]")
    
    def update(self, new_settings: Dict[str, Any]) -> None:
        """Update configuration with new settings and save to file"""
        try:
            # Update in memory
            self.config.update(new_settings)
            # Save to file
            self._save_config(self.config)
            # Validate paths
            self._validate_paths()
        except Exception as e:
            console.print(f"[red]Error updating configuration: {e}[/red]")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback to default"""
        return self.config.get(key, default) 