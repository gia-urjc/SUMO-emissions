#! /usr/bin/env python
class Vehicle():
    """This class contains all vehicle definitions"""

    def __init__(self, NOx = 0, km = 0):
        self.NOx = NOx
        self.total_km = km

    """
    ADD METHODS
    """
    def add_NOx(self,NOx):
        self.NOx +=NOx

    def add_total_km(self,km):
        self.total_km +=km

    """
    GETTERS AND SETTERS
    """
    @property
    def NOx(self):
        return self._NOx
    @NOx.setter
    def NOx(self,NOx):
        self._NOx = NOx

    @property
    def total_km(self):
        return self._total_km

    @total_km.setter
    def total_km(self, total_km):
        self._total_km = total_km

