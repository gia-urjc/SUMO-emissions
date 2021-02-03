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

def update_vehicles_to_control_area(simulation):
    for veh_load in simulation.vehs_load:
        if (veh_load != "simulation.findRoute"):
            traci.vehicle.setParameter(veh_load, "has.rerouting.device", "true") ## Add rerouter tool

            # Currently route and vehicle class
            vClass_last = traci.vehicle.getVehicleClass(veh_load)
            edges_last = traci.vehicle.getRoute(veh_load)
            string_edge = edges_last[len(edges_last) - 1] + "_0"

            # If destination in control area:
            if (string_edge in simulation.control_area_edges):
                traci.vehicle.setType(vehID=veh_load, typeID="authority") # Here the program changes the vClass
                if (vClass_last == "evehicle"):
                    traci.vehicle.setEmissionClass(veh_load, "zero")


def run():
    print("RUN")
    simulation = Simulation(step = 0, threshold = 14,
                            control_area_edges=["gneE19_0", "-gneE19_0", "gneE21_0", "-gneE21_0", "gneE16_0",
                                                "-gneE16_0", "gneE17_0", "-gneE17_0",
                                                "gneE18_0", "-gneE18_0", "gneE22_0", "-gneE22_0", "gneE20_0",
                                                "-gneE20_0", "gneE15_0", "-gneE15_0",
                                                "gneE24_0", "-gneE24_0", "gneE25_0", "-gneE25_0", "gneE14_0",
                                                "-gneE14_0", "gneE23_0", "-gneE23_0"])
    window = Window()

    while traci.simulation.getMinExpectedNumber() > 0:  # While there are cars (and waiting cars)
        # LAST STEP
        # Vehicles to control area
        vehs_load = traci.simulation.getLoadedIDList()
        simulation.vehs_load = vehs_load
        update_vehicles_to_control_area(simulation)

        # NEW STEP
        traci.simulationStep()  # Advance one time step: one second
        simulation.update_Step()

        # Window
        if simulation.step != 0 and ((simulation.step % 50) == 0) and window.vehicles_in_w != []:  # Each window 50 steps # TODO change [] for set()
            # Discount NOx of the last window:
            for w in range(len(simulation.windows)):
                if simulation.windows[w][0] == simulation.step - 50:
                    print(simulation.NOx_control_zone_restriction_mode, simulation.windows[w][4])
                    simulation.sub_NOx_control_zone_restriction_mode(simulation.windows[w][4])
                    print(simulation.NOx_control_zone_restriction_mode, simulation.windows[w][4])



                    

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
    #traci.start([sumoBinary, "-c", "base_case.sumocfg", "--step-length", "0.001",  "--tripinfo-output", "tripinfo.xml", "--emission-output","emissionOutput.xml"])
    traci.start([sumoBinary, "-c", "case3.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])

    run()
