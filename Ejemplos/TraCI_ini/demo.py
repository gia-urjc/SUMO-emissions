import os
import sys
import optparse

# We need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary # checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# Contains TraCI control loop:
def run():
    step = 0 # way of keeping track of our time step
    while traci.simulation.getMinExpectedNumber() > 0: # exit when no more vehicles left in the simulation
        traci.simulationStep() # Advance the simulation in one time step
        print(step)
        #if step == 100:
        #    traci.vehicle.changeTarget("1", "e9")
        #    traci.vehicle.changeTarget("3", "e9")

        # See which vehicles have passed in the last time step:
        det_vehicles = traci.inductionloop.getLastStepVehicleIDs("det_0")
        for veh in det_vehicles:
            print("Vehicle:",veh)
            traci.vehicle.changeLane(veh,2,25)
        step+=1
    traci.close()
    sys.stdout.flush() #consol
# Main entry point:
if __name__ == "__main__":
    options = get_options()

    # check binary:
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')



    # TraCI starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "demo.sumocfg", "--tripinfo-output", "tripinfo.xml"])

    run()
