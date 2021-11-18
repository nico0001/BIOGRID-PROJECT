from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys


# Tuto pour avoir une bonne base de notre GUI : 
# https://soniakopel.wordpress.com/2017/11/15/network-visualization-with-networkx-tutorial/
# https://towardsdatascience.com/python-interactive-network-visualization-using-networkx-plotly-and-dash-e44749161ed7


def window_screen():
    app = QApplication(sys.argv)
    screen= QMainWindow()
    screen.setGeometry(200,200,300,300)
    screen.setWindowTitle("BIOGRID PROJECT")

    label = QtWidgets.QLabel(screen)
    label.setText("Exemple de label")
    label.move(50,50)

    screen.show()
    sys.exit(app.exec_())


window_screen()
