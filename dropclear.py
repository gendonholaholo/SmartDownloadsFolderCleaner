from src.utils.config import Config
from src.cli.commands import CommandHandler
from rich.console import Console

console = Console()

def main():
    try:
        config = Config()
        handler = CommandHandler(config.config)
        
        while True:
            choice = handler.menu.display_main_menu()
            
            if choice == "1":
                handler.handle_scan()
            elif choice == "2":
                handler.handle_clean()
            elif choice == "3":
                handler.handle_archive()
            elif choice == "4":
                handler.handle_config()
            elif choice == "5":
                console.print("[cyan]Thank you for using DropClear![/cyan]")
                break
            
            input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        console.print("\n[cyan]Goodbye![/cyan]")
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    main() 