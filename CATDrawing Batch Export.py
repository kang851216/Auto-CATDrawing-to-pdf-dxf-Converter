import glob
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from win32com.client import Dispatch

def browse_folder():
    selected_folder = filedialog.askdirectory(title="Select folder containing CATDrawing files")
    if selected_folder:
        folder_var.set(selected_folder)


def append_log(message):
    log_box.config(state="normal")
    log_box.insert("end", f"{message}\n")
    log_box.see("end")
    log_box.config(state="disabled")
    root.update_idletasks()


def export_drawings():
    folder_path = folder_var.get().strip()
    export_format = format_var.get().strip().lower()

    if not folder_path:
        messagebox.showerror("Missing Folder", "Select a folder that contains CATDrawing files.")
        return

    if not os.path.isdir(folder_path):
        messagebox.showerror("Invalid Folder", "The selected folder does not exist.")
        return

    pattern = os.path.join(folder_path, "*.CATDrawing")
    drawing_files = sorted(glob.glob(pattern))

    if not drawing_files:
        messagebox.showinfo("No Files Found", "No CATDrawing files were found in the selected folder.")
        return

    append_log(f"Detected {len(drawing_files)} CATDrawing file(s) in {folder_path}")

    try:
        catia = Dispatch("CATIA.Application")
    except Exception as error:
        messagebox.showerror("CATIA Error", f"Could not connect to CATIA.\n\n{error}")
        return

    success_count = 0
    failed_files = []
    export_button.config(state="disabled")
    status_var.set(f"Starting export to {export_format.upper()}...")
    append_log(f"Starting batch export as {export_format.upper()}")

    try:
        for drawing_file in drawing_files:
            base_name = os.path.splitext(drawing_file)[0]
            output_file = f"{base_name}.{export_format}"
            doc = None

            try:
                status_var.set(f"Exporting {os.path.basename(drawing_file)}...")
                append_log(f"Opening {os.path.basename(drawing_file)}")
                doc = catia.Documents.Open(drawing_file)
                doc.ExportData(output_file, export_format)
                time.sleep(1)
                success_count += 1
                append_log(f"Saved {os.path.basename(output_file)}")
            except Exception as error:
                failure_message = f"{os.path.basename(drawing_file)}: {error}"
                failed_files.append(failure_message)
                append_log(f"Failed {failure_message}")
            finally:
                if doc is not None:
                    try:
                        doc.Close()
                    except Exception:
                        pass
    finally:
        export_button.config(state="normal")

    if failed_files:
        status_var.set("Completed with errors.")
        append_log(
            f"Finished with errors. Exported {success_count} of {len(drawing_files)} file(s)."
        )
        messagebox.showwarning(
            "Export Finished",
            f"Exported {success_count} of {len(drawing_files)} files as {export_format.upper()}.\n\n"
            + "Failed files:\n"
            + "\n".join(failed_files),
        )
    else:
        status_var.set("Export completed successfully.")
        append_log(f"Finished successfully. Exported {success_count} file(s).")
        messagebox.showinfo(
            "Export Finished",
            f"Exported {success_count} CATDrawing files as {export_format.upper()}.",
        )


root = tk.Tk()
root.title("CATDrawing Batch Export")
root.geometry("860x620")

folder_var = tk.StringVar()
format_var = tk.StringVar(value="pdf")
status_var = tk.StringVar(value="Select a folder and export format.")

main_frame = tk.Frame(root, padx=12, pady=12)
main_frame.pack(fill="both", expand=True)

explanation_text = (
    "1. This script exports CATDrawing files in bulk from a selected folder.\n"
    "2. Select the folder that contains the target CATDrawing file(s).\n"
    "3. Choose one export format: PDF or DXF.\n"
    "4. Click 'Export Files' to process every CATDrawing file in that folder.\n"
    "5. The exported file is saved in the same folder with the same file name as the CATDrawing file.\n"
    "6. Run CATIA before starting. Warning or error messages from CATIA may appear during export.\n"
    "7. Review the log window at the bottom for progress and any failed files."
)
explanation_label = tk.Label(
    main_frame,
    text=explanation_text,
    justify="left",
    anchor="w",
    wraplength=810,
    bg="#f3f3f3",
    relief="groove",
    padx=10,
    pady=10,
)
explanation_label.grid(row=0, column=0, columnspan=3, sticky="we", pady=(0, 12))


def add_row(row, label, variable, browse_command=None):
    tk.Label(main_frame, text=label, anchor="w").grid(row=row, column=0, sticky="w", pady=4)
    tk.Entry(main_frame, textvariable=variable, width=70).grid(row=row, column=1, sticky="we", pady=4)
    if browse_command:
        tk.Button(main_frame, text="Browse", command=browse_command).grid(row=row, column=2, padx=6)


add_row(1, "Drawing folder", folder_var, browse_folder)

tk.Label(main_frame, text="Export format", anchor="w").grid(row=2, column=0, sticky="w", pady=4)
options_frame = tk.Frame(main_frame)
options_frame.grid(row=2, column=1, sticky="w", pady=4)
tk.Radiobutton(options_frame, text="PDF", variable=format_var, value="pdf").grid(row=0, column=0, padx=(0, 16))
tk.Radiobutton(options_frame, text="DXF", variable=format_var, value="dxf").grid(row=0, column=1)

export_button = tk.Button(main_frame, text="Export Files", width=16, command=export_drawings)
export_button.grid(row=3, column=0, pady=6, sticky="w")

tk.Label(main_frame, textvariable=status_var, anchor="w").grid(row=4, column=0, columnspan=3, sticky="we", pady=(0, 6))

log_box = tk.Text(main_frame, height=12, width=95, state="disabled")
log_box.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(5, weight=1)

root.mainloop()