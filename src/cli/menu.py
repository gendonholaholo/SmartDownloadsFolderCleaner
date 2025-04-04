from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.tree import Tree
from typing import Dict, Any, List

console = Console()

class MainMenu:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def display_main_menu(self) -> str:
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]DropClear[/bold cyan] - Smart CLI Cleaner for Windows Downloads Folder",
            border_style="cyan"
        ))
        
        table = Table(show_header=False, box=None, show_lines=False)
        table.add_row("[1]", "[cyan]Scan files[/cyan]")
        table.add_row("[2]", "[red]Clean files[/red]")
        table.add_row("[3]", "[green]Archive files[/green]")
        table.add_row("[4]", "[yellow]Configure settings[/yellow]")
        table.add_row("[5]", "[white]Exit[/white]")
        
        console.print(table)
        
        choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5"])
        return choice
    
    def display_scan_options(self) -> Dict[str, Any]:
        console.clear()
        console.print(Panel("📊 [bold]Scan Options[/bold]"))
        
        days = Prompt.ask("Minimum age in days", default=str(self.config['max_age_days']))
        min_size = Prompt.ask("Minimum size in MB", default=str(self.config['min_size_mb']))
        pattern = Prompt.ask("Search pattern (optional, press Enter to skip)")
        include_hidden = Confirm.ask("Include hidden files?", default=False)
        
        return {
            'days': int(days),
            'min_size': float(min_size),
            'pattern': pattern,
            'include_hidden': include_hidden
        }
    
    def display_scan_results(self, grouped_files: Dict[str, List[Dict[str, Any]]]) -> None:
        """Display scan results in a tree structure"""
        if not grouped_files:
            console.print("[yellow]No files found matching the criteria[/yellow]")
            return
        
        total_files = sum(len(files) for files in grouped_files.values())
        total_size = sum(
            sum(f['size'] for f in files)
            for files in grouped_files.values()
        )
        
        console.print(Panel(f"Found {total_files} files (Total size: {total_size:.1f} MB)"))
        
        # Create tree structure
        tree = Tree("[bold]📁 Downloads[/bold]")
        
        # Sort folders by file count
        sorted_folders = sorted(
            grouped_files.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for folder, files in sorted_folders:
            folder_size = sum(f['size'] for f in files)
            folder_node = tree.add(
                f"[bold blue]📁 {folder}[/bold blue] ({len(files)} files, {folder_size:.1f} MB)"
            )
            
            # Sort files by size
            sorted_files = sorted(files, key=lambda x: x['size'], reverse=True)
            for file in sorted_files:
                age_color = "red" if file['age'] > 90 else "yellow" if file['age'] > 30 else "green"
                folder_node.add(
                    f"[{age_color}]📄 {file['name']}[/{age_color}] - "
                    f"{file['size']:.1f}MB ({file['age']} days old)"
                )
        
        console.print(tree)
    
    def display_clean_confirmation(self, files: List[Dict[str, Any]]) -> bool:
        console.clear()
        console.print(Panel(f"🧹 Found {len(files)} files to clean"))
        
        table = Table(show_header=True)
        table.add_column("File")
        table.add_column("Size")
        table.add_column("Age (days)")
        table.add_column("Location")
        
        total_size = 0
        for file in files[:10]:  # Show first 10 files
            table.add_row(
                file['name'],
                f"{file['size']:.1f} MB",
                str(file['age']),
                str(file['relative_path'].parent)
            )
            total_size += file['size']
        
        if len(files) > 10:
            console.print(f"... and {len(files) - 10} more files")
        
        console.print(table)
        console.print(f"\nTotal size to be cleaned: {total_size:.1f} MB")
        return Confirm.ask("Do you want to proceed with cleaning?") 