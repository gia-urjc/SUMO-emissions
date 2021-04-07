from SUMO_emissions_runner.main import run_main
from configuration import readConfigurationCSV as rCSV
import pandas as pd
import os
from collections import OrderedDict

def generateHistorical():
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
        route = r"../generate_historical/noControl_resultsHistorical/results_file_noControl.csv" # CHANGE IF YOU NEED
    elif election == "2":
        print("First, runs noControl to create the historical")
        if not os.path.exists("noControl_resultsHistorical"): # If the folder doesn't exists  -> Create folder
            os.makedirs("noControl_resultsHistorical")
        route = r"../generate_historical/noControl_resultsHistorical/results_file_noControl.csv" # CHANGE IF YOU NEED
        # TODO: Crear una condicion para que no se reescriba un nocontrol ya creado
        run_main("noControl", "", dict(), window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
                   subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges, route)

    print("Creating historical...")
if __name__ == "__main__":
    strategy, timeStep, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()

    route = r"../generate_historical/noControl_resultsHistorical/results_file_noControl.csv"  # CHANGE IF YOU NEED
    df = pd.read_csv(route, delimiter=";")

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

    total_prob = probability_E + probability_G + probability_D + probability_HD + probability_N + probability_H + probability_T

    prob_norm = {"eVehicle": probability_E / total_prob, 'gasolineEuroSix': probability_G / total_prob,
                 'dieselEuroSix': probability_D / total_prob, 'hovDieselEuroSix': probability_HD / total_prob,
                 'normalVehicle': probability_N / total_prob, 'highEmissions': probability_H / total_prob,
                 'truck': probability_T / total_prob}


    em_average_s_o = OrderedDict(em_average_s)

    acc = dict()
    ilast = ""
    for i in em_average_s_o:
        if tuple(em_average_s_o.keys()).index(i) == 0:
            acc[i] = prob_norm[i]
        else:
            acc[i] = acc[ilast]+prob_norm[i]
        ilast = i

    print(acc)


    # HECHO PARA VE, FALTARIA SACARLO A UN TXT
    # FALTARIA VERLO PARA RRE, VEEP, RREP









