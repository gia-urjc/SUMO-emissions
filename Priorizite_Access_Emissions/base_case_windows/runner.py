import os
import sys
import optparse
import random

# import python modules from $SUMO/HOME directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exist("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

def run():
    print("RUN")

    step = 0

    NOx_total = 0
    NOx_control_zone = 0
    NOx_per_vehicle = []

    veh_total_number=0
    total_kilometers = 0

    vehicles_in_simulation = []
    km_per_vehicle = []

    # WINDOW
    # Each window 50 steps
    count_window = -1
    NOx_total_window = 0
    NOx_control_zone_window = 0
    veh_total_number_window = 0
    vehicles_in_window = []
    window = []


    while traci.simulation.getMinExpectedNumber() > 0: # While there are cars (and waiting cars)
        traci.simulationStep() # Advance one time step: one second
        # WINDOWS
        if step != 0 and ((step % 50) == 0) and vehicles_in_window!=[]:
            print(step)
            window.append([vehicles_in_window, veh_total_number_window, NOx_total_window, NOx_control_zone])
            print(window)
            # Reboot all
            NOx_total_window = 0
            NOx_control_zone_window = 0
            veh_total_number_window = 0
            vehicles_in_window = []

            count_window += 1

        # PREPARE DATA
        id_vehicles_departed = traci.simulation.getDepartedIDList()
        id_list_vehicles_departed = list(id_vehicles_departed)
        if (id_list_vehicles_departed):
            # Per window:
            vehicles_in_window.extend(id_list_vehicles_departed)
            veh_total_number_window += len(id_list_vehicles_departed)
            # All simulation:
            vehicles_in_simulation.extend(id_list_vehicles_departed)
            km_per_vehicle.extend(id_list_vehicles_departed)
            NOx_per_vehicle.extend(id_list_vehicles_departed)
            for lVeh in range(len(NOx_per_vehicle)):
                vehi = NOx_per_vehicle[lVeh]
                #print(len(NOx_per_vehicle[lVeh]))
                if(len(NOx_per_vehicle[lVeh])!=2):
                    NOx_per_vehicle[lVeh] = [vehi, 0]
                    #print(NOx_per_vehicle)


            #print("km", km_per_vehicle)
            #print(vehicles_in_simulation)

        id_vehicles_arrived = traci.simulation.getArrivedIDList()
        for veh in id_vehicles_arrived:
            if veh in vehicles_in_simulation:
                # All simulation
                vehicles_in_simulation.remove(veh)
                veh_total_number +=1


        #print(vehicles_in_simulation)

        for veh in vehicles_in_simulation:

            # Emissions:
                # All simulation
            vehNOxEmission = traci.vehicle.getNOxEmission(veh)
            NOx_total += vehNOxEmission
            for iNVeh in range(len(NOx_per_vehicle)):
                if veh in NOx_per_vehicle[iNVeh]:
                    NOx_per_vehicle[iNVeh][1] = float(NOx_per_vehicle[iNVeh][1])+ vehNOxEmission

                # Per Window
            NOx_total_window +=vehNOxEmission


            # Control Area:
            pos = traci.vehicle.getPosition(vehID=veh)
            #print(pos, vehNOxEmission, veh)

            if (pos[1]<=296 and pos[1]>=3) and (pos[0]>=3 and pos[0]<=296):
                # All simulation:
                NOx_control_zone += vehNOxEmission
                #print("SI ", CO2_zona_control)

                # Per window:
                NOx_control_zone_window += vehNOxEmission


            # Route lenght per vehicle
            rouIndex = traci.vehicle.getRouteIndex(veh)
            bordes = traci.vehicle.getRoute(veh)

            if rouIndex==(len(bordes)-1):
                #print(bordes, veh, rouIndex, bordes[0],'-',bordes[rouIndex])
                for iVeh in range(len(km_per_vehicle)):
                    #if veh in km_per_vehicle[iVeh]:
                    if km_per_vehicle[iVeh] == veh:
                        stage = traci.simulation.findRoute(bordes[0], bordes[rouIndex])
                        rouLength = stage.length
                        km_per_vehicle[iVeh] = [veh,rouLength]
                        #print(km_per_vehicle)

        step +=1

    minutes = round(step/60,3)
    for i in range(len(km_per_vehicle)):
        total_kilometers += km_per_vehicle[i][1]
    print("NOx_per_vehicle: ",NOx_per_vehicle)
    print("NOx_total: ", NOx_total, ". NOx_control_zone", NOx_control_zone, ". In ", step, "seconds (",minutes," minutes)")
    print(veh_total_number," vehicles - ",total_kilometers," kilometers")


    traci.close()
    sys.stdout.flush()


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action ="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary("SUMO")
    else:
        sumoBinary = checkBinary("sumo-gui")
    #traci.start([sumoBinary, "-c", "base_case.sumocfg", "--step-length", "0.001",  "--tripinfo-output", "tripinfo.xml", "--emission-output","emissionOutput.xml"])
    traci.start([sumoBinary, "-c", "base_case.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])

    run()