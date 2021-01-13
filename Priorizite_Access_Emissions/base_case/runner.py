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

def run():
    print("RUN")

    step = 0

    CO2_total = 0
    CO2_zona_control = 0

    vehicles_in_simulation = []
    while traci.simulation.getMinExpectedNumber() > 0: # While there are cars (and waiting cars)

        traci.simulationStep() # Advance one time step

        id_vehicles_departed = traci.simulation.getDepartedIDList()
        id_list_vehicles_departed = list(id_vehicles_departed)
        if (id_list_vehicles_departed):
            vehicles_in_simulation.extend(id_list_vehicles_departed)
            #print(vehicles_in_simulation)

        id_vehicles_arrived = traci.simulation.getArrivedIDList()
        for veh in id_vehicles_arrived:
            if veh in vehicles_in_simulation:
                vehicles_in_simulation.remove(veh)
        #print(vehicles_in_simulation)

        for veh in vehicles_in_simulation:
            vehCO2Emission = traci.vehicle.getCO2Emission(vehID=veh)
            pos = traci.vehicle.getPosition(vehID=veh)
            #print(pos, vehCO2Emission, veh)
            CO2_total += vehCO2Emission
            # Control Area:
            if (pos[1]<=302 and pos[1]>=-4) and (pos[0]>=-4 and pos[0]<=302):
                CO2_zona_control += vehCO2Emission
                print("SI ", CO2_zona_control)
        step +=1

    print("CO2_total: ", CO2_total, ". CO2_zona_control", CO2_zona_control)
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
    traci.start([sumoBinary, "-c", "base_case.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output","emissionOutput.xml"])

    run()