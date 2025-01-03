import sys

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, Signal, Slot, QAbstractItemModel
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QTableView, QPushButton, QApplication, QWidget, QLabel


# подумать как реализовать бота,
# игра с ботом будет пошаговой
# после решить как реализовать режимы игры,
# подумать как реализовать логику игры

class XvOModel(QAbstractTableModel):
    endGame = Signal()

    def __init__(self, game_mod, parent=None):
        super().__init__(parent)
        self.game_mod = game_mod
        self.count_mot = 0
        if game_mod == 1:
            self.__data = [[' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ']]
        else:
            self.__data = [[' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', 'O', ' ', ' '],
                           [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ']]
            self.count_mot = 1
        self.__head_col = [i for i in range(len(self.__data))]
        self.__head_row = [i for i in range(len(self.__data[0]))]
        self.game_mod = game_mod
        self.flag_ap_left = False
        self.flag_ap_top = False
        self.flag_end_game = False

    def rowCount(self, parent=None):
        return len(self.__data)

    def columnCount(self, parent=None):
        return len(self.__data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return f"{self.__data[index.row()][index.column()]}"
        elif role == Qt.EditRole:
            return self.__data[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            if self.flag_end_game:  # тут типа можно в конце закрасить выйгрыш но потом
                pass
            if self.__data[index.row()][index.column()] == "O":
                return QColor('#CCE5FF')
            if self.__data[index.row()][index.column()] == "X":
                return QColor('#FFCCCC')
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if self.game_mod == 1:
                self.flag_ap_top = False
                self.flag_ap_left = False
                if self.__data[index.row()][index.column()] == " ":
                    if self.count_mot % 2 == 0:
                        self.current_elem = "O"
                        self.__data[index.row()][index.column()] = "O"
                        self.count_mot += 1
                    elif self.count_mot % 2 == 1:
                        self.current_elem = "X"
                        self.__data[index.row()][index.column()] = "X"
                        self.count_mot += 1

                if index.row() == 0 and index.column() == len(self.__data[0]) - 1:  # угл правый верхний
                    self.append_top()
                    self.append_right()
                elif index.row() == 0 and index.column() == 0:  # угл левый верхний
                    self.append_top()
                    self.append_left()
                elif index.row() == len(self.__data) - 1 and index.column() == len(
                        self.__data[0]) - 1:  # угл правый нижний
                    self.append_bot()
                    self.append_right()
                elif index.row() == len(self.__data) - 1 and index.column() == 0:  # угл левый нижний
                    self.append_bot()
                    self.append_left()
                elif index.row() == 0:  # верх
                    self.append_top()
                elif index.row() == len(self.__data) - 1:  # низ
                    self.append_bot()
                elif index.column() == 0:  # лево
                    self.append_left()
                elif index.column() == len(self.__data[0]) - 1:  # право
                    self.append_right()
                self.flag_end_game = self.check_win(index.row(), index.column(), self.current_elem)
                if self.flag_end_game:
                    self.endGame.emit()
                return True
            if self.game_mod == 2:
                self.flag_ap_top = False
                self.flag_ap_left = False
                if self.__data[index.row()][index.column()] == " ":
                    if self.count_mot % 2 == 1:
                        self.current_elem = "X"
                        self.__data[index.row()][index.column()] = "X"
                        self.count_mot += 1

                if index.row() == 0 and index.column() == len(self.__data[0]) - 1:  # угл правый верхний
                    self.append_top()
                    self.append_right()
                elif index.row() == 0 and index.column() == 0:  # угл левый верхний
                    self.append_top()
                    self.append_left()
                elif index.row() == len(self.__data) - 1 and index.column() == len(
                        self.__data[0]) - 1:  # угл правый нижний
                    self.append_bot()
                    self.append_right()
                elif index.row() == len(self.__data) - 1 and index.column() == 0:  # угл левый нижний
                    self.append_bot()
                    self.append_left()
                elif index.row() == 0:  # верх
                    self.append_top()
                elif index.row() == len(self.__data) - 1:  # низ
                    self.append_bot()
                elif index.column() == 0:  # лево
                    self.append_left()
                elif index.column() == len(self.__data[0]) - 1:  # право
                    self.append_right()
                self.flag_end_game = self.check_win(row=index.row(), col=index.column(), elem="X")
                if self.flag_end_game:
                    self.endGame.emit()
                else:

                    self.flag_ap_top = False
                    self.flag_ap_left = False
                    self.count_mot += 1
                    if self.count_mot % 2 == 1:
                        self.current_elem = "O"
                    bot_mot = self.computer(index.row(), index.column())

                    if bot_mot[0] == 0 and bot_mot[1] == len(self.__data[0]) - 1:  # угл правый верхний
                        self.append_top()
                        self.append_right()
                    elif bot_mot[0] == 0 and bot_mot[1] == 0:  # угл левый верхний
                        self.append_top()
                        self.append_left()
                    elif bot_mot[0] == len(self.__data) - 1 and bot_mot[1] == len(
                            self.__data[0]) - 1:  # угл правый нижний
                        self.append_bot()
                        self.append_right()
                    elif bot_mot[0] == len(self.__data) - 1 and bot_mot[1] == 0:  # угл левый нижний
                        self.append_bot()
                        self.append_left()
                    elif bot_mot[0] == 0:  # верх
                        self.append_top()
                    elif bot_mot[0] == len(self.__data) - 1:  # низ
                        self.append_bot()
                    elif bot_mot[1] == 0:  # лево
                        self.append_left()
                    elif bot_mot[1] == len(self.__data[0]) - 1:  # право
                        self.append_right()
                    self.flag_end_game = self.check_win(bot_mot[0], bot_mot[1], "O")
                    if self.flag_end_game:
                        self.endGame.emit()
                return True
        return False

    def flags(self, index):
        """Returns an appropriate value for the item's flags. Valid items are
           enabled, selectable, and editable."""
        if not index.isValid() or self.flag_end_game:
            return Qt.ItemIsEnabled
        return super().flags(index) | Qt.ItemIsEditable

    def insertRows(self, row, count, parent=QModelIndex()):
        if row < 0 or count < 1:
            return False
        self.beginInsertRows(parent, row, row + count - 1)
        self.endInsertRows()
        return True

    def insertColumns(self, column, count, parent=QModelIndex()):
        if column < 0 or count < 1:
            return False
        self.beginInsertColumns(parent, column, column + count - 1)
        self.endInsertColumns()
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.__head_col[section]
        if orientation == Qt.Vertical:
            return self.__head_row[section]
        return section

    def append_top(self):
        self.__data.insert(0, [" " for i in range(len(self.__data[0]))])
        self.__head_row = [i for i in range(len(self.__data))]
        self.insertRow(0)
        self.flag_ap_top = True

    def append_bot(self):
        self.__data.append([" " for i in range(len(self.__data[0]))])
        self.__head_row = [i for i in range(len(self.__data))]
        self.insertRow(len(self.__data) - 1)

    def append_left(self):
        for i in range(len(self.__data)):
            self.__data[i].insert(0, " ")
        self.__head_col = [i for i in range(len(self.__data[0]))]
        self.insertColumns(0, 1)
        self.flag_ap_left = True

    def append_right(self):
        for i in range(len(self.__data)):
            self.__data[i].append(" ")
        self.__head_col = [i for i in range(len(self.__data[0]))]
        self.insertColumns(len(self.__data) - 1, 1)

    def check_win(self, row, col, elem):
        count_elem = 0
        # проход слева на право
        check_left_from = col - 4
        check_left_to = col + 5 + self.flag_ap_left
        # print(index)
        while check_left_from < 0:
            check_left_from += 1

        while check_left_to > len(self.__data[0]):
            check_left_to -= 1

        for i in range(check_left_from, check_left_to):
            if self.__data[row][i] == elem:
                count_elem += 1
            else:
                count_elem = 0
            if count_elem == 5:
                return True

        # проход снизу вверх
        check_top_from = row - 4
        check_top_to = row + 5 + self.flag_ap_top

        while check_top_from < 0:
            check_top_from += 1
        #
        while check_top_to > len(self.__data):
            check_top_to -= 1
        for i in range(check_top_from, check_top_to):
            if self.__data[i][col] == elem:
                count_elem += 1
            else:
                count_elem = 0
            if count_elem == 5:
                return True

        # по диагонали в сверху слева на низ право
        for i in range(-5, 6):
            if row + i + self.flag_ap_top < 0 or col + i + self.flag_ap_left < 0:
                continue
            if row + i + self.flag_ap_top >= len(self.__data) or col + i + self.flag_ap_left >= len(self.__data[0]):
                continue
            if self.__data[row + i + self.flag_ap_top][col + i + self.flag_ap_left] == elem:
                count_elem += 1
            else:
                count_elem = 0
            if count_elem == 5:
                return True

        # по диагонали в снизу слева наверх право

        for i in range(-5, 5):
            if row - i + self.flag_ap_top < 0 or col + i + self.flag_ap_left < 0:
                continue
            if row - i + self.flag_ap_top >= len(self.__data) or col + i + self.flag_ap_left >= len(
                    self.__data[0]):
                continue
            if self.__data[row - i + self.flag_ap_top][
                col + i + self.flag_ap_left] == elem:
                count_elem += 1
            else:
                count_elem = 0
            if count_elem == 5:
                return True

        return False

    def check_price(self, board, row, col, elem):  # возвращает цену для клетки со стороны крестика
        price = 1
        count_elem = 0
        # проход слева на право
        check_left_from = col - 4
        check_left_to = col + 5 + self.flag_ap_left

        while check_left_from < 0:
            check_left_from += 1

        while check_left_to > len(board[0]):
            check_left_to -= 1

        for i in range(check_left_from, check_left_to):
            if board[row][i] == elem:
                count_elem += 1
                price += 1 * count_elem
            else:
                count_elem = 0

        # проход снизу вверх
        check_top_from = row - 4
        check_top_to = row + 5 + self.flag_ap_top

        while check_top_from < 0:
            check_top_from += 1
        #
        while check_top_to > len(board):
            check_top_to -= 1

        for i in range(check_top_from, check_top_to):
            if board[i][col] == elem:
                count_elem += 1
                price += 1 * count_elem
            else:
                count_elem = 0

        # по диагонали в сверху слева на низ право

        for i in range(-5, 6):
            if row + i + self.flag_ap_top < 0 or col + i + self.flag_ap_left < 0:
                continue
            if row + i + self.flag_ap_top >= len(board) or col + i + self.flag_ap_left >= len(board[0]):
                continue
            if self.__data[row + i + self.flag_ap_top][col + i + self.flag_ap_left] == elem:
                count_elem += 1
                price += 1 * count_elem
            else:
                count_elem = 0

        # по диагонали в снизу слева наверх право

        for i in range(-5, 5):
            if row - i + self.flag_ap_top < 0 or col + i + self.flag_ap_left < 0:
                continue
            if row - i + self.flag_ap_top >= len(board) or col + i + self.flag_ap_left >= len(
                    board[0]):
                continue
            if board[row - i + self.flag_ap_top][col + i + self.flag_ap_left] == elem:
                count_elem += 1
                price += 1 * count_elem
            else:
                count_elem = 0
        return price

    def computer(self, i, j):
        move = (0, 0, 0)
        price = 0

        row = i
        col = j
        board = [self.__data[i].copy() for i in range(len(self.__data))]
        boardO = [self.__data[i].copy() for i in range(len(self.__data))]
        boardX = [self.__data[i].copy() for i in range(len(self.__data))]
        # self.__data[0+self.count_mot][0+self.count_mot] = "O"
        elem = "X"
        check_left_from = col - 10
        check_left_to = col + 10

        while check_left_from < 0:
            check_left_from += 1

        while check_left_to > len(board[0]):
            check_left_to -= 1

        check_top_from = row - 10
        check_top_to = row + 10

        while check_top_from < 0:
            check_top_from += 1
        #
        while check_top_to > len(board):
            check_top_to -= 1

        best_price = 0
        priceO = 0
        priceX = 0
        best_move = (0, 0, 0)  # i,j,price

        for y in range(check_top_from, check_top_to):
            for x in range(check_left_from, check_left_to):
                if board[y][x] == " ":
                    price = self.check_price(board,y,x,"X")

                    if price > best_price:
                        move = (y,x,price)
                        best_price = price

        # for y in range(check_top_from, check_top_to):
        #     for x in range(check_left_from, check_left_to):
        #         if board[y][x] == " ":
        #             priceX = self.check_price(board,y,x,"X")
        #             priceO = self.check_price(board,y,x,"O")
        #             if priceO >= priceX:
        #                 if priceO > best_price:
        #                     move = (y,x,priceO)
        #                     best_price = priceO
        #             else:
        #                 if priceX > best_price:
        #                     move = (y,x,priceX)
        #                     best_price = priceX

        self.__data[move[0]][move[1]] = "O"
        return move


# алкоритм, в радиусе 5 на 5 от хода крестика расмматриваем поле и считаем
# для каждой клетки выщитываем цену (количество победы) для противника, на максимальное ставим наш кружок

# найти все сочитания из 3их элеметнов в ряду из 5 и проверять на достижимость и выставлять соответствующую цену

# короче 2 класса будет. В начале приложение спрашивает какой режим игр предпочитает. После запускается окно с игроком
# или компьютером и играется. после завершения опять выкидывает на начальный экран
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(700)
        self.setMinimumWidth(1000)

        self.window = QWidget()

        self.mainlayout = QVBoxLayout()

        self.flag_pvp = False
        self.flag_pve = False

        self.view = QTableView()
        self.view.setMinimumWidth(600)
        self.view.setMinimumHeight(600)

        self.label = QLabel("Крестики нолики 5 в ряд")
        self.mainlayout.addWidget(self.label)

        self.button_pvp = QPushButton("Игра с человеком")
        self.button_pve = QPushButton("Игра с компьютером")
        self.button_restart = QPushButton("Начать заново")

        self.mainlayout.addWidget(self.button_pvp)
        self.mainlayout.addWidget(self.button_pve)

        self.button_pvp.clicked.connect(self.pvp)
        self.button_pve.clicked.connect(self.pve)
        self.button_restart.clicked.connect(self.restart)

        self.mainlayout.addWidget(self.view)
        self.view.setVisible(False)

        self.mainlayout.addWidget(self.button_restart)
        self.button_restart.setVisible(False)

        self.window.setLayout(self.mainlayout)
        self.setCentralWidget(self.window)

    def pvp(self):
        self.model = XvOModel(1)
        self.view.setModel(self.model)
        self.model.endGame.connect(self.update)
        self.view.setVisible(True)
        self.button_pvp.setVisible(False)
        self.button_pve.setVisible(False)

        self.button_restart.setVisible(True)

        self.flag_pvp = True

    def pve(self):
        self.model = XvOModel(2)
        self.view.setModel(self.model)
        self.model.endGame.connect(self.update)
        self.view.setVisible(True)

        self.button_pvp.setVisible(False)
        self.button_pve.setVisible(False)

        self.button_restart.setVisible(True)

    def restart(self):
        self.view.setVisible(False)

        self.button_pvp.setVisible(True)
        self.button_pve.setVisible(True)

        self.button_restart.setVisible(False)

        self.label.setStyleSheet("")
        self.label.setText("Крестики нолики 5 в ряд")

    @Slot()
    def update(self):
        if self.model.flag_end_game:
            print(self.model.current_elem)
            # self.label.setStyleSheet("text-color: blue;, font: bold 14px;")
            self.label.setStyleSheet("font: 30pt Comic Sans MS")
            self.label.setText(f"Победил игрок за : {'Нолики' if self.model.current_elem == 'O' else 'Крестики'}")


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
