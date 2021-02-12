import os
import sys
import optparse
import random

# import python modules from $SUMO/HOME directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exist("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

from Vehicle import Vehicle
from Simulation import Simulation
from Window import Window

from pathlib import Path

"""
PARAMETERS TO CONFIGURE

"""

""" 10 veh
window_size = 50
threshold_L = 30
threshold_H = 40
"""
# +100 veh:
window_size = 60
threshold_L = 200
threshold_H = 250

# p(t)
alpha_ini = 0.5
p_t_ini = 75

# Nº packages:
min_packages = 5
max_packages = 10

# Control Area:
control_area_edges_cnf=["gneE191_0", "-gneE191_0", "gneE192_0", "-gneE192_0", "gneE197_0", "-gneE197_0",
                        "gneE198_0", "-gneE198_0", "gneE203_0", "-gneE203_0", "gneE199_0", "-gneE199_0",
                        "gneE279_0", "-gneE279_0", "gneE209_0", "-gneE209_0", "gneE210_0", "-gneE210_0",
                        "gneE215_0", "-gneE215_0", "gneE211_0", "-gneE211_0", "gneE216_0", "-gneE216_0"]
    # Control Area Limits. See with NetEdit:
min_x = 3503
min_y = -3503
max_x = 8746
max_y = -8746

"""
CONTINUE WITH DEF's

"""
def update_vehicles_to_control_area(simulation):
    for veh_load in simulation.vehs_load:
        #if (veh_load.id != "simulation.findRoute"):
        traci.vehicle.setParameter(veh_load.id, "has.rerouting.device", "true") ## Add rerouter tool
        #print(veh_load.id)
        # Currently route and vehicle class
        vClass_last = traci.vehicle.getVehicleClass(veh_load.id)
        edges_last = traci.vehicle.getRoute(veh_load.id)
        string_edge = edges_last[len(edges_last) - 1] + "_0"
        """
        # If destination in control area:
        if (string_edge in simulation.control_area_edges):
            traci.vehicle.setType(vehID=veh_load.id, typeID="authority") # Here the program changes the vClass
            if (vClass_last == "evehicle"):
                traci.vehicle.setEmissionClass(veh_load.id, "zero")
        """


def decision_maker(simulation, w):
    p = simulation.NOx_control_zone_restriction_mode

    if p <= simulation.threshold_L: # NO RESTRICTIONS
        simulation.k = 1
        if simulation.restrictionMode:
            print("CONTROL ZONE OFF", simulation.NOx_control_zone_restriction_mode, simulation.step)
            print("p:", p, "k:", simulation.k)
            simulation.restrictionMode = False
            for aEd in simulation.control_area_edges:
                traci.lane.setAllowed(laneID=aEd, allowedClasses=["authority", "passenger", "evehicle"])
            for veh in simulation.vehicles_in_simulation:
                traci.vehicle.rerouteTraveltime(veh.id, True)

    elif p >= simulation.threshold_H: # NO VEHICLES ALLOWED
        simulation.k = 0

    else: # OTHERWISE
        simulation.k = (simulation.threshold_H - p)/(simulation.threshold_H - simulation.threshold_L)

    if p>simulation.threshold_L:
        # CONTROL ZONE ON
        # print(simulation.step, simulation.NOx_control_zone_restriction_mode)
        if simulation.vehicles_in_simulation != [] and simulation.restrictionMode == False:
            print("CONTROL ZONE ON", simulation.NOx_control_zone_restriction_mode, simulation.step)
            print("p:", p, "k:", simulation.k)
            simulation.restrictionMode = True

            for aEd in simulation.control_area_edges:
                traci.lane.setDisallowed(laneID=aEd, disallowedClasses=["passenger", "evehicle"])
                traci.lane.setAllowed(laneID=aEd, allowedClasses=["authority"])
    w.k = simulation.k

def setEmissionClass(emiLastClass, veh):
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

def setSwitchVehicleClass(emiClass, veh):
    if emiClass == "Zero/default":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="evehicle")
        traci.vehicle.setType(vehID=veh.id, typeID="eVehicle")
    elif emiClass == "HBEFA3/LDV_G_EU6":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="gasolineEuroSix")
    elif emiClass == "HBEFA3/LDV_D_EU6":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="dieselEuroSix")
    elif emiClass == "HBEFA3/PC_D_EU6":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="hovGasolinaEuroSix")
    elif emiClass == "HBEFA3/PC_G_EU4":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="normalVehicle")
    elif emiClass == "HBEFA3/PC_G_EU3":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="passenger")
        traci.vehicle.setType(veh.id, typeID="highEmissions")
    elif emiClass == "HBEFA3/HDV_D_EU4":
        traci.vehicle.setVehicleClass(vehID=veh.id, clazz="truck")
        traci.vehicle.setType(veh.id, typeID="truck")
    print("We switch to its previous class", traci.vehicle.getVehicleClass(vehID=veh.id))


def class_veh_changer (simulation, veh):
    # simulation.k = 1 NO RESTRICTIONS
    # simulation.k = 0 NO VEHICLES ALLOWED
    print(simulation.step, veh.id, veh.NOx , simulation.k, simulation.NOx_control_zone_restriction_mode) # step, veh, k, p
    if simulation.k != 1:
        # current edge in control area
        rouIndex = traci.vehicle.getRouteIndex(veh.id)
        edges = traci.vehicle.getRoute(veh.id)

        string_current_edge = edges[rouIndex] + "_0"
        if simulation.restrictionMode and traci.vehicle.getVehicleClass(veh.id) != "authority":
            if (string_current_edge in simulation.control_area_edges):  # current edge in control area
                emiLastClass = traci.vehicle.getEmissionClass(veh.id)
                traci.vehicle.setType(vehID=veh.id, typeID="authority")
                setEmissionClass(emiLastClass, veh)


        if simulation.k != 0 and (string_current_edge not in simulation.control_area_edges):  # OTHERWISE - PROBABILITY and current edge not in control area
            """ k is the probability """
            rand = random.uniform(0, 1)
            print(rand, simulation.k)
            if rand < simulation.k:
                print("Enter")
                if "authority" not in traci.vehicle.getTypeID(veh.id):
                    print("No Auto")
                    emiLastClass = traci.vehicle.getEmissionClass(veh.id)
                    print(traci.vehicle.getTypeID(veh.id))
                    traci.vehicle.setType(vehID=veh.id, typeID="authority")
                    print(traci.vehicle.getTypeID(veh.id))
                    setEmissionClass(emiLastClass, veh)
                    print(traci.vehicle.getTypeID(veh.id), traci.vehicle.getEmissionClass(veh.id))
            elif traci.vehicle.getVehicleClass(vehID=veh.id)=="authority":
                print("AUTHORITY", traci.vehicle.getTypeID(veh.id), traci.vehicle.getEmissionClass(veh.id), traci.vehicle.getVehicleClass(veh.id))
                em_Class = traci.vehicle.getEmissionClass(veh.id)
                setSwitchVehicleClass(em_Class, veh)
                print(traci.vehicle.getTypeID(veh.id), traci.vehicle.getEmissionClass(veh.id), traci.vehicle.getVehicleClass(veh.id))


def run():
    random.seed(1)
    print("RUN")
    simulation = Simulation(step = 0, threshold_L = threshold_L, threshold_H= threshold_H, k = 1,
                            control_area_edges=control_area_edges_cnf)
    window = Window(simulation.step,set(), set(), 0,  0, 0, 0, 0, 1, 0.5, 0.8)

    while traci.simulation.getMinExpectedNumber() > 0:  # While there are cars (and waiting cars)
        # LAST STEP
        # Vehicles to control area
        vehs_load = traci.simulation.getLoadedIDList()
        vehs_load_Vehicle = []
        for veh in vehs_load:
            if veh != "simulation.findRoute":
                vehicl = Vehicle(veh)
                vehs_load_Vehicle.append(vehicl)

        simulation.vehs_load = vehs_load_Vehicle
        update_vehicles_to_control_area(simulation)

        if simulation.step == 0:
            simulation.NOx_control_zone_restriction_mode = p_t_ini
            window.NOx_total_w = p_t_ini
            window.NOx_control_zone_w = p_t_ini
            window.p_t = p_t_ini
            window.p_t_total=p_t_ini
            window.lambda_l = 0.8
            window.alpha = alpha_ini
            simulation.add_alpha(alpha_ini)
            #print("STEP 0", simulation.alphas)
            #print(simulation.alphas[len(simulation.alphas) - 1])

            # Add variables for the last 50 steps
            simulation.add_window(window)
            print("Window: ", window)

            # Reboot all
            window = Window(simulation.step, window.vehicles_in_w.copy(), set(), 0, 0, window.veh_total_number_w)


            # NEW STEP
        traci.simulationStep()  # Advance one time step: one second
        simulation.update_Step()
        window.update_Step()




        # MANAGE VEHICLES - All simulation
        id_vehs_departed = list(traci.simulation.getDepartedIDList()) # Vehicles in simulation

        if(id_vehs_departed): # if the list is not empty
            # All simulation:
            id_vehs_departed_Vehicle = []
            for id_veh_dep in id_vehs_departed:
                if id_veh_dep != "simulation.findRoute":
                    id_veh_dep_Vehicle = Vehicle(id_veh_dep)
                    id_veh_dep_Vehicle.step_ini = simulation.step
                    num_packages = random.randint(min_packages, max_packages)
                    id_veh_dep_Vehicle.n_packages = num_packages
                    id_veh_dep_Vehicle.vType = traci.vehicle.getTypeID(id_veh_dep_Vehicle.id)
                    id_vehs_departed_Vehicle.append(id_veh_dep_Vehicle)
            simulation.add_vehicles_in_simulation(id_vehs_departed_Vehicle) # Add vehicles to the simulation list
            simulation.add_all_veh(id_vehs_departed_Vehicle)
            # Per window:
            window.add_vehicles_in_w(simulation.vehicles_in_simulation)
            window.veh_total_number_w = len(window.vehicles_in_w)

        # Taking into account the vehicles that reach their destination:
        id_vehicles_arrived = traci.simulation.getArrivedIDList()
        for veh in id_vehicles_arrived:
            for veh_sim in simulation.vehicles_in_simulation:
                if veh == veh_sim.id: # If the vehicle has arrived then remove it from the simulation
                    simulation.update_step_fin_veh(simulation.step, veh_sim)
                    simulation.remove_vehicles_in_simulation(veh_sim)
                    simulation.add_veh_total_number(1)  # Update Vehicle Total Number in all simulation
                    for veh_w in window.vehicles_in_w:
                        if veh == veh_w.id:
                            window.remove_vehicles_in_w(veh_w)
                            window.sub_veh_total_number_w(1)
                            break
                    break



        ## IMPORTANT PART - FOR EACH VEHICLE:
        for veh in simulation.vehicles_in_simulation:
            # Emissions:
                # All simulation
            vehNOxEmission = traci.vehicle.getNOxEmission(veh.id)  # Return the NOx value per vehicle in each step
            simulation.add_NOx_Total(vehNOxEmission)
            veh.add_NOx(vehNOxEmission)
            #print(veh.id, veh.NOx)
                # Per Window
            window.add_NOx_Total_w(vehNOxEmission)

            # Control Area:
            pos = traci.vehicle.getPosition(vehID=veh.id)  # (x,y)

            if (pos[1] <= min_y and pos[1] >= max_y) and (pos[0] >= min_x and pos[0] <= max_x):  # x=> 0, y=>1. If the vehicle is in the control area
                # All simulation:
                simulation.add_NOx_control_zone(vehNOxEmission)
                # Per window:
                window.add_NOx_control_zone_w(vehNOxEmission)
                # Control area:
                simulation.add_NOx_control_zone_restriction_mode(vehNOxEmission)


            # Route lenght per vehicle
            rouIndex = traci.vehicle.getRouteIndex(veh.id)
            edges = traci.vehicle.getRoute(veh.id)

            if veh not in window.vehicles_in_control_zone_w and edges[rouIndex]+ "_0" in control_area_edges_cnf:
                window.add_vehicles_in_control_zone_w(veh.id)
            """
            if rouIndex == (len(edges) - 1):  # Only if is the last edge
                stage = traci.simulation.findRoute(edges[0], edges[rouIndex])
                rouLength = stage.length  # Route Length
                veh.total_km = rouLength
            """

            # Control area - Threshold:
            class_veh_changer(simulation, veh)

                # REROUTE VEHICLES:
            if simulation.restrictionMode:
                inList = False
                for edg in edges:
                    edgStrng = edg + "_0"
                    if edgStrng in simulation.control_area_edges:
                        inList = True
                        break
                if inList:
                    traci.vehicle.rerouteTraveltime(veh.id, True)

        # Window
        if ((simulation.step % window_size) == 0):
            # Discount NOx of the last window:
            for w in range(len(simulation.windows)):
                if simulation.windows[w].step == simulation.step - window_size:
                    lambda_l = random.uniform(0.8, 1.2)

                    alpha = max(0.5, min(1, lambda_l * simulation.alphas[len(simulation.alphas) - 1]))
                    simulation.add_alpha(alpha)

                    window.lambda_l = lambda_l
                    window.alpha = alpha

                    p_t = alpha * simulation.windows[w].p_t + window.NOx_control_zone_w
                    p_t_total = alpha * simulation.windows[w].p_t_total + window.NOx_total_w

                    simulation.NOx_control_zone_restriction_mode = p_t

                    # CONTROL ZONE
                    decision_maker(simulation, window)

                    window.p_t = p_t
                    window.p_t_total = p_t_total

                    if simulation.NOx_control_zone_restriction_mode < 0:
                        simulation.NOx_control_zone_restriction_mode = 0
                        window.p_t = 0

            # Add variables for the last 50 steps
            simulation.add_window(window)
            print("Window: ", window)

            # Reboot all

            window = Window(simulation.step, window.vehicles_in_w.copy(), window.vehicles_in_control_zone_w.copy(), 0, 0, window.veh_total_number_w)
            window.vehicles_in_control_zone_w = set()

        # CONTROL ZONE
        decision_maker(simulation, window)


        #print(simulation.step, "NOx_control_zone: ", simulation.NOx_control_zone, ". NOx_control_zone_restriction_mode: ", simulation.NOx_control_zone_restriction_mode, ". NOx_total: ", simulation.NOx_total)


    minutes = round(simulation.step / 60, 0)
    """
    for v in simulation.all_veh:
        simulation.total_kilometers += v.total_km
    """
    ## RESULTS FILE
    cont_file = 0
    file = "results_file_"
    fileName = r"./results/"+file+str(cont_file)+".txt"
    print(fileName)
    fileObject = Path(fileName)
    while fileObject.is_file():
        cont_file += 1
        fileName = r"./results/"+ file + str(cont_file) +".txt"
        print(fileName)
        fileObject = Path(fileName)
    f=open(fileName, "w")

    # Results:
    print("Windows:")
    f.write("Windows:\n")
    for w in simulation.windows:
        print(w)

        vehInW = ""
        for veh in w.vehicles_in_w:
            vehInW += veh.id + ","

        cont_vehInWCZ = len(w.vehicles_in_control_zone_w)

        vehInWCZ = ""
        for veh in w.vehicles_in_control_zone_w:
            vehInWCZ += veh + ","

        f.write(str(w.step) + ". NOx_total_w: " + str(w.NOx_total_w) + ". NOx_control_zone_w: " + str(w.NOx_control_zone_w) + ". veh_total_number_w: " + str(w.veh_total_number_w) + ". Vehicles: " + vehInW + ". Nº veh in control zone: " + str(cont_vehInWCZ) +". Vehicles in control zone: " + vehInWCZ +"\n")
    print("Vehicles:")
    f.write("Vehicles:\n")
    for v in simulation.all_veh:
        print(v)
        f.write(str(v.id) + " . Total NOx per vehicle: " + str(v.NOx) +"\n")
    print("In ", simulation.step, "seconds (", minutes, " minutes)")
    f.write("In "+ str(simulation.step)+ " seconds ("+ str(minutes)+ " minutes)\n")
    print("All simulation:")
    f.write("All simulation:\n")
    print(simulation)
    f.write(str(simulation.step) + ". restrictionMode: " + str(simulation.restrictionMode) + ".  NOx_total:" + str(simulation.NOx_total)+ \
               ". NOx_control_zone:" + str(simulation.NOx_control_zone) + ". veh_total_number: " + str(simulation.veh_total_number) +"\n")

    f.close()

    ## RESULTS FILE 2
    cont_file = 0
    file = "results_file_"
    fileName = r"./results2/" + file + str(cont_file) + ".csv"
    print(fileName)
    fileObject = Path(fileName)
    while fileObject.is_file():
        cont_file += 1
        fileName = r"./results2/" + file + str(cont_file) + ".csv"
        print(fileName)
        fileObject = Path(fileName)
    f = open(fileName, "w")

    # Results:

    f.write("BASELINE, "+"\n")
    f.write("PARAMETERS,"+"\n")
    f.write("window_size, threshold_L, threshold_H, alpha_ini, p_t_ini, min_packages, max_packages,"+"\n")
    f.write(str(window_size) +","+ str(threshold_L) +","+ str(threshold_H) +","+ str(alpha_ini) +","+ str(p_t_ini)+","+ str(min_packages) +","+ str(max_packages)+","+"\n")
    f.write("WINDOWS,"+"\n")
    f.write("step, NOx_total_w, NOx_total_acum, alpha, lambda, p_t_total, e_t_total, p_t_control_zone, e_t_control_zone, k_control_zone, num_veh_total, num_vehicles_control_zone,  "+"\n")

    acum = 0
    for w in simulation.windows:
        acum += w.NOx_total_w
        f.write(str(w.step) +","+ str(w.NOx_total_w) +","+ str(acum) +","+ str(w.alpha)+","+str(w.lambda_l)+","+str(w.p_t_total)+","+str(w.NOx_total_w)+","+str(w.p_t) +","+ str(w.NOx_control_zone_w) +","+ str(w.k)+","+ str(w.veh_total_number_w)+","+str(len(w.vehicles_in_control_zone_w))+","+"\n")

    f.write("VEHICLES,"+"\n")
    f.write("id, vType, NOx_total_veh, n_packages, step_ini, step_fin, total_time(sec),median_package,"+"\n")

    p_all= 0
    cont = 0
    for v in simulation.all_veh:
        total_time = v.step_fin - v.step_ini
        median_package = total_time / v.n_packages
        p_all += median_package
        cont +=1

        f.write(v.id  +","+ v.vType +","+ str(v.NOx)  +","+  str(v.n_packages)  +","+ str(v.step_ini) +","+  str(v.step_fin) +","+ str(total_time)+","+str(median_package) +","+"\n")

    median_package_all = p_all / cont
    f.write("ALL SIMULATION," + "\n")
    f.write("total_steps(sec), minutes, median_package_all_sim,"+ "\n")
    f.write(str(simulation.step) + "," + str(minutes)+ "," + str(median_package_all) +"," + "\n")

    f.close()


    # TraCI
    traci.close()
    sys.stdout.flush()













def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action ="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary("SUMO")
    else:
        sumoBinary = checkBinary("sumo-gui")
    traci.start([sumoBinary, "-c", "casebase.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])

    run()
