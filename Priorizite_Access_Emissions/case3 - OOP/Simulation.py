#! /usr/bin/env python
class Simulation():
    """TODO"""
    def Simulation(self, threshold, NOx_total = 0, NOx_control_zone = 0, veh_total_number = 0, vehicles_in_simulation = [], total_kilometers = 0 ,windows = []):

        self.threshold = threshold

        self.NOx_total = NOx_total
        self.NOx_control_zone = NOx_control_zone
        self.veh_total_number = veh_total_number
        self.vehicles_in_simulation = vehicles_in_simulation
        self.total_kilometers = total_kilometers
        self.windows = windows

    """
    ADD METHODS
    """

    def add_NOx_Total(self,NOx):
        self.NOx_total +=NOx

    def add_NOx_control_zone(self,NOx):
        self.NOx_control_zone +=NOx

    def add_veh_total_number(self,num):
        self.veh_total_number +=num

    # def add_vehicles_in_simulation(self,num) # SEE vehicles_in_simulation.SETTER!!

    def add_total_kilometers(self,km):
        self.total_kilometers +=km

    # def add_window(self,wind) # SEE windows.SETTER!!

    """
    GETTERS AND SETTERS
    """

    @property  ##Getter
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        self._threshold = threshold

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
    def veh_total_number(self):
        return self._veh_total_number

    @veh_total_number.setter
    def veh_total_number(self, veh_total_number):
        self._veh_total_number = veh_total_number

    @property  ##Getter
    def vehicles_in_simulation(self):
        return self._vehicles_in_simulation

    @vehicles_in_simulation.setter
    def vehicles_in_simulation(self, vehicles_in_simulation):
        self._vehicles_in_simulation.append(vehicles_in_simulation)

    @property  ##Getter
    def total_kilometers(self):
        return self._total_kilometers

    @total_kilometers.setter
    def total_kilometers(self, total_kilometers):
        self._total_kilometers = total_kilometers

    @property  ##Getter
    def windows(self):
        return self._windows

    @windows.setter
    def windows(self, windows):
        self._windows.append(windows)



