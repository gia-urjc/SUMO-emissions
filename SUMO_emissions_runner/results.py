""" Write results in a file """
from pathlib import Path
import os
import csv



def results(simulation, window_size, p_t_ini, size_ratio, subs_NOx, e_ini, min_packages, max_packages, route = ""):
    """ Write results in a file """

    """ First, we open the file"""
    if route =="":
        if not os.path.exists("results"): # If the folder doesn't exists  -> Create folder
            os.makedirs("results")

        cont_file = 0
        file = "results_file_" + simulation.strategy
        fileName = r"./results/" + file + str(cont_file) + ".csv"
        fileObject = Path(fileName)
        while fileObject.is_file(): # If the file exists -> new file name
            cont_file += 1
            fileName = r"./results/" + file + str(cont_file) + ".csv"
            print(fileName)
            fileObject = Path(fileName)


    else:
        fileName = route

    with open(fileName, mode='w', newline='') as f_csv:
        print(fileName)
        f = csv.writer(f_csv, delimiter=';')
        """Second, we write the parameters"""
        f.writerow(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
        f.writerow([simulation.strategy])
        f.writerow(["PARAMETERS"])

        f.writerow(["window_size", "threshold_L", "threshold_H", "p_t_ini", "e_ini", "size_ratio", "subs_NOx",
                    "min_packages", "max_packages"])
        f.writerow([str(window_size), str(simulation.threshold_L), str(simulation.threshold_H), str(p_t_ini),
                    str(e_ini), str(size_ratio), str(subs_NOx), str(min_packages), str(max_packages)])

        """Third, we write all simulation results """
        minutes = round(simulation.step / 60, 0)
        # Windows values

        acum, p_t_total_all_steps, e_t_total_all_steps, p_t_control_zone_all_steps = 0, 0, 0, 0
        e_t_control_zone_all_steps, avg_k_all_steps = 0, 0
        for w in simulation.windows:
            p_t_total_all_steps += w.p_t_total
            e_t_total_all_steps += w.NOx_total_w
            p_t_control_zone_all_steps += w.p_t
            e_t_control_zone_all_steps += w.NOx_control_zone_w
            avg_k_all_steps += w.k
            acum += w.NOx_total_w

        avg_k_all_steps = avg_k_all_steps / len(simulation.windows)
        # Vehicles values
        p_all, cont, avg_contrib, total_packages, enter_cz_all_steps, not_enter_cz_all_steps, avg_total_time_all_steps = 0, 0, 0, 0, 0, 0, 0
        for v in simulation.all_veh:
            total_time = v.step_fin - v.step_ini
            avg_total_time_all_steps += total_time
            p_all += (total_time / v.n_packages)
            cont += 1
            avg_contrib += total_time * v.n_packages
            total_packages += v.n_packages
            if v.enter_cz == True:
                enter_cz_all_steps += 1
            else:
                not_enter_cz_all_steps += 1

        avg_total_time_all_steps = avg_total_time_all_steps / cont
        avg_time_per_package = avg_contrib / total_packages

        # Write:

        f.writerow(["ALL SIMULATION RESULTS"])
        f.writerow(["total_steps(sec)", "minutes", "avg_time_per_package (sec)", "p_t_total_all_steps",
                    "e_t_total_all_steps", "p_t_control_zone_all_steps", "e_t_control_zone_all_steps",
                    "avg_k_all_steps", "veh_enter_cz_all_steps", "not_veh_enter_cz_all_steps",
                    "avg_total_time_all_steps"])
        f.writerow([str(simulation.step), str(minutes), str(avg_time_per_package), str(p_t_total_all_steps),
                    str(e_t_total_all_steps), str(p_t_control_zone_all_steps), str(e_t_control_zone_all_steps),
                    str(avg_k_all_steps), str(enter_cz_all_steps), str(not_enter_cz_all_steps),
                    str(avg_total_time_all_steps)])

        """Fourth, the rest of results """

        f.writerow(["WINDOWS"])
        f.writerow(["step", "NOx_total_w", "NOx_total_acum", "lambda", "p_t_total", "e_t_total", "p_t_control_zone",
                    "e_t_control_zone", "k_control_zone", "num_veh_total", "num_vehicles_control_zone"])

        acum = 0
        for w in simulation.windows:
            acum += w.NOx_total_w
            f.writerow([str(w.step), str(w.NOx_total_w), str(acum), str(w.lambda_l), str(w.p_t_total),
                        str(w.NOx_total_w), str(w.p_t), str(w.NOx_control_zone_w), str(w.k),
                        str(w.veh_total_number_w),
                        str(len(w.vehicles_in_control_zone_w))])
        # avg_k_all_steps = avg_k_all_steps / cont

        f.writerow(["VEHICLES"])
        f.writerow(["id", "vType", "NOx_total_veh", "n_packages", "step_ini", "step_fin", "total_time(sec)",
                    "average_package", "enter_cz"])

        def sortFunc(v):
            return v.step_ini

        simulation.all_veh = sorted(simulation.all_veh, key=sortFunc)

        enter_cz_all_steps = 0

        vTypes_vehs = set() # For Density Distribution
        NOx_total_vehs = dict() # For Density Distribution
        total_time_vehs = dict() # For Density Distribution
        count_vehs = dict()  # For Density Distribution

        for v in simulation.all_veh:
            total_time = v.step_fin - v.step_ini
            average_package = total_time / v.n_packages
            if v.enter_cz == True: enter_cz_all_steps += 1
            f.writerow(
                [v.id, v.vType, str(v.NOx), str(v.n_packages), str(v.step_ini), str(v.step_fin), str(total_time),
                 str(average_package), str(v.enter_cz)])

            # For Density Distribution:
            vTypes_vehs.add(v.vType)
            if not v.vType in NOx_total_vehs:
                NOx_total_vehs[v.vType] = 0
                total_time_vehs[v.vType] = 0
                count_vehs[v.vType] = 0
            NOx_total_vehs[v.vType] += v.NOx
            total_time_vehs[v.vType] += total_time
            count_vehs[v.vType] += 1



        # For Density Distribution:
        f.writerow(["FOR_DENSITY_DISTRIBUTION"])
        f.writerow(["vType", "NOx_total", "total_time"])

        for v in vTypes_vehs:
            NOx_write = NOx_total_vehs[v] / count_vehs[v]
            total_time_write = total_time_vehs[v] / count_vehs[v]
            f.writerow([v, NOx_write, total_time_write])


