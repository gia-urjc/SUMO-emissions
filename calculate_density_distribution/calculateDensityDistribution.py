from configuration import readConfigurationCSV as rCSV
from collections import OrderedDict
import pandas as pd
from pathlib import Path
import os
import csv
import operator
import re


def getProbability(vType, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T):
    p = 0
    if vType == "eVehicle":
        p = probability_E
    elif vType == "gasolineEuroSix":
        p = probability_G
    elif vType == "dieselEuroSix":
        p = probability_D
    elif vType == "hovDieselEuroSix":
        p = probability_HD
    elif vType == "normalVehicle":
        p = probability_N
    elif vType == "highEmissions":
        p = probability_H
    elif vType == "truck":
        p = probability_T
    return p

def calculateAcc(acc, prob_norm, ordenationDict):
    ilast = ""
    for i in ordenationDict:
        if tuple(ordenationDict.keys()).index(i) == 0:
            acc[i] = prob_norm[i]
        else:
            acc[i] = acc[ilast] + prob_norm[i]
        ilast = i
    return acc

def normalize(prob, sum_prob):
    prob_norm = dict()
    for i in prob:
        prob_norm[i] = prob[i] / sum_prob
    return prob_norm

def calculateDensityDistribution():
    ##################################
    ########### CONFIGURE ############
    ##################################
    """ Change if you need"""
    # File route e means:
    # VEP uses VE em_means and RREP uses RRE em_means
    route_e_means_calculated = r"../calculate_em_means/em_means_calculated/em_means_results_VE_0.csv"
    # Results file:
    folderResults = "density_distribution_calculated"
    fileResults = "density_distribution_results_"
    ##################################
    ##################################
    ##################################

    strategy, number_of_time_steps, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    ini_lambda_l, min_randomLambda, max_randomLambda, ini_k_window, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()


    print(strategy)
    print("Calculating acc...")

    acc = dict()

    em_means_s = dict()
    df = pd.read_csv(route_e_means_calculated, delimiter=";")

    for i in range(df.shape[0]):
        em_means_s[df.iloc[i][0]] = df.iloc[i][1]
    print("em_means =", em_means_s)
    em_means_s_o = OrderedDict(em_means_s)

    if strategy == "VE" or strategy == "RRE":

        total_prob = probability_E + probability_G + probability_D + probability_HD + probability_N + probability_H + probability_T

        prob_norm = {"eVehicle": probability_E / total_prob, 'gasolineEuroSix': probability_G / total_prob,
                     'dieselEuroSix': probability_D / total_prob, 'hovDieselEuroSix': probability_HD / total_prob,
                     'normalVehicle': probability_N / total_prob, 'highEmissions': probability_H / total_prob,
                     'truck': probability_T / total_prob}

        if strategy == "VE":
            """ Return acc prob n"""
            acc = calculateAcc(acc, prob_norm, em_means_s_o)
        elif strategy == "RRE":
            """Return acc em prob n"""
            em_x_prob = dict()
            sum_em_x_prob = 0
            for i in em_means_s_o:
                res_em_x_prob = (em_means_s_o[i] * prob_norm[i])
                em_x_prob[i] = res_em_x_prob
                sum_em_x_prob += res_em_x_prob
            em_x_prob_norm = normalize(em_x_prob, sum_em_x_prob)
            acc = calculateAcc(acc, em_x_prob_norm, em_x_prob_norm)

    elif strategy == "VEP" or strategy == "RREP":
        packages_range = range(min_packages, max_packages + 1)

        em_packages = dict()
        for i in em_means_s_o: # For each vType
            for j in packages_range:
                vType_pack = i + "-" + str(j)
                em_packages[vType_pack] = em_means_s_o[i] / j

        prob_veh_pack = dict()
        sum_prob_veh_pack = 0
        for i in em_means_s_o: # For each vType
            for j in packages_range: # For each num package
                vType_pack = i + "-" + str(j)
                p = getProbability(i, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T)
                prob_veh_pack[vType_pack] = p * 1/max_packages
                sum_prob_veh_pack += prob_veh_pack[vType_pack]

        prob_veh_pack_norm = normalize(prob_veh_pack, sum_prob_veh_pack)

        em_packages_s = dict(sorted(em_packages.items(),key=operator.itemgetter(1)))

        if strategy == "VEP":
            acc = calculateAcc(acc, prob_veh_pack_norm, em_packages_s)

        if strategy == "RREP":
            probN_x_em = dict()
            sum_probN_x_em = 0
            for i in em_packages_s:
                vTypeVeh = (re.search(r"[a-zA-Z]+", i)).group()
                probN_x_em[i] = prob_veh_pack_norm[i] * em_means_s[vTypeVeh]
                sum_probN_x_em += probN_x_em[i]

            probN_x_em_norm = normalize(probN_x_em, sum_probN_x_em)

            acc = calculateAcc(acc, probN_x_em_norm, em_packages_s)

    print("acc = ", acc)


    """ Write results in a file """

    if not os.path.exists(folderResults):  # If the folder doesn't exists  -> Create folder
        os.makedirs(folderResults)

    cont_file_results = 0
    routeWrite = r"./" + folderResults +"/" + fileResults + strategy + "_"+ str(cont_file_results) + ".csv"
    fileObjectResults = Path(routeWrite)
    while fileObjectResults.is_file():  # If the file exists -> new file name
        cont_file_results += 1
        routeWrite = r"./" + folderResults +"/" + fileResults + strategy + "_"+ str(cont_file_results) + ".csv"
        fileObjectResults = Path(routeWrite)

    with open(routeWrite, mode='w', newline='') as f_csv:
        print(routeWrite)
        f = csv.writer(f_csv, delimiter=';')
        """Second, we write the parameters"""
        f.writerow(["vType", "em_means"])

        for m in acc:
            f.writerow([m, acc[m]])

    print("done")

if __name__ == "__main__":
    calculateDensityDistribution()