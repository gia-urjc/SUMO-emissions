import csv
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('../configurationFile.csv', delimiter=";")
    df = df.drop(columns = ["2","4","5"])
    df = df.set_index("1")

    strategy = df.iloc[df.index.get_loc("strategy"),0]
    timeStep = df.iloc[df.index.get_loc("timeStep"), 0]
    probability_E = df.iloc[df.index.get_loc("probability_E"), 0]
    probability_G = df.iloc[df.index.get_loc("probability_G"), 0]
    probability_D = df.iloc[df.index.get_loc("probability_D"), 0]
    probability_HG = df.iloc[df.index.get_loc("probability_HG"), 0]
    probability_N = df.iloc[df.index.get_loc("probability_N"), 0]
    probability_H = df.iloc[df.index.get_loc("probability_H"), 0]
    probability_T = df.iloc[df.index.get_loc("probability_T"), 0]

    window_size = df.iloc[df.index.get_loc("window_size"), 0]
    threshold_L = df.iloc[df.index.get_loc("threshold_L"), 0]
    threshold_H = df.iloc[df.index.get_loc("threshold_H"), 0]

    p_t_ini = df.iloc[df.index.get_loc("p_t_ini"), 0]
    size_ratio = df.iloc[df.index.get_loc("timeStep"), 0]
    subs_Nox = df.iloc[df.index.get_loc("subs_Nox"),0]
    e_ini = df.iloc[df.index.get_loc("e_ini"), 0]

    min_packages = df.iloc[df.index.get_loc("min_packages"), 0]
    max_packages = df.iloc[df.index.get_loc("max_packages"), 0]

    control_area_edges_cnf_ini = df.iloc[df.index.get_loc("control_area_edges_cnf"), 0]
    control_area_edges_cnf_split = control_area_edges_cnf_ini.split(sep=",")
    control_area_edges_cnf = [(i.replace(" ","").replace("\"","")) for i in control_area_edges_cnf_split]

    enter_control_area_edges_ini = df.iloc[df.index.get_loc("enter_control_area_edges"), 0]
    enter_control_area_edges_split = enter_control_area_edges_ini.split(sep=",")
    enter_control_area_edges = [(i.replace(" ", "").replace("\"", "")) for i in enter_control_area_edges_split]