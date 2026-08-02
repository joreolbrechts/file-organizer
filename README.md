# File Organizer 

A Python command-line tool that automatically sorts files in a folder
into subfolders, based on file type and/or modification date.

## Features
- Sort by type (Images, Documents, Code, Audio, Video, Archives, ...)
- Sort by date (year-month of last modification)
- Combine both (type/date)
- Dry-run mode: preview what would happen without moving anything
- Prevents overwriting files with the same name
- No external dependencies (Python standard library only)

## Usage

```bash
python organizer.py <folder> [--by type|date|both] [--dry-run]
```

### Examples

Sort by file type:
```bash
python organizer.py ~/Downloads
```

Sort by date:
```bash
python organizer.py ~/Downloads --by date
```

Sort by type and date, preview first:
```bash
python organizer.py ~/Downloads --by both --dry-run
```

## Supported categories

| Category | Extensions |
|---|---|
| Images | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .heic |
| Documents | .pdf, .doc, .docx, .txt, .odt, .rtf, .md |
| Spreadsheets | .xls, .xlsx, .csv, .ods |
| Presentations | .ppt, .pptx, .odp |
| Audio | .mp3, .wav, .flac, .aac, .m4a |
| Video | .mp4, .mov, .avi, .mkv, .webm |
| Archives | .zip, .rar, .7z, .tar, .gz |
| Code | .py, .java, .js, .html, .css, .c, .cpp, .ipynb, .json, .sh |
| Executables | .exe, .msi, .app, .dmg |
| Other | anything not recognized |

## Requirements
- Python 3.6+
- No external packages needed

## Possible extensions
- Configurable categories via a JSON file
- Recursive sorting into subfolders
- GUI version with tkinter
