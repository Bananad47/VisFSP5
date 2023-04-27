import sys

import sql_test_module
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtChart import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QValueAxis,
)
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QTextCharFormat
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class BarChat(QChart):
    def __init__(self, mainwindow):
        super().__init__()

        self.chartView = QChartView(self)

        self.wid = QtWidgets.QWidget(mainwindow)
        self.wid.setGeometry(QtCore.QRect(0, 30, 800, 590))
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.chartView)
        self.wid.setLayout(self.layout)
        self.setTitle("")
        self.names = (
            '<font size="5" style="color: rgb(0, 150, 0);">Норма</font>',
            '<font size="5" style="color: rgb(210, 210, 0);">'
            'Предупреждение</font>',
            '<font size="5" style="color: rgb(255, 0, 0);">Брак</font>',
        )
        self.axisX = QBarCategoryAxis()
        self.axisX.append(self.names)
        self.axisY = QValueAxis()
        self.axisY.setRange(0, 100)
        self.addAxis(self.axisX, Qt.AlignBottom)
        self.addAxis(self.axisY, Qt.AlignLeft)
        self.legend().setVisible(False)
        self.legend().setAlignment(Qt.AlignBottom)

    def addData(self, data):
        series = QBarSeries()

        set0 = QBarSet("Кол-во")
        set0.append(data)
        series.append(set0)
        self.removeAllSeries()
        self.addSeries(series)
        self.axisY.setRange(0, max(data))


class Statistics(QDialog):
    errorsig = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("Form")
        self.setFixedSize(800, 700)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(
            "QDialog{"
            "background-color: white;"
            "border-width: 2;"
            "border-radius: 1;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)}"
        )

        self.bar = BarChat(self)

        self.label = QLabel(self)
        self.label.setText("Статистика")
        self.label.setGeometry(QtCore.QRect(325, 5, 150, 25))
        self.label.setFont(QtGui.QFont("Times", 20))

        self.datelbl1 = QLabel(self)
        self.datelbl1.setText("Дата начала:")
        self.datelbl1.setGeometry(QtCore.QRect(10, 630, 120, 50))
        self.datelbl1.setFont(QtGui.QFont("Times", 11))

        self.datebtn1 = QPushButton(self)
        self.datebtn1.setGeometry(QtCore.QRect(140, 630, 100, 50))
        self.datebtn1.setObjectName("closebtn")
        self.datebtn1.setText(str(QDate.currentDate().toPyDate()))
        self.datebtn1.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.datebtn1.setFont(QtGui.QFont("Times", 11))
        self.datebtn1.clicked.connect(self.test)

        self.datelbl2 = QLabel(self)
        self.datelbl2.setText("Дата окончания:")
        self.datelbl2.setGeometry(QtCore.QRect(300, 630, 120, 50))
        self.datelbl2.setFont(QtGui.QFont("Times", 11))

        self.datebtn2 = QPushButton(self)
        self.datebtn2.setGeometry(QtCore.QRect(430, 630, 100, 50))
        self.datebtn2.setObjectName("closebtn")
        self.datebtn2.setText(str(QDate.currentDate().toPyDate()))
        self.datebtn2.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.datebtn2.setFont(QtGui.QFont("Times", 11))
        self.datebtn2.clicked.connect(self.test)

        self.closebtn = QPushButton(self)
        self.closebtn.setGeometry(QtCore.QRect(680, 630, 100, 50))
        self.closebtn.setObjectName("closebtn")
        self.closebtn.setText("Закрыть")
        self.closebtn.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.closebtn.setFont(QtGui.QFont("Times", 11))
        self.closebtn.clicked.connect(self.close)
        date1 = self.datebtn1.text()
        date2 = self.datebtn2.text()
        try:
            data = sql_test_module.statistic(date1, date2)
            self.bar.addData(data)
        finally:
            self.errorsig.emit()
        self.exec_()

    def test(self):
        sender = self.sender()
        self.calendar = Calendarpro()
        date = self.calendar.selectedDate()
        l = sender.text().split("-")
        year = int(l[0])
        mounth = int(l[1])
        day = int(l[2])
        date.setDate(year, mounth, day)
        self.calendar.setSelectedDate(date)
        if self.calendar.exec_():
            self.UpdateData(sender)

    def UpdateData(self, sender):
        newDate = self.calendar.newDate
        sender.setText(newDate)
        date1 = self.datebtn1.text()
        date2 = self.datebtn2.text()
        try:
            data = sql_test_module.statistic(date1, date2)
            self.bar.addData(data)
        finally:
            self.errorsig.emit()


class Calendarpro(QDialog):
    signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(QtCore.QRect(200, 200, 200, 100))
        self.setWindowTitle("Calendar")
        self.vbox = QVBoxLayout()
        self.calendar = MyCalendar()

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
        self.calendar.setWeekdayTextFormat(Qt.Saturday, self.weekendFormat)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, self.weekendFormat)

        self.calendar.setGridVisible(True)
        self.calendar.setStyleSheet(
            "color: black;" "background-color : white;"
        )

        self.calendar.setVerticalHeaderFormat(
            QtWidgets.QCalendarWidget.NoVerticalHeader
        )

        self.vbox.addWidget(self.calendar)
        self.setLayout(self.vbox)

        self.calendar.selectionChanged.connect(self.calendar_date)

    def calendar_date(self):
        dateselected = self.calendar.selectedDate()
        date_in_string = str(dateselected.toPyDate())
        self.newDate = date_in_string
        self.accept()

    def setDate(self, date):
        self.calendar.setDate(date)

    def selectedDate(self):
        return self.calendar.selectedDate()

    def setSelectedDate(self, date):
        self.calendar.setSelectedDate(date)


class MyCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        QtWidgets.QCalendarWidget.__init__(self, parent)

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        if date == date.currentDate():
            painter.setBrush(QtGui.QColor(250, 150, 0, 100))
            painter.setPen(QtGui.QColor(0, 0, 0, 0))
            painter.drawRect(rect)

    def setDate(self, date):
        QtWidgets.QCalendarWidget.setDate(date)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Statistics()

    exit()
    sys.exit(app.exec_())
