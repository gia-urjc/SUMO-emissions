#! /usr/bin/env python
class Window():
    """TODO"""
    def __init__(self, step, vehicles_in_w, vehicles_in_control_zone_w,
                 NOx_total_w = 0, NOx_control_zone_w = 0, veh_total_number_w = 0,
                 p_t = 0, p_t_total = 0, alpha = 0.5, lambda_l = 0.8):
        self.step = step
        self.NOx_total_w = NOx_total_w
        self.NOx_control_zone_w = NOx_control_zone_w
        self.veh_total_number_w = veh_total_number_w

        self.vehicles_in_w = vehicles_in_w
        self.vehicles_in_control_zone_w = vehicles_in_control_zone_w

        self.p_t = p_t
        self.p_t_total = p_t_total
        self.alpha = alpha
        self.lambda_l = lambda_l
    """
    ADD METHODS
    """
    def add_NOx_Total_w(self,NOx):
        self.NOx_total_w +=NOx

    def add_NOx_control_zone_w(self,NOx):
        self.NOx_control_zone_w +=NOx

    def add_veh_total_number_w(self,num):
        self.veh_total_number_w +=num

    def add_vehicles_in_w(self, vehw):
        for veh in vehw:
            self.vehicles_in_w.add(veh)

    def add_vehicles_in_control_zone_w(self, vehw):
       self.vehicles_in_control_zone_w.add(vehw)

    """
        REMOVE METHODS
    """

    def remove_vehicles_in_w(self, veh):
        self.vehicles_in_w.remove(veh)

    def remove_vehicles_in_control_zone_w(self, veh):
        self.vehicles_in_control_zone_w.remove(veh)

    """
        SUBSTRACTION METHODS
    """

    def sub_veh_total_number_w(self, num):
        self.veh_total_number_w -= num
    """
       UPDATE METHODS
    """

    def update_Step(self):
        self.step += 1

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

    @property  ##Getter
    def vehicles_in_control_zone_w(self):
        return self._vehicles_in_control_zone_w

    @vehicles_in_control_zone_w.setter
    def vehicles_in_control_zone_w(self, vehicles_in_control_zone_w):
        self._vehicles_in_control_zone_w = vehicles_in_control_zone_w

    @property  ##Getter
    def p_t(self):
        return self._p_t

    @p_t.setter
    def p_t(self, p_t):
        self._p_t = p_t

    @property  ##Getter
    def p_t_total(self):
        return self._p_t_total

    @p_t_total.setter
    def p_t_total(self, p_t_total):
        self._p_t_total = p_t_total

    @property  ##Getter
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha

    @property  ##Getter
    def lambda_l(self):
        return self._lambda_l

    @lambda_l.setter
    def lambda_l(self, lambda_l):
        self._lambda_l = lambda_l

    def __str__(self):
        vehInW = ""
        for veh in self.vehicles_in_w:
            vehInW += veh.id +","
        cont_vehInWCZ = len(self.vehicles_in_control_zone_w)
        vehInWCZ = ""
        for veh in self.vehicles_in_control_zone_w:
            vehInWCZ += veh + ","
        return str(self.step) + ". NOx_total_w: " + str(self.NOx_total_w) + ". NOx_control_zone_w: " + \
               str(self.NOx_control_zone_w) +". p_t: "+str(self.p_t)  +". p_t_total: "+str(self.p_t_total) + \
               ". alpha: " + str(self.alpha) + ". lambda: " + str(self.lambda_l) +". veh_total_number_w: " + \
               str(self.veh_total_number_w) + ". Vehicles: " + vehInW + ". Nº veh in control zone: "+\
               str(cont_vehInWCZ) +". Vehicles in control zone: " + vehInWCZ

