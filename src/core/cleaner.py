from pathlib import Path
from typing import List, Dict, Any
from rich.progress import Progress
from ..utils.file_utils import get_file_info

class FileCleaner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def identify_files_to_clean(self) -> List[Dict[str, Any]]:
        downloads_path = Path(self.config['downloads_path'])
        files_to_clean = []
        
        files = list(downloads_path.glob('*'))
        with Progress() as progress:
            task = progress.add_task("[cyan]Identifying files to clean...", total=len(files))
            
            for file_path in files:
                if file_path.is_file():
                    info = get_file_info(file_path)
                    if (info['age'] >= self.config['max_age_days'] and 
                        info['size'] >= self.config['min_size_mb'] and
                        info['extension'] not in self.config['exclude_extensions']):
                        files_to_clean.append(info)
                progress.update(task, advance=1)
        
        return files_to_clean
    
    def clean_files(self, files_to_clean: List[Dict[str, Any]]) -> List[str]:
        deleted_files = []
        
        with Progress() as progress:
            task = progress.add_task("[red]Deleting files...", total=len(files_to_clean))
            
            for file_info in files_to_clean:
                try:
                    Path(file_info['path']).unlink()
                    deleted_files.append(file_info['name'])
                except Exception as e:
                    print(f"Error deleting {file_info['name']}: {e}")
                progress.update(task, advance=1)
        
        return deleted_files 