from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyPDF2 import PdfFileMerger

__author__ = "Shovra Das"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)

        # Controls
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Signals
        self.addButton.clicked.connect(self.addButton_clicked)
        self.removeButton.clicked.connect(self.removeButton_clicked)
        self.mergeButton.clicked.connect(self.mergeButton_clicked)
        self.clearButton.clicked.connect(lambda: self.fileListWidget.clear())
        self.outputDirectoryButton.clicked.connect(self.outputDirectoryButton_clicked)

        # Actions        
        self.actionExit.triggered.connect(lambda: exit())

        # Initializations
        self.outputDirectoryLineEdit.setText(str(Path.home()))

    def addButton_clicked(self):
        dialog = QFileDialog()        
        dialog.setFileMode(QFileDialog.ExistingFiles)
        # dialog.setFilter("PDF files (*.pdf)")
        if dialog.exec_():
            files = dialog.selectedFiles()
            
            # Checking if same file is selected intentionally or not
            duplicate_files = []
            for i, file in enumerate(files, 1):
                if self.fileListWidget.findItems(file, Qt.MatchExactly):
                    duplicate_files.append(f'{i}. {file}')
            if duplicate_files:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Confirm")
                msg.setText("One or more file(s) in your selection already exists")
                msg.setInformativeText("Do you still want to proceed?")            
                msg.setDetailedText('Duplicate files: \n' + '\n'.join(duplicate_files))
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                reply = msg.exec_()
                if reply==QMessageBox.Cancel:
                    return

            self.fileListWidget.addItems(files)

    def removeButton_clicked(self):
        self.fileListWidget.takeItem(
            self.fileListWidget.row(
                self.fileListWidget.currentItem()
            )
        )
        
    def mergeButton_clicked(self):
        output_file = self.outputFileLineEdit.text()
        if len(output_file) < 5:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Output File name is incorrectly specified")
            msg.exec_()
            return
        if output_file[-4:] != '.pdf':
            output_file += '.pdf'
        output_path = Path(self.outputDirectoryLineEdit.text()) / output_file

        merger = PdfFileMerger()
        for i in range(self.fileListWidget.count()):
            item = self.fileListWidget.item(i)
            merger.append(item.text())        
        merger.write(str(output_path))
        merger.close()

        self.statusBar.showMessage(f'Status: PDF saved at {output_path.as_uri()}')

    def outputDirectoryButton_clicked(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_():
            selected_directory = dialog.selectedFiles()[0]
            self.outputDirectoryLineEdit.setText(selected_directory)


