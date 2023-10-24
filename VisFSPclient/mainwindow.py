import base64
import statistics
import sys
import time

import detailedScreen
import findwin
import pymysql
import settingsScreen
import sql_test_module
from PyQt5 import QtCore, QtGui, QtSvg, QtWidgets
from PyQt5.QtCore import QDate, QDateTime, QThread, QTime, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QStyle,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ImageLabel(QtWidgets.QGraphicsView):  ###########################
    """без понятия что оно делает, скорее всего за лого отвечает"""

    def __init__(self, *args, **kwargs):
        super(ImageLabel, self).__init__(*args, **kwargs)
        self.setScene(QtWidgets.QGraphicsScene())
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def setImage(self, filename):
        self.setPixmap(QtGui.QPixmap(filename))

    def setPixmap(self, pixmap):
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        item.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.scene().addItem(item)

    def resizeEvent(self, event):
        r = self.scene().itemsBoundingRect()
        self.fitInView(r, QtCore.Qt.KeepAspectRatio)
        super(ImageLabel, self).resizeEvent(event)


class Information(QFrame):
    """виджет информации(типо скорости и статуса)"""

    def __init__(self, text, info=""):
        super().__init__()
        self.text = text
        self.setStyleSheet(
            "background-color:white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(10, 10, 10)"
        )

        self.layout = QHBoxLayout()
        self.label = QtWidgets.QLabel()
        self.label.setText(
            """{0} <font style="color: rgb(0, 0, 0);">{1}</font>""".format(
                self.text, info
            )
        )
        self.label.setStyleSheet("border-width: 0;" "min-height: 30px;")
        self.label.setFont(QtGui.QFont("Times", 14))

        self.layout.addStretch(1)
        self.layout.addWidget(self.label, 2)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def setText(self, info, color="rgb(0,150,0)"):
        self.label.setText(
            f"""{self.text} <font style="color: {color};">{info}</font>"""
        )


class Time(QFrame):
    """виджет времени"""

    def __init__(self, text=""):
        super().__init__()
        self.setStyleSheet(
            "background-color:white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(10, 10, 10)"
        )

        self.layout = QHBoxLayout()
        self.label = QtWidgets.QLabel()
        self.label.setText(text)
        self.label.setStyleSheet("border-width: 0;" "min-height: 30px;")
        self.label.setFont(QtGui.QFont("Times", 14))
        self.layout.addStretch(1)
        self.layout.addWidget(self.label, 2)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def setText(self, text):
        self.label.setText(text)


class MainWindow(QMainWindow):
    """само окно"""

    def setupUi(self):
        """создаем само окно"""
        self.setObjectName("MainWindow")
        self.setFont(QtGui.QFont("Times", 12))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.timeLabel = Time()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        # дальше идет создание кнопок и тд

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(" Сервис")
        self.pushButton.setFont(QtGui.QFont("Times", 12))
        self.pushButton.setStyleSheet(
            "min-height: 70px;"
            "min-width: 150px;"
            "background-color:white;"
            "border-width: 1;"
            "border-radius: 6;"
            "border-style: solid;"
            "border-color: rgb(10, 10, 10)"
        )

        icon = QtGui.QIcon("icons/zamok.png")
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(50, 50))

        self.status = Information("Статус: ", "Инспекция")
        self.speed = Information("Скорость: ", "60 м/мин")
        self.thickness = Information("Толщина:", "4.00мм")

        self.Table = QtWidgets.QTableWidget()

        pixmap = QPixmap("iss.png")
        pixmap = pixmap.scaledToHeight(75)
        self.logo = QtWidgets.QLabel()
        self.logo.setPixmap(pixmap)

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.logo)
        self.topLayout.addStretch(1)

        self.topLayout.addWidget(self.timeLabel)
        self.topLayout.addStretch(2)
        self.topLayout.addWidget(self.status)
        self.topLayout.addWidget(self.speed)
        self.topLayout.addWidget(self.thickness)
        self.topLayout.addStretch(2)
        self.topLayout.addWidget(self.pushButton)

        self.tableLayout = QVBoxLayout()
        self.tableLayout.addLayout(self.topLayout)
        self.tableLayout.addWidget(self.Table, 10)
        self.centralwidget.setLayout(self.tableLayout)

        self.verticalWidget = QtWidgets.QFrame(self)
        self.verticalWidget.setGeometry(QtCore.QRect(870, 110, 220, 360))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalWidget.setStyleSheet(
            "background-color: rgb(190, 190, 190);"
            "border-width: 1;"
            "border-radius: 2;"
            "border-style: solid;"
            "border-color: rgb(10, 10, 10)"
        )

        self.verticalWidget.hide()

        self.pushButton_3 = QtWidgets.QPushButton(self.verticalWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Настройки")
        self.pushButton_3.setFont(QtGui.QFont("Times", 15))
        self.pushButton_3.setGeometry(QtCore.QRect(10, 10, 200, 100))
        self.pushButton_3.setStyleSheet(
            "background-color:white;" "border-radius: 6;"
        )
        self.pushButton_3.clicked.connect(self.openSettingsScreen)

        self.pushButton_4 = QtWidgets.QPushButton(self.verticalWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("Статистика")
        self.pushButton_4.setFont(QtGui.QFont("Times", 15))
        self.pushButton_4.setGeometry(QtCore.QRect(10, 130, 200, 100))
        self.pushButton_4.setStyleSheet(
            "background-color:white;" "border-radius: 6;"
        )
        self.pushButton_4.clicked.connect(self.openStatisticsScreen)

        self.pushButton_5 = QtWidgets.QPushButton(self.verticalWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText("Поиск")
        self.pushButton_5.setFont(QtGui.QFont("Times", 15))
        self.pushButton_5.setGeometry(QtCore.QRect(10, 250, 200, 100))
        self.pushButton_5.setStyleSheet(
            "background-color:white;" "border-radius: 6;"
        )
        self.pushButton_5.clicked.connect(self.openSearchWin)

        icon3 = QtGui.QIcon("icons/settings.png")
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setIconSize(QtCore.QSize(20, 20))

        icon4 = QtGui.QIcon("icons/stat.png")
        self.pushButton_4.setIcon(icon4)
        self.pushButton_4.setIconSize(QtCore.QSize(20, 20))

        icon5 = QtGui.QIcon("icons/find.jpg")
        self.pushButton_5.setIcon(icon5)
        self.pushButton_5.setIconSize(QtCore.QSize(20, 20))  # 360

        self.setCentralWidget(self.centralwidget)

        self.pushButton.clicked.connect(
            lambda: self.testFunc(self.verticalWidget)
        )
        self.createWorker()

    def testFunc(self, item):
        """функция которая делает видимым боковое меню с настройками и тд"""
        if item.isVisible():
            item.hide()
        else:
            self.verticalWidget.move(self.size().width() - 230, 110)
            item.show()

    def setupTable(self):
        """настраиваем таблицу"""
        self.Table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.Table.setObjectName("listWidget")
        self.Table.setColumnCount(12)
        self.Table.setHorizontalHeaderLabels(
            [
                "Id",
                "Дата",
                "Длина",
                "Длина+-",
                "Ширина",
                "Ширина+-",
                "Диагональ+-",
                "Прямоуг-ть",
                "Допуск",
                "Положение",
                "Дефект",
                "Статус",
            ]
        )
        self.Table.verticalHeader().hide()

        self.Table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.Table.itemClicked.connect(self.openDetailedScreen)

        # self.Table.setColumnWidth(1, 150)

    def addDefaultItemInTable(self):
        """заполняем таблицу"""
        self.Table.setRowCount(
            200
        )  # тут изменить значение для меньшего кол-ва рядов
        try:
            data = sql_test_module.sql_all_data(
                200
            )  # тут изменить значение для меньшего кол-ва рядов
            self.addtableitems(data)
        except:
            self.errorFunc()

    def showTime(self):
        current_time = QDateTime.currentDateTime()

        label_time = current_time.toString(
            """dd.MM.yyyy
hh:mm:ss"""
        )

        self.timeLabel.setText(label_time)

    # дальше идут функции для открытия чего-то по нажатию на кнопку

    def openSearchWin(self):
        self.finder = findwin.Finder()
        self.finder.errorsig.connect(self.errorFunc)

    def openStatisticsScreen(self):
        self.stat = statistics.Statistics()
        self.stat.errorsig.connect(self.errorFunc)

    def openSettingsScreen(self):
        self.settings = settingsScreen.Settings()
        self.settings.errorsig.connect(self.errorFunc)

    def openDetailedScreen(self, item):
        Id = self.Table.item(item.row(), 0).text()
        self.detailed = detailedScreen.Detailed(Id)
        self.detailed.errorsig.connect(self.errorFunc)

    def addtableitems(self, rows, k=False):
        """заполняем таблицу значениями(как новыми так и изначальными)"""
        data = rows
        self.namesql = [
            "id",
            "date",
            "length_n",
            "length_f",
            "width_n",
            "width_f",
            "diag_n",
            "diag_f",
            "squareness_f",
            "tolerance",
            "turn_f",
            "defect",
            "status",
        ]

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
        font = QtGui.QFont("Times", 9)
        for i in range(len(data)):
            data2 = sql_test_module.settingsData(
                data[i]["tolerance"]
            )[1]
            names3 = [
                "length_overlarge_"
                if float(data[i]["length_f"]) - float(data[i]["length_n"]) >= 0
                else "length_extrasmall_",
                "width_overlarge_"
                if float(data[i]["width_f"]) - float(data[i]["width_n"]) > 0
                else "width_extrasmall_",
                "diag_",
                "squareness_",
                "turn_",
            ]
            z = 0
            p = i
            diff = 0
            if k:
                self.Table.insertRow(0)
                self.Table.removeRow(200)
                p = 0
            for j in range(13):
                if j == 12:
                    self.Table.setItem(p, 11, QTableWidgetItem(""))
                    self.Table.item(p, 11).setBackground(
                        colors[str(data[i]["status"])]
                    )
                elif j == 11:
                    defect = str(data[i]["defect"])
                    if defect != "0":
                        pixmap = QPixmap(icons[defect])
                        pixmap = pixmap.scaledToHeight(25)
                        iconItem = QtWidgets.QLabel()
                        # icon = QIcon(icons[defect])
                        # iconItem = QTableWidgetItem()
                        iconItem.setPixmap(pixmap)
                        # iconItem.setIcon(icon)
                        # iconItem.setIconSize(50,50)
                        self.Table.setCellWidget(p, 10, iconItem)
                        self.Table.item(p, 10)
                    else:
                        self.Table.setItem(p, 10, QTableWidgetItem(""))

                elif j == 8:
                    self.Table.setItem(
                        p, 7, QTableWidgetItem(str(data[i][self.namesql[j]]))
                    )
                    if data[i]["squareness_f"] == "0":
                        self.Table.item(p, 7).setForeground(QColor(255, 0, 0))
                    else:
                        self.Table.item(p, 7).setForeground(QColor(0, 150, 0))
                    z += 1
                elif j in [0, 1, 2, 4, 9]:
                    self.Table.setItem(
                        p, j-diff, QTableWidgetItem(str(data[i][self.namesql[j]]))
                    )
                elif j == 10:
                    self.Table.setItem(
                        p, 9, QTableWidgetItem(str(data[i][self.namesql[j]]))
                    )
                    if abs(float(data[i][self.namesql[j]])) >= float(
                        data2[names3[4] + "b"]
                    ):
                        self.Table.item(p, 9).setForeground(QColor(255, 0, 0))
                    elif abs(float(data[i][self.namesql[j]])) < float(
                        data2[names3[4] + "w"]
                    ):
                        self.Table.item(p, 9).setForeground(QColor(0, 150, 0))
                    else:
                        self.Table.item(p, 9).setForeground(
                            QColor(210, 210, 0)
                        )
                    z += 1
                elif j == 6:
                    diff = 1
                else:
                    self.Table.setItem(
                        p, j-diff, QTableWidgetItem(str(data[i][self.namesql[j]]))
                    )
                    if abs(float(data[i][self.namesql[j]]) - float(data[i][self.namesql[j-1]])) >= float(
                        data2[names3[z] + "b"]
                    ):
                        self.Table.item(p, j-diff).setForeground(QColor(255, 0, 0))
                    elif abs(float(data[i][self.namesql[j]]) - float(data[i][self.namesql[j-1]])) < float(
                        data2[names3[z] + "w"]
                    ):
                        self.Table.item(p, j-diff).setForeground(QColor(0, 150, 0))
                    else:
                        self.Table.item(p, j-diff).setForeground(
                            QColor(210, 210, 0)
                        )
                    z += 1

            self.Table.item(p, 1).setFont(font)
    
    def updateStatus(self):
        """обновляем статус и информацию"""
        try:
            data = sql_test_module.checkUpdate()
            speed = data["speed"]
            thickness = data["thickness"]
            status = data["status"]
            self.speed.setText(speed + "м/мин", color="rgb(0,0,0)")
            self.thickness.setText(thickness + "мм", color="rgb(0,0,0)")
            if status == "0":
                self.status.setText("Ошибка", color="rgb(255,0,0)")
            elif status == "1":
                self.status.setText("Инспекция", color="rgb(0,150,0)")
            elif status == "2":
                self.status.setText("Ожидание", color="rgb(0,0,0)")
        except:
            self.errorFunc()

    def errorFunc(self):
        """при ошибках ставим статус ошибки"""
        self.status.setText("Ошибка", color="rgb(255,0,0)")

    def createWorker(self):
        """создаем второй поток"""
        self.thread = QThread()
        self.worker = UpdateSql()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.updateStatusBar.connect(self.updateStatus)
        self.worker.newItems.connect(self.updateTable)
        self.worker.errorsig.connect(self.errorFunc)
        self.thread.start()

    def updateTable(self):
        """при новых элементах добавляем их в таблицу"""
        try:
            newId = sql_test_module.last_item_id()
            Id = self.Table.item(0, 0)
            k = True
            if Id == None:
                Id = 0
                k = False
            else:
                Id = Id.text()
            num = int(newId) - int(Id)
            rows = sql_test_module.new_rows(num)
            self.addtableitems(rows, k)
        except:
            self.errorFunc()

    def closeEvent(self, event):
        super().closeEvent()
        self.worker.get_close()
        self.pool.waitForDone()


class UpdateSql(QtCore.QObject):
    """класс для 2 потока"""

    app = QApplication(sys.argv)
    newItems = pyqtSignal()
    updateStatusBar = pyqtSignal()
    errorsig = pyqtSignal()

    def run(self):
        """смотрим на наличие апдейтов, если они есть отправляем сигнал в основной поток, чтобы их применить"""
        while True:
            try:
                update = sql_test_module.checkUpdate()
                self.updateStatusBar.emit()
                if update["scan"] == 1:
                    self.newItems.emit()
                QtCore.QThread.sleep(2)
            except:
                self.errorsig.emit()

    def get_close(self):
        try:
            sys.exit(a.exec_())
            exit()
        except:
            time.sleep(15)
            sys.exit(a.exec_())
            exit()


def main():
    """запуск приложения"""
    a = QApplication(sys.argv)
    win = MainWindow()
    win.setupUi()
    win.setupTable()
    win.addDefaultItemInTable()
    win.show()
    sys.exit(a.exec_())
    exit()
    sys.exit(0)


if __name__ == "__main__":
    main()
