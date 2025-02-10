import sys
from openai import OpenAI
import requests
import markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QThread, pyqtSignal


class ApiWorker(QThread):
    """
    worker thread to handle API requests in the back.
    """
    response_ready = pyqtSignal(str)  # Signal to emit the response
    error_occurred = pyqtSignal(str)  # Signal to emit errors

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",

            )
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>",
                    "X-Title": "<YOUR_SITE_NAME>",
                },
                model="qwen/qwen-plus",
                messages=[
                    {
                        "role": "user",
                        "content": self.prompt
                    }
                ]
            )
            response = completion.choices[0].message.content
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))


class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensei")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 12))
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter your program question here...")
        self.input_field.setFont(QFont("Arial", 12))
        # Connect the returnPressed signal to send_message
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field)

        send_button = QPushButton("Send", self)
        send_button.setFont(QFont("Arial", 12))
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        central_widget.setLayout(layout)

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        self.append_message("U", user_input, "#4CAF5080", "right")

        self.input_field.clear()

        self.typing_placeholder = self.append_typing_placeholder()

        # API worker thread
        self.api_worker = ApiWorker(user_input)
        self.api_worker.response_ready.connect(self.handle_response)
        self.api_worker.error_occurred.connect(self.handle_error)
        self.api_worker.finished.connect(self.remove_typing_placeholder)
        self.api_worker.start()

    def append_typing_placeholder(self):
        placeholder = (
            '<div style="display: flex; justify-content: left; margin: 8px;">'
            '  <div style="background-color: #42A5F580; border-radius: 16px; padding: 8px 16px; max-width: 50%; word-wrap: break-word;">'  # Semi-transparent blue
            '    <b>Qwen:</b> Typing...'
            '  </div>'
            '</div>'
        )
        self.chat_display.append(placeholder)
        return placeholder

    def handle_response(self, response):

        html_response = markdown.markdown(response)
        self.append_message("Qwen", html_response, "#42A5F580", "left")

    def handle_error(self, error_message):

        self.append_message("Error", f"Failed to fetch response: {error_message}", "#FF525280", "left")  # Semi-transparent red

    def remove_typing_placeholder(self):

        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        if cursor.selectedText().strip() == "Typing...":
            cursor.removeSelectedText()
            cursor.deletePreviousChar()
        self.chat_display.setTextCursor(cursor)

        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def append_message(self, sender, message, color, align):
        """
        appends a styled msg to the chat display.
        :param sender: The sender's name (e.g., "You" or "Qwen").
        :param message: The msg content.
        :param color: The back color of the msg tile (e.g., "#4CAF5080" for semi-transparent green).
        :param align: The alignment of the msg ("left" or "right").
        """
        html_message = (
            f'<div style="display: flex; justify-content: {align}; margin: 8px;">'
            f'  <div style="background-color: {color}; border-radius: 16px; padding: 8px 16px; max-width: 50%; word-wrap: break-word;">'
            f'    <b>{sender}:</b> {message}'
            f'  </div>'
            f'</div>'
        )
        self.chat_display.append(html_message)

    def apply_dark_theme(self):
        dark_theme = """
        QMainWindow {
            background-color: #2B2B2B;
            color: #FFFFFF;
        }
        QTextEdit {
            background-color: #3C3F41;
            color: #FFFFFF;
            border: 1px solid #444444;
            border-radius: 8px;
            padding: 8px;
        }
        QLineEdit {
            background-color: #3C3F41;
            color: #FFFFFF;
            border: 1px solid #444444;
            border-radius: 8px;
            padding: 8px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
        }
        QPushButton:hover {
            background-color: #45A049;
        }
        QPushButton:pressed {
            background-color: #3E8E41;
        }
        """
        self.setStyleSheet(dark_theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.setWindowIcon(QIcon("icon.png"))
    chat_app.show()
    sys.exit(app.exec_())