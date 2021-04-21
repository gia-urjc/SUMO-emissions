""" Main program. Set the parameters below imports and run this .py """
import os
import sys
import optparse
from sumolib import checkBinary  # noqa
import traci  # noqa

from SUMO_emissions_runner import runner
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

strategy, timeStep,probability_E ,probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T,\
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
    rCSV.readConfigurationCSV()

##################################
########### CONFIGURE ############
##################################
# DENSITY FILE
if strategy == "VE":
    file_name_density = r"../calculate_density_distribution/density_distribution_calculated/density_distribution_results_VE_0.csv"  # Change the txt name if is necessary
elif strategy == "VEP":
    file_name_density = r"../calculate_density_distribution/density_distribution_calculated/density_distribution_results_VEP_0.csv"  # Change the txt name if is necessary
elif strategy == "RRE":
    file_name_density = r"../calculate_density_distribution/density_distribution_calculated/density_distribution_results_RRE_0.csv"  # Change the txt name if is necessary
elif strategy == "RREP":
    file_name_density = r"../calculate_density_distribution/density_distribution_calculated/density_distribution_results_RREP_0.csv"  # Change the txt name if is necessary
else:
    file_name_density = ""
##################################
##################################
##################################

densityTable = dict()

"""
MAIN PROGRAM

"""

def get_options():
    """" SUMO options """
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action ="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run_main(strategy, file_name_density, densityTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
               subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges, route):
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary("SUMO")
    else:
        sumoBinary = checkBinary("sumo-gui")

    #traci.start([sumoBinary, "-c", "casebase.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])
    traci.start([sumoBinary, "-c", "../configuration/emissions.sumocfg"])

    # runner.py :
    runner.run(strategy, file_name_density, densityTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
               subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges, route)

if __name__ == "__main__":
    run_main(strategy, file_name_density, densityTable, window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
               subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges, "")