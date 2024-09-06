from PyQt6 import QtCore
from PyQt6.QtGui import QColor, QPainter, QPixmap, QPen
from PyQt6.QtWidgets import QLabel, QMessageBox, QApplication
from time import sleep

from stack import Stack

app = QApplication([])
msg = QMessageBox()
msg.setWindowTitle("Ошибка")
msg.setText("Затравочный пиксель находиться на границе фигуры!")

msg.exec()


def show_error_message():
    msg.show()


class Draw():
    """Класс для реализации рисования различных объектов на пиксельном полотне."""
    edges_color = QColor(1, 1, 1)  # Цвет для граней фигуры.
    outline_color = QColor(2, 2, 2)  # Цвет для обводки.
    background_color = QColor(255, 255, 255)  # Цвет фона.

    list1 = list()

    def __init__(self, painter: QPainter, label: QLabel, pixmap: QPixmap):
        super().__init__()

        self.painter = painter
        self.label = label
        self.pixmap = pixmap
        self.image = pixmap.toImage()

        self.stack = Stack()

        self.setPainterColor(self.edges_color)

    def updateImageInformation(self):
        """Обновляет информацию о пикселях."""
        self.image = self.pixmap.toImage()

    def _updatePixmap(self):
        """Обновляет состояние полотна пикселей."""
        self.label.setPixmap(self.pixmap)

    def setPainterColor(self, color: QColor):
        """Устанавливает цвет ручки."""
        self.color = color
        self.painter.setPen(QPen(self.color, 1))

    def drawPixel(self, point: tuple):
        """Рисует один пиксель."""
        x, y = point

        self.painter.drawPoint(x, y)

    def _drawPixelWithColor(self, point: tuple, color: QColor):
        """Позволяет нарисовать один пиксель, отдельно задавая его цвет."""
        self.setPainterColor(color)
        self.drawPixel(point)

    def _length(self, point0, point1) -> int:
        """Вычисляет длину отрезка."""
        x0, y0 = point0
        x1, y1 = point1

        if abs(x1 - x0) >= abs(y1 - y0):
            length = abs(x1 - x0)
        else:
            length = abs(y1 - y0)

        return length

    def _sign(self, number: int) -> int:
        """Возвращает -1, 0, 1 для отрицательного, нулевого и положительного аргумента соответственно."""
        if number < 0:
            return -1
        elif number == 0:
            return 0
        else:
            return 1

    def drawLineSegment(self, point0: tuple, point1: tuple):
        """Рисует отрезок с помощью ЦДА."""
        self.setPainterColor(self.edges_color)

        x0, y0 = point0
        x1, y1 = point1

        length = self._length(point0, point1)

        try:
            dx, dy = (x1 - x0) / length, (y1 - y0) / length
            x, y = x0, y0
        except ZeroDivisionError:
            pass
        else:

            for i in range(length):
                self.drawPixel((round(x), round(y)))

                x += dx
                y += dy

    def fillWithSeed(self, seed_pixel: tuple, color_filling: QColor, delay=False):
        """Алгоритм заполнения с затравкой."""
        self.setPainterColor(color_filling)

        self.stack.push(seed_pixel)

        while self.stack.number_stack_elements != 0:
            pixel = self.stack.pop()
            x, y = pixel

            if self.image.pixelColor(x, y) != color_filling:
                self.drawPixel(pixel)
                self.updateImageInformation()  # Обновление информации о пикселях полотна.

            if (self.image.pixelColor(x, y + 1) != color_filling
                    and self.image.pixelColor(x, y + 1) != self.edges_color):
                self.stack.push((x, y + 1))

            if (self.image.pixelColor(x - 1, y) != color_filling
                    and self.image.pixelColor(x - 1, y) != self.edges_color):
                self.stack.push((x - 1, y))

            if (self.image.pixelColor(x, y - 1) != color_filling
                    and self.image.pixelColor(x, y - 1) != self.edges_color):
                self.stack.push((x, y - 1))

    def fillLineWithSeed(self, seed_pixel: tuple, color_filling: QColor, delay=False):
        """Алгоритм построчного заполнения с затравкой."""
        self.setPainterColor(color_filling)

        if self.image.pixelColor(seed_pixel[0], seed_pixel[1]) == self.edges_color:
            show_error_message()

            return

        self.stack.push(seed_pixel)

        while self.stack.number_stack_elements != 0:
            self.updateImageInformation()  # Обновление информации о пикселях полотна.
            pixel = self.stack.pop()
            x, y = pixel

            self.drawPixel(pixel)

            tmp_x, tmp_y = x, y

            # Заполнение интервала справа от затравки.
            x = tmp_x + 1
            while self.image.pixelColor(x, y) != self.edges_color:
                self.drawPixel((x, y))
                x += 1

            x_right = x - 1

            # Заполнение интервала слева от затравки.
            x = tmp_x - 1
            while self.image.pixelColor(x, y) != self.edges_color:
                self.drawPixel((x, y))
                x -= 1

            x_left = x + 1

            # Проход по верхней строке.
            x = x_left
            y = tmp_y - 1
            while x <= x_right:
                flag = False

                while (self.image.pixelColor(x, y) != self.edges_color
                       and self.image.pixelColor(x, y) != color_filling and x < x_right):

                    flag = True
                    x += 1

                if flag:
                    if (x == x_right and self.image.pixelColor(x, y) != self.edges_color
                            and self.image.pixelColor(x, y) != color_filling):
                        self.stack.push((x, y))
                    else:
                        self.stack.push((x - 1, y))

                    flag = False

                x_beg = x
                while ((self.image.pixelColor(x, y) == self.edges_color or self.image.pixelColor(x, y) == color_filling)
                       and x <= x_right):
                    x += 1

                if x == x_beg:
                    x += 1

            # Проход по нижней строке.
            x = x_left
            y = tmp_y + 1
            while x <= x_right:
                flag = False

                while (self.image.pixelColor(x, y) != self.edges_color
                       and self.image.pixelColor(x, y) != color_filling and x < x_right):
                    if not flag:
                        flag = True
                    x += 1

                if flag:
                    if (x == x_right and self.image.pixelColor(x, y) != self.edges_color
                            and self.image.pixelColor(x, y) != color_filling):
                        self.stack.push((x, y))
                    else:
                        self.stack.push((x - 1, y))

                    flag = False

                x_beg = x
                while ((self.image.pixelColor(x, y) == self.edges_color or self.image.pixelColor(x, y) == color_filling)
                       and x <= x_right):
                    x += 1

                if x == x_beg:
                    x += 1

            if delay:
                self._updatePixmap()
                QtCore.QCoreApplication.processEvents()
                sleep(0.025)
