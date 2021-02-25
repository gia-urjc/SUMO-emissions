import os
import sys
import optparse

import runner

# import python modules from $SUMO/HOME directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exist("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

"""
PARAMETERS TO CONFIGURE

"""
strategies = {0:"noControl", 1:"baseline", 2:"VE", 3:"VEP", 4:"RRE", 5:"RREP"}
strategy = strategies[2] # SELECT ONE: strategies[0] = historical_ve
                         #      ...    strategies[6] = RREP

# HISTORICAL FILE
if strategy == "VE":
    file_name = r"./historicals/historical_VE.txt" # Change the txt name if is necessary
elif strategy == "VEP":
    file_name = r"./historicals/historical_VEP.txt" # Change the txt name if is necessary
elif strategy == "RRE":
    file_name = r"./historicals/historical_RRE.txt" # Change the txt name if is necessary
elif strategy == "RREP":
    file_name = r"./historicals/historical_RREP.txt" # Change the txt name if is necessary

historicalTable = dict()

# Window size (steps) and thresholds:
window_size = 60

#values with no truck:
threshold_L = 80000
threshold_H = 100000
p_t_ini = 100000
size_ratio = 4
subs_NOx = 9000
e_ini=4000

# Nº packages:
min_packages = 1
max_packages = 20

# Control Area:
control_area_edges_cnf=["gneE191_0", "-gneE191_0", "gneE192_0", "-gneE192_0", "gneE197_0", "-gneE197_0",
                        "gneE198_0", "-gneE198_0", "gneE203_0", "-gneE203_0", "gneE199_0", "-gneE199_0",
                        "gneE279_0", "-gneE279_0", "gneE209_0", "-gneE209_0", "gneE210_0", "-gneE210_0",
                        "gneE215_0", "-gneE215_0", "gneE211_0", "-gneE211_0", "gneE216_0", "-gneE216_0"]
enter_control_area_edges=["gneE179_0", "-gneE179_0", "gneE181_0", "-gneE181_0", "gneE200_0", "-gneE200_0",
                        "gneE212_0", "-gneE212_0", "gneE239_0", "-gneE239_0", "gneE238_0", "-gneE238_0",
                        "gneE208_0", "-gneE208_0", "gneE196_0", "-gneE196_0"]

    # Control Area Limits. See with NetEdit:
min_x = 3503
min_y = -3503
max_x = 8746
max_y = -8746

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
    #traci.start([sumoBinary, "-c", "casebase.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])
    traci.start([sumoBinary, "-c", "emissions.sumocfg"])

    runner.run(strategy, file_name, historicalTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
               subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges,
               min_x, min_y, max_x, max_y)
