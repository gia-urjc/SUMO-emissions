""" Main program. Set the parameters below imports and run this .py """
import os
import sys
import optparse
from sumolib import checkBinary  # noqa
import traci  # noqa

import runner
from configuration import readConfigurationCSV as rCSV

# import python modules from $SUMO/HOME directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exist("please declare environment variable 'SUMO_HOME'")


"""
PARAMETERS TO CONFIGURE

"""

strategy, timeStep,probability_E ,probability_G, probability_D, probability_HG, probability_N, probability_H, probability_T,\
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
    rCSV.readConfigurationCSV()

# HISTORICAL FILE
if strategy == "VE":
    file_name = r"./historicals/historical_VE.txt" # Change the txt name if is necessary
elif strategy == "VEP":
    file_name = r"./historicals/historical_VEP.txt" # Change the txt name if is necessary
elif strategy == "RRE":
    file_name = r"./historicals/historical_RRE.txt" # Change the txt name if is necessary
elif strategy == "RREP":
    file_name = r"./historicals/historical_RREP.txt" # Change the txt name if is necessary
else:
    file_name = ""

historicalTable = dict()

"""
MAIN PROGRAM

"""
def get_options():
    """" SUMO options """
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

    # runner.py :
    runner.run(strategy, file_name, historicalTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
               subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges)
