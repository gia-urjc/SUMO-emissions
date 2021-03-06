"""
    main def at the end:
        run (strategy,file_name,historicalTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
            subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges)
"""

from pathlib import Path
import math
import random
import traci
import sys
import os
import re

import results
from Vehicle import Vehicle
from Simulation import Simulation
from Window import Window


def getNumPackages(randomPackages, min_packages, max_packages, id_veh_dep_Vehicle):
    """ No uniform distribution"""
    if id_veh_dep_Vehicle.vType == "eVehicle":
        if max_packages < (min_packages+4):
            num_packages = randomPackages.randint(min_packages, min_packages+4)
        else:
            num_packages = randomPackages.randint(min_packages, max_packages)
    elif id_veh_dep_Vehicle.vType == "gasolineEuroSix" or id_veh_dep_Vehicle.vType == "dieselEuroSix" or id_veh_dep_Vehicle.vType == "normalVehicle" or id_veh_dep_Vehicle.vType == "highEmissions":
        num_packages = randomPackages.randint(min_packages, max_packages)
    elif id_veh_dep_Vehicle.vType == "hovDieselEuroSix":
        num_packages = randomPackages.randint(min_packages+10, max_packages + 10)
    elif id_veh_dep_Vehicle.vType == "truck":
        num_packages = randomPackages.randint(min_packages + 20, max_packages + 20)
    else:
        num_packages = randomPackages.randint(min_packages, max_packages)
    return num_packages

def closeToRestrictedArea(veh, enter_control_area_edges):
    """ Return true if the veh is near (100) the control zone area """
    string_current_edge = traci.vehicle.getLaneID(veh.id)
    if string_current_edge in enter_control_area_edges:
        dist = traci.vehicle.getLanePosition(veh.id)
        lane = traci.vehicle.getLaneID(veh.id)
        tam = traci.lane.getLength(lane)
        # only allow changes if not within 100 meters of the crossing
        if (tam - dist) > 100:
            return True
        else:
            return False
    else:
        return False


def setAllowCar(veh, simulation):
    """ Returns to the original vClass and vType for vehicles entering the control zone. Changes veh color and reroutes"""
    em_Class = traci.vehicle.getEmissionClass(veh.id)
    setSwitchVehicleClass(em_Class, veh, simulation)
    traci.vehicle.setColor(vehID=veh.id, color=(0, 0, 128))
    traci.vehicle.rerouteTraveltime(veh.id, True)


def setNotAllowCar(veh):
    """ Set veh as custom1 and noauthority, Keeps its emission class, changes color and reroutes"""
    emiLastClass = traci.vehicle.getEmissionClass(veh.id)
    traci.vehicle.setType(vehID=veh.id, typeID="noauthority")
    setEmissionClass(emiLastClass, veh)
    traci.vehicle.setColor(vehID=veh.id, color=(255, 0, 0))
    traci.vehicle.rerouteTraveltime(veh.id, True)


def all_cars_enter(simulation, enter_control_area_edges):
    """ If the vehicle is near the control area and is custom1 (custom veh doesn't have access to control zone) =>
    Returns to the original vClass and vType for vehicles entering the control zone. Changes veh color and reroutes"""
    for veh in simulation.vehicles_in_simulation:
        if closeToRestrictedArea(veh, enter_control_area_edges):
            if traci.vehicle.getVehicleClass(veh.id) == "custom1":
                setAllowCar(veh, simulation)


def no_cars_enter(simulation, enter_control_area_edges):
    """ If the vehicle is near the control area and is NOT custom1 (custom veh doesn't have access to control zone) =>
    Set veh as custom1 and noauthority, Keeps its emission class, changes color and reroutes"""

    for veh in simulation.vehicles_in_simulation:
        if closeToRestrictedArea(veh, enter_control_area_edges):
            if traci.vehicle.getVehicleClass(veh.id) != "custom1":
                setNotAllowCar(veh)


def some_cars_enter(simulation, enter_control_area_edges, historicalTable, historical_max_num_pack):
    """ If the vehicle is near the control area => Calculate whether or not a vehicle enters the control area (depends on strategy)"""

    for veh in simulation.vehicles_in_simulation:
        if closeToRestrictedArea(veh, enter_control_area_edges):
            # determine whether the car enters
            enters = False
            try:
                if simulation.strategy == "baseline":
                    enters = baselineTester(simulation.k)
                elif simulation.strategy != "noControl":
                    enters = historicalTester(simulation, veh, historicalTable, historical_max_num_pack)
            except NameError:
                print("Strategy doesn't found")
                raise RuntimeError('error')

            if enters:  # car should enter the area
                if traci.vehicle.getVehicleClass(veh.id) == "custom1":
                    setAllowCar(veh, simulation)
            else:  # car should not enter the area
                if traci.vehicle.getVehicleClass(veh.id) != "custom1":
                    setNotAllowCar(veh)


def calculate_k(simulation, w):
    """ Calculate k: access permission level """
    if simulation.strategy != "noControl":
        aux = (simulation.threshold_H - simulation.p_t) / (simulation.threshold_H - simulation.threshold_L)
        simulation.k = min(1, max(aux, 0))
    else:
        simulation.k = 1
    w.k = simulation.k


def setEmissionClass(emiLastClass, veh):
    """ Keeps its emission class """
    if emiLastClass == "Zero/default":
        traci.vehicle.setEmissionClass(veh.id, "zero")
    elif emiLastClass == "HBEFA3/LDV_G_EU6":
        traci.vehicle.setEmissionClass(veh.id, "HBEFA3/LDV_G_EU6")
    elif emiLastClass == "HBEFA3/LDV_D_EU6":
        traci.vehicle.setEmissionClass(veh.id, "HBEFA3/LDV_D_EU6")
    elif emiLastClass == "HBEFA3/PC_D_EU6":
        traci.vehicle.setEmissionClass(veh.id, "HBEFA3/PC_D_EU6")
    elif emiLastClass == "HBEFA3/PC_G_EU4":
        traci.vehicle.setEmissionClass(veh.id, "HBEFA3/PC_G_EU4")
    elif emiLastClass == "HBEFA3/PC_G_EU3":
        traci.vehicle.setEmissionClass(veh.id, "HBEFA3/PC_G_EU3")
    elif emiLastClass == "HBEFA3/HDV_D_EU4":
        traci.vehicle.setEmissionClass(veh.id, "HBEFA3/HDV_D_EU4")


def setSwitchVehicleClass(emiClass, veh, simulation):
    """ Returns to the original vClass and vType for vehicles entering the control zone"""
    if emiClass == "Zero/default":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="evehicle")
        traci.vehicle.setType(vehID=veh.id, typeID="eVehicle")
        newType = "eVehicle"
    elif emiClass == "HBEFA3/LDV_G_EU6":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="gasolineEuroSix")
        newType = "gasolineEuroSix"
    elif emiClass == "HBEFA3/LDV_D_EU6":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="dieselEuroSix")
        newType = "dieselEuroSix"
    elif emiClass == "HBEFA3/PC_D_EU6":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="hovDieselEuroSix")
        newType = "hovDieselEuroSix"
    elif emiClass == "HBEFA3/PC_G_EU4":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="normalVehicle")
        newType = "normalVehicle"
    elif emiClass == "HBEFA3/PC_G_EU3":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="highEmissions")
        newType = "highEmissions"
    elif emiClass == "HBEFA3/HDV_D_EU4":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="truck")
        traci.vehicle.setType(veh.id, typeID="truck")
        newType = "truck"
    else:
        newType = ""
    simulation.vType = newType
    # print("We switch to its previous class", traci.vehicle.getVehicleClass(vehID=veh.id))


"""
STRATEGIES

"""


def baselineTester(simk):
    """ If random <= k => True (vehicle is allowed)"""
    # simulation.k = 1 NO RESTRICTIONS
    # simulation.k = 0 NO VEHICLES ALLOWED
    if random.uniform(0, 1) <= simk:
        return True
    else:
        return False


def historicalTester(simulation, veh, historicalTable, historical_max_num_pack):
    """ If True (vehicle is allowed)"""
    # simulation.k = 1 NO RESTRICTIONS
    # simulation.k = 0 NO VEHICLES ALLOWED
    # num_control = (k-acc(ant))/(acc-acc(ant))
    if simulation.strategy == "VEP" or simulation.strategy == "RREP":
        if veh.n_packages > historical_max_num_pack[veh.originalvType]: # TODO REVISAR ESTO, tiene que ver con el historico y con que ahora tenemos vehiculos con más paquetes que en el histórico
            vType = veh.originalvType + "-" + str(historical_max_num_pack[veh.originalvType])
        else:
            vType = veh.originalvType + "-" + str(veh.n_packages)
    else:
        vType = veh.originalvType
    previous = ""
    for key, value in historicalTable.items():
        if key == vType:
            break
        previous = key
    if previous == "":
        aux = 0
    else:
        aux = historicalTable[previous]
    if (historicalTable[vType] - aux) == 0:
        num_control = 2
    else:
        num_control = (simulation.k - aux) / (historicalTable[vType] - aux)
    if random.uniform(0, 1) <= num_control:
        return True
    else:
        return False


def openHistorical(file_name, historicalTable, historical_max_num_pack):
    """ Opens historical and writes the data in a variable historicalTable (dict())"""
    # OPEN HISTORICAL
    try:
        count_lines = 0
        h_t = []
        f = open(file_name, 'r')
        for l in f:
            h_t.append("")
            h_t[count_lines] = l.split()
            count_lines += 1
        for list_h_t in h_t:
            historicalTable[list_h_t[0]] = float(list_h_t[1])
            name_veh = re.search(r'([A-z]+)', list_h_t[0]).group(0)
            number_packages_hist = int(re.search(r'(?<=-)\w+', list_h_t[0]).group(0))
            if name_veh in historical_max_num_pack:
                if historical_max_num_pack[name_veh] < number_packages_hist:
                    historical_max_num_pack[name_veh] = number_packages_hist
            else:
                historical_max_num_pack[name_veh] = number_packages_hist
        print("HISTORICAL: ", historicalTable)
        print("historical_max_num_pack",historical_max_num_pack)
        f.close()
    except OSError:
        print('cannot open', file_name)

"""
RUN - MAIN DEF 

"""
def run(strategy,file_name,historicalTable, historical_max_num_pack, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
            subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges):
    """"""
    # Initialization
    random.seed(1)
    randomLambda = random.Random(1)
    randomPackages = random.Random(1)
    print("RUN")
    print(strategy)
    simulation = Simulation(step=0, threshold_L=threshold_L, threshold_H=threshold_H, k=1, strategy=strategy)
    window = Window(simulation.step, set(), set(), 0, 0, 0, 0, 0, 1, 0.8)

    # open history file if is necessary
    if (strategy != "baseline" and strategy != "noControl"):
        openHistorical(file_name, historicalTable, historical_max_num_pack)

    # put the centre closed for not allowed cars
    # On this version, all the cars have the access opened at the beginning, and  later we calculate if one car enter or not
    for aEd in control_area_edges_cnf:
        traci.lane.setDisallowed(laneID=aEd, disallowedClasses=["custom1"])

    lastkSmaller1 = True
    start_total = True
    start_control = True

    # MAIN LOOP FOR THE SIMULATION
    while traci.simulation.getMinExpectedNumber() > 0:  # While there are cars (and cars waiting)
        # LAST STEP
        # Vehicles in simulation and vehicles waiting
        vehs_load = traci.simulation.getLoadedIDList()
        vehs_load_Vehicle = []
        for veh in vehs_load:
            if veh != "simulation.findRoute":
                vehicl = Vehicle(veh)
                vehs_load_Vehicle.append(vehicl)

        simulation.vehs_load = vehs_load_Vehicle

        # initialize variables
        if simulation.step == 0:
            traci.simulationStep()
            simulation.p_t = p_t_ini
            window.NOx_total_w = 0
            window.NOx_control_zone_w = 0
            window.p_t = p_t_ini
            window.p_t_total = p_t_ini
            window.lambda_l = 0.8

            # Add variables for the last 50 steps
            simulation.add_window(window)
            print("Window: ", window)
            # Reboot all
            window = Window(simulation.step, window.vehicles_in_w.copy(), set(), 0, 0, window.veh_total_number_w)

            # calculate k
            calculate_k(simulation, window)

        # NEW STEP

        traci.simulationStep()  # Advance one time step: one second
        simulation.update_Step()
        window.update_Step()

        # MANAGE VEHICLES - All simulation
        id_vehs_departed = list(traci.simulation.getDepartedIDList())  # Vehicles in simulation
        if (id_vehs_departed):  # if the list is not empty
            # All simulation:
            id_vehs_departed_Vehicle = []
            for id_veh_dep in id_vehs_departed:
                if id_veh_dep != "simulation.findRoute":
                    id_veh_dep_Vehicle = Vehicle(id_veh_dep)
                    id_veh_dep_Vehicle.step_ini = simulation.step
                    id_veh_dep_Vehicle.vType = traci.vehicle.getTypeID(id_veh_dep_Vehicle.id)
                    id_veh_dep_Vehicle.originalvType = traci.vehicle.getTypeID(id_veh_dep_Vehicle.id)
                    id_veh_dep_Vehicle.n_packages = getNumPackages(randomPackages, min_packages, max_packages, id_veh_dep_Vehicle)
                    id_vehs_departed_Vehicle.append(id_veh_dep_Vehicle)
            simulation.add_vehicles_in_simulation(id_vehs_departed_Vehicle)  # Add vehicles to the simulation list
            simulation.add_all_veh(id_vehs_departed_Vehicle)
            # Per window:
            window.add_vehicles_in_w(simulation.vehicles_in_simulation)
            window.veh_total_number_w = len(window.vehicles_in_w)

        # Taking into account the vehicles that reach their destination:
        id_vehicles_arrived = traci.simulation.getArrivedIDList()
        for veh in id_vehicles_arrived:
            for veh_sim in simulation.vehicles_in_simulation:
                if veh == veh_sim.id:  # If the vehicle has arrived then remove it from the simulation
                    simulation.update_step_fin_veh(simulation.step, veh_sim)
                    simulation.remove_vehicles_in_simulation(veh_sim)
                    simulation.add_veh_total_number(1)  # Update Vehicle Total Number in all simulation
                    for veh_w in window.vehicles_in_w:
                        if veh == veh_w.id:
                            window.remove_vehicles_in_w(veh_w)
                            window.sub_veh_total_number_w(1)
                            break
                    break

        ## FOR EACH VEHICLE calculate its emisions :
        for veh in simulation.vehicles_in_simulation:
            # emissions:
            vehNOxEmission = traci.vehicle.getNOxEmission(veh.id)  # Return the NOx value per vehicle in each ste
            # simulation
            simulation.add_NOx_Total(vehNOxEmission)
            veh.add_NOx(vehNOxEmission)
            # Per Window
            window.add_NOx_Total_w(vehNOxEmission)
            # Control Area:
            string_current_edge = traci.vehicle.getLaneID(veh.id)
            if string_current_edge in control_area_edges_cnf:
                # All simulation:
                simulation.add_NOx_control_zone(vehNOxEmission)
                # Per window:
                window.add_NOx_control_zone_w(vehNOxEmission)
                # Control area:
                veh.enter_cz = True
                window.add_vehicles_in_control_zone_w(veh.id)

        ## IMPORTANT PART - FOR EACH VEHICLE analyze whether it can enter or not :
        if strategy != "noControl":
            if simulation.k >= 1:  # all cars enter
                if lastkSmaller1: # if the last k is >1 no need to redo
                    all_cars_enter(simulation, enter_control_area_edges)
                lastkSmaller1 = False
            elif simulation.k < 0:  # no cars enter
                no_cars_enter(simulation, enter_control_area_edges)
                lastkSmaller1 = True
            else:  # some cars enter
                some_cars_enter(simulation, enter_control_area_edges, historicalTable, historical_max_num_pack)
                lastkSmaller1 = True

        # Window
        if ((simulation.step % window_size) == 0):
            # Discount NOx of the last window:
            for w in range(len(simulation.windows)):
                if simulation.windows[w].step == simulation.step - window_size:
                    lambda_l = randomLambda.uniform(0.8, 1.2)
                    window.lambda_l = lambda_l
                    x_cz = lambda_l * subs_NOx
                    # for heating up if emissens are lower than e_ini, use e_ini
                    if start_control and window.NOx_control_zone_w < e_ini:
                        p_t = max(0, simulation.windows[w].p_t + e_ini - x_cz)
                    else:
                        p_t = max(0, simulation.windows[w].p_t + window.NOx_control_zone_w - x_cz)
                        start_control = False

                    y_total = x_cz * size_ratio
                    if start_total and window.NOx_total_w < (e_ini * size_ratio):
                        p_t_total = max(0, simulation.windows[w].p_t_total + (e_ini * size_ratio) - y_total)
                    else:
                        p_t_total = max(0, simulation.windows[w].p_t_total + window.NOx_total_w - y_total)
                        start_total = False

                    simulation.p_t = p_t
                    window.p_t = p_t
                    window.p_t_total = p_t_total

            # Add variables for the last 50 steps
            simulation.add_window(window)
            print("Window: ", window)

            # Reboot all

            window = Window(simulation.step, window.vehicles_in_w.copy(), window.vehicles_in_control_zone_w.copy(), 0,
                            0, window.veh_total_number_w)
            window.vehicles_in_control_zone_w = set()

            # CONTROL ZONE
            # calculate k
            calculate_k(simulation, window)

    results.results(simulation, window_size, p_t_ini,size_ratio, subs_NOx, e_ini, min_packages, max_packages)

    # TraCI
    traci.close()
    sys.stdout.flush()