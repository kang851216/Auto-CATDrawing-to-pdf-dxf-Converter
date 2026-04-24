# Auto CATDrawing to PDF/DXF Converter

A Windows desktop GUI tool that batch-exports CATIA `.CATDrawing` files to **PDF** or **DXF** format using the CATIA COM automation API.

## Features

- Select any folder containing `.CATDrawing` files
- Export all drawings in one click — PDF or DXF
- Exported files are saved alongside the originals with the same filename
- Live log window shows per-file progress and any errors
- Skips and reports failed files without stopping the entire batch

## Requirements

- Windows OS
- CATIA V5 installed and licensed (must be running before export)
- Python 3.8+
- See [requirements.txt](requirements.txt) for Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Launch CATIA and ensure it is open and ready.
2. Run the script or exe file(on Windows only):
   ```bash
   python "CATDrawing Batch Export.py"
   ```
3. Click **Browse** and select the folder containing your `.CATDrawing` files.
4. Choose an export format: **PDF** or **DXF**.
5. Click **Export Files**.
6. Monitor the log window for progress. Exported files appear in the same folder as the originals.

## Notes

- CATIA warning or confirmation dialogs may appear during export — dismiss them manually if needed.
- The tool opens each drawing, exports it, then closes it before moving to the next file.
- A 1-second delay is applied after each export to allow CATIA to finish writing the file.

## Project Structure

```
Auto CATDrawing-to-PDFDXF Converter/
├── Auto CATIA drawing pdf or dwg saver.py   # Main application
├── requirements.txt
├── README.md
└── CATfile/                                 # Sample/test CATDrawing files
```

## License

MIT
