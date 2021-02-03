#! /usr/bin/env python
class Simulation():
    """TODO"""
    def Simulation(self, NOx_total = 0, NOx_control_zone = 0, total_kilometers = 0, vehicles_in_simulation = [],windows = []):
        # Emissions
        self.NOx_total = NOx_total
        self.NOx_control_zone = NOx_control_zone
        self.total_kilometers = total_kilometers
        self.vehicles_in_simulation = vehicles_in_simulation
        self.windows = windows



    def add_NOx_Total(self,NOx):
        self.NOx_total +=NOx

    def add_NOx_control_zone(self,NOx):
        self.NOx_control_zone +=NOx

    def add_total_kilometers(self,km):
        self.total_kilometers +=km


    @property ##Getter
    def NOx_Total(self):
        return self._NOx_Total
    @NOx_Total.setter
    def NOx_Total(self,NOx_Total):
        self._NOx_Total = NOx_Total

    @property  ##Getter
    def NOx_control_zone(self):
        return self._NOx_control_zone

    @NOx_control_zone.setter
    def NOx_control_zone(self, NOx_control_zone):
        self._NOx_control_zone = NOx_control_zone

    @property  ##Getter
    def total_kilometers(self):
        return self._total_kilometers

    @total_kilometers.setter
    def total_kilometers(self, total_kilometers):
        self._total_kilometers = total_kilometers

    @property  ##Getter
    def vehicles_in_simulation(self):
        return self._vehicles_in_simulation

    @total_kilometers.setter
    def vehicles_in_simulation(self, vehicles_in_simulation):
        self._vehicles_in_simulation.append(vehicles_in_simulation)

    @property  ##Getter
    def windows(self):
        return self._windows

    @windows.setter
    def windows(self, windows):
        self._windows.append(windows)



