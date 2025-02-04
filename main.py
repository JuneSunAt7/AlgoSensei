import sys
from PyQt5 import QtWidgets
import widget


class SenseiApp(QtWidgets.QWidget, widget.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_msg)
    def add_msg(self):




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
