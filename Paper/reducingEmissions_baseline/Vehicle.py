#! /usr/bin/env python
class Vehicle():
    """This class contains all vehicle definitions"""

    def __init__(self, id="",vType="", NOx=0, n_packages = 0, step_ini=0, step_fin=0, enter_cz = False):
        self.id = id
        self.vType = vType
        self.NOx = NOx
        self.n_packages = n_packages
        self.step_ini = step_ini
        self.step_fin = step_fin
        self.enter_cz = enter_cz
    """
    def __init__(self, id = "", NOx = 0, total_km = 0):
        self.id = id
        self.NOx = NOx
        self.total_km = total_km
    """

    """
    ADD METHODS
    """
    def add_NOx(self,NOx):
        self.NOx +=NOx

    def add_n_packages(self,num):
        self.n_packages +=num

    """
    def add_total_km(self,km):
        self.total_km +=km
    """

    """
    GETTERS AND SETTERS
    """
    @property # Getter
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property # Getter
    def vType(self):
        return self._vType

    @vType.setter
    def vType(self, vType):
        self._vType = vType
        
    @property
    def NOx(self):
        return self._NOx

    @NOx.setter
    def NOx(self,NOx):
        self._NOx = NOx

    @property
    def step_ini(self):
        return self._step_ini

    @step_ini.setter
    def step_ini(self, step_ini):
        self._step_ini = step_ini

    @property
    def step_fin(self):
        return self._step_fin

    @step_fin.setter
    def step_fin(self, step_fin):
        self._step_fin = step_fin

    @property
    def n_packages(self):
        return self._n_packages

    @n_packages.setter
    def n_packages(self, n_packages):
        self._n_packages = n_packages

    @property
    def enter_cz(self):
        return self._enter_cz

    @enter_cz.setter
    def enter_cz(self, enter_cz):
        self._enter_cz = enter_cz

    """
    @property
    def total_km(self):
        return self._total_km

    @total_km.setter
    def total_km(self, total_km):
        self._total_km = total_km
    

    def __str__(self):
        return str(self.id) + " . Total NOx per vehicle: " + str(self.NOx) + " . Km: " + str(self.total_km)
    """

    def __str__(self):
        return str(self.id) + " . vType: " + str(self.vType) + " . Total NOx per vehicle: " + str(self.NOx) +" . Step ini: " + str(self.step_ini) +\
               " . Step fin: " + str(self.step_fin) + " . Nº Packages: " + str(self.n_packages)


