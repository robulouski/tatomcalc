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
#  position.py
#  
#  Position and stop loss calculations module.
#

import decimal

D=decimal.Decimal

class Position(object):
    def __init__(self, r=100, e=20):
        # risk and entry and not modified in any (re)calculation
        self._risk = D(r)
        self._entry = D(e)
        # we store stop loss price, calculate other variations from that.
        self._stop_price = D(0.75) * self._entry
        print self._stop_price
        self.is_valid = True

    @property
    def risk(self):
        return self._risk

    @risk.setter
    def risk(self, value):
        if isinstance(value, decimal.Decimal):
            self._risk = value
        else:        
            self._risk = D(value)

    @property
    def entry(self):
        return self._entry

    @entry.setter
    def entry(self, value):
        if isinstance(value, decimal.Decimal):
            self._entry = value
        else:        
            self._entry = D(value)

    @property
    def stop_price(self):
        print "getting ", self._stop_price
        return self._stop_price

    @stop_price.setter
    def stop_price(self, value):
        if isinstance(value, decimal.Decimal):
            self._stop_price = value
        else:        
            self._stop_price = D(value)

        if (self._stop_price >= self._stop_price):
            self.is_valid = False

    @property
    def stop_distance(self):
        return abs(self._entry - self._stop_price)

    @stop_distance.setter
    def stop_distance(self, value):
        if isinstance(value, decimal.Decimal):
            dist = value
        else:        
            dist = D(value)
        if self._entry > self._stop_price:
            if (dist > self._entry):
                dist = self._entry
            self._stop_price = self._entry - dist
        if self._entry < self._stop_price:
            self._stop_price = self._entry + dist

    @property
    def stop_percent(self):
        if (self._entry <= 0):
            return 0
        if self._entry > self._stop_price:
            return (D(1) - self._stop_price / self._entry) * D(100.0)
        if (self._stop_price <= 0):
            return 0
        if self._entry < self._stop_price:
            return (self._stop_price / self._entry - 1) * D(100.0)
        return 0

    @stop_percent.setter
    def stop_percent(self, value):
        if isinstance(value, decimal.Decimal):
            p = value
        else:        
            p = D(value)
        if self._entry >= self._stop_price:
            self._stop_price = self._entry * (D(1) - p)
        if self._entry < self._stop_price:
            self._stop_price = self._entry + (self._entry * p)
            

    @property
    def quantity(self):
        loss = self.stop_distance
        if loss == 0:
            return 0
        print "Quantity: ", self._risk / loss
        return D(self._risk / loss).to_integral_value(
            rounding=decimal.ROUND_DOWN)

    @property
    def total_value(self):
        return self.quantity * self._entry
