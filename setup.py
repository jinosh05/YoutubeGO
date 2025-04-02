import os

folders = [
    "core",
    "ui",
    "assets"
]

files = {
    "core": ["downloader.py", "profile.py", "utils.py", "history.py", "__init__.py"],
    "ui": ["main_window.py", "__init__.py"],
    "assets": [],
    "": ["requirements.txt", "README.md", "LICENSE", "history.json", "main.py"]
}

base_dir = os.getcwd()

for folder in folders:
    path = os.path.join(base_dir, folder)
    os.makedirs(path, exist_ok=True)
    print(f"Created folder: {folder}")

for folder, file_list in files.items():
    for file in file_list:
        path = os.path.join(base_dir, folder, file)
        with open(path, "w", encoding="utf-8") as f:
            if file.endswith(".py"):
                f.write("# Auto-generated file\n")
        print(f"Created file: {os.path.join(folder, file)}")

print("\n✅ Project structure ready. Now go make some magic!")
