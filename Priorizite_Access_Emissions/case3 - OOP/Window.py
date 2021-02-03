#! /usr/bin/env python
class Window():
    """TODO"""
    def __init__(self, NOx_total_w = 0, NOx_control_zone_w = 0, veh_total_number_w = 0, vehicles_in_w=set()):
        self.NOx_total_w = NOx_total_w
        self.NOx_control_zone_w = NOx_control_zone_w
        self.veh_total_number_w = veh_total_number_w
        self.vehicles_in_w = vehicles_in_w
    """
    ADD METHODS
    """
    def add_NOx_Total_w(self,NOx):
        self.NOx_total_w +=NOx

    def add_NOx_control_zone_w(self,NOx):
        self.NOx_control_zone_w +=NOx

    def add_veh_total_number_w(self,num):
        self.veh_total_number_w +=num

    def add_vehicles_in_w(self, vehicles_in_w):
        for veh in vehicles_in_w:
            self._vehicles_in_w.add(veh)


    """
    GETTERS AND SETTERS
    """
    @property  ##Getter
    def NOx_total_w(self):
        return self._NOx_total_w

    @NOx_total_w.setter
    def NOx_total_w(self, NOx_total_w):
        self._NOx_total_w = NOx_total_w

    @property  ##Getter
    def NOx_control_zone_w(self):
        return self._NOx_control_zone_w

    @NOx_control_zone_w.setter
    def NOx_control_zone_w(self, NOx_control_zone_w):
        self._NOx_control_zone_w = NOx_control_zone_w

    @property  ##Getter
    def veh_total_number_w(self):
        return self._veh_total_number_w

    @veh_total_number_w.setter
    def veh_total_number_w(self, veh_total_number_w):
        self._veh_total_number_w = veh_total_number_w

    @property  ##Getter
    def vehicles_in_w(self):
        return self._vehicles_in_w

    @vehicles_in_w.setter
    def vehicles_in_w(self, vehicles_in_w):
        self._vehicles_in_w = vehicles_in_w

