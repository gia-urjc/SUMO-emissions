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

    while traci.simulation.getMinExpectedNumber() > 0: # While there are cars (and waiting cars)

        traci.simulationStep() # Advance one time step
        #det_vehicles = traci.inductionloop.getLastStepVehicleIDs("det_1_0")
        step +=1
        print("1")

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