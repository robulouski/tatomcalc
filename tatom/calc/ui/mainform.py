 #!/usr/bin/env python
#
#  Trade-A-Tron-O-Matic Calc
#  Copyright (C) 2012-2013 Robert Iwancz
#
#  This file is part of Trade-A-Tron-O-Matic Calc.
#
#  Trade-A-Tron-O-Matic Calc is free software: you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  Trade-A-Tron-O-Matic Calc is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with Trade-A-Tron-O-Matic Calc.  If not, see
#  <http://www.gnu.org/licenses/>.
#
############################################################################
#
#  mainform.py
#  Application's main dialog
#  - For better or worse, I'm not using any UI builder tool assistance,
#    it's all handcrafted goodness here...
# 
#
import sys
#import decimal
from PySide.QtCore import *
from PySide.QtGui import *

from tatom.calc import VERSION_STRING, APPLICATION_NAME
from tatom.calc.portfolio import Portfolio
from tatom.calc.position import Position
import tatom.calc.ui.disclaimer

#g_debug = True
g_debug = False

class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.is_updating_port = False
        self.is_updating_pos = False
        self.is_updating_stop = False

        font = QFont(self.font())
        font.setPointSize(10)
        self.setFont(font)

        self.setupMenu()
        self.setupControls()
        self.setWindowTitle("%s - v%s" % (APPLICATION_NAME, VERSION_STRING))

        self.pos = Position(self.riskDollarEdit.value(),
                            self.entryPriceEdit.value())

        self.is_updating_port = True
        #self.stopPriceEdit.setValue(99.9)
        self.stopPriceEdit.setValue(float(self.pos.stop_price))
        self.stopDistEdit.setValue(float(self.pos.stop_distance))
        self.stopPercentEdit.setValue(float(self.pos.stop_percent))
        self.is_updating_port = False

        self.connect(self.totalEdit, SIGNAL("valueChanged(int)"), 
                     self.updateDollarRisk)
        self.connect(self.riskPercentEdit, SIGNAL("valueChanged(double)"), 
                     self.updateDollarRisk)
        self.connect(self.riskDollarEdit, SIGNAL("valueChanged(double)"), 
                     self.updatePercentRisk)

        self.connect(self.entryPriceEdit, SIGNAL("valueChanged(double)"), 
                     self.changedEntryPrice)

        self.connect(self.stopPriceEdit, SIGNAL("valueChanged(double)"), 
                     self.changedStopPrice)
        self.connect(self.stopPercentEdit, SIGNAL("valueChanged(double)"), 
                     self.changedStopPercent)
        self.connect(self.stopDistEdit, SIGNAL("valueChanged(double)"), 
                     self.changedStopDist)

        self.connect(self.qtyEdit, SIGNAL("valueChanged(int)"), 
                     self.changedQty)
        self.updateDollarRisk()
        QTimer.singleShot(1, self.showDisclaimer)

    def setupMenu(self):
        self.menuBar = QMenuBar()
        fileExitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)
        editCopyPortAct = QAction("Copy portfolio", self, shortcut="F2",
                statusTip="Copy portfolio values to clipboard",
                triggered=self.copy_port)
        editCopyPosAct = QAction("Copy position", self, shortcut="F3",
                statusTip="Copy trade position values to the clipboard",
                triggered=self.copy_pos)
        editCopyAllAct = QAction("Copy all values", self,  shortcut="F4",
                statusTip="Copy all values to clipboard",
                triggered=self.copy_all)
        helpAboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.fileMenu = self.menuBar.addMenu("&File")
        #self.fileMenuActions = (#fileNewAction, fileOpenAction, None,
        self.fileMenu.addAction(fileExitAct)

        self.editMenu = self.menuBar.addMenu("&Edit")
        self.editMenu.addAction(editCopyPortAct)
        self.editMenu.addAction(editCopyPosAct)
        self.editMenu.addAction(editCopyAllAct)
        self.editMenu.addSeparator()

        self.helpMenu = self.menuBar.addMenu("&Help")
        self.helpMenu.addAction(helpAboutAct)


    def setupControls(self):
        titleLabel = QLabel("Position Calculator")
        font = QFont(self.font())
        font.setPointSize(14)
        font.setBold(True)
        titleLabel.setFont(font)

        totalLabel = QLabel("Total portfolio value: ")
        self.totalEdit = QSpinBox()
        self.totalEdit.setRange(1000, 99999999)
        self.totalEdit.setValue(10000)
        self.totalEdit.setSingleStep(1000)
        totalLabel.setBuddy(self.totalEdit)

        riskPercentLabel = QLabel("Risk (%): ")
        self.riskPercentEdit = QDoubleSpinBox()
        self.riskPercentEdit.setRange(0.0, 99.9)
        self.riskPercentEdit.setValue(1.0)
        self.riskPercentEdit.setSingleStep(0.25)
        riskPercentLabel.setBuddy(self.riskPercentEdit)

        riskDollarLabel = QLabel("Risk ($): ")
        self.riskDollarEdit = QDoubleSpinBox()
        self.riskDollarEdit.setRange(0.00, 9999999)
        self.riskDollarEdit.setValue(0)
        self.riskDollarEdit.setSingleStep(100)
        riskDollarLabel.setBuddy(self.riskDollarEdit)

        layoutPort = QHBoxLayout()
        layoutPort.addWidget(totalLabel, 0, Qt.AlignLeft)
        layoutPort.addWidget(self.totalEdit,  0, Qt.AlignLeft)
        layoutPort.addWidget(riskPercentLabel, 0, Qt.AlignLeft)
        layoutPort.addWidget(self.riskPercentEdit, 0, Qt.AlignLeft)
        layoutPort.addWidget(riskDollarLabel, 0, Qt.AlignLeft)
        layoutPort.addWidget(self.riskDollarEdit, 0, Qt.AlignLeft)
        self.groupPort = QGroupBox("Portfolio")
        self.groupPort.setLayout(layoutPort)

        #
        # Trade -- stop loss sub-group 
        #
        stopPriceLabel = QLabel("Stop price: ")
        self.stopPriceEdit = QDoubleSpinBox()
        self.stopPriceEdit.setRange(0.00, 99999)
        self.stopPriceEdit.setValue(10)
        self.stopPriceEdit.setSingleStep(1)
        stopPriceLabel.setBuddy(self.stopPriceEdit)

        stopDistLabel = QLabel("Stop size ($): ")
        self.stopDistEdit = QDoubleSpinBox()
        self.stopDistEdit.setRange(0.00, 99999)
        self.stopDistEdit.setValue(10)
        self.stopDistEdit.setSingleStep(1)
        stopDistLabel.setBuddy(self.stopDistEdit)

        stopPercentLabel = QLabel("Stop size (%): ")
        self.stopPercentEdit = QDoubleSpinBox()
        self.stopPercentEdit.setRange(0.0, 9999.9)
        self.stopPercentEdit.setValue(1.0)
        self.stopPercentEdit.setSingleStep(0.25)
        stopPercentLabel.setBuddy(self.stopPercentEdit)

        layoutStop = QGridLayout()
        layoutStop.addWidget(stopPriceLabel, 0, 0)
        layoutStop.addWidget(self.stopPriceEdit, 0, 1)
        layoutStop.addWidget(stopDistLabel, 1, 0)
        layoutStop.addWidget(self.stopDistEdit, 1, 1)
        layoutStop.addWidget(stopPercentLabel, 2, 0)
        layoutStop.addWidget(self.stopPercentEdit, 2, 1)
        self.groupStop = QGroupBox("Stop Loss")
        self.groupStop.setLayout(layoutStop)

        #
        # Trade/Position
        #
        entryPriceLabel = QLabel("Entry Price: ")
        self.entryPriceEdit = QDoubleSpinBox()
        self.entryPriceEdit.setRange(0.00, 99999)
        self.entryPriceEdit.setValue(20)
        self.entryPriceEdit.setSingleStep(1)
        entryPriceLabel.setBuddy(self.entryPriceEdit)

        posValueLabel = QLabel("Position value: ")
        self.posValueEdit = QLineEdit()
        self.posValueEdit.setReadOnly(True)
        self.posValueEdit.setEnabled(False)
        posValueLabel.setBuddy(self.posValueEdit)

        posDirLabel = QLabel("Direction: ")
        self.posDirEdit = QLineEdit()
        self.posDirEdit.setReadOnly(True)
        self.posDirEdit.setEnabled(False)
        posDirLabel.setBuddy(self.posDirEdit)

        proportionLabel = QLabel("Proportion of portfolio (%): ")
        self.proportionEdit = QLineEdit()
        self.proportionEdit.setReadOnly(True)
        self.proportionEdit.setEnabled(False)
        proportionLabel.setBuddy(self.proportionEdit)

        #
        # Sub-group for read-only "position" values
        #
        layoutPos = QGridLayout()
        layoutPos.addWidget(posDirLabel, 0, 0)
        layoutPos.addWidget(self.posDirEdit, 0, 1)
        layoutPos.addWidget(posValueLabel, 1, 0)
        layoutPos.addWidget(self.posValueEdit, 1, 1)
        layoutPos.addWidget(proportionLabel, 2, 0)
        layoutPos.addWidget(self.proportionEdit, 2, 1)
        self.groupPos = QGroupBox("Position")
        self.groupPos.setLayout(layoutPos)

        qtyLabel = QLabel("Position quantity: ")
        self.qtyEdit = QSpinBox()
        self.qtyEdit.setRange(0, 999999)
        self.qtyEdit.setValue(100)
        self.qtyEdit.setSingleStep(1)
        qtyLabel.setBuddy(self.qtyEdit)

        layoutTrade = QGridLayout()
        layoutTrade.addWidget(entryPriceLabel, 0, 0, Qt.AlignLeft)
        layoutTrade.addWidget(self.entryPriceEdit, 0, 1, Qt.AlignLeft)
        layoutTrade.addWidget(self.groupStop, 1, 0, 3, 2)
        layoutTrade.addWidget(qtyLabel, 0, 2)
        layoutTrade.addWidget(self.qtyEdit, 0, 3)
        layoutTrade.addWidget(self.groupPos, 1, 2, 3, 2)
#        layoutTrade.addWidget(self., , , , )

        self.groupTrade = QGroupBox("Trade position")
        self.groupTrade.setLayout(layoutTrade)
        
        layoutMain = QVBoxLayout()
        #layoutMain.addWidget(self.menuBar)
        layoutMain.setMenuBar(self.menuBar)
        layoutMain.addWidget(titleLabel)
        layoutMain.addWidget(self.groupPort)
        layoutMain.addWidget(self.groupTrade)
        #layoutMain.addWidget(buttonBox)
        self.setLayout(layoutMain)

    # Called when % risk or portfolio total updated
    def updateDollarRisk(self):
        if self.is_updating_port:
            debug_trace("dollar risk: skipping")
            return
        self.is_updating_port = True
        debug_trace("==== START: Dollar risk update")
        p = Portfolio("default", self.totalEdit.value())
        p.setRiskPercent(self.riskPercentEdit.value())
        self.pos.risk = p.getRiskDollar()
        self.qtyEdit.setValue(self.pos.quantity)
        self.riskDollarEdit.setValue(float(p.getRiskDollar()))
        self.is_updating_port = False
        debug_trace(str(p))
        debug_trace("==== END: Dollar risk update")

    # Called when dollar risk edit updated
    def updatePercentRisk(self):
        if self.is_updating_port:
            debug_trace("percent risk: skipping")
            return
        self.is_updating_port = True
        debug_trace("==== START: Percent risk update")
        p = Portfolio("default", self.totalEdit.value())
        p.setRiskDollar(self.riskDollarEdit.value())
        self.pos.risk = p.getRiskDollar()
        self.qtyEdit.setValue(self.pos.quantity)
        self.riskPercentEdit.setValue(float(p.getRiskPercent()))
        debug_trace(str(p))
        debug_trace("==== END: Percent risk update")
        self.is_updating_port = False

    def handlePriceChange(self, desc):
        if self.is_updating_pos:
            debug_trace(desc + ": skipping")
            return
        self.is_updating_pos = True
        debug_trace("==== START: " + desc)
        self.pos.entry = self.entryPriceEdit.value()
        self.pos.stop_price = self.stopPriceEdit.value()
        self.updateCalc()
        debug_trace("==== END: " + desc)
        self.is_updating_pos = False

    def changedEntryPrice(self):
        self.handlePriceChange("Entry price")

    def changedStopPrice(self):
        self.handlePriceChange("Stop price")

    def changedStopPercent(self):
        if self.is_updating_stop or self.is_updating_pos:
            return
        self.is_updating_stop = True
        self.pos.stop_percent = self.stopPercentEdit.value() / 100.0
        self.stopPriceEdit.setValue(float(self.pos.stop_price))
        self.is_updating_stop = False

    def changedStopDist(self):
        if self.is_updating_stop or self.is_updating_pos:
            return
        self.is_updating_stop = True
        self.pos.stop_distance = self.stopDistEdit.value()
        self.stopPriceEdit.setValue(float(self.pos.stop_price))
        self.is_updating_stop = False

    def changedQty(self):
        if (not self.is_updating_stop and 
            not self.is_updating_pos and 
            not self.is_updating_port):
                self.pos.quantity = self.qtyEdit.value()
                self.stopPriceEdit.setValue(float(self.pos.stop_price))
            #return
        position_value = float(self.pos.total_value)
        portfolio_value = float(self.totalEdit.value())
        proportion = position_value / portfolio_value * 100.0
        self.posValueEdit.setText("%.2f" % position_value) 
        self.proportionEdit.setText("%.2f" % proportion)
        if self.pos.stop_price > self.pos.entry:
            self.posDirEdit.setText("SHORT")
        else:
            self.posDirEdit.setText("LONG")

    def updateCalc(self):
        self.stopDistEdit.setValue(float(self.pos.stop_distance))
        self.stopPercentEdit.setValue(float(self.pos.stop_percent))
        self.qtyEdit.setValue(self.pos.quantity)


    def about(self):
        about_text = "<h1>" + APPLICATION_NAME + "</h1>" + \
           "<i>Stupid name, smart (and free!) trading software.</i><br />" + \
           "Version " + VERSION_STRING + " " 
        about_text += """
<p>Design and coding by Robert Iwancz <br />
Copyright (c) 2012-2013</p>
<p><a href="http://www.voidynullness.net">www.voidynullness.net</a></p>
<center><p>___ </p></center>
<p>This application is free software released under the GNU General Public License.  It is distributed WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>
"""
        QMessageBox.about(self, "About", about_text)
                          

    def copy_port(self):
        text = '%d\t%f\t%f\n' % (self.totalEdit.value(), 
                                 self.riskPercentEdit.value(), 
                                 self.riskDollarEdit.value())
        QApplication.clipboard().setText(text);

    def copy_pos(self):
        text = '%f\t%f\t%d\t%s\n' % (self.entryPriceEdit.value(),
                                     self.stopPriceEdit.value(),
                                     self.qtyEdit.value(),
                                     self.posValueEdit.text())
        QApplication.clipboard().setText(text);

    def copy_all(self):
        text = '%d\t%f\t%f\t%f\t%f\t%d\t%s\n' % (self.totalEdit.value(), 
                                                 self.riskPercentEdit.value(), 
                                                 self.riskDollarEdit.value(),
                                                 self.entryPriceEdit.value(),
                                                 self.stopPriceEdit.value(),
                                                 self.qtyEdit.value(),
                                                 self.posValueEdit.text())
        QApplication.clipboard().setText(text);

    def showDisclaimer(self):
        dlg = tatom.calc.ui.disclaimer.DisclaimerForm(self)
        dlg.exec_()

    def unimplemented(self):
        pass


def debug_trace(str):
    if not g_debug:
        return
    print str
