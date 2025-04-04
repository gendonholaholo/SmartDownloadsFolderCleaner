import shutil
from pathlib import Path
from typing import List, Dict, Any
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from rich.console import Console
from ..utils.file_utils import get_file_info, scan_directory

console = Console()

class FileArchiver:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def archive_files(self, extensions: List[str] = None, target_dir: str = None) -> List[str]:
        """
        Archive files with specified extensions to target directory
        
        Args:
            extensions: List of file extensions to archive (without dots)
            target_dir: Target directory for archived files
        """
        downloads_path = Path(self.config['downloads_path'])
        archive_path = Path(target_dir) if target_dir else Path(self.config['archive_path'])
        extensions = extensions or ['pdf', 'docx', 'xlsx']
        
        # Create archive directory
        archive_path.mkdir(parents=True, exist_ok=True)
        
        # First, scan for files recursively with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True
        ) as progress:
            scan_task = progress.add_task("[cyan]Scanning for files to archive...", total=None)
            
            # Scan directory recursively
            all_files = scan_directory(downloads_path, progress)
            
            # Filter files by extension
            files_to_archive = [
                f for f in all_files 
                if f.suffix.lower()[1:] in extensions
            ]
            
            if not files_to_archive:
                return []
            
            # Update progress for archiving phase
            archive_task = progress.add_task(
                "[green]Archiving files...",
                total=len(files_to_archive),
                start=False
            )
            
            # Calculate total size for progress
            total_size = sum(f.stat().st_size for f in files_to_archive)
            size_task = progress.add_task(
                "[blue]Total size processed...",
                total=total_size,
                start=False
            )
            
            archived_files = []
            current_size = 0
            
            # Start archiving phase
            progress.start_task(archive_task)
            progress.start_task(size_task)
            
            for file_path in files_to_archive:
                try:
                    # Get relative path to maintain folder structure
                    rel_path = file_path.relative_to(downloads_path)
                    target_path = archive_path / rel_path
                    
                    # Create parent directories if needed
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    shutil.move(str(file_path), str(target_path))
                    archived_files.append(str(rel_path))
                    
                    # Update progress
                    file_size = file_path.stat().st_size
                    current_size += file_size
                    progress.update(size_task, completed=current_size)
                    progress.update(archive_task, advance=1)
                    
                    # Show current file being processed
                    progress.console.print(
                        f"[dim]Archived: {rel_path}[/dim]",
                        overflow="ellipsis"
                    )
                    
                except Exception as e:
                    progress.console.print(
                        f"[red]Error archiving {file_path.name}: {e}[/red]"
                    )
        
        return archived_files 