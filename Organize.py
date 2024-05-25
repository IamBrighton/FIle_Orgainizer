import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil

class FileOrganizerApp:
    def __init__(self, master):
        self.master = master
        master.title('File Organizer')

        # Title Label
        self.title_label = ttk.Label(master, text="File Organizer", font=("Helvetica", 16, "bold"))
        self.title_label.pack(anchor="n", pady=10)

        # Frame for buttons
        self.button_frame = ttk.Frame(master)
        self.button_frame.pack(anchor="center", pady=20)

        # Button to select the folder to organize
        self.select_folder_button = ttk.Button(self.button_frame, text="Select Folder", command=self.select_folder)
        self.select_folder_button.grid(row=0, column=0, padx=10)

        # Button to start the file organization
        self.organize_button = ttk.Button(self.button_frame, text="Organize Files", command=self.organize_files)
        self.organize_button.grid(row=0, column=1, padx=10)

        # Status Label
        self.status_label = ttk.Label(master, text="Please select a folder to organize.", font=("Helvetica", 10))
        self.status_label.pack(anchor="s", pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(anchor="s", pady=10)

        # Help Button
        self.help_button = ttk.Button(master, text="Help", command=self.show_help)
        self.help_button.pack(anchor="s", pady=10)

        # Done Button
        self.done_button = ttk.Button(master, text="Done", command=self.close_app)
        self.done_button.pack(anchor="s", pady=10)

    def select_folder(self):
        # Opens a dialog to select a folder
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.status_label.config(text=f"Selected Folder: {self.folder_path}")
        else:
            self.status_label.config(text="Folder selection cancelled.")

    def organize_files(self):
        # Checks if a folder has been selected
        if hasattr(self, 'folder_path') and self.folder_path:
            self.organize_files_by_format()
        else:
            messagebox.showwarning("Warning", "Please select a folder first.")

    def organize_files_by_format(self):
        # File formats and their corresponding folders
        file_formats = {
            "PDF": [".pdf", ".docx"],
            "Music": [".mp3", ".wav", ".ogg", ".m4a"],
            "Videos": [".mp4", ".avi", ".mkv"],
            "Applications": [".exe", ".msi"],
            "Shortcuts": [".lnk"]
        }

        try:
            files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
            total_files = len(files)
            self.progress["value"] = 0
            self.progress["maximum"] = total_files

            # Create folders for each file format and move files accordingly
            for i, file in enumerate(files):
                file_path = os.path.join(self.folder_path, file)
                file_name, file_ext = os.path.splitext(file)
                for folder_name, extensions in file_formats.items():
                    if file_ext.lower() in extensions:
                        folder_path = os.path.join(self.folder_path, folder_name)
                        os.makedirs(folder_path, exist_ok=True)
                        dest_path = os.path.join(folder_path, file)
                        shutil.move(file_path, dest_path)
                        print(f"Moved: {file} to {folder_name}")
                        break
                self.progress["value"] = i + 1
                self.master.update_idletasks()

            self.status_label.config(text="Files organized successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_help(self):
        help_message = (
            "To use the File Organizer:\n"
            "1. Click 'Select Folder' to choose the folder you want to organize.\n"
            "2. Click 'Organize Files' to start organizing the files by format.\n"
            "3. The files will be moved to respective folders based on their formats."
        )
        messagebox.showinfo("Help", help_message)

    def close_app(self):
        # Closes the application
        self.master.destroy()

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.geometry("400x400")
    root.mainloop()

if __name__ == "__main__":
    main()
