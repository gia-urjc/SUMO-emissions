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

    # All simulation
    step = 0

        # Emissions
    NOx_total = 0
    NOx_control_zone = 0
    NOx_per_vehicle = []

    veh_total_number=0
    total_kilometers = 0 # In all simulation
    vehicles_in_simulation = [] # Vehicles in each step
    km_per_vehicle = [] # all km per vehicle

    # Window
        # Each window 50 steps
        # Emissions in each window
    NOx_total_window = 0
    NOx_control_zone_window = 0
        # Variables in each window
    veh_total_number_window = 0
    vehicles_in_window = []
        # All windows
    windows = []


    while traci.simulation.getMinExpectedNumber() > 0: # While there are cars (and waiting cars)
        traci.simulationStep() # Advance one time step: one second

        # Window
        if step != 0 and ((step % 50) == 0) and vehicles_in_window!=[]: # Each window 50 steps
            #print(step)

            # Add variables for the last 50 steps
            windows.append([vehicles_in_window, veh_total_number_window, NOx_total_window, NOx_control_zone])
            #print(windows)

            # Reboot all
            NOx_total_window = 0
            NOx_control_zone_window = 0
            veh_total_number_window = 0
            vehicles_in_window = []


        # MANAGE VEHICLES - All simulation
        id_vehicles_departed = traci.simulation.getDepartedIDList() # Vehicles in simulation
        id_list_vehicles_departed = list(id_vehicles_departed)

        if (id_list_vehicles_departed): # if the list is not empty

            # Per window:
            vehicles_in_window.extend(id_list_vehicles_departed) # Add the vehicles in the window list
            veh_total_number_window += len(id_list_vehicles_departed) # Add vehicles to the vehicle window counter

            # All simulation:
            vehicles_in_simulation.extend(id_list_vehicles_departed) # Add vehicles to the simulation list
            km_per_vehicle.extend(id_list_vehicles_departed) # Add vehicles to the km list
            NOx_per_vehicle.extend(id_list_vehicles_departed) # Add vehicles to the NOx list
                # Initialize NOx values for each vehicle:
            for lVeh in range(len(NOx_per_vehicle)):
                vehi = NOx_per_vehicle[lVeh] # Select vehicle
                #print(len(NOx_per_vehicle[lVeh]))
                if(len(NOx_per_vehicle[lVeh])!=2): # If not initialized
                    NOx_per_vehicle[lVeh] = [vehi, 0] # Initialized
                    #print(NOx_per_vehicle)

            # Taking into account the vehicles that reach their destination:
        id_vehicles_arrived = traci.simulation.getArrivedIDList()
        for veh in id_vehicles_arrived:
            if veh in vehicles_in_simulation: # If the vehicle has arrived then remove it from the simulation list
                vehicles_in_simulation.remove(veh)
                veh_total_number +=1 # Update Vehicle Total Number in all simulation

        for veh in vehicles_in_simulation: # For each vehicle
            # Emissions:
                # All simulation
            vehNOxEmission = traci.vehicle.getNOxEmission(veh)  # Return the NOx value per vehicle in each step
            NOx_total += vehNOxEmission
            for iNVeh in range(len(NOx_per_vehicle)):
                if veh in NOx_per_vehicle[iNVeh]:
                    NOx_per_vehicle[iNVeh][1] = float(NOx_per_vehicle[iNVeh][1])+ vehNOxEmission  # Update the NOx value per vehicle

                # Per Window
            NOx_total_window +=vehNOxEmission


            # Control Area:
            pos = traci.vehicle.getPosition(vehID=veh) # (x,y)
            #print(pos, vehNOxEmission, veh)

            if (pos[1]<=296 and pos[1]>=3) and (pos[0]>=3 and pos[0]<=296): # x=> 0, y=>1. If the vehicle is in the control area
                # All simulation:
                NOx_control_zone += vehNOxEmission
                #print("SI ", CO2_zona_control)

                # Per window:
                NOx_control_zone_window += vehNOxEmission


            # Route lenght per vehicle
            rouIndex = traci.vehicle.getRouteIndex(veh)
            edges = traci.vehicle.getRoute(veh)

            if rouIndex==(len(edges)-1): # Only if is the last edge
                #print(edges, veh, rouIndex, edges[0],'-',edges[rouIndex])
                for iVeh in range(len(km_per_vehicle)):
                    #if veh in km_per_vehicle[iVeh]:
                    if km_per_vehicle[iVeh] == veh: # km_per_vehicle position selected for this vehicle
                        stage = traci.simulation.findRoute(edges[0], edges[rouIndex])
                        rouLength = stage.length  # Route Length
                        km_per_vehicle[iVeh] = [veh,rouLength]
                        #print(km_per_vehicle)

        step +=1


    minutes = round(step/60,3)
    for i in range(len(km_per_vehicle)):
        total_kilometers += km_per_vehicle[i][1]

    # Results:

    print("[vehicles_in_window, veh_total_number_window, NOx_total_window, NOx_control_zone] :")
    print(windows)
    print("NOx_per_vehicle: ",NOx_per_vehicle)
    print("NOx_total: ", NOx_total, ". NOx_control_zone", NOx_control_zone, ". In ", step, "seconds (",minutes," minutes)")
    print(veh_total_number," vehicles - ",total_kilometers," kilometers")

    # TraCI
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
    traci.start([sumoBinary, "-c", "base_case_windows.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])

    run()