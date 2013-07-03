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
#  main.py
#  Application entry point.
#
import sys
from PySide.QtCore import *
from PySide.QtGui import *

from tatom.calc import VERSION_STRING, APPLICATION_NAME
from tatom.calc.ui.mainform import MainForm

def main():
    try:
        import argparse
        parser = argparse.ArgumentParser(description=
            'A cross-platform position sizing calculator for traders.')
        parser.add_argument('-v', '--version', 
                            action='version', 
                            version="%s %s" % (APPLICATION_NAME, 
                                               VERSION_STRING))
        parser.parse_known_args()
    except ImportError:
        # Just forget the whole thing if running a version of python 
        # without argparse :(
        pass

    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()
