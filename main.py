import sys
from openai import OpenAI
import requests
import markdown
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget


class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programmer's Assistant")
        self.setGeometry(100, 100, 600, 400)


        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter your programming question here...")
        layout.addWidget(self.input_field)

        send_button = QPushButton("Send", self)
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        central_widget.setLayout(layout)

    def send_message(self):

        user_input = self.input_field.text().strip()
        if not user_input:
            return

        self.chat_display.append(f"You: {user_input}")

        self.input_field.clear()

        response = self.get_qwen_response(user_input)

        html_response = markdown.markdown(response)
        self.chat_display.append(f"Qwen: {html_response}")

    def get_qwen_response(self, prompt):
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key="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",
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
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())