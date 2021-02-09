#! /usr/bin/env python
class Vehicle():
    """This class contains all vehicle definitions"""

    def __init__(self, id = "", NOx = 0, n_packages = 0):
        self.id = id
        self.NOx = NOx
        self.n_packages = n_packages

    """
    ADD METHODS
    """
    def add_NOx(self,NOx):
        self.NOx +=NOx

    def add_n_packages(self,num):
        self.n_packages +=num

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
    def n_packages(self):
        return self._n_packages

    @n_packages.setter
    def n_packages(self, n_packages):
        self._n_packages = n_packages

    def __str__(self):
        return str(self.id) + " . Total NOx per vehicle: " + str(self.NOx) + " . Nº Packages: " + str(self.n_packages)



