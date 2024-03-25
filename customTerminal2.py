import cmd
import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable, Optional, Union
from PIL import Image

class CustomTerminal(cmd.Cmd):
    intro = "Welcome to Custom Terminal. Type 'help' to list commands."
    prompt = "(Custom Terminal) >> "

    def do_hello(self, _: str) -> None:
        """Prints a greeting."""
        print("Hello, how can I help you?")

    def do_get_this_img(self, arg: str) -> None:
        """Opens and displays the specified image file."""
        self._handle_file(arg, self._display_image)

    def do_get_this(self, arg: str) -> None:
        """Opens the specified file."""
        self._handle_file(arg, self._print_file_contents)

    def do_delete_file(self, arg: str) -> None:
        """Deletes the specified file."""
        self._handle_file(arg, self._delete_file)

    def do_rename_this(self, arg: str) -> None:
        """Renames the specified file."""
        args = arg.split()
        if len(args) != 2:
            print("Usage: rename_this <current_name> <new_name>")
            return

        current_name, new_name = args
        current_path = Path.cwd() / current_name
        new_path = Path.cwd() / new_name

        if current_path.exists():
            try:
                current_path.rename(new_path)
                print(f"File '{current_name}' renamed to '{new_name}' successfully.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("File not found.")

    def do_make_this(self, arg: str) -> None:
        """Creates a new directory."""
        new_dir = Path.cwd() / arg
        try:
            new_dir.mkdir(exist_ok=True)
            print(f"Directory '{arg}' created successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def do_list_all(self, arg: str) -> None:
        """Lists files and directories in the current or specified directory."""
        directory = Path.cwd() if not arg else Path(arg)
        if directory.exists() and directory.is_dir():
            for item in sorted(directory.iterdir()):
                if item.is_dir():
                    print(f"{item.name}/")
                else:
                    print(item.name)
        else:
            print(f"Directory '{arg}' not found.")

    def do_change(self, arg: str) -> None:
        """Changes the current working directory."""
        try:
            os.chdir(arg)
            print(f"Current working directory changed to '{os.getcwd()}'")
        except FileNotFoundError:
            print(f"Directory '{arg}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_copy_this(self, arg: str) -> None:
        """Copies a file from one location to another."""
        args = arg.split()
        if len(args) != 2:
            print("Usage: copy <source_file> <destination_file>")
            return

        source, destination = args
        source_path = Path(source)
        destination_path = Path(destination)

        if source_path.exists():
            try:
                shutil.copy(source_path, destination_path)
                print(f"File '{source}' copied to '{destination}'")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"Source file '{source}' not found.")

    def do_move_this (self, arg: str) -> None:
        """Moves a file or directory from one location to another."""
        args = arg.split()
        if len(args) != 2:
            print("Usage: move <source> <destination>")
            return

        source, destination = args
        source_path = Path(source)
        destination_path = Path(destination)

        if source_path.exists():
            try:
                shutil.move(source_path, destination_path)
                print(f"'{source}' moved to '{destination}'")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"Source '{source}' not found.")

    def do_shell(self, arg: str) -> None:
        """Runs a command in the system shell."""
        try:
            subprocess.run(arg, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command returned non-zero exit status: {e.returncode}")
        except Exception as e:
            print(f"Error: {e}")

    def do_quit(self, _: str) -> bool:
        """Quits the terminal."""
        print("Goodbye!")
        return True

    def _handle_file(self, filename: str, callback: Callable[[Path], Optional[Union[str, None]]]) -> None:
        """Searches for a file and handles it using the provided callback function."""
        search_directories = [Path.cwd(), Path.home()]
        for directory in search_directories:
            file_path = directory / filename
            if file_path.exists():
                result = callback(file_path)
                if result is not None:
                    print(result)
                return

        print("File not found.")

    def _display_image(self, file_path: Path) -> None:
        """Opens and displays the specified image file."""
        if file_path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.bmp'):
            try:
                img = Image.open(file_path)
                img.show()
            except Exception as e:
                return f"Error: {e}"
        else:
            return "File is not an image file."

    def _print_file_contents(self, file_path: Path) -> str:
        """Opens and prints the contents of the specified file."""
        try:
            with file_path.open('r') as file:
                return file.read()
        except Exception as e:
            return f"Error: {e}"

    def _delete_file(self, file_path: Path) -> Optional[str]:
        """Deletes the specified file."""
        try:
            file_path.unlink()
            return f"File '{file_path.name}' deleted successfully."
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    CustomTerminal().cmdloop()