import sys
import os
import zipfile
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QTextEdit, QLabel
)
from PyQt6.QtCore import Qt


class AssetZipper(QWidget):
    def __init__(self):
        super().__init__()
        self.input_folder = ""
        self.output_folder = "asset-zip"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Asset Zipper by @mujib_banget')
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        layout = QVBoxLayout()

        # Input folder selection
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel('No folder selected')
        self.select_folder_btn = QPushButton('Select Input Folder')
        self.select_folder_btn.clicked.connect(self.select_input_folder)
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.select_folder_btn)
        layout.addLayout(folder_layout)

        # Process button
        self.process_btn = QPushButton('Process Files')
        self.process_btn.clicked.connect(self.process_files)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)

        # Output folder button (initially hidden)
        self.open_output_btn = QPushButton('Buka Folder Output')
        self.open_output_btn.clicked.connect(self.open_output_folder)
        self.open_output_btn.setVisible(False)
        layout.addWidget(self.open_output_btn)

        # Status display
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        layout.addWidget(self.status_display)

        self.setLayout(layout)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder')
        if folder:
            self.input_folder = folder
            self.folder_label.setText(f'Selected: {os.path.basename(folder)}')
            self.process_btn.setEnabled(True)
            self.status_display.append(f"Input folder selected: {folder}")

    def process_files(self):
        if not self.input_folder:
            self.status_display.append("Please select an input folder first.")
            return

        # Create output folder inside input folder if it doesn't exist
        output_path = Path(self.input_folder) / self.output_folder
        output_path.mkdir(exist_ok=True)

        # Get all files in input folder
        input_path = Path(self.input_folder)
        files = list(input_path.iterdir())

        # Group files by name (without extension)
        file_groups = {}
        for file in files:
            if file.is_file():
                name_without_ext = file.stem
                if name_without_ext not in file_groups:
                    file_groups[name_without_ext] = []
                file_groups[name_without_ext].append(file)

        # Process each group
        zipped_count = 0
        for name, file_list in file_groups.items():
            if len(file_list) > 1:
                # Create zip file for this group
                zip_filename = f"{name}.zip"
                zip_filepath = output_path / zip_filename

                with zipfile.ZipFile(zip_filepath, 'w') as zipf:
                    for file in file_list:
                        zipf.write(file, file.name)

                zipped_count += 1
                self.status_display.append(f"Zipped {len(file_list)} files with name '{name}'")

        self.status_display.append(f"Process completed. {zipped_count} groups zipped.")
        self.open_output_btn.setVisible(True)

    def open_output_folder(self):
        # Open folder in system file browser
        output_folder_path = Path(self.input_folder) / self.output_folder
        os.system(f"open '{output_folder_path}'")


def main():
    app = QApplication(sys.argv)
    window = AssetZipper()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
