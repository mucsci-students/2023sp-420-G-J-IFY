#!/usr/bin/env

###############################################################################
# HexCluster.py
# Author: Isaak Weidman
# Date of Creation: 02-25-2023
#
# Classes:
#
# Functions:
#
###############################################################################

import os
import math
from PyQt6.QtCore import (
    Qt,
    QRect,
    QRectF,
    QPointF
)
from PyQt6.QtGui import (
    QMouseEvent,
    QPainter,
    QPen,
    QBrush,
    QColor,
    QFont,
    QPolygonF,
    QPixmap,
    QFontDatabase,
)
from PyQt6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QPushButton,
    QLabel,
)


###############################################################################
# class HexCluster()
#
# DESCRIPTION:
#   Cluster of 7 hexagon buttons arranged in a honey-comb pattern.
#
# ARGUMENTS:
#   parent : QWidget
#     - parent widget
#   letters : list[str]
#    - list of 7 key letters
# ATTRIBUTES:
#   buttons:
#     - list of 7 HexButtons, one for each key letter
###############################################################################
class HexCluster(QWidget):
    def __init__(
            self,
            parent: QWidget,
            letters: list[str],
            keyLet: str,
            *args,
            **kwargs):
        super(HexCluster, self).__init__(parent, *args, **kwargs)

        self.buttons: list[HexButton] = []
        self.keyLet = keyLet

        self._addButtons(letters)
        self._arrangeButtons()

    ###########################################################################
    # setLetters(legends: list[str]) -> None:
    #
    # Change key letters
    ###########################################################################
    def setLetters(self, legends: list[str]) -> None:
        for i, c in enumerate(legends):
            self.buttons[i].text = c

    ###########################################################################
    # _addButtons()
    #
    # DESCRIPTION:
    #   loops through list of characters and creats a HexButton for each one
    #
    # PARAMS:
    #   legends : list[str]
    #     - list of 7 characters to be 'printed' on each key
    ###########################################################################
    def _addButtons(self, legends: list[str]) -> None:
        for c in legends:
            button = HexButton(self, c)
            self.buttons.append(button)

        self.buttons[0].setColor(QColor('#FFCC2F'))

    ###########################################################################
    # _arrangeButtons()
    #
    # DESCRIPTIONS:
    #   places buttons in a honey comb formation
    ###########################################################################
    def _arrangeButtons(self):

        height = self.buttons[0].height
        width = self.buttons[0].width

        xpad = 10
        ypad = int(math.sqrt(xpad**2 - (xpad / 2)**2))

        posx = int(width / 2 + xpad / 2)
        posy = 0

        self.buttons[1].move(posx, posy)
        posx += width + xpad
        self.buttons[2].move(posx, posy)

        posx = 0
        posy += int((3 * height / 4) + ypad)
        self.buttons[3].move(posx, posy)
        posx += width + xpad
        self.buttons[0].move(posx, posy)
        posx += width + xpad
        self.buttons[4].move(posx, posy)

        posx = int(width / 2 + xpad / 2)
        posy += int((3 * height / 4) + ypad)
        self.buttons[5].move(posx, posy)
        posx += width + xpad
        self.buttons[6].move(posx, posy)

        self.setMinimumHeight(int(((5 / 2) * height) + (2.5 * ypad)))
        self.setMinimumWidth(int((3 * width) + (2.5 * xpad)))


###############################################################################
# class HexButton()
#
# DESCRIPTION:
#   A custom QPushButton object that overrides the paint event to paint a
#   a hexagonal button with a label centered on the button.
#
# ARGUMENTS:
#   parent : QWidget | None
#     - the parent widget
#   text : str
#     - button label
#
# ATTRIBUTES:
#   color : QColor
#     - Overall color of the button
#   textColor : QColor
#     - Color of the text
#   text : str
#     - button label
#   height : int
#     - height of the button
#   width : int
#     - width of the button
#   x : int
#     - x coord of the top left corner of the buttons bounding box
#   y : int
#     - y coord of the top left corner of the buttons bounding box
#   boundingBox : QRect
#     - boundingBox of the hexagon
#   hexagon : QPolygonF
#     - object representing the coords of all 6 points of the hexagon
#
# FUNCTIONS:
#   setColor(color : QColor)
#
#   setTextColor(color : QColor)
#
#   setSize(color : QColor)
#
###############################################################################
class HexButton(QPushButton):
    def __init__(
        self,
        parent: QWidget | None,
        text: str,
        *args,
        **kwargs
    ):
        super(HexButton, self).__init__(parent, *args, **kwargs)

        self.color = QColor(210, 210, 210)
        self.textColor = QColor(Qt.GlobalColor.black)
        self.text = text
        self.height = 90
        self.width = int(45 * math.sqrt(3))
        self.x = 3
        self.y = 3
        self.boundingBox = QRect(self.x, self.y + 1, self.width, self.height)
        self.radius = self.height / 2
        self.hexagon = self._calcHex()
        self.setFlat(True)
        self.setText(text)

        self.setMinimumSize(self.width + 10, self.height + 10)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )

    ###########################################################################
    # setColor(self, color : QColor) -> None
    #
    # DESCRIPTION:
    #   set the color of the button
    #
    # PARAMS:
    #   color : QColor
    #     - color of the button
    ###########################################################################
    def setColor(self, color: QColor) -> None:
        self.color = color

    ###########################################################################
    # setTextColor(color : QColor) -> None
    #
    # DESCRIPTION:
    #   sets the color of the button's text
    #
    # PARAMS:
    #   color : QColor
    #     - color of the text
    ###########################################################################
    def setTextColor(self, color: QColor) -> None:
        self.textColor = color

    ###########################################################################
    # setSize(size : int) -> None:
    #
    # DESCRIPTION:
    #   sets the buttons size
    #
    # PARAMS:
    #   size : int
    #     - height of the button. Width is calculated based on 30-60-90
    #       triangle where height/2 = hypotenuse, hex side length, and
    #       hyp * root 3 = base length.
    ###########################################################################
    def setSize(self, size: int) -> None:
        self.height = size
        self.width = int((self.height / 2) * math.sqrt(3))

    ###########################################################################
    # paintEvent(event) -> None
    #
    # DESCRIPTION:
    #   paints hexagon rather than rectangular button
    #
    # PARAMS:
    #   event : QEvent
    #     - event signaling repaint of button
    ###########################################################################
    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self._drawHex(painter)
        self._drawText(painter)
        painter.end()

    ###########################################################################
    # mousePressEvent(self, e: QMouseEvent) -> None:
    #
    # DESCRIPTION
    #   Makes buttons smaller when pressed
    ###########################################################################
    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.radius -= 2
        return super().mousePressEvent(e)

    ###########################################################################
    # mouseReleaseEvent(self, e: QMouseEvent) -> None:
    #
    # DESCRIPTION
    #   returns buttons to original size when button is released
    ###########################################################################
    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.radius += 2
        return super().mouseReleaseEvent(e)

    ###########################################################################
    # _drawBoundingBox(painter : QPainter) -> None
    #
    # DESCRIPTION:
    #   draws the bounding box around the hexagon. Helps with manual
    #   positioning
    #
    # PARAMS:
    #   painter : QPainter
    #     - painter object that paints the rectangle
    ###########################################################################
    def _drawBoundingBox(self, painter: QPainter) -> None:
        pen = QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine)
        box = QRect(0, 0, self.width, self.height)

        painter.setPen(pen)
        painter.drawRect(box)

    ###########################################################################
    # _drawHex(painter : QPainter) -> None:
    #
    # DESCRIPTION:
    #   draws a hexagon filled with a pre-defined color
    #
    # PARAMS:
    #   painter : QPainter
    #     - painter object that paints the hexagon
    ###########################################################################
    def _drawHex(self, painter: QPainter) -> None:
        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(self.color)
        pen = QPen(self.color, 2, Qt.PenStyle.SolidLine)

        self.hexagon = self._calcHex()

        painter.setBrush(brush)
        painter.drawPolygon(self.hexagon)

        painter.setPen(pen)
        painter.drawPolygon(self.hexagon)

    ###########################################################################
    # _drawText(painter : QPainter) -> None
    #
    # DESCRIPTION:
    #   draws the text label in the center of the button
    #
    # PARMAS:
    #   painter : QPainter
    #     - painter object that draws the text
    ###########################################################################
    def _drawText(self, painter: QPainter) -> None:
        font_id = QFontDatabase.addApplicationFont(
            os.getcwd() + '/fonts/Comfortaa-VariableFont_wght.ttf'
        )
        families = QFontDatabase.applicationFontFamilies(font_id)

        font = QFont()
        font.setFamily(families[0])
        font.setBold(True)
        font.setPointSize(25)

        pen = QPen()
        pen.setColor(self.textColor)

        painter.setFont(font)
        painter.setPen(pen)

        painter.drawText(
            self.boundingBox,
            Qt.AlignmentFlag.AlignCenter,
            self.text
        )

    ###########################################################################
    # _calcHex() -> QPolygonF
    #
    # DESCRIPTION:
    #   Creates a hexagon QPolygonF object by calculating the points of a hex
    #     with a bounding box with side length self.size
    # RETURN:
    #   QPolygonF:
    #     - an equilateral hexagon of size radius
    ###########################################################################
    def _calcHex(self) -> QPolygonF:

        hexagon = QPolygonF()

        posX = self.width / 2 + self.x
        posY = self.height / 2 + self.y
        rads = math.pi / 2

        for i in range(6):
            hexagon.append(QPointF(
                posX + math.cos(rads) * self.radius,
                posY + math.sin(rads) * self.radius
            ))
            rads += math.pi / 3

        return hexagon


###############################################################################
# class HexLabel()
#
# DESCRIPTION:
#   A custom widget that draws a label within a hexagon
#
# ARGUMENTS:
#   parent : QWidget | None,
#     - This widgets parent widget
#   text : str | None,
#     - The label text
#   radius : int | None,
#     - The radius of the hexagon
#   color : str | None,
#     - The color of the hexagon (hex value, or QColor)
#   pos : tuple [int, int] | None
#     - The positional coordinates for the top left corner of the bounding box
# ATTRIBUTES:
#
# FUNCTIONS:
###############################################################################
class HexLabel(QWidget):
    def __init__(
        self,
        parent: QWidget | None,
        text: str = '',
        radius: int = 20,
        pos: tuple[int, int] = (0, 0),
        *args,
        **kwargs
    ):
        super(HexLabel, self).__init__(parent, *args, **kwargs)

        self._lbl = QLabel()
        self._text = text
        self._x = pos[0] + 12
        self._y = pos[1] + 12
        self._radius = radius
        self._width = radius * math.sqrt(3)
        self._height = radius * 2
        self._hex = calcHex(radius, self._x, self._y)
        self._color = Qt.GlobalColor.gray
        self._font = QFont('Helvetica', 12)
        self._fontColor = Qt.GlobalColor.black
        self._canvas = QPixmap(int(self._width), int(self._height))
        self._initUI()

    def _initUI(self):
        self._lbl.setFixedSize(
            int(self._width),
            int(self._height)
        )
        self._lbl.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        layout = QVBoxLayout()
        layout.addWidget(self._lbl)
        self.setLayout(layout)

    ###########################################################################
    # _drawHex(painter : QPainter) -> None:
    #
    # DESCRIPTION:
    #   draws a hexagon filled with a pre-defined color
    #
    # PARAMS:
    #   painter : QPainter
    #     - painter object that paints the hexagon
    ###########################################################################
    def _drawHex(self, painter: QPainter) -> None:

        brush = QBrush(Qt.BrushStyle.SolidPattern)
        brush.setColor(QColor(self._color))
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setColor(QColor(self._color))

        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawPolygon(self._hex)

    ###########################################################################
    # _drawText(painter : QPainter) -> None
    #
    # DESCRIPTION:
    #   draws the text label in the center of the button
    #
    # PARMAS:
    #   painter : QPainter
    #     - painter object that draws the text
    ###########################################################################
    def _drawText(self, painter: QPainter) -> None:
        font = self._font

        pen = QPen()
        pen.setColor(self._fontColor)

        painter.setFont(font)
        painter.setPen(pen)

        painter.drawText(
            QRectF(self._x, self._y, self._width, self._height),
            Qt.AlignmentFlag.AlignCenter,
            self._text
        )

    ###########################################################################
    # setFont(font: QFont) -> None
    #
    # DESCRIPTION:
    #   Sets the label font to provided QFont
    ###########################################################################
    def setFont(self, font: QFont) -> None:
        self._font = font

    ###########################################################################
    # setFontColor(color: QColor) -> None
    #
    # DESCRIPTION:
    #   Sets the label font to provided QFont
    ###########################################################################
    def setFontColor(self, color: QColor) -> None:
        self._fontColor = color

    ###########################################################################
    # setColor(color: QColor) -> None
    #
    # DESCRIPTION:
    #   Sets the hex color to provided QColor
    ###########################################################################
    def setColor(self, color: QColor) -> None:
        self._color = color

    ###########################################################################
    # setText(text: str) -> None
    #
    # DESCRIPTION:
    #   sets the text to provided string
    ###########################################################################
    def setText(self, text: str) -> None:
        self._text = text

    ###########################################################################
    # paintEvent(event) -> None
    #
    # DESCRIPTION:
    #   paints hexagon rather than rectangular button
    #
    # PARAMS:
    #   event : QEvent
    #     - event signaling repaint of button
    ###########################################################################
    def paintEvent(self, event) -> QPixmap:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self._drawHex(painter)
        self._drawText(painter)
        painter.end()


###############################################################################
# calcHex() -> QPolygonF
#
# DESCRIPTION:
#   Creates a hexagon QPolygonF object by calculating the points of a hex
#     with a bounding box with side length self.size
# RETURN:
#   QPolygonF:
#     - an equilateral hexagon of size radius
###############################################################################
def calcHex(radius: int, x, y) -> QPolygonF:
    hexagon = QPolygonF()
    # radius is from point to point.
    # minor radius is from edge to edge and is given by the following
    minorRad = radius * (math.sqrt(3) / 2)

    posX = minorRad + x
    posY = radius + y
    rads = math.pi / 2

    # calculate and append coords to each corner of the hex
    for i in range(6):
        hexagon.append(QPointF(
            posX + math.cos(rads) * radius,
            posY + math.sin(rads) * radius
        ))

        rads += math.pi / 3

    return hexagon
