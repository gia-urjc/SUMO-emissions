#! /usr/bin/env python
class Simulation():
    """TODO"""
    def Simulation(self, threshold, control_area_edges = [], restrictionMode = False,
                   NOx_total = 0, NOx_control_zone = 0, NOx_control_zone_restriction_mode=0,
                   veh_total_number = 0, vehicles_in_simulation = [], vehs_load = [], total_kilometers = 0,
                   windows = []):

        self.threshold = threshold
        self.control_area_edges = control_area_edges
        self.restrictionMode = restrictionMode

        self.NOx_total = NOx_total
        self.NOx_control_zone = NOx_control_zone
        self.NOx_control_zone_restriction_mode= NOx_control_zone_restriction_mode

        self.veh_total_number = veh_total_number
        self.vehicles_in_simulation = vehicles_in_simulation
        self.vehs_load = vehs_load
        self.total_kilometers = total_kilometers

        self.windows = windows


    """
    ADD METHODS
    """

    def add_NOx_Total(self,NOx):
        self.NOx_total +=NOx

    def add_NOx_control_zone(self,NOx):
        self.NOx_control_zone +=NOx

    def add_NOx_control_zone_restriction_mode(self, NOx):
        self.NOx_control_zone_restriction_mode += NOx

    def add_veh_total_number(self,num):
        self.veh_total_number +=num

    def add_vehicles_in_simulation(self,veh):
        self.vehicles_in_simulation.append(veh)

    def add_vehs_load(self,veh):
        self.vehs_load.append(veh)

    def add_total_kilometers(self,km):
        self.total_kilometers +=km

    def add_window(self,wind):
        self.windows.append(wind)

    """
    UPDATE METHODS
    """

    def change_Restriction_Mode(self,mode):
        """ Mode = True or False """
        self.restrictionMode = mode



    """
    GETTERS AND SETTERS
    """

    @property  ##Getter
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        self._threshold = threshold

    @property  ##Getter
    def control_area_edges(self):
        return self._control_area_edges

    @control_area_edges.setter
    def control_area_edges(self, control_area_edges):
        self._control_area_edges = control_area_edges

    @property  ##Getter
    def restrictionMode(self):
        return self._restrictionMode

    @restrictionMode.setter
    def restrictionMode(self, restrictionMode):
        self._restrictionMode = restrictionMode

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
    def NOx_control_zone_restriction_mode(self):
        return self._NOx_control_zone_restriction_mode

    @NOx_control_zone_restriction_mode.setter
    def NOx_control_zone_restriction_mode(self, NOx_control_zone_restriction_mode):
        self._NOx_control_zone_restriction_mode = NOx_control_zone_restriction_mode

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
        self._vehicles_in_simulation = vehicles_in_simulation

    @property  ##Getter
    def vehs_load(self):
        return self._vehs_load

    @vehs_load.setter
    def vehs_load(self, vehs_load):
        self._vehs_load = vehs_load

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
        self._windows = windows



