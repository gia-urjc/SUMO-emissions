import csv
import pandas as pd
from fractions import Fraction

def readConfigurationCSV():
    df = pd.read_csv('../configurationFile.csv', delimiter=";")
    df = df.drop(columns = ["2","4","5"])
    df = df.set_index("1")

    strategy = df.iloc[df.index.get_loc("strategy"),0].replace(" ", "")
    timeStep = int(df.iloc[df.index.get_loc("timeStep"), 0].replace(" ", ""))
    probability_E = float(Fraction(df.iloc[df.index.get_loc("probability_E"), 0].replace(" ", "").replace(".", "")))
    probability_G = float(Fraction(df.iloc[df.index.get_loc("probability_G"), 0].replace(" ", "").replace(".", "")))
    probability_D = float(Fraction(df.iloc[df.index.get_loc("probability_D"), 0].replace(" ", "").replace(".", "")))
    probability_HG = float(Fraction(df.iloc[df.index.get_loc("probability_HG"), 0].replace(" ", "").replace(".", "")))
    probability_N = float(Fraction(df.iloc[df.index.get_loc("probability_N"), 0].replace(" ", "").replace(".", "")))
    probability_H = float(Fraction(df.iloc[df.index.get_loc("probability_H"), 0].replace(" ", "").replace(".", "")))
    probability_T = float(Fraction(df.iloc[df.index.get_loc("probability_T"), 0].replace(" ", "").replace(".", "")))

    window_size = int(df.iloc[df.index.get_loc("window_size"), 0])
    threshold_L = int(df.iloc[df.index.get_loc("threshold_L"), 0])
    threshold_H = int(df.iloc[df.index.get_loc("threshold_H"), 0])

    p_t_ini = int(df.iloc[df.index.get_loc("p_t_ini"), 0])
    size_ratio = int(df.iloc[df.index.get_loc("timeStep"), 0])
    subs_NOx = int(df.iloc[df.index.get_loc("subs_NOx"),0])
    e_ini = int(df.iloc[df.index.get_loc("e_ini"), 0])

    min_packages = int(df.iloc[df.index.get_loc("min_packages"), 0])
    max_packages = int(df.iloc[df.index.get_loc("max_packages"), 0])

    control_area_edges_cnf_ini = df.iloc[df.index.get_loc("control_area_edges_cnf"), 0]
    control_area_edges_cnf_split = control_area_edges_cnf_ini.split(sep=",")
    control_area_edges_cnf = [(i.replace(" ","").replace("\"","")) for i in control_area_edges_cnf_split]

    enter_control_area_edges_ini = df.iloc[df.index.get_loc("enter_control_area_edges"), 0]
    enter_control_area_edges_split = enter_control_area_edges_ini.split(sep=",")
    enter_control_area_edges = [(i.replace(" ", "").replace("\"", "")) for i in enter_control_area_edges_split]


    return strategy, timeStep,probability_E ,probability_G, probability_D, probability_HG, probability_N, probability_H, probability_T, \
           window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
           min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges
