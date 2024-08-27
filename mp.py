"""
mp -i ./demo.md
basic features ->
it will take the file path as the command line argument and
watch this file for changes and then it will re-render the webpage
"""

import os
import sys
import typing
import markdown
import argparse

from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeyEvent, QCloseEvent
from PyQt5.QtCore import Qt, QFileSystemWatcher, pyqtSlot

DEFAULT_STYLE = """
				<style>
					body {
						background-color: #272828;
						padding: 16px;
						font-family: system-ui;
						color: white;
					}
					h1 {
						font-weight: bold;
					}
				</style>
				"""

class MarkDownPreview(QMainWindow):
	def __init__(self) -> None:
		super().__init__()

		self.args: argparse.Namespace = self.__init_parser().parse_args()
		self.file_to_watch: typing.Optional[str] = self.args.input[0] if self.args.input else None

		exists = os.path.exists(os.path.abspath(self.file_to_watch if self.file_to_watch is not None else '').replace("~",""))
		if (self.file_to_watch is None or not exists):
			print("file not found")
			sys.exit()

		self.setWindowTitle("Markdown Preview")

		self.file_watcher  = QFileSystemWatcher([self.file_to_watch])
		self.file_watcher.fileChanged.connect(self.on_file_change)

		self.view: QWebEngineView = QWebEngineView()

		self.setCentralWidget(self.view)

		self._load_html()

	def __init_parser(self) -> argparse.ArgumentParser:
		self.parser = argparse.ArgumentParser(description="quick markdown preview")
		self.parser.add_argument('-i', '--input', nargs=1, help='file input')
		return self.parser

	def _load_html(self) ->None:
		if self.file_to_watch is not None:
			with open(self.file_to_watch, 'r') as f:
				html = markdown.markdown(f.read())
				self.view.setHtml(html+DEFAULT_STYLE)

	def keyPressEvent(self, a0) -> None:
		if a0 is not None:
			key = a0.key()
			if key == 82: # r key
				self._load_html()

		return super().keyPressEvent(a0)

	@pyqtSlot()
	def on_file_change(self) -> None:
		if self.file_to_watch is not None:
			with open(self.file_to_watch, 'r') as f:
				html = markdown.markdown(f.read())
				if html is not None and len(html) > 0:
					self.view.setHtml(html+DEFAULT_STYLE)

	def closeEvent(self, a0: typing.Optional[QCloseEvent]) -> None:
		if a0 is not None:
			if self.file_watcher is not None:
				self.file_watcher.fileChanged.disconnect(self.on_file_change)
				self.file_watcher.removePath(self.file_to_watch)
				self.file_watcher = None

			a0.accept()

		return super().closeEvent(a0)


if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MarkDownPreview()
	window.show()

	sys.exit(app.exec())
