#! /usr/bin/env python
class Simulation():
    """ Simulation """

    def __init__(self, step, threshold_L, threshold_H , k=1, control_area_edges = [], restrictionMode = False,
                   NOx_total = 0, NOx_control_zone = 0, NOx_control_zone_restriction_mode=0,
                   veh_total_number = 0, vehicles_in_simulation = [], vehs_load = [], all_veh = set(), windows = [],
                   alphas=[], p_t = 0,  max_historical = 0):
                #total_kilometers = 0,windows = []):

        self.step = step
        self.threshold_L = threshold_L
        self.threshold_H = threshold_H
        self.k = k
        self.control_area_edges = control_area_edges
        self.restrictionMode = restrictionMode

        self.NOx_total = NOx_total
        self.NOx_control_zone = NOx_control_zone
        self.NOx_control_zone_restriction_mode= NOx_control_zone_restriction_mode

        self.veh_total_number = veh_total_number
        self.vehicles_in_simulation = vehicles_in_simulation
        self.vehs_load = vehs_load      # ID LIST
        self.all_veh = all_veh
        #self.total_kilometers = total_kilometers

        self.windows = windows

        self.alphas = alphas
        self.p_t = p_t

        # VE, VEP, RRE, RREP
        self.max_historical = max_historical


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
        self.vehicles_in_simulation.extend(veh)

    def add_vehs_load(self,veh):
        self.vehs_load.append(veh)

    def add_all_veh(self, all_v):
        for veh in all_v:
            self.all_veh.add(veh)
    """
    def add_total_kilometers(self,km):
        self.total_kilometers +=km
    """
    def add_window(self,wind):
        self.windows.append(wind)

    def add_alpha(self,alp):
        self.alphas.append(alp)

    """
        REMOVE METHODS
    """
    def remove_vehicles_in_simulation(self,veh):
        self.vehicles_in_simulation.remove(veh)

    """
        SUBSTRACTION METHODS
    """
    def sub_NOx_control_zone_restriction_mode(self, NOx):
        self.NOx_control_zone_restriction_mode -= NOx

    """
    UPDATE METHODS
    """
    def change_Restriction_Mode(self,mode):
        """ Mode = True or False """
        self.restrictionMode = mode

    def update_Step(self):
        self.step +=1

    def update_step_fin_veh(self, step, veh):
        for i in range(len(self.vehicles_in_simulation)):
            if self.vehicles_in_simulation[i].id==veh.id :
                veh.step_fin = step


    """
    GETTERS AND SETTERS
    """
    @property  ##Getter
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        self._step = step

    @property  ##Getter
    def threshold_L(self):
        return self._threshold_L

    @threshold_L.setter
    def threshold_L(self, threshold_L):
        self._threshold_L = threshold_L

    @property  ##Getter
    def threshold_H(self):
        return self._threshold_H

    @threshold_H.setter
    def threshold_H(self, threshold_H):
        self._threshold_H = threshold_H

    @property  ##Getter
    def k(self):
        return self._k

    @k.setter
    def k(self, k):
        self._k = k

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
    def all_veh(self):
        return self._all_veh

    @all_veh.setter
    def all_veh(self, all_veh):
        self._all_veh = all_veh

    """
    @property  ##Getter
    def total_kilometers(self):
        return self._total_kilometers

    @total_kilometers.setter
    def total_kilometers(self, total_kilometers):
        self._total_kilometers = total_kilometers
    """

    @property  ##Getter
    def windows(self):
        return self._windows

    @windows.setter
    def windows(self, windows):
        self._windows = windows

    @property  ##Getter
    def alphas(self):
        return self._alphas

    @alphas.setter
    def alphas(self, alphas):
        self._alphas = alphas

    @property  ##Getter
    def p_t(self):
        return self._p_t

    @p_t.setter
    def p_t(self, p_t):
        self._p_t = p_t

    @property  ##Getter
    def max_historical(self):
        return self._max_historical

    @max_historical.setter
    def max_historical(self, max_historical):
        self._max_historical = max_historical


    def __str__(self):

        w = ""
        for wi in self.windows:
            w += "\n"+ wi.__str__()

        return str(self.step) + ". restrictionMode: " + str(self.restrictionMode) + ".  NOx_total:" + str(self.NOx_total)+ \
               ". NOx_control_zone:" + str(self.NOx_control_zone) + ". veh_total_number: " + str(self.veh_total_number) + \
               ". Windows:" + w  # +". Total km: " + str(self.total_kilometers)








