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
#  portfolio.py
#  
#  Portfolio calculations module.
#

import decimal

# Define exceptions
#class PortfolioError(Exception): pass
#class OtherError(PortfolioError): pass
#class OtherOtherError(PortfolioError): pass


class Portfolio(object):
    def __init__(self, name, total=decimal.Decimal(10000)):
        self._name = name
        self._risk_percent = 0
        self._risk_dollar = 0
        if isinstance(total, decimal.Decimal):
            self._total = total
        else:
            self._total= decimal.Decimal(total)
        self.setRiskPercent(decimal.Decimal(1))

    def updateRiskDollar(self):
        self._risk_dollar = (self._risk_percent / 100) * self._total

    def setRiskPercent(self, value):
        if value is not None and value >= 0:
            if isinstance(value, decimal.Decimal):
                self._risk_percent = value
            else:
                self._risk_percent = decimal.Decimal(value)
            self.updateRiskDollar()

    def getRiskPercent(self):
        return self._risk_percent

    def setRiskDollar(self, value):
        if value is not None and value >= 0:
            if isinstance(value, decimal.Decimal):
                self._risk_dollar = value
            else:
                self._risk_dollar = decimal.Decimal(value)
            self._risk_percent = (self._risk_dollar / self._total * 100)

    def getRiskDollar(self):
        return self._risk_dollar

    def setTotal(self, value):
        if value is not None and value >= 0:
            if isinstance(value, decimal.Decimal):
                self._total = value
            else:
                self._total= decimal.Decimal(value)
            self.updateRiskDollar()

    def __str__(self):
        return "Portfolio %s: $%s Risk: %s%% $%s" % (self._name, str(self._total), str(self._risk_percent), str(self._risk_dollar))

def main():
    p = Portfolio("test1", decimal.Decimal(20000))
    print p
    print p._name
    print p._total
    print p._risk_dollar
    print "==="
    p.setRiskDollar(400)
    print p._risk_percent

if __name__ == '__main__':
    main()
