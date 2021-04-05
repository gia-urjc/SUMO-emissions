from SUMO_emissions_runner import runner
from configuration import readConfigurationCSV as rCSV

if __name__ == "__main__":
#def generateHistorical():
    strategy, timeStep, probability_E, probability_G, probability_D, probability_HG, probability_N, probability_H, probability_T, \
    window_size, threshold_L, threshold_H, p_t_ini, size_ratio, subs_NOx, e_ini, \
    min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges = \
        rCSV.readConfigurationCSV()

    election = input("Press 1 to use your noControl file or 2 to create a new file \n")
    while election != "1" and election != "2":
        election = input("Press 1 to use your noControl file or 2 to create a new file. Introduce: 1 or 2 \n")
    if election == "1":
        print("1")
        # LEER EL ARCHIVO DE noControl, yo crearía otra clase o def o algo para leer este archivo ya que lo vamos a
        # utilizar en ambos defs
    elif election == "2":
        print("First runs noControl to create the historical")
        runner.run("noControl", "", dict(), window_size, threshold_L, threshold_H, p_t_ini, size_ratio,
                   subs_NOx, e_ini, min_packages, max_packages, control_area_edges_cnf, enter_control_area_edges)
        print("Creating historical...")
        # LEER EL ARCHIVO DE noControl CREADO. - Ver como recoger la ruta creada... Quizás la última?
        print("")

    # Con el archivo No control obtener NOx_total y total_time
    # En el archivo sumo_emissions_runner/createHistorical está como leer el XML de rutas generadas que lo necesitaremos
    # para obtener los tipos de vehículos
    # Podemos hacer el punto anterior o meter los tipos de vehículos directamente en el csv de configuración y guardarlos al leerlo
    # y así ya los tendríamos y no tendríamos que estar leyendo el xml de rutas...
    # Una vez ya tengamos los tipos de vehículos, NOx_total, total_time y las probabilidades ya podemos calcular el historico!


