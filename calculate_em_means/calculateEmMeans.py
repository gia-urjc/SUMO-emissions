from SUMO_emissions_runner.main import run_main
from configuration import readConfigurationCSV as rCSV
import pandas as pd
from pathlib import Path
import os
import csv

def calculateEmMeans():
#if __name__ == "__main__":
    strategy, timeStep, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()

    election = input("Press 1 to use your noControl file (change in code) or 2 to create a new file \n")
    while election != "1" and election != "2":
        election = input("Press 1 to use your noControl file (change in code) or 2 to create a new file. Introduce: 1 or 2 \n")

    if election == "1":
        print("1")
        route_NoControl = r"../generate_historical/noControl_resultsHistorical/results_file_noControl.csv" # CHANGE IF YOU NEED
    elif election == "2":
        print("First, runs noControl to create the historical")
        if not os.path.exists("noControl_resultsHistorical"): # If the folder doesn't exists  -> Create folder
            os.makedirs("noControl_resultsHistorical")
        route_NoControl = r"../generate_historical/noControl_resultsHistorical/results_file_noControl.csv" # CHANGE IF YOU NEED
        # TODO: Crear una condicion para que no se reescriba un nocontrol ya creado
        run_main("noControl", "", dict(), window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
                   subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges, route_NoControl)

    print("Creating historical...")

    df = pd.read_csv(route_NoControl, delimiter=";")

    limit = (df[df["1"]=="FOR_HISTORICAL"].index.values[0])+1
    drop_index = range(0, limit)
    df = df.drop(drop_index)
    df = df.drop(columns=["4", "5", "6", "7", "8", "9", "10", "11"])
    df = df.rename({'1':df.loc[limit]["1"], '2':df.loc[limit]["2"], '3':df.loc[limit]["3"]}, axis = 1)
    df = df.drop(limit)

    vTypes_vehs = set()
    em_average = dict()

    for v in df["vType"]:
        vTypes_vehs.add(v)

    df.set_index('vType', inplace=True)

    for v in vTypes_vehs:
        em_average[v] = float(df.loc[v]["NOx_total"]) / float(df.loc[v]["total_time"])
    em_average_s = sorted(em_average.items(), key= lambda x: x[1])

    print(em_average_s)

    """ Write results in a file """
    if not os.path.exists("e_means_calculated"):  # If the folder doesn't exists  -> Create folder
        os.makedirs("e_means_calculated")

    cont_file = 0
    file = "e_means_results_"
    fileName = r"./e_means_calculated/" + file + str(cont_file) + ".csv"
    fileObject = Path(fileName)
    while fileObject.is_file():  # If the file exists -> new file name
        cont_file += 1
        fileName = r"./e_means_calculated/" + file + str(cont_file) + ".csv"
        print(fileName)
        fileObject = Path(fileName)


    with open(fileName, mode='w', newline='') as f_csv:
        print(fileName)
        f = csv.writer(f_csv, delimiter=';')
        """Second, we write the parameters"""
        f.writerow(["vType", "em_means"])
        for m, k in em_average_s:
            f.writerow([m,k])



if __name__ == "__main__":
    calculateEmMeans()