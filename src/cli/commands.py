from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from pathlib import Path
from ..core.scanner import FileScanner
from ..core.cleaner import FileCleaner
from ..core.archiver import FileArchiver
from .menu import MainMenu

console = Console()

class CommandHandler:
    def __init__(self, config):
        self.config = config
        self.menu = MainMenu(config)
        self.scanner = FileScanner(config)
        self.cleaner = FileCleaner(config)
        self.archiver = FileArchiver(config)
    
    def handle_scan(self):
        options = self.menu.display_scan_options()
        files = self.scanner.scan_files(
            min_age=options['days'],
            min_size=options['min_size'],
            pattern=options['pattern'],
            include_hidden=options['include_hidden']
        )
        
        # Group files by folder and display results
        grouped_files = self.scanner.group_files_by_folder(files)
        self.menu.display_scan_results(grouped_files)
    
    def handle_clean(self):
        # Scan files with default criteria
        files = self.scanner.scan_files()
        if not files:
            console.print("[yellow]No files to clean[/yellow]")
            return
        
        # Group files by folder for display
        grouped_files = self.scanner.group_files_by_folder(files)
        
        if self.menu.display_clean_confirmation(files):
            deleted = self.cleaner.clean_files(files)
            console.print(f"[green]Successfully deleted {len(deleted)} files[/green]")
            
            # Show summary of cleaned folders
            if deleted:
                console.print("\n[bold]Cleaned folders:[/bold]")
                cleaned_folders = {}
                for file in files:
                    folder = str(file['relative_path'].parent)
                    if folder == '.':
                        folder = 'Root'
                    cleaned_folders[folder] = cleaned_folders.get(folder, 0) + 1
                
                for folder, count in cleaned_folders.items():
                    console.print(f"📁 {folder}: {count} files")
    
    def handle_archive(self):
        extensions = console.input("Enter file extensions to archive (comma-separated, default: pdf,docx,xlsx): ")
        if extensions:
            extensions = [ext.strip() for ext in extensions.split(',')]
        
        archived = self.archiver.archive_files(extensions)
        if archived:
            console.print(f"\n[green]Successfully archived {len(archived)} files[/green]")
            
            # Show summary of archived files by type
            console.print("\n[bold]Archive Summary:[/bold]")
            
            # Group by extension
            by_type = {}
            for file in archived:
                ext = Path(file).suffix.lower()[1:] or 'no extension'
                by_type[ext] = by_type.get(ext, 0) + 1
            
            # Group by folder
            by_folder = {}
            for file in archived:
                folder = str(Path(file).parent)
                if folder == '.':
                    folder = 'Root'
                by_folder[folder] = by_folder.get(folder, 0) + 1
            
            # Display extension summary
            console.print("\n[cyan]Files by type:[/cyan]")
            for ext, count in sorted(by_type.items()):
                console.print(f"📄 .{ext}: {count} files")
            
            # Display folder summary
            console.print("\n[cyan]Files by folder:[/cyan]")
            for folder, count in sorted(by_folder.items()):
                console.print(f"📁 {folder}: {count} files")
        else:
            console.print("[yellow]No files were archived[/yellow]")
    
    def handle_config(self):
        """Handle configuration settings"""
        while True:
            console.clear()
            console.print(Panel("⚙️ [bold]Configuration Settings[/bold]"))
            
            # Display current settings
            console.print("\n[bold]Current Settings:[/bold]")
            console.print(f"Downloads Path: [cyan]{self.config['downloads_path']}[/cyan]")
            console.print(f"Archive Path: [cyan]{self.config['archive_path']}[/cyan]")
            console.print(f"Minimum Size: [cyan]{self.config['min_size_mb']} MB[/cyan]")
            console.print(f"Maximum Age: [cyan]{self.config['max_age_days']} days[/cyan]")
            console.print(f"Excluded Extensions: [cyan]{', '.join(self.config['exclude_extensions'])}[/cyan]")
            console.print(f"Excluded Folders: [cyan]{', '.join(self.config['exclude_folders'])}[/cyan]")
            
            # Ask what to configure
            console.print("\n[bold]What would you like to configure?[/bold]")
            console.print("1. Downloads Path")
            console.print("2. Archive Path")
            console.print("3. Minimum File Size")
            console.print("4. Maximum File Age")
            console.print("5. Exclusion Settings")
            console.print("6. Back to Main Menu")
            
            choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "6":
                break
                
            if choice == "1":
                new_path = Prompt.ask("Enter new Downloads path", default=self.config['downloads_path'])
                path = Path(new_path)
                if path.exists() and path.is_dir():
                    self.config.update({"downloads_path": str(path)})
                    console.print(f"[green]Downloads path updated to: {path}[/green]")
                else:
                    console.print(f"[red]Path does not exist: {path}[/red]")
            
            elif choice == "2":
                new_path = Prompt.ask("Enter new Archive path", default=self.config['archive_path'])
                path = Path(new_path)
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self.config.update({"archive_path": str(path)})
                    console.print(f"[green]Archive path updated to: {path}[/green]")
                except Exception as e:
                    console.print(f"[red]Failed to create archive path: {e}[/red]")
            
            elif choice == "3":
                new_size = Prompt.ask("Enter minimum file size in MB", default=str(self.config['min_size_mb']))
                try:
                    size = float(new_size)
                    self.config.update({"min_size_mb": size})
                    console.print(f"[green]Minimum file size updated to: {size} MB[/green]")
                except ValueError:
                    console.print("[red]Invalid size. Please enter a number.[/red]")
            
            elif choice == "4":
                new_age = Prompt.ask("Enter maximum file age in days", default=str(self.config['max_age_days']))
                try:
                    age = int(new_age)
                    self.config.update({"max_age_days": age})
                    console.print(f"[green]Maximum file age updated to: {age} days[/green]")
                except ValueError:
                    console.print("[red]Invalid age. Please enter a number.[/red]")
            
            elif choice == "5":
                # Create submenu for exclusion settings
                console.clear()
                console.print(Panel("[bold]Exclusion Settings[/bold]"))
                console.print("\n[bold]Current Exclusions:[/bold]")
                console.print(f"File Extensions: [cyan]{', '.join(self.config['exclude_extensions'])}[/cyan]")
                console.print(f"Folders: [cyan]{', '.join(self.config['exclude_folders'])}[/cyan]")
                
                console.print("\n[bold]What would you like to configure?[/bold]")
                console.print("1. Excluded File Extensions")
                console.print("2. Excluded Folders")
                console.print("3. Back to Main Settings")
                
                sub_choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3"])
                
                if sub_choice == "1":
                    current_exts = ", ".join(self.config['exclude_extensions'])
                    console.print("\n[bold]Exclude files with these extensions:[/bold]")
                    console.print("[dim]Examples: zip, exe, mp4[/dim]")
                    new_exts = Prompt.ask("Enter excluded extensions (comma-separated)", default=current_exts)
                    extensions = [ext.strip().lower() for ext in new_exts.split(',') if ext.strip()]
                    self.config.update({"exclude_extensions": extensions})
                    console.print(f"[green]Excluded extensions updated to: {', '.join(extensions)}[/green]")
                
                elif sub_choice == "2":
                    current_folders = ", ".join(self.config['exclude_folders'])
                    console.print("\n[bold]Exclude these folders from scanning:[/bold]")
                    console.print("[dim]Examples: node_modules, .git, venv[/dim]")
                    console.print("[dim]Note: This will exclude these folders at any level in the directory tree[/dim]")
                    new_folders = Prompt.ask("Enter excluded folders (comma-separated)", default=current_folders)
                    folders = [folder.strip() for folder in new_folders.split(',') if folder.strip()]
                    self.config.update({"exclude_folders": folders})
                    console.print(f"[green]Excluded folders updated to: {', '.join(folders)}[/green]")
            
            # Pause to show the result before refreshing the menu
            if choice != "6":
                input("\nPress Enter to continue...") 