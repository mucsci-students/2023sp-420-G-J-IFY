#!/usr/bin/env

################################################################################
# MainWindow.py
# Author: Isaak Weidman
# Date of Creation: 02-18-2023
#
# CLASSES:
#   MainWindow()
#
# FUNCTIONS:
#
#
################################################################################

import sys, os
filePath = os.path.dirname(__file__)
sys.path.append(filePath)

from SimpleBCluster import simpleButtonCluster
from StatsPanel import StatsPanel
from PyQt6.QtGui import (
    QAction,
    QFont,
)
from PyQt6.QtCore import (
    Qt,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
    QMenuBar,
    QMenu,
    QToolBar,
    QStatusBar,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QLabel,
    QProgressBar,
    QTextEdit,
    QLineEdit,
    QSpacerItem,
)

################################################################################
# class MainWindow()
#
# DESCRIPTION:
#   represents the main window of the application, handles overall layout
#
# ARGUMENTS:
#   *args : 
#
#   **kwargs :
#
#
################################################################################
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Tentative placeholder
        self.setWindowTitle('Spelling Bee')
        self.setGeometry(100, 100, 700, 400)
        

        # Creation Functions
        self._createCentralWidget()
        self._createMenuBar()
        self._createToolBar()
        self._createStatsBar()
        

    ############################################################################
    #
    ############################################################################
    def _createMenuBar(self):

        # Create manu bar
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        windowMenu = menuBar.addMenu('&Window')
        helpMenu = menuBar.addMenu('Help')
        
        action = QAction('A menu action', self)
        fileMenu.addAction(action)
        windowMenu.addAction(action)
        helpMenu.addAction(action)


    ############################################################################
    #
    ############################################################################
    def _createToolBar(self):
        toolBar = QToolBar('Tools', self)
        toolBar.setMovable(False)

        saveAction = QAction('Save', self)
        loadAction = QAction('Load', self)
        statsAction = QAction('Stats', self)
        helpAction = QAction('Help', self)

        toolBar.addAction(saveAction)
        toolBar.addAction(loadAction)
        toolBar.addAction(statsAction)
        toolBar.addAction(helpAction)

        self.addToolBar(toolBar)


    ############################################################################
    #
    ############################################################################
    def _createStatsBar(self):
        statsBar = QToolBar('Stats', self)
        statsBar.setMovable(False)

        statsPanel = StatsPanel(statsBar)
        
        statsBar.addWidget(statsPanel)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, statsBar)


    ############################################################################
    #
    ############################################################################
    def _createCentralWidget(self):
    
        centralWidget = simpleButtonCluster(
            self,
            ['S', 'A', 'M', 'P', 'L', 'E', 'D']
        )

        self.setCentralWidget(centralWidget)


def main():
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()