import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from thefuzz import fuzz
from rich.progress import Progress

def get_file_info(file_path: Path, base_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get detailed file information"""
    stats = os.stat(file_path)
    
    # Calculate relative path from base_path if provided
    if base_path:
        try:
            relative_path = file_path.relative_to(base_path)
        except ValueError:
            relative_path = file_path
    else:
        relative_path = file_path
    
    return {
        'path': file_path,
        'name': file_path.name,
        'relative_path': relative_path,
        'size': stats.st_size / (1024 * 1024),  # Size in MB
        'age': (datetime.now() - datetime.fromtimestamp(stats.st_mtime)).days,
        'last_access': datetime.fromtimestamp(stats.st_atime),
        'extension': file_path.suffix.lower()[1:] if file_path.suffix else '',
        'is_hidden': file_path.name.startswith('.'),
        'parent_folder': file_path.parent.name
    }

def format_size(size_mb: float) -> str:
    """Format file size for display"""
    if size_mb >= 1024:
        return f"{size_mb/1024:.1f} GB"
    return f"{size_mb:.1f} MB"

def scan_directory(path: Path, progress: Optional[Progress] = None) -> List[Path]:
    """Recursively scan directory and return all files"""
    files = []
    try:
        for item in path.rglob('*'):
            if progress:
                progress.advance(0)  # Update progress without incrementing
            if item.is_file():
                files.append(item)
    except PermissionError:
        pass  # Skip directories we can't access
    return files

def fuzzy_match_file(file_info: Dict[str, Any], pattern: str, threshold: int = 60) -> bool:
    """Check if file matches pattern using fuzzy matching"""
    if not pattern:
        return True
        
    # Convert pattern to lowercase for case-insensitive matching
    pattern = pattern.lower()
    name = file_info['name'].lower()
    
    # Check exact substring match first (faster)
    if pattern in name:
        return True
    
    # Check fuzzy match on name
    if fuzz.partial_ratio(pattern, name) >= threshold:
        return True
    
    # Check fuzzy match on relative path
    rel_path = str(file_info['relative_path']).lower()
    if fuzz.partial_ratio(pattern, rel_path) >= threshold:
        return True
    
    return False

def filter_files(files: List[Dict[str, Any]], 
                min_age: int = 0, 
                min_size: float = 0, 
                pattern: str = "",
                exclude_extensions: List[str] = None,
                exclude_folders: List[str] = None,
                include_hidden: bool = False) -> List[Dict[str, Any]]:
    """
    Filter files based on various criteria
    
    Args:
        files: List of file information dictionaries
        min_age: Minimum age of files in days
        min_size: Minimum size of files in MB
        pattern: Optional search pattern for fuzzy matching
        exclude_extensions: List of file extensions to exclude
        exclude_folders: List of folder names to exclude
        include_hidden: Whether to include hidden files
    """
    exclude_extensions = exclude_extensions or []
    exclude_folders = exclude_folders or []
    filtered = []
    
    for file_info in files:
        # Skip hidden files unless explicitly included
        if not include_hidden and file_info['is_hidden']:
            continue
            
        # Skip excluded extensions
        if file_info['extension'] in exclude_extensions:
            continue
            
        # Skip files in excluded folders
        rel_path = str(file_info['relative_path'])
        if any(folder in rel_path.split(os.sep) for folder in exclude_folders):
            continue
            
        # Check age and size criteria
        if file_info['age'] < min_age or file_info['size'] < min_size:
            continue
            
        # Apply fuzzy matching if pattern is provided
        if pattern and not fuzzy_match_file(file_info, pattern):
            continue
            
        filtered.append(file_info)
    
    return filtered 