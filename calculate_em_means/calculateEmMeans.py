from SUMO_emissions_runner.main import run_main
from configuration import readConfigurationCSV as rCSV
import pandas as pd
from pathlib import Path
import os
import csv
import sys

def calculateEmMeans():
    ##################################
    ########### CONFIGURE ############
    ##################################
    """ Change if you need"""
    # No control file:
    folderNoControl = "noControl_resultsHistorical"
    nameFileNoControl = "results_file_noControl"  #If you are going to create a new NoControl, yo don't need to change it
    # Results file:
    fileEmMeansResults = "em_means_results_"
    folderEmMeansResults = "em_means_calculated"
    ##################################
    ##################################
    ##################################

    strategy, timeStep, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    ini_lambda_l, min_randomLambda, max_randomLambda, ini_k_window, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()


    election = input("Press 1 to use your noControl file (change in code) or 2 to create a new file \n")
    while election != "1" and election != "2":
        election = input("Press 1 to use your noControl file (change in code) or 2 to create a new file. Introduce: 1 or 2 \n")

    if election == "1":
        print("1")
        route_NoControl = r"./" + folderNoControl +"/" + nameFileNoControl + ".csv"
    elif election == "2":
        print("First, runs noControl to create the historical")

        if not os.path.exists(folderNoControl): # If the folder doesn't exists  -> Create folder
            os.makedirs(folderNoControl)

        cont_file = 0
        route_NoControl = r"./" + folderNoControl +"/"+ nameFileNoControl + str(cont_file) + ".csv"
        fileObject = Path(route_NoControl)
        while fileObject.is_file():  # If the file exists -> new file name
            cont_file += 1
            route_NoControl = r"./" + folderNoControl + "/" + nameFileNoControl + str(cont_file) + ".csv"
            fileObject = Path(route_NoControl)

        run_main("noControl", "", dict(), window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
                   subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges, route_NoControl)

    try:
        df = pd.read_csv(route_NoControl, delimiter=";")
    except FileNotFoundError:
        print('File does not exist, change it and rerun')
        sys.exit()
    print("Calculating em_means...")

    limit = (df[df["1"]=="FOR_DENSITY_DISTRIBUTION"].index.values[0])+1
    drop_index = range(0, limit)
    df = df.drop(drop_index)
    df = df.drop(columns=["4", "5", "6", "7", "8", "9", "10", "11"])
    df = df.rename({'1':df.loc[limit]["1"], '2':df.loc[limit]["2"], '3':df.loc[limit]["3"]}, axis = 1)
    df = df.drop(limit)

    vTypes_vehs = set()
    em_means = dict()

    for v in df["vType"]:
        vTypes_vehs.add(v)

    df.set_index('vType', inplace=True)

    for v in vTypes_vehs:
        em_means[v] = float(df.loc[v]["NOx_total"]) / float(df.loc[v]["total_time"])
    em_means_s = sorted(em_means.items(), key= lambda x: x[1])

    print(em_means_s)

    """ Write results in a file """

    if not os.path.exists(folderEmMeansResults):  # If the folder doesn't exists  -> Create folder
        os.makedirs(folderEmMeansResults)

    cont_file_write = 0
    fileNameWrite = r"./"+ folderEmMeansResults + "/" + fileEmMeansResults + strategy + "_" + str(cont_file_write) + ".csv"
    fileObjectWrite = Path(fileNameWrite)
    while fileObjectWrite.is_file():  # If the file exists -> new file name
        cont_file_write += 1
        fileNameWrite = r"./" + folderEmMeansResults +"/" + fileEmMeansResults + strategy + "_" +str(cont_file_write) + ".csv"
        fileObjectWrite = Path(fileNameWrite)


    with open(fileNameWrite, mode='w', newline='') as f_csv:
        print(fileNameWrite)
        f = csv.writer(f_csv, delimiter=';')
        """Second, we write the parameters"""
        f.writerow(["vType", "em_means"])

        for m, k in em_means_s:
            f.writerow([m,k])

    print("done")



if __name__ == "__main__":
    calculateEmMeans()