import xml.etree.ElementTree as et
from configuration import readConfigurationCSV as rCSV



if __name__ == "__main__":
#def createHistoricalVEP():
    strategy, timeStep, probability_E, probability_G, probability_D, probability_HG, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()

    NOx_total_veh_dict = dict()
    total_time_dict = dict()

    xtree = et.parse("1h.rou.xml")
    xroot = xtree.getroot()

    xml_vTypes = xroot.findall("vType")
    xml_trips =  xroot.findall("trip")
    for x_vT in xml_vTypes:
        items_dict = dict(x_vT.items())
        print(items_dict)
        NOx_total_veh_dict[items_dict.get("id")]=0
    print(NOx_total_veh_dict)

    for x_tps in xml_trips:
        print(dict(x_tps.items()))
