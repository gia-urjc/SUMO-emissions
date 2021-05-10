import pandas as pd
from fractions import Fraction
import os

def readConfigurationCSV():
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(CURR_DIR+'/configurationFile.csv', delimiter=";")
    df = df.drop(columns = ["2","4","5"])
    df = df.set_index("1")

    strategy = str(df.iloc[df.index.get_loc("strategy"),0].replace(" ", "").replace("\"",""))
    random_seed = int(df.iloc[df.index.get_loc("random_seed"),0])
    number_of_time_steps = int(df.iloc[df.index.get_loc("number_of_time_steps"), 0].replace(" ", ""))
    probability_E = float(Fraction(df.iloc[df.index.get_loc("probability_E"), 0].replace(" ", "").replace(".", "")))
    probability_G = float(Fraction(df.iloc[df.index.get_loc("probability_G"), 0].replace(" ", "").replace(".", "")))
    probability_D = float(Fraction(df.iloc[df.index.get_loc("probability_D"), 0].replace(" ", "").replace(".", "")))
    probability_HD = float(Fraction(df.iloc[df.index.get_loc("probability_HD"), 0].replace(" ", "").replace(".", "")))
    probability_N = float(Fraction(df.iloc[df.index.get_loc("probability_N"), 0].replace(" ", "").replace(".", "")))
    probability_H = float(Fraction(df.iloc[df.index.get_loc("probability_H"), 0].replace(" ", "").replace(".", "")))
    probability_T = float(Fraction(df.iloc[df.index.get_loc("probability_T"), 0].replace(" ", "").replace(".", "")))

    window_size = int(df.iloc[df.index.get_loc("window_size"), 0])
    threshold_L = int(df.iloc[df.index.get_loc("threshold_L"), 0])
    threshold_H = int(df.iloc[df.index.get_loc("threshold_H"), 0])

    p_t_ini = int(df.iloc[df.index.get_loc("p_t_ini"), 0])
    size_ratio = int(df.iloc[df.index.get_loc("size_ratio"), 0])
    subs_NOx = int(df.iloc[df.index.get_loc("subs_NOx"),0])
    e_ini = int(df.iloc[df.index.get_loc("e_ini"), 0])
    ini_lambda_l = float(df.iloc[df.index.get_loc("ini_lambda_l"), 0])
    min_randomLambda = float(df.iloc[df.index.get_loc("min_randomLambda"), 0])
    max_randomLambda = float(df.iloc[df.index.get_loc("max_randomLambda"), 0])
    ini_k_window = float(df.iloc[df.index.get_loc("ini_k_window"), 0])

    min_packages = int(df.iloc[df.index.get_loc("min_packages"), 0])
    max_packages = int(df.iloc[df.index.get_loc("max_packages"), 0])

    control_area_edges_cnf_ini = df.iloc[df.index.get_loc("control_area_edges_cnf"), 0]
    control_area_edges_cnf_split = control_area_edges_cnf_ini.split(sep=",")
    control_area_edges_cnf = [(i.replace(" ","").replace("\"","")) for i in control_area_edges_cnf_split]

    enter_control_area_edges_ini = df.iloc[df.index.get_loc("enter_control_area_edges"), 0]
    enter_control_area_edges_split = enter_control_area_edges_ini.split(sep=",")
    enter_control_area_edges = [(i.replace(" ", "").replace("\"", "")) for i in enter_control_area_edges_split]



    return ( strategy, random_seed, number_of_time_steps, probability_E, probability_G, probability_D, \
           probability_HD, probability_N, probability_H, probability_T, \
           window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
           ini_lambda_l, min_randomLambda, max_randomLambda, ini_k_window,\
           min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges)


if __name__ == "__main__":
    print(readConfigurationCSV())