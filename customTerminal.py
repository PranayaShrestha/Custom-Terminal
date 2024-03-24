import cmd
import os
from PIL import Image


class CustomTerminal(cmd.Cmd):
    intro = "Welcome to Custom Terminal. Type 'help' to list commands."
    prompt = "(Custom Terminal) >> "

    def do_hello(self, arg):
        """Prints a greeting."""
        print("Hello, how can I help you?")

    def do_get_this_img(self, arg):
        """Opens and displays the specified image file."""
        if not arg:
            print("Please provide a file name.")
            return

        # List of directories to search for the file
        search_directories = ["", os.path.expanduser("~")]

        # Search for the file in each directory
        found = False
        for directory in search_directories:
            file_path = os.path.join(directory, arg)
            if os.path.exists(file_path):
                try:
                    # Check if the file is an image file
                    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        # Open and display the image
                        img = Image.open(file_path)
                        img.show()
                        found = True
                        break
                    else:
                        print("File is not an image file.")
                        return
                except Exception as e:
                    print(f"Error: {e}")

        if not found:
            print("File not found.")

    def do_get_this(self, arg):
        """Opens the specified file."""
        if not arg:
            print("Please provide a file name.")
            return

        # List of directories to search for the file
        search_directories = ["", os.path.expanduser("~")]

        # Search for the file in each directory
        found = False
        for directory in search_directories:
            file_path = os.path.join(directory, arg)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as file:
                        print(file.read())
                    found = True
                    break
                except Exception as e:
                    print(f"Error: {e}")

        if not found:
            print("File not found.")

    def do_delete_file(self, arg):
        """Deletes the specified file."""
        if not arg:
            print("Please provide a file name.")
            return

        file_path = os.path.join(os.getcwd(), arg)  # Get the absolute path to the file

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"File '{arg}' deleted successfully.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("File not found.")

    def do_rename_this(self, arg):
        """Renames the specified file."""
        args = arg.split()
        if len(args) != 2:
            print("Usage: rename_this <current_name> <new_name>")
            return

        current_name, new_name = args

        if not current_name or not new_name:
            print("Please provide both current and new names.")
            return

        current_path = os.path.join(os.getcwd(), current_name)  # Get the absolute path to the current file
        new_path = os.path.join(os.getcwd(), new_name)  # Get the absolute path to the new file

        if os.path.exists(current_path):
            try:
                os.rename(current_path, new_path)
                print(f"File '{current_name}' renamed to '{new_name}' successfully.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("File not found.")

    def do_quit(self, arg):
        """Quits the terminal."""
        print("Goodbye!")
        return True


if __name__ == '__main__':
    CustomTerminal().cmdloop()
