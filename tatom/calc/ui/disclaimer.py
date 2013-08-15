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
#  disclaimer.py
#  Obligatory Disclaimer
#
from PySide.QtCore import *
from PySide.QtGui import *

disclaimer = """
<h1>Disclaimer</h1>
<p><strong>This application is FREE software released under the GNU General Public 
License.  It is distributed WITHOUT ANY WARRANTY; without even the implied 
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.</strong></p>
<p>This software is provided for entertainment purposes only, it comes with 
NO WARRANTY, and is fit for no purpose whatsoever. It does not constitute 
financial advice, or indeed any advice. It should not be interpreted in 
any way as an explicit or even implied endorsement of any trading or 
position sizing strategy.</p>  
"""

class DisclaimerForm(QDialog):
    style = "QDialog {border: 2px solid rgb(255, 0, 0);}"

    def __init__(self, parent=None):
        super(DisclaimerForm, self).__init__(parent, Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        lblMain = QLabel(disclaimer)
        lblMain.setWordWrap(True)
        btnAccept = QPushButton("Yep, sure, got it, I agree, totally")
        layoutMain = QVBoxLayout()
        layoutMain.addWidget(lblMain)
        layoutMain.addWidget(btnAccept)
        self.setLayout(layoutMain)
        self.setWindowTitle("Obligatory Disclaimer")
        self.connect(btnAccept, SIGNAL("clicked()"), self.accept)
        self.setStyleSheet(self.style)
        
        
