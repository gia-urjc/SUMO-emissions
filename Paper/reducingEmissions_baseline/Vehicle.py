#! /usr/bin/env python
class Vehicle():
    """This class contains all vehicle definitions"""

    def __init__(self, id = "", NOx = 0, total_km = 0):
        self.id = id
        self.NOx = NOx
        self.total_km = total_km

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
    @property # Getter
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id
        
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

    def __str__(self):
        return str(self.id) + " . Total NOx per vehicle: " + str(self.NOx) + " . Km: " + str(self.total_km)



