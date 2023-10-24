import sys

import detailedScreen
import sql_test_module
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPixmap, QTextCharFormat
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QLabel,
    QPushButton,
    QTableWidgetItem,
)
from qtwidgets import Toggle


class Tableclass(QtWidgets.QWidget):
    """таблица"""

    def __init__(self, mainwindow):
        super().__init__()
        self.setFont(QtGui.QFont("Times", 12))
        self.Table = QtWidgets.QTableWidget(mainwindow)
        self.Table.setFont(QtGui.QFont("Times", 12))
        self.Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table.setObjectName("listWidget")
        self.Table.setColumnCount(4)
        self.Table.setHorizontalHeaderLabels(
            ["Id", "Дата", "Дефект", "Статус"]
        )
        self.Table.verticalHeader().hide()
        self.Table.setGeometry(QtCore.QRect(10, 250, 780, 440))  # 800 700

        font = self.Table.horizontalHeader().font()
        font.setPointSize(12)
        for i in range(4):
            self.Table.horizontalHeaderItem(i).setFont(font)

        self.Table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.Table.itemClicked.connect(self.openDetailedScreen)

    def openDetailedScreen(self, item):
        """открытие детального экрана"""
        Id = self.Table.item(item.row(), 0).text()
        self.detailed = detailedScreen.Detailed(Id)

    def addtableitems(self, rows):
        """добавление в таблицу новых элементов"""
        self.Table.setRowCount(0)
        data = rows
        self.Table.setRowCount(len(data))
        self.namesql = ["id", "date", "defect", "status"]
        colors = {
            "1": QtGui.QColor(0, 255, 0),
            "2": QtGui.QColor(255, 255, 0),
            "3": QtGui.QColor(255, 0, 0),
        }
        icons = {
            "1": "defects/1.png",
            "2": "defects/2.png",
            "3": "defects/3.png",
            "4": "defects/4.png",
            "5": "defects/5.png",
            "6": "defects/6.png",
            "7": "defects/7.png",
            "8": "defects/8.png",
            "9": "defects/9.png",
            "10": "defects/10.png",
            "11": "defects/11.png",
            "12": "defects/12.png",
            "13": "defects/13.png",
            "14": "defects/14.png",
            "15": "defects/15.png",
            "16": "defects/16.png",
        }
        font = QtGui.QFont("Times", 12)
        for i in range(len(data)):
            for j in range(4):
                if j == 3:
                    self.Table.setItem(i, 3, QTableWidgetItem(""))
                    self.Table.item(i, 3).setBackground(
                        colors[str(data[i]["status"])]
                    )
                elif j == 2:
                    defect = str(data[i]["defect"])
                    if defect != "0":
                        pixmap = QPixmap(icons[defect[0]])
                        pixmap = pixmap.scaledToHeight(25)
                        iconItem = QtWidgets.QLabel()
                        # icon = QIcon(icons[defect])
                        # iconItem = QTableWidgetItem()
                        iconItem.setPixmap(pixmap)
                        # iconItem.setIcon(icon)
                        # iconItem.setIconSize(50,50)
                        self.Table.setCellWidget(i, 2, iconItem)
                        self.Table.item(i, 2)
                    else:
                        self.Table.setItem(i, 2, QTableWidgetItem(""))
                else:
                    self.Table.setItem(
                        i, j, QTableWidgetItem(str(data[i][self.namesql[j]]))
                    )
            self.Table.item(i, 1).setFont(font)


class ToggleSwitch(Toggle):
    """создание переключателей"""

    def __init__(self, window, text=""):
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

    def move(self, x, y):
        self.container.setGeometry(QtCore.QRect(x, y, 200, 50))


class Finder(QDialog):
    """окно поиска"""

    errorsig = pyqtSignal()

    def __init__(self):
        """создаение самого окна"""
        super().__init__()
        self.setObjectName("Form")
        self.setFixedSize(800, 700)  # 800 220
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(
            "QDialog{"
            "background-color: white;"
            "border-width: 2;"
            "border-radius: 1;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)}"
        )
        self.setFont(QtGui.QFont("Times", 12))

        self.table = Tableclass(self)
        self.toggle1 = ToggleSwitch(self, text="Норма")
        self.toggle2 = ToggleSwitch(self, text="Предупреждение")
        self.toggle3 = ToggleSwitch(self, text="Брак")
        self.toggle1.move(550, 40)
        self.toggle2.move(550, 110)
        self.toggle3.move(550, 180)
        self.toggle1.setChecked(True)
        self.toggle2.setChecked(True)
        self.toggle3.setChecked(True)

        self.startlabel = QLabel(self)
        self.startlabel.setText("Дата начала: ")
        self.startlabel.setGeometry(QtCore.QRect(15, 50, 130, 30))
        self.startlabel.setFont(QtGui.QFont("Times", 12))
        self.startdate = QtWidgets.QDateTimeEdit(self)
        self.startdate.setGeometry(QtCore.QRect(150, 50, 160, 30))
        self.startdate.setFont(QtGui.QFont("Times", 12))
        self.startdate.setCalendarPopup(True)
        self.calendar1 = Calendarpro()
        self.calendar1.setStyleSheet(
            """
            #qt_calendar_prevmonth, #qt_calendar_nextmonth {
                border: none;
                color: white;
                font-weight: bold;
                qproperty-icon: none;
                background-color: transparent;
            }
            #qt_calendar_prevmonth {
                qproperty-text: "<";
            }
            #qt_calendar_nextmonth {
                qproperty-text: ">";
            }
            """
        )

        self.calendar2 = Calendarpro()
        self.calendar2.setStyleSheet(
            """
            #qt_calendar_prevmonth, #qt_calendar_nextmonth {
                border: none;
                color: white;
                font-weight: bold;
                qproperty-icon: none;
                background-color: transparent;
            }
            #qt_calendar_prevmonth {
                qproperty-text: "<";
            }
            #qt_calendar_nextmonth {
                qproperty-text: ">";
            }
            """
        )

        self.startdate.setCalendarWidget(self.calendar1)
        self.startdate.setDate(QDate.currentDate().toPyDate())

        self.finishlabel = QLabel(self)
        self.finishlabel.setText("Дата окончания: ")
        self.finishlabel.setGeometry(QtCore.QRect(15, 100, 130, 30))
        self.finishlabel.setFont(QtGui.QFont("Times", 12))
        self.finishdate = QtWidgets.QDateTimeEdit(self)
        self.finishdate.setFont(QtGui.QFont("Times", 12))
        self.finishdate.setGeometry(QtCore.QRect(150, 100, 160, 30))
        self.finishdate.setCalendarPopup(True)

        self.finishdate.setCalendarWidget(self.calendar2)

        self.finishdate.setDate(QDate.currentDate().toPyDate())

        self.label = QLabel(self)
        self.label.setText("Поиск")
        self.label.setGeometry(QtCore.QRect(325, 10, 150, 25))
        self.label.setFont(QtGui.QFont("Times", 20))

        self.closebtn = QPushButton(self)
        self.closebtn.setGeometry(QtCore.QRect(150, 170, 100, 50))
        self.closebtn.setObjectName("closebtn")
        self.closebtn.setText("Закрыть")
        self.closebtn.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.closebtn.setFont(QtGui.QFont("Times", 12))
        self.closebtn.clicked.connect(self.close)

        iconex = QtGui.QIcon("icons/krest.png")
        self.closebtn.setIcon(iconex)
        self.closebtn.setIconSize(QtCore.QSize(20, 20))

        self.findbtn = QPushButton(self)
        self.findbtn.setGeometry(QtCore.QRect(20, 170, 100, 50))
        self.findbtn.setObjectName("findbtn")
        self.findbtn.setText("Поиск")
        self.findbtn.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.findbtn.setFont(QtGui.QFont("Times", 12))

        iconf = QtGui.QIcon("icons/find.jpg")
        self.findbtn.setIcon(iconf)
        self.findbtn.setIconSize(QtCore.QSize(20, 20))
        self.findbtn.clicked.connect(self.find)

        self.exec_()

    def find(self):
        """выполняем поиск и заполняем таблицу"""
        l = [
            self.toggle1.isChecked(),
            self.toggle2.isChecked(),
            self.toggle3.isChecked(),
        ]
        start = self.startdate.dateTime().toPyDateTime()
        finish = self.finishdate.dateTime().toPyDateTime()
        try:
            data = sql_test_module.search(l, start, finish)[::-1]
            self.table.addtableitems(data)
        except:
            self.errorsig.emit()


class MyCalendar(QtWidgets.QCalendarWidget):
    """календарь"""

    def __init__(self, parent=None):
        QtWidgets.QCalendarWidget.__init__(self, parent)

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        if date == date.currentDate():
            painter.setBrush(QtGui.QColor(250, 150, 0, 100))
            painter.setPen(QtGui.QColor(0, 0, 0, 0))
            painter.drawRect(rect)


class Calendarpro(MyCalendar):
    """календарь"""

    def __init__(self):
        super().__init__()
        self.setGeometry(QtCore.QRect(200, 200, 200, 100))
        self.setWindowTitle("Calendar")

        self.setStyleSheet(
            """
            #qt_calendar_prevmonth, #qt_calendar_nextmonth {
                border: none;
                color: white;
                font-weight: bold;
                qproperty-icon: none;
                background-color: transparent;
            }
            #qt_calendar_prevmonth {
                qproperty-text: "<";
            }
            #qt_calendar_nextmonth {
                qproperty-text: ">";
            }
            """
        )

        self.weekendFormat = QTextCharFormat()
        self.weekendFormat.setForeground(QBrush(QColor(0, 0, 0)))
        self.setWeekdayTextFormat(Qt.Saturday, self.weekendFormat)
        self.setWeekdayTextFormat(Qt.Sunday, self.weekendFormat)

        self.setGridVisible(True)
        self.setStyleSheet("color: black;" "background-color : white;")

        self.setVerticalHeaderFormat(
            QtWidgets.QCalendarWidget.NoVerticalHeader
        )
