from pathlib import Path
from typing import List, Dict, Any
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Confirm
from ..utils.file_utils import get_file_info, scan_directory, filter_files

class FileScanner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def scan_files(self, min_age: int = None, min_size: float = None, pattern: str = "", include_hidden: bool = False) -> List[Dict[str, Any]]:
        """
        Scan files recursively in downloads directory
        
        Args:
            min_age: Minimum age of files in days
            min_size: Minimum size of files in MB
            pattern: Optional search pattern for fuzzy matching
            include_hidden: Whether to include hidden files
        """
        downloads_path = Path(self.config['downloads_path'])
        min_age = min_age or self.config['max_age_days']
        min_size = min_size or self.config['min_size_mb']
        
        # Create progress bar with spinner for scanning
        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            transient=True
        ) as progress:
            scan_task = progress.add_task("[cyan]Scanning files...", total=None)
            
            # Scan directory recursively
            files = scan_directory(downloads_path, progress)
            
            # Get file info for all files
            file_infos = [
                get_file_info(f, downloads_path) 
                for f in files
            ]
            
            # Update progress
            progress.update(scan_task, total=len(file_infos))
            
            # Filter files based on criteria
            matching_files = filter_files(
                file_infos,
                min_age=min_age,
                min_size=min_size,
                pattern=pattern,
                exclude_extensions=self.config['exclude_extensions'],
                exclude_folders=self.config['exclude_folders'],
                include_hidden=include_hidden
            )
            
            progress.update(scan_task, completed=len(file_infos))
        
        return matching_files
    
    def group_files_by_folder(self, files: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group files by their parent folder"""
        grouped = {}
        for file in files:
            parent = str(file['relative_path'].parent)
            if parent == '.':
                parent = 'Root'
            if parent not in grouped:
                grouped[parent] = []
            grouped[parent].append(file)
        return grouped 