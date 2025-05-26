from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLabel,
    QComboBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import sys
from convertor import (
    read_json, write_json,
    read_xml, write_xml,
    read_yaml, write_yaml
)


class Worker(QThread):
    """
    Worker thread for asynchronous file conversion
    to prevent GUI freezing during operations
    """
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_file, output_file, output_format):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.output_format = output_format

    def run(self):
        """Main conversion logic executed in separate thread"""
        try:
            self.convert(self.input_file, self.output_file, self.output_format)
            self.finished.emit(self.output_file)
        except Exception as e:
            self.error.emit(str(e))

    def convert(self, input_file: str, output_file: str, output_format: str):
        """Handles actual file format conversion"""
        input_ext = input_file.split('.')[-1].lower()

        if input_ext == 'json':
            data = read_json(input_file)
        elif input_ext in ('yml', 'yaml'):
            data = read_yaml(input_file)
        elif input_ext == 'xml':
            data = read_xml(input_file)
        else:
            raise ValueError("Unsupported input file format")


        if output_format == 'json':
            write_json(data, output_file)
        elif output_format in ('yml', 'yaml'):
            write_yaml(data, output_file)
        elif output_format == 'xml':
            write_xml(data, output_file)
        else:
            raise ValueError("Unsupported output format")


class ConverterApp(QMainWindow):
    """Main application window for the converter GUI"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Converter (JSON/XML/YAML)")
        self.setGeometry(300, 300, 400, 200)
        self.input_file = ""

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        """Initialize all UI components"""
        self.label = QLabel("Select file to convert:", self)
        self.btn_select = QPushButton("Browse File", self)
        self.format_label = QLabel("Select target format:", self)
        self.format_combobox = QComboBox(self)
        self.format_combobox.addItems(["JSON", "XML", "YAML"])
        self.btn_convert = QPushButton("Convert", self)
        self.status_label = QLabel("Ready", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combobox)
        layout.addWidget(self.btn_convert)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def connect_signals(self):
        """Connect buttons to their functions"""
        self.btn_select.clicked.connect(self.select_file)
        self.btn_convert.clicked.connect(self.convert_file)

    def select_file(self):
        """Open file dialog to select input file"""
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "JSON (*.json);;XML (*.xml);;YAML (*.yaml *.yml)"
        )
        if file:
            self.input_file = file
            self.status_label.setText(f"Selected: {file.split('/')[-1]}")

    def convert_file(self):
        """Handle conversion process with thread"""
        if not self.input_file:
            self.status_label.setText("Error: No file selected!")
            return

        output_format = self.format_combobox.currentText().lower()
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save As...",
            "",
            f"{output_format.upper()} (*.{output_format})"
        )

        if output_file:
            self.status_label.setText("Converting...")
            self.worker = Worker(
                self.input_file,
                output_file,
                output_format
            )
            self.worker.finished.connect(
                lambda path: self.status_label.setText(f"Saved: {path.split('/')[-1]}")
            )
            self.worker.error.connect(
                lambda err: self.status_label.setText(f"Error: {err}")
            )
            self.worker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())