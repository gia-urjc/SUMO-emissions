"""
Runner with one normal threshold:
k(t) = Kp·e(t) + bias
e(t) = ((θH +θL )/2 )– p(t)=  θM – p(t)
Kp = 1/(θH – θL)

--------------
    main def at the end:
        run (strategy,file_name_density, densityTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
            subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges)
"""

from pathlib import Path
import math
import random
import traci
import sys
import os
import pandas as pd

from SUMO_emissions_runner import results
from SUMO_emissions_runner.Vehicle import Vehicle
from SUMO_emissions_runner.Simulation import Simulation
from SUMO_emissions_runner.Window import Window


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


def some_cars_enter(simulation, enter_control_area_edges, densityTable):
    """ If the vehicle is near the control area => Calculate whether or not a vehicle enters the control area (depends on strategy)"""

    for veh in simulation.vehicles_in_simulation:
        if closeToRestrictedArea(veh, enter_control_area_edges):
            # determine whether the car enters
            enters = False
            try:
                if simulation.strategy == "baseline":
                    enters = baselineTester(simulation.k)
                elif simulation.strategy != "noControl":
                    enters = densityTester(simulation, veh, densityTable)
            except NameError:
                print("Strategy doesn't found")
                raise RuntimeError('error')

            if enters:  # car should enter the area
                if traci.vehicle.getVehicleClass(veh.id) == "custom1":
                    setAllowCar(veh, simulation)
            else:  # car should not enter the area
                if traci.vehicle.getVehicleClass(veh.id) != "custom1":
                    setNotAllowCar(veh)


def calculate_k(simulation, w, bias):
    """ Calculate k: access permission level """
    if simulation.strategy != "noControl":
        aux = ((((simulation.threshold_H + simulation.threshold_L)/2) - simulation.p_t) / (simulation.threshold_H - simulation.threshold_L)) + bias
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


def densityTester(simulation, veh, densityTable):
    """ If True (vehicle is allowed)"""
    # simulation.k = 1 NO RESTRICTIONS
    # simulation.k = 0 NO VEHICLES ALLOWED
    # num_control = (k-acc(ant))/(acc-acc(ant))
    if simulation.strategy == "VEP" or simulation.strategy == "RREP":
        vType = veh.originalvType + "-" + str(veh.n_packages)
    else:
        vType = veh.originalvType
    previous = ""
    for key, value in densityTable.items():
        if key == vType:
            break
        previous = key
    if previous == "":
        aux = 0
    else:
        aux = densityTable[previous]
    if (densityTable[vType] - aux) == 0:
        num_control = 2
    else:
        num_control = (simulation.k - aux) / (densityTable[vType] - aux)
    if random.uniform(0, 1) <= num_control:
        return True
    else:
        return False


def openDensityDistribution(file_name_density, densityTable):
    """ Opens density distribution and writes the data in a variable densityTable (dict())"""
    # OPEN DENSITY DISTRIBUTION
    try:
        df = pd.read_csv(file_name_density, delimiter=";")
        for i in range(df.shape[0]):
            densityTable[df.iloc[i][0]] = df.iloc[i][1]
        print("densityTable =", densityTable)
    except OSError:
        if file_name_density == "":
            print('density distribution is not necessary')
        else:
            print('cannot open', file_name_density)

"""
RUN - MAIN DEF 

"""
def run(strategy, random_seed, file_name_density, densityTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
            subs_NOx, e_ini, ini_lambda_l, min_randomLambda, max_randomLambda, ini_k_window, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges, bias, route = ""):
    """"""
    # Initialization
    random.seed(random_seed)
    randomLambda = random.Random(random_seed)
    randomPackages = random.Random(random_seed)
    print("RUN")
    print(strategy)
    simulation = Simulation(step=0, threshold_L=threshold_L, threshold_H=threshold_H, k=1, strategy=strategy)
    window = Window(simulation.step, set(), set(), 0, 0, 0, 0, 0, ini_k_window, ini_lambda_l)

    # open density distribution file if is necessary (only with VE, VEP, RRE or RREP
    if (strategy != "baseline" and strategy != "noControl"):
        openDensityDistribution(file_name_density, densityTable)

    # put the centre closed for not allowed cars
    # On this version, all the cars have the access opened at the beginning, and  later we calculate if one car enter or not (class custom1)
    for aEd in control_area_edges_cnf:
        traci.lane.setDisallowed(laneID=aEd, disallowedClasses=["custom1"]) # All the class are not custom1 at the beginning

    # Control variables
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
            #traci.simulationStep() # TODO QUITAR
            simulation.p_t = p_t_ini
            window.step = simulation.step
            window.NOx_total_w = 0 ## All the map
            window.NOx_control_zone_w = 0 ## Control zone
            window.p_t = p_t_ini
            window.p_t_total = p_t_ini
            window.lambda_l = ini_lambda_l

            # Add variables for the last 50 steps
            simulation.add_window(window)
            print("Window: ", window)
            # Reboot all
            #window = Window(simulation.step, window.vehicles_in_w.copy(), set(), 0, 0, window.veh_total_number_w) # TODO QUITAR

            # calculate k
            calculate_k(simulation, window, bias) ## k: access permission level

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
                    id_veh_dep_Vehicle = Vehicle(id_veh_dep) # We create the Vehicle Object only with the id
                    id_veh_dep_Vehicle.step_ini = simulation.step
                    num_packages = randomPackages.randint(min_packages, max_packages)
                    id_veh_dep_Vehicle.n_packages = num_packages
                    id_veh_dep_Vehicle.vType = traci.vehicle.getTypeID(id_veh_dep_Vehicle.id)
                    id_veh_dep_Vehicle.originalvType = traci.vehicle.getTypeID(id_veh_dep_Vehicle.id)
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

        ## FOR EACH VEHICLE calculate its emissions :
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
            if string_current_edge in control_area_edges_cnf: # If a car is in the control area:
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
                if lastkSmaller1: # if the last k is >1 no need to redo, else:
                    all_cars_enter(simulation, enter_control_area_edges)
                lastkSmaller1 = False
            elif simulation.k < 0:  # no cars enter
                no_cars_enter(simulation, enter_control_area_edges)
                lastkSmaller1 = True
            else:  # some cars enter
                some_cars_enter(simulation, enter_control_area_edges, densityTable)
                lastkSmaller1 = True

        # Window
        if ((simulation.step % window_size) == 0):
            # Discount NOx of the last window:
            for w in range(len(simulation.windows)):
                if simulation.windows[w].step == simulation.step - window_size:
                    lambda_l = randomLambda.uniform(min_randomLambda, max_randomLambda) # (0.8,1.2)
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
            calculate_k(simulation, window, bias)

    results.results(simulation, window_size, p_t_ini,size_ratio, subs_NOx, e_ini, min_packages, max_packages, route)

    # TraCI
    traci.close()
    sys.stdout.flush()