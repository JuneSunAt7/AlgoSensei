import sys
from PyQt5 import QtWidgets, QtCore
import markdown
import time
import widget, ai_setup


class SenseiApp(QtWidgets.QWidget, widget.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_msg)

    def add_msg(self):
        try:
            user_input = self.textBrowser.toPlainText().strip()
            if not user_input:
                return
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight)
            item.setText(f" (U):\n{user_input}")
            self.listWidget.addItem(item)
            time.sleep(2)


            markdown_answ = ai_setup.ai_question(user_input)
            # html_string = markdown.markdown(markdown_answ)


            answ_item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            answ_item.setText(f"QWEN: \n{markdown_answ}")
            self.listWidget.addItem(answ_item)

            self.textBrowser.clear()
        except Exception as e:
            print(f"Error occurred: {e}")
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SenseiApp()
    window.show()
    window.setWindowOpacity(0.8)
    window.setWindowTitle("AlgoSensei")
    window.setFixedSize(611, 681)
    app.exec_()


if __name__ == '__main__':
    main()
