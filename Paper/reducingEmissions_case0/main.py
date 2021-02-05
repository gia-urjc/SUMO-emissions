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

"""
PARAMETERS TO CONFIGURE

"""
window_size = 50
threshold_size = 14

# Control Area:
control_area_edges_cnf=["gneE191_0", "-gneE191_0", "gneE192_0", "-gneE192_0", "gneE197_0", "-gneE197_0",
                        "gneE198_0", "-gneE198_0", "gneE203_0", "-gneE203_0", "gneE199_0", "-gneE199_0",
                        "gneE204_0", "-gneE204_0", "gneE209_0", "-gneE209_0", "gneE210_0", "-gneE210_0",
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

        # If destination in control area:
        if (string_edge in simulation.control_area_edges):
            traci.vehicle.setType(vehID=veh_load.id, typeID="authority") # Here the program changes the vClass
            if (vClass_last == "evehicle"):
                traci.vehicle.setEmissionClass(veh_load.id, "zero")


def run():
    print("RUN")
    simulation = Simulation(step = 0, threshold = threshold_size,
                            control_area_edges=control_area_edges_cnf)
    window = Window(simulation.step,0,  0, 0, set())

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

        # NEW STEP
        traci.simulationStep()  # Advance one time step: one second
        simulation.update_Step()
        window.update_Step()

        # Window
        if  ((simulation.step % window_size) == 0) and window.vehicles_in_w != []:  # Each window, window_size steps # TODO change [] for set()
            # Discount NOx of the last window:
            for w in range(len(simulation.windows)):
                if simulation.windows[w].step == simulation.step - window_size:
                    print(simulation.step, simulation.NOx_control_zone_restriction_mode)
                    simulation.sub_NOx_control_zone_restriction_mode(simulation.windows[w].NOx_control_zone_w)
                    if simulation.NOx_control_zone_restriction_mode < 0:
                        simulation.NOx_control_zone_restriction_mode = 0
                        print(simulation.step, simulation.NOx_control_zone_restriction_mode)


            # Add variables for the last 50 steps
            simulation.add_window(window)
            #print("Window: ", window)

            # Reboot all
            window = Window(simulation.step, 0,  0, 0, set())

        # MANAGE VEHICLES - All simulation
        id_vehs_departed = list(traci.simulation.getDepartedIDList()) # Vehicles in simulation
        if(id_vehs_departed): # if the list is not empty
            # All simulation:
            id_vehs_departed_Vehicle = []
            for id_veh_dep in id_vehs_departed:
                if id_veh_dep != "simulation.findRoute":
                    id_veh_dep_Vehicle = Vehicle(id_veh_dep)
                    id_vehs_departed_Vehicle.append(id_veh_dep_Vehicle)
            simulation.add_vehicles_in_simulation(id_vehs_departed_Vehicle) # Add vehicles to the simulation list
            simulation.add_all_veh(id_vehs_departed_Vehicle)
            # Per window:
            window.add_vehicles_in_w(simulation.vehicles_in_simulation)
            window.veh_total_number_w = len(window.vehicles_in_w)
            #print("Window: ", window)

        # Taking into account the vehicles that reach their destination:
        id_vehicles_arrived = traci.simulation.getArrivedIDList()
        for veh in id_vehicles_arrived:
            for veh_sim in simulation.vehicles_in_simulation:
                if veh == veh_sim.id: # If the vehicle has arrived then remove it from the simulation
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
            print(pos)

            if (pos[1] <= max_y and pos[1] >= min_y) and (pos[0] >= min_x and pos[0] <= max_x):  # x=> 0, y=>1. If the vehicle is in the control area
                # All simulation:
                simulation.add_NOx_control_zone(vehNOxEmission)
                # Per window:
                window.add_NOx_control_zone_w(vehNOxEmission)
                # Control area:
                simulation.add_NOx_control_zone_restriction_mode(vehNOxEmission)

            # Route lenght per vehicle
            rouIndex = traci.vehicle.getRouteIndex(veh.id)
            edges = traci.vehicle.getRoute(veh.id)

            if rouIndex == (len(edges) - 1):  # Only if is the last edge
                stage = traci.simulation.findRoute(edges[0], edges[rouIndex])
                rouLength = stage.length  # Route Length
                veh.total_km = rouLength

            # Control area - Threshold:
            string_current_edge = edges[rouIndex] + "_0"
            if simulation.restrictionMode and traci.vehicle.getVehicleClass(veh.id)!="authority":
                if (string_current_edge in simulation.control_area_edges):  #  current edge in control area
                    vClass_last2 = traci.vehicle.getVehicleClass(veh.id)
                    traci.vehicle.setType(vehID=veh.id, typeID="authority")
                    if (vClass_last2 != "passenger"):
                        traci.vehicle.setEmissionClass(veh.id, "zero")

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

        # CONTROL ZONE ON
        #print(simulation.step, simulation.NOx_control_zone_restriction_mode)
        if simulation.vehicles_in_simulation != [] and simulation.restrictionMode == False and simulation.NOx_control_zone_restriction_mode > threshold_size:
            print("CONTROL ZONE ON", simulation.NOx_control_zone_restriction_mode)
            simulation.restrictionMode = True

            for aEd in simulation.control_area_edges:
                traci.lane.setDisallowed(laneID=aEd, disallowedClasses=["passenger", "evehicle"])
                #print("disa ", traci.lane.getDisallowed(laneID=aEd))
                traci.lane.setAllowed(laneID=aEd, allowedClasses=["authority"])
                #print("alo ", traci.lane.getAllowed(laneID=aEd))

        # CONTROL ZONE OFF
        if (simulation.restrictionMode and simulation.NOx_control_zone_restriction_mode <= threshold_size):
            print("CONTROL ZONE OFF", simulation.NOx_control_zone_restriction_mode)
            simulation.restrictionMode = False
            for aEd in simulation.control_area_edges:
                traci.lane.setAllowed(laneID=aEd, allowedClasses=["authority", "passenger", "evehicle"])
            for veh in simulation.vehicles_in_simulation:
                traci.vehicle.rerouteTraveltime(veh.id, True)

        #print(simulation.step, "NOx_control_zone: ", simulation.NOx_control_zone, ". NOx_control_zone_restriction_mode: ", simulation.NOx_control_zone_restriction_mode, ". NOx_total: ", simulation.NOx_total)
    """
    print("HOLA")
    for w in simulation.windows:
        print("w")
        for veh in w.vehicles_in_w:
            print(veh)
    """

    minutes = round(simulation.step / 60, 3)
    for v in simulation.all_veh:
        simulation.total_kilometers += v.total_km

    # Results:
    print("Windows:")
    for w in simulation.windows:
        print(w)
    print("Vehicles:")
    for v in simulation.all_veh:
        print(v)
    print("In ", simulation.step, "seconds (", minutes, " minutes)")
    print("All simulation:")
    print(simulation)



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
    traci.start([sumoBinary, "-c", "case0.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])

    run()
