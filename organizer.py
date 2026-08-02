import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime

EXTENSION_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".js", ".html", ".css", ".c", ".cpp", ".ipynb", ".json", ".sh"],
    "Executables": [".exe", ".msi", ".app", ".dmg"],
}


def get_category(extension):
    extension = extension.lower()
    for category, extensions in EXTENSION_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def get_date_folder(file_path):
    timestamp = file_path.stat().st_mtime
    date = datetime.fromtimestamp(timestamp)
    return date.strftime("%Y-%m")


def build_destination(file_path, base_dir, mode):
    if mode == "type":
        subfolder = get_category(file_path.suffix)
        return base_dir / subfolder
    elif mode == "date":
        subfolder = get_date_folder(file_path)
        return base_dir / subfolder
    elif mode == "both":
        category = get_category(file_path.suffix)
        date_folder = get_date_folder(file_path)
        return base_dir / category / date_folder
    else:
        raise ValueError(f"Unknown mode: {mode}")


def organize_folder(target_dir, mode="type", dry_run=False):
    base_dir = Path(target_dir).expanduser().resolve()

    if not base_dir.exists() or not base_dir.is_dir():
        print(f"Error: '{base_dir}' does not exist or is not a directory.")
        sys.exit(1)

    files = [f for f in base_dir.iterdir() if f.is_file()]

    if not files:
        print("No files found to organize.")
        return

    moved_count = 0
    skipped_count = 0

    for file_path in files:
        if file_path.name.startswith("."):
            continue

        destination_folder = build_destination(file_path, base_dir, mode)
        destination_path = destination_folder / file_path.name

        if destination_path.exists():
            counter = 1
            stem, suffix = file_path.stem, file_path.suffix
            while destination_path.exists():
                destination_path = destination_folder / f"{stem} ({counter}){suffix}"
                counter += 1

        if dry_run:
            print(f"[DRY-RUN] {file_path.name} -> {destination_folder.relative_to(base_dir)}/")
            moved_count += 1
            continue

        try:
            destination_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(destination_path))
            print(f"Moved: {file_path.name} -> {destination_folder.relative_to(base_dir)}/")
            moved_count += 1
        except Exception as e:
            print(f"Could not move '{file_path.name}': {e}")
            skipped_count += 1

    print("\n--- Summary ---")
    print(f"Processed: {moved_count} file(s)")
    if skipped_count:
        print(f"Skipped (errors): {skipped_count} file(s)")
    if dry_run:
        print("(This was a dry run: nothing was actually moved.)")


def main():
    parser = argparse.ArgumentParser(
        description="Automatically sorts files in a folder by type and/or date."
    )
    parser.add_argument("directory", help="Path to the folder you want to organize")
    parser.add_argument(
        "--by",
        choices=["type", "date", "both"],
        default="type",
        help="Sorting criterion: type (default), date, or both",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without actually moving files",
    )

    args = parser.parse_args()
    organize_folder(args.directory, mode=args.by, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
