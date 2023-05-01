import pyqtgraph as pg
import sql_test_module
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QTableWidgetItem,
    QWidget
)


class Graph(QtWidgets.QWidget):
    """класс отвечающий за график"""

    def __init__(self, data):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.data = data
        self.view = pg.PlotWidget(background="w")
        self.view.setMouseEnabled(x=False, y=False)
        self.set_plot()
        layout.addWidget(self.view)

    def set_plot(self):
        """заполняем график данными, которые получили при создании обьекта класса"""
        outline = self.data.pop(0)
        scatter = pg.ScatterPlotItem(size=7, brush=pg.mkBrush(255, 0, 0, 255))
        self.curve = self.view.plot(name="Line")
        self.curve.setData(outline[0], outline[1], pen="black")

        x = self.data[0][0]
        y = self.data[0][1]
        scatter.addPoints(x, y)
        self.view.addItem(scatter)


class Detailed(QDialog):
    """сам детальный экран"""

    errorsig = pyqtSignal()  # сигнал для ошибок в случае чего

    def __init__(self, idx):
        super().__init__()
        self.Id = idx
        self.setupUi()
        self.setupTables()
        self.exec_()

    def setupUi(self):
        """создаем само окно"""
        self.setObjectName("Form")
        self.setFixedSize(820, 680)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(
            "QDialog{"
            "background-color: white;"
            "border-width: 2;"
            "border-radius: 1;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)}"
        )

        self.nameLabel = QtWidgets.QLabel(self)
        self.nameLabel.setGeometry(QtCore.QRect(20, 2, 500, 60))
        self.nameLabel.setText("Отображение результатов")
        self.nameLabel.setFont(QtGui.QFont("Times", 15))

        self.statusLabel = QtWidgets.QLabel(self)
        self.statusLabel.setGeometry(QtCore.QRect(580, 2, 250, 60))
        self.statusLabel.setText(
            'Статус: <font style="color: rgb(0, 255, 0);">good</font>'
        )
        self.statusLabel.setFont(QtGui.QFont("Times", 15))

        self.imageLabelBg = QWidget(self)
        self.imageLabelBg.setGeometry(QtCore.QRect(10, 65, 800, 350))
        self.imageLabelBg.setObjectName("imageLabelBg")

        self.smallTable = QtWidgets.QTableWidget(self)
        self.smallTable.setGeometry(QtCore.QRect(5, 420, 450, 55))
        self.smallTable.setObjectName("smallTable")
        self.smallTable.setColumnCount(3)
        self.smallTable.setRowCount(1)
        self.smallTable.setFont(QtGui.QFont("Times", 11))
        self.smallTable.setHorizontalHeaderLabels(["Время", "Id", "Допуск"])
        self.smallTable.verticalHeader().hide()
        self.smallTable.setColumnWidth(0, 200)

        self.smallTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.smallTable.setStyleSheet(
            "background-color: white;"
            "border-width: 0;"
            "border-radius: 0;"
            "border-color: white"
        )

        font = self.smallTable.horizontalHeader().font()
        font.setPointSize(11)
        for i in range(3):
            self.smallTable.horizontalHeaderItem(i).setFont(font)

        self.bigTable = QtWidgets.QTableWidget(self)
        self.bigTable.setGeometry(QtCore.QRect(5, 485, 810, 130))
        self.bigTable.setObjectName("bigTable")
        self.bigTable.setColumnCount(7)
        self.bigTable.setRowCount(2)
        self.bigTable.setFont(QtGui.QFont("Times", 11))
        self.bigTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.bigTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.bigTable.setHorizontalHeaderLabels(
            [
                "Длина",
                "Ширина",
                "Положение",
                "Диагональ",
                "Поворот",
                "Прямоуг-ть",
                "Загрязн-е",
            ]
        )
        self.bigTable.setVerticalHeaderLabels(
            ["Номинальные значения", "Измеренные значения"]
        )
        self.bigTable.setStyleSheet(
            "background-color: white;"
            "border-width: 0;"
            "border-radius: 0;"
            "border-color: white"
        )
        for i in range(7):
            self.bigTable.horizontalHeaderItem(i).setFont(font)
            font.setPointSize(11)

        for i in range(2):
            self.bigTable.verticalHeaderItem(i).setFont(font)

        self.previousButton = QtWidgets.QPushButton(self)
        self.previousButton.setGeometry(QtCore.QRect(10, 620, 160, 50))
        self.previousButton.setObjectName("pushButton")
        self.previousButton.setText("Предыдущий элемент")
        self.previousButton.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.previousButton.setFont(QtGui.QFont("Times", 11))
        self.previousButton.clicked.connect(
            lambda: self.new_detailed_win(int(self.Id) - 1)
        )

        self.nextButton = QtWidgets.QPushButton(self)
        self.nextButton.setGeometry(QtCore.QRect(180, 620, 160, 50))
        self.nextButton.setObjectName("pushButton_2")
        self.nextButton.setText("Следущий элемент")
        self.nextButton.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.nextButton.setFont(QtGui.QFont("Times", 11))
        self.nextButton.clicked.connect(
            lambda: self.new_detailed_win(int(self.Id) + 1)
        )

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setGeometry(QtCore.QRect(690, 620, 100, 50))
        self.exitButton.setObjectName("pushButton_5")
        self.exitButton.setText("Закрыть")
        self.exitButton.setStyleSheet(
            "background-color: white;"
            "border-width: 1;"
            "border-radius: 4;"
            "border-style: solid;"
            "border-color: rgb(0, 0, 0)"
        )
        self.exitButton.setFont(QtGui.QFont("Times", 12))
        iconex = QtGui.QIcon("icons/krest.png")
        self.exitButton.setIcon(iconex)
        self.exitButton.setIconSize(QtCore.QSize(20, 20))
        self.exitButton.clicked.connect(self.close)

    def setupImage(
        self, data
    ):  ######################################################################################################## стереть data и убрать коментарий со следущей строки
        """создаем график"""
        # data = json.dumps(data)
        data = [
            [[5, 5, 7, 10, 10, 5], [20, 13, 10, 10, 20, 20]],
            [[6, 8, 10], [18, 15, 12]],
        ]  # это пример данных, его потом нужно удалить и добавить data = json.dumps(data) для распаковки json

        self.graph = Graph(data)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.graph)
        self.imageLabelBg.setLayout(self.layout)
        return 0

    def setupTables(self):
        """настраиваем таблицы и заполняеми значениями"""
        names = ["date", "id", "tolerance"]
        names2 = [
            "length_n",
            "length_f",
            "width_n",
            "width_f",
            "position_n",
            "position_f",
            "diag_n",
            "diag_f",
            "turn_n",
            "turn_f",
            "squareness_n",
            "squareness_f",
            "spot_n",
            "spot_f",
        ]
        try:
            data = sql_test_module.sql_search_data(self.Id)
            self.setupImage(data["image"])

            stat = {
                "1": 'rgb(0,150,0);">Норма</font>',
                "2": 'rgb(210,210,0);">Предупреждение</font>',
                "3": 'rgb(255,0,0);">Брак</font>',
            }
            data2 = sql_test_module.settingsData(data["tolerance"])[1]
            names3 = [
                "length_overlarge_"
                if float(data["length_f"]) >= 0
                else "length_extrasmall_",
                "width_overlarge_"
                if float(data["width_f"]) > 0
                else "width_extrasmall_",
                "position_",
                "diag_",
                "turn_",
                "squareness_",
                "spot_",
            ]

            self.statusLabel.setText(
                'Статус: <font style="color:' + stat[str(data["status"])]
            )

            for i in range(3):
                self.smallTable.setItem(
                    0, i, QTableWidgetItem(str(data[names[i]]))
                )

            for i in range(0, 14, 2):
                if i not in [10, 8, 12]:
                    self.bigTable.setItem(
                        0, i // 2, QTableWidgetItem(str(data[names2[i]]))
                    )
                    self.bigTable.setItem(
                        1, i // 2, QTableWidgetItem(str(data[names2[i + 1]]))
                    )
                    if abs(float(data[names2[i + 1]])) >= float(
                        data2[names3[i // 2] + "b"]
                    ):
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(255, 0, 0)
                        )
                    elif abs(float(data[names2[i + 1]])) < float(
                        data2[names3[i // 2] + "w"]
                    ):
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(0, 150, 0)
                        )
                    else:
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(210, 210, 0)
                        )
                elif i == 10:
                    sq = data["squareness_f"]
                    self.bigTable.setItem(0, 5, QTableWidgetItem("1"))
                    self.bigTable.setItem(1, 5, QTableWidgetItem(str(sq)))
                    if sq == "0":
                        self.bigTable.item(1, 5).setForeground(QColor(255, 0))
                    else:
                        self.bigTable.item(1, 5).setForeground(
                            QColor(0, 150, 0)
                        )
                elif i == 8:
                    sq = abs(float(data["turn_f"]))
                    self.bigTable.setItem(0, 4, QTableWidgetItem("0"))
                    self.bigTable.setItem(
                        1, 4, QTableWidgetItem(str(data["turn_f"]))
                    )
                    if sq >= float(data2[names3[i // 2] + "b"]):
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(255, 0, 0)
                        )
                    elif sq < float(data2[names3[i // 2] + "w"]):
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(0, 150, 0)
                        )
                    else:
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(210, 210, 0)
                        )
                else:
                    sq = abs(float(data["spot_f"]))
                    self.bigTable.setItem(0, 6, QTableWidgetItem("0"))
                    self.bigTable.setItem(
                        1, 6, QTableWidgetItem(str(data["spot_f"]))
                    )
                    if sq >= float(data2[names3[i // 2] + "b"]):
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(255, 0, 0)
                        )
                    elif sq < float(data2[names3[i // 2] + "w"]):
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(0, 150, 0)
                        )
                    else:
                        self.bigTable.item(1, i // 2).setForeground(
                            QColor(210, 210, 0)
                        )
        except:
            self.errorsig.emit()

    def new_detailed_win(self, id):
        """создание нового детального экрана и закрытие текущего"""
        try:
            p = int(sql_test_module.last_item_id())
        except:
            self.errorsig.emit()
        if id <= p and id >= 1:
            Detailed(str(id))
            self.close()
        else:
            msg = QMessageBox()
            msg.about(self, "Ошибка", "Это последний элемент")
            msg.setIcon(QMessageBox.Warning)
