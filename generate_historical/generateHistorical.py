from SUMO_emissions_runner import runner
from configuration import readConfigurationCSV as rCSV

if __name__ == "__main__":
#def generateHistorical():
    strategy, timeStep, probability_E, probability_G, probability_D, probability_HG, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()

    election = input("Press 1 to use your noControl file or 2 to create a new file \n")
    while election != "1" and election != "2":
        election = input("Press 1 to use your noControl file or 2 to create a new file. Introduce: 1 or 2 \n")
    if election == "1":
        print("1")
    elif election == "2":
        print("First runs noControl to create the historical")
        runner.run("noControl", "", dict(), window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
                   subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges)
        print("Creating historical...")

        print("")
