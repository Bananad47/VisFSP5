from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QStyle, QFormLayout, QWidget, QStyleFactory, QLabel,QDialog, QMessageBox, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QColor
from PyQt5.QtCore import QThread,pyqtSignal,QDate, QDateTime,QTimer,QTime, Qt
import sys
import pymysql
import base64
import time
from qtwidgets import Toggle, AnimatedToggle
import sql_test_module

class ToggleSwitch(Toggle):#размер 200/40
    def __init__(self,window,text = ""):
        super().__init__()
        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        self.label.setFont(QtGui.QFont("Times", 12))
        self.container = QtWidgets.QWidget(window)
        self.container.setGeometry(QtCore.QRect(0, 0, 330, 50))

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 5, 5)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self)
        self.layout.setStretch(0, 1)
        self.container.setLayout(self.layout)
        self._readOnly = False

    def move(self,x,y):
        self.container.setGeometry(QtCore.QRect(x,y,330,50))

    def isReadOnly( self ):
        return self._readOnly

    def mousePressEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(ToggleSwitch, self).mousePressEvent(event)

    def mouseMoveEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(ToggleSwitch, self).mouseMoveEvent(event)

    def mouseReleaseEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(ToggleSwitch, self).mouseReleaseEvent(event)

    def keyPressEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            super(ToggleSwitch, self).keyPressEvent(event)

    @QtCore.pyqtSlot(bool)
    def setReadOnly( self, state ):
        self._readOnly = state

    readOnly = QtCore.pyqtProperty(bool, isReadOnly, setReadOnly)


class PasswordClass(QLineEdit):
    def __init__(self,window):
        super().__init__()
        self.passwordLabel = QLabel()
        self.container = QtWidgets.QWidget(window)
        self.passwordLabel.setText("Пароль:")
        self.passwordLabel.setFont(QtGui.QFont("Times", 12))
        self.setFont(QtGui.QFont("Times", 12))
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self)
        self.container.setLayout(self.layout)
        self.container.setGeometry(QtCore.QRect(150, 590, 300, 50))

class LineEdit(QtWidgets.QLineEdit):
    def __init__(self,window,text = ""):
        super().__init__()
        self.setFont(QtGui.QFont("Times", 12))
        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        self.label.setFont(QtGui.QFont("Times", 12))
        self.container = QtWidgets.QWidget(window)
        self.container.setGeometry(QtCore.QRect(0, 0, 330, 25))

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 5, 5)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self)
        self.layout.setStretch(0, 1)
        self.container.setLayout(self.layout)


    def move(self,x,y):
        self.container.setGeometry(QtCore.QRect(x,y,350,25))





class Settings(QDialog):
    errorsig = pyqtSignal()
    def __init__(self):
        super().__init__()   
        self.setupUi()
        self.setupTab1()
        self.setupTab2()
        self.addDefaultData()
        self.exec_()


    def setupUi(self):
        self.setObjectName("Form")
        self.setFixedSize(755, 650)
        self.setFont(QtGui.QFont("Times", 11))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("QDialog{"
                            "background-color: white;"
                            "border-width: 1;"
                            "border-radius: 1;"
                            "border-style: solid;"
                            "border-color: rgb(0, 0, 0)}")



        self.closebtn = QtWidgets.QPushButton(self)
        self.closebtn.setGeometry(QtCore.QRect(630, 590, 110, 50))
        self.closebtn.setObjectName("closebtn")
        self.closebtn.setText(" Закрыть")
        self.closebtn.setStyleSheet("background-color: white;"
                                "border-width: 1;"
                                "border-radius: 4;"
                                "border-style: solid;"
                                "border-color: rgb(0, 0, 0)"
                                )
        iconex = QtGui.QIcon("icons/krest.png")
        self.closebtn.setIcon(iconex)
        self.closebtn.setIconSize(QtCore.QSize(20, 20))
        self.closebtn.clicked.connect(self.close)
        self.closebtn.setFont(QtGui.QFont("Times", 12))



        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(2, 2, 751, 568))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setStyleSheet("QTabBar::tab {height: 50px; width: 360px}")


        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "Сканирование")
        self.tabWidget.setFont(QtGui.QFont("Times", 12))




        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_2.setFont(QtGui.QFont("Times", 12))
        self.tabWidget.addTab(self.tab_2,"Допуски")







        self.tabWidget.setCurrentIndex(0)


    def setupTab1(self):
        self.tab1label = QLabel(self.tab)
        self.tab.setFont(QtGui.QFont("Times", 11))
        self.tab1label.setGeometry(QtCore.QRect(10,5,200,25))
        self.tab1label.setText("<b>Сканирование</b>")
        self.tab1label.setFont(QtGui.QFont("Times", 15))

        self.toggle_1 = ToggleSwitch(self.tab,"Скол угла")
        self.toggle_1.move(20,40)
        self.toggle_1.setObjectName("checkBox_1")

        self.toggle_8 = ToggleSwitch(self.tab,"Скол кромки")
        self.toggle_8.move(20,120)
        self.toggle_8.setObjectName("checkBox_8")

        self.toggle_9 = ToggleSwitch(self.tab,"Трещины или разломы")
        self.toggle_9.move(20,200)
        self.toggle_9.setObjectName("checkBox_9")

        self.toggle_10 = ToggleSwitch(self.tab,"Несоответствие длины")
        self.toggle_10.move(20,280)
        self.toggle_10.setObjectName("checkBox_10")

        self.toggle_11 = ToggleSwitch(self.tab,"Несоответствие ширины")
        self.toggle_11.move(20,360)
        self.toggle_11.setObjectName("checkBox_11")


        self.toggle_12 = ToggleSwitch(self.tab,"Несоответствие диагоналей")
        self.toggle_12.move(400,40)
        self.toggle_12.setObjectName("checkBox_12")

        self.toggle_13 = ToggleSwitch(self.tab,"Нарушение прямоугольности листа")
        self.toggle_13.move(400,120)
        self.toggle_13.setObjectName("checkBox_13")

        self.toggle_14 = ToggleSwitch(self.tab,"Поворот листа")
        self.toggle_14.move(400,200)
        self.toggle_14.setObjectName("checkBox_14")

        self.toggle_15 = ToggleSwitch(self.tab,"Ошибка положения листа")
        self.toggle_15.move(400,280)
        self.toggle_15.setObjectName("checkBox_15")

        self.toggle_16 = ToggleSwitch(self.tab,"Загрязнение")
        self.toggle_16.move(400,360)
        self.toggle_16.setObjectName("checkBox_16")


    def setupTab2(self):
        self.tab_2.setFont(QtGui.QFont("Times", 12))
        self.tab1label = QLabel(self.tab_2)
        self.tab1label.setGeometry(QtCore.QRect(10,5,200,25))
        self.tab1label.setText("<b>Допуски</b>")
        self.tab1label.setFont(QtGui.QFont("Times", 15))



        self.bunkerLabel = QtWidgets.QLabel(self.tab_2)
        self.bunkerLabel.setText("Брак          Предупреждение")
        self.bunkerLabel.setGeometry(QtCore.QRect(10, 30, 300, 30))
        self.bunkerLabel.setFont(QtGui.QFont("Times", 13))

        self.bunkerLabel2 = QtWidgets.QLabel(self.tab_2)
        self.bunkerLabel2.setText("Брак         Предупреждение")
        self.bunkerLabel2.setGeometry(QtCore.QRect(430, 30, 300, 30))
        self.bunkerLabel2.setFont(QtGui.QFont("Times", 13))



        self.label1 = QtWidgets.QLabel(self.tab_2)
        self.label1.setText("Длина завышенный размер, mm")
        self.label1.setFont(QtGui.QFont("Times", 10))
        self.label1.setGeometry(QtCore.QRect(170, 70, 200, 30))
        self.lineEdit1 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit1.setGeometry(QtCore.QRect(10, 70, 70, 30))
        self.lineEdit1.setObjectName("lineEdit")
        self.lineEdit1.setAlignment(Qt.AlignRight)
        self.lineEdit1_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit1_2.setGeometry(QtCore.QRect(90, 70, 70, 30))
        self.lineEdit1_2.setObjectName("lineEdit")
        self.lineEdit1_2.setAlignment(Qt.AlignRight)


        self.label2 = QtWidgets.QLabel(self.tab_2)
        self.label2.setText("Длина заниженный размер, mm")
        self.label2.setFont(QtGui.QFont("Times", 10))
        self.label2.setGeometry(QtCore.QRect(170, 120, 200, 30))
        self.lineEdit2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit2.setGeometry(QtCore.QRect(10, 120, 70, 30))
        self.lineEdit2_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit2_2.setGeometry(QtCore.QRect(90, 120, 70, 30))


        self.label3 = QtWidgets.QLabel(self.tab_2)
        self.label3.setText("Ширина завышенный размер, mm")
        self.label3.setFont(QtGui.QFont("Times", 10))
        self.label3.setGeometry(QtCore.QRect(170, 170, 212, 30))
        self.lineEdit3 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit3.setGeometry(QtCore.QRect(10, 170, 70, 30))
        self.lineEdit3_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit3_2.setGeometry(QtCore.QRect(90, 170, 70, 30))

        self.label4 = QtWidgets.QLabel(self.tab_2)
        self.label4.setText("Ширина заниженный размер, mm")
        self.label4.setFont(QtGui.QFont("Times", 10))
        self.label4.setGeometry(QtCore.QRect(170, 220, 212, 30))
        self.lineEdit4 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit4.setGeometry(QtCore.QRect(10, 220, 70, 30))
        self.lineEdit4_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit4_2.setGeometry(QtCore.QRect(90, 220, 70, 30))

        self.label5 = QtWidgets.QLabel(self.tab_2)
        self.label5.setText("Диагональ, mm")
        self.label5.setFont(QtGui.QFont("Times", 10))
        self.label5.setGeometry(QtCore.QRect(170, 270, 180, 30))
        self.lineEdit5 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit5.setGeometry(QtCore.QRect(10, 270, 70, 30))
        self.lineEdit5_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit5_2.setGeometry(QtCore.QRect(90, 270, 70, 30))






        self.label12 = QtWidgets.QLabel(self.tab_2)
        self.label12.setText("Загрязнение, mm")
        self.label12.setFont(QtGui.QFont("Times", 10))
        self.label12.setGeometry(QtCore.QRect(170, 320, 180, 30))
        self.lineEdit12 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit12.setGeometry(QtCore.QRect(10, 320, 70, 30))
        self.lineEdit12_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit12_2.setGeometry(QtCore.QRect(90, 320, 70, 30))









        self.label9 = QtWidgets.QLabel(self.tab_2)
        self.label9.setText("Поперечная кромка, mm")
        self.label9.setFont(QtGui.QFont("Times", 10))
        self.label9.setGeometry(QtCore.QRect(590, 70, 180, 30))
        self.lineEdit9 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit9.setGeometry(QtCore.QRect(430, 70, 70, 30))
        self.lineEdit9_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit9_2.setGeometry(QtCore.QRect(510, 70, 70, 30))


        self.label10 = QtWidgets.QLabel(self.tab_2)
        self.label10.setText("Продольная кромка, mm")
        self.label10.setFont(QtGui.QFont("Times", 10))
        self.label10.setGeometry(QtCore.QRect(590, 120, 180, 30))
        self.lineEdit10 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit10.setGeometry(QtCore.QRect(430, 120, 70, 30))
        self.lineEdit10_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit10_2.setGeometry(QtCore.QRect(510, 120, 70, 30))

        self.label11 = QtWidgets.QLabel(self.tab_2)
        self.label11.setText("Угол, °")
        self.label11.setFont(QtGui.QFont("Times", 10))
        self.label11.setGeometry(QtCore.QRect(590, 170, 180, 30))
        self.lineEdit11 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit11.setGeometry(QtCore.QRect(430, 170, 70, 30))
        self.lineEdit11_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit11_2.setGeometry(QtCore.QRect(510, 170, 70, 30))



        self.label6 = QtWidgets.QLabel(self.tab_2)
        self.label6.setText("Положение, mm")
        self.label6.setFont(QtGui.QFont("Times", 10))
        self.label6.setGeometry(QtCore.QRect(590, 220, 180, 30))
        self.lineEdit6 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit6.setGeometry(QtCore.QRect(430, 220, 70, 30))
        self.lineEdit6_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit6_2.setGeometry(QtCore.QRect(510, 220, 70, 30))

        self.label7 = QtWidgets.QLabel(self.tab_2)
        self.label7.setText("Поворот, °")
        self.label7.setFont(QtGui.QFont("Times", 10))
        self.label7.setGeometry(QtCore.QRect(590, 270, 180, 30))
        self.lineEdit7 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit7.setGeometry(QtCore.QRect(430, 270, 70, 30))
        self.lineEdit7_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit7_2.setGeometry(QtCore.QRect(510, 270, 70, 30))




        self.lineEdit2.setAlignment(Qt.AlignRight)
        self.lineEdit2_2.setAlignment(Qt.AlignRight)


        self.lineEdit3.setAlignment(Qt.AlignRight)
        self.lineEdit3_2.setAlignment(Qt.AlignRight)


        self.lineEdit4.setAlignment(Qt.AlignRight)
        self.lineEdit4_2.setAlignment(Qt.AlignRight)


        self.lineEdit5.setAlignment(Qt.AlignRight)
        self.lineEdit5_2.setAlignment(Qt.AlignRight)


        self.lineEdit6.setAlignment(Qt.AlignRight)
        self.lineEdit6_2.setAlignment(Qt.AlignRight)


        self.lineEdit7.setAlignment(Qt.AlignRight)
        self.lineEdit7_2.setAlignment(Qt.AlignRight)


        self.lineEdit9.setAlignment(Qt.AlignRight)
        self.lineEdit9_2.setAlignment(Qt.AlignRight)


        self.lineEdit10.setAlignment(Qt.AlignRight)
        self.lineEdit10_2.setAlignment(Qt.AlignRight)


        self.lineEdit11.setAlignment(Qt.AlignRight)
        self.lineEdit11_2.setAlignment(Qt.AlignRight)




        self.lineEdit12.setAlignment(Qt.AlignRight)
        self.lineEdit12_2.setAlignment(Qt.AlignRight)


        self.spinLabel = QtWidgets.QLabel(self.tab_2)
        self.spinLabel.setText("Текущий набор допусков")
        self.spinLabel.setGeometry(QtCore.QRect(10, 450, 200, 30))

        self.spin = QtWidgets.QSpinBox(self.tab_2)
        self.spin.setGeometry(QtCore.QRect(220, 450, 50, 30))
        self.spin.setRange(1,10)
        self.spin.lineEdit().setStyleSheet(
                                       "selection-color: black;"
                                       "selection-background-color: white;"
                                       )
        self.spin.lineEdit().setReadOnly(True)
        self.spin.lineEdit().setFocusPolicy(Qt.NoFocus)
        self.spin.valueChanged.connect(self.changeSpinList)





        self.spin2Labelmain = QtWidgets.QLabel(self.tab_2)
        self.spin2Labelmain.setText("Текущий активный набор допусков")
        self.spin2Labelmain.setGeometry(QtCore.QRect(370, 450, 300, 30))



    def changeSpinList(self):
        num = self.sender().value()
        self.addDefaultData(num = num)






    def addDefaultData(self,num = 11):
        #tab1 setChecked
        tabs1toggle = [self.toggle_10, self.toggle_11, self.toggle_12, self.toggle_15, 
        self.toggle_14, self.toggle_13, self.toggle_8, self.toggle_1, self.toggle_9, self.toggle_16]


        tab2names = [self.lineEdit5_2, self.lineEdit5, self.lineEdit11_2, self.lineEdit11, self.lineEdit9_2, self.lineEdit9, self.lineEdit10_2, self.lineEdit10, 
        self.lineEdit7_2, self.lineEdit7, self.lineEdit6_2, self.lineEdit6, self.lineEdit1_2, self.lineEdit1, self.lineEdit2_2, self.lineEdit2, self.lineEdit3_2, self.lineEdit3, self.lineEdit4_2, self.lineEdit4, self.lineEdit12_2, self.lineEdit12]
        try:
            l1,l2 = sql_test_module.settingsData(num)
            if num == 11:
                num = l2["actual_tolerance"]
                self.setupDefaultSpinValue(num)
            l1 = [True if l1[x] == 1 else False for x in l1]
            names = ['diag_w', 'diag_b', 'corner_w', 'corner_b', 'front_rib_w', 'front_rib_b', 'side_rib_w', 'side_rib_b', 'turn_w', 'turn_b', 'position_w', 'position_b', 'length_overlarge_w', 'length_overlarge_b', 'length_extrasmall_w', 'length_extrasmall_b', 'width_overlarge_w', 'width_overlarge_b', 'width_extrasmall_w', 'width_extrasmall_b',"spot_w","spot_b"]
            l2 = [l2[x] for x in names]
            for toggle,state in zip(tabs1toggle,l1):
                toggle.setChecked(state)
                toggle.setReadOnly(True)



            for name,data in zip(tab2names,l2):
                name.setText(data)
                name.setReadOnly(True)

        except:
            self.errorsig.emit()


    def setupDefaultSpinValue(self,num):
        self.spin.setValue(int(num))
        self.spin2Labelmain.setText(f"Текущий активный набор допусков {num}")













def main():
    app = QApplication(sys.argv)
    win = Settings()
    sys.exit(app.exec_())
    exit()




if __name__ == "__main__":
    main()

