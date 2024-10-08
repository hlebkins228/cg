# Form implementation generated from reading ui file 'ui_files\main_window.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1248, 750)
        MainWindow.setMinimumSize(QtCore.QSize(1245, 750))
        MainWindow.setMaximumSize(QtCore.QSize(1250, 750))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scale_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.scale_button.setGeometry(QtCore.QRect(70, 580, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.scale_button.setFont(font)
        self.scale_button.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(146, 164, 175);\n"
"    border-radius: 10px;\n"
"    border: 2px solid rgb(115, 138, 153);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(115, 138, 153);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.scale_button.setObjectName("scale_button")
        self.rotate_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.rotate_button.setGeometry(QtCore.QRect(70, 170, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.rotate_button.setFont(font)
        self.rotate_button.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(146, 164, 175);\n"
"    border-radius: 10px;\n"
"    border: 2px solid rgb(115, 138, 153);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(115, 138, 153);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.rotate_button.setObjectName("rotate_button")
        self.graphics_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.graphics_widget.setGeometry(QtCore.QRect(380, 10, 861, 731))
        self.graphics_widget.setObjectName("graphics_widget")
        self.rotate_angle_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.rotate_angle_field.setGeometry(QtCore.QRect(220, 30, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.rotate_angle_field.setFont(font)
        self.rotate_angle_field.setObjectName("rotate_angle_field")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 20, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 80, 91, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(190, 80, 21, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.rotate_x_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.rotate_x_field.setGeometry(QtCore.QRect(220, 80, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.rotate_x_field.setFont(font)
        self.rotate_x_field.setObjectName("rotate_x_field")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(190, 120, 21, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.rotate_y_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.rotate_y_field.setGeometry(QtCore.QRect(220, 120, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.rotate_y_field.setFont(font)
        self.rotate_y_field.setObjectName("rotate_y_field")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 230, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(60, 270, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.shift_x_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.shift_x_field.setGeometry(QtCore.QRect(220, 240, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.shift_x_field.setFont(font)
        self.shift_x_field.setObjectName("shift_x_field")
        self.shift_y_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.shift_y_field.setGeometry(QtCore.QRect(220, 280, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.shift_y_field.setFont(font)
        self.shift_y_field.setObjectName("shift_y_field")
        self.shift_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.shift_button.setGeometry(QtCore.QRect(70, 330, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.shift_button.setFont(font)
        self.shift_button.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(146, 164, 175);\n"
"    border-radius: 10px;\n"
"    border: 2px solid rgb(115, 138, 153);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(115, 138, 153);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.shift_button.setObjectName("shift_button")
        self.scale_x_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.scale_x_field.setGeometry(QtCore.QRect(220, 400, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.scale_x_field.setFont(font)
        self.scale_x_field.setObjectName("scale_x_field")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(190, 440, 21, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.scale_y_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.scale_y_field.setGeometry(QtCore.QRect(220, 440, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.scale_y_field.setFont(font)
        self.scale_y_field.setObjectName("scale_y_field")
        self.label_9 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(190, 400, 21, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 400, 171, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 490, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.scale_coefficient_x_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.scale_coefficient_x_field.setGeometry(QtCore.QRect(220, 490, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.scale_coefficient_x_field.setFont(font)
        self.scale_coefficient_x_field.setObjectName("scale_coefficient_x_field")
        self.label_11 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(180, 490, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.info_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.info_button.setGeometry(QtCore.QRect(0, 0, 81, 28))
        self.info_button.setObjectName("info_button")
        self.scale_coefficient_y_field = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.scale_coefficient_y_field.setGeometry(QtCore.QRect(220, 530, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.scale_coefficient_y_field.setFont(font)
        self.scale_coefficient_y_field.setObjectName("scale_coefficient_y_field")
        self.label_12 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(180, 530, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.draw_figure_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.draw_figure_button.setGeometry(QtCore.QRect(50, 660, 231, 71))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.draw_figure_button.setFont(font)
        self.draw_figure_button.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(134, 226, 130);\n"
"    border-radius: 10px;\n"
"    border: 2px solid rgb(65, 190, 55);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(65, 190, 55);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.draw_figure_button.setObjectName("draw_figure_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "computer graphic lab_02"))
        self.scale_button.setText(_translate("MainWindow", "Масштабирование"))
        self.rotate_button.setText(_translate("MainWindow", "Поворот"))
        self.label.setText(_translate("MainWindow", "угол поворота:\n"
"(в градусах)"))
        self.label_2.setText(_translate("MainWindow", "центр\n"
"поворота"))
        self.label_3.setText(_translate("MainWindow", "X:"))
        self.label_4.setText(_translate("MainWindow", "Y:"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p>смещение по   <span style=\" font-weight:600;\">X:</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p>смещение по <span style=\" font-weight:600;\">Y:</span></p></body></html>"))
        self.shift_button.setText(_translate("MainWindow", "Перемещение"))
        self.label_7.setText(_translate("MainWindow", "Y:"))
        self.label_9.setText(_translate("MainWindow", "X:"))
        self.label_8.setText(_translate("MainWindow", "            центр\n"
"масштабирования"))
        self.label_10.setText(_translate("MainWindow", "    коэффициенты\n"
"масштабирования"))
        self.label_11.setText(_translate("MainWindow", "KX:"))
        self.info_button.setText(_translate("MainWindow", "справка"))
        self.label_12.setText(_translate("MainWindow", "KY:"))
        self.draw_figure_button.setText(_translate("MainWindow", "Нарисовать фигуру"))
