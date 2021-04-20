
from collections import OrderedDict


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
    # FALTARIA VERLO PARA RRE, VEP, RREP








if __name__ == "__main__":
    generateHistorical()