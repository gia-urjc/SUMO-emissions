#! /usr/bin/env python
class Vehicle():
    """This class contains all vehicle definitions"""

    veh_total_number = 0
    def __init__(self, NOx, km):
        self.NOx = NOx
        self.total_km = km
        Vehicle.veh_total_number += 1

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

