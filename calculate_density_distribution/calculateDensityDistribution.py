from configuration import readConfigurationCSV as rCSV
from collections import OrderedDict
import pandas as pd

def calculateDensityDistribution():
    route_e_means_calculated = r"../calculate_em_means/em_means_calculated/em_means_results_0.csv" # CHANGE IF YOU NEED
    em_means_s = dict()
    df = pd.read_csv(route_e_means_calculated, delimiter=";")

    for i in range (df.shape[0]):
        em_means_s[df.iloc[i][0]] = df.iloc[i][1]
    print("em_means :", em_means_s)




    strategy, timeStep, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()



    total_prob = probability_E + probability_G + probability_D + probability_HD + probability_N + probability_H + probability_T

    prob_norm = {"eVehicle": probability_E / total_prob, 'gasolineEuroSix': probability_G / total_prob,
                 'dieselEuroSix': probability_D / total_prob, 'hovDieselEuroSix': probability_HD / total_prob,
                 'normalVehicle': probability_N / total_prob, 'highEmissions': probability_H / total_prob,
                 'truck': probability_T / total_prob}


    em_means_s_o = OrderedDict(em_means_s)

    acc = dict()
    ilast = ""
    for i in em_means_s_o:
        if tuple(em_means_s_o.keys()).index(i) == 0:
            acc[i] = prob_norm[i]
        else:
            acc[i] = acc[ilast]+prob_norm[i]
        ilast = i

    print(acc)


    # HECHO PARA VE, FALTARIA SACARLO A UN TXT
    # FALTARIA VERLO PARA RRE, VEP, RREP








if __name__ == "__main__":
    calculateDensityDistribution()