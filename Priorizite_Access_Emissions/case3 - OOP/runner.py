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
    vehicles_in_window = set()
        # All windows
    windows = []

    ## Case 1
        # Threshold:
    threshold = 14 # NOx_total in main_case_window = 28 => 28/2 = 14
    control_area_edges = ["gneE19_0","-gneE19_0","gneE21_0","-gneE21_0","gneE16_0","-gneE16_0","gneE17_0","-gneE17_0",
                          "gneE18_0","-gneE18_0","gneE22_0","-gneE22_0","gneE20_0","-gneE20_0","gneE15_0","-gneE15_0",
                          "gneE24_0","-gneE24_0","gneE25_0","-gneE25_0","gneE14_0","-gneE14_0","gneE23_0","-gneE23_0"]

    restrictionMode = False
    NOx_control_zone_restriction_mode = 0

    # Vehicles to control area
    vehs_load = traci.simulation.getLoadedIDList()
    for veh_load in vehs_load:
        if (veh_load != "simulation.findRoute"):
            traci.vehicle.setParameter(veh_load, "has.rerouting.device", "true")
            vClass_last = traci.vehicle.getVehicleClass(veh_load)
            edges_last = traci.vehicle.getRoute(veh_load)
            string_edge = edges_last[len(edges_last) - 1] + "_0"
            if (string_edge in control_area_edges):  # Destination in control area
                traci.vehicle.setType(vehID=veh_load, typeID="authority")
                if (vClass_last == "evehicle"):
                    traci.vehicle.setEmissionClass(veh_load, "zero")



    while traci.simulation.getMinExpectedNumber() > 0: # While there are cars (and waiting cars)
        # LAST STEP

            # Vehicles to control area
        vehs_load = traci.simulation.getLoadedIDList()
        for veh_load in vehs_load:
            if(veh_load!="simulation.findRoute"):
                traci.vehicle.setParameter(veh_load, "has.rerouting.device", "true")
                vClass_last = traci.vehicle.getVehicleClass(veh_load)
                edges_last = traci.vehicle.getRoute(veh_load)
                string_edge = edges_last[len(edges_last) - 1] + "_0"
                if (string_edge in control_area_edges):  # Destination in control area
                    traci.vehicle.setType(vehID=veh_load, typeID="authority")
                    if(vClass_last=="evehicle"):
                        traci.vehicle.setEmissionClass(veh_load,"zero")


        # NEW STEP
        traci.simulationStep() # Advance one time step: one second
        step += 1


        # Window
        if step != 0 and ((step % 50) == 0) and vehicles_in_window!=[]: # Each window 50 steps

            for w in range(len(windows)):# Discount NOx of the last window
                if windows[w][0] == step - 50:
                    print(NOx_control_zone_restriction_mode, windows[w][4])
                    NOx_control_zone_restriction_mode -= windows[w][4]
                    if (NOx_control_zone_restriction_mode < 0): NOx_control_zone_restriction_mode = 0 # TODO NOS QUEDAMOS AQUI
                    print(NOx_control_zone_restriction_mode)
            #print(step)

            # Add variables for the last 50 steps
            windows.append([step, vehicles_in_window, veh_total_number_window, NOx_total_window, NOx_control_zone_window])
            #windows.append([step, vehicles_in_window, veh_total_number_window, NOx_total_window, NOx_control_zone_restriction_mode])
            print(windows)

            # Reboot all
            NOx_total_window = 0
            NOx_control_zone_window = 0
            veh_total_number_window = 0
            vehicles_in_window = set()


        # MANAGE VEHICLES - All simulation
        id_vehicles_departed = traci.simulation.getDepartedIDList() # Vehicles in simulation
        id_list_vehicles_departed = list(id_vehicles_departed)

        if (id_list_vehicles_departed): # if the list is not empty
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

            # Per window:
            for veh in vehicles_in_simulation:
                vehicles_in_window.add(veh)  # Add the vehicles in the window list
            veh_total_number_window = len(vehicles_in_window)  # Add vehicles to the vehicle window counter

            # Taking into account the vehicles that reach their destination:
        id_vehicles_arrived = traci.simulation.getArrivedIDList()
        for veh in id_vehicles_arrived:
            if veh in vehicles_in_simulation: # If the vehicle has arrived then remove it from the simulation list
                vehicles_in_simulation.remove(veh)
                if veh in vehicles_in_window:
                    vehicles_in_window.remove(veh)

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

                # Control are:
                NOx_control_zone_restriction_mode += vehNOxEmission


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
            #print(veh, NOx_control_zone, NOx_total, pos)

            # Control area - Threshold:
            string_current_edge = edges[rouIndex] + "_0"
            if restrictionMode == True and traci.vehicle.getVehicleClass(veh)!="authority":
                if (string_current_edge in control_area_edges): #  current edge in control area
                    vClass_last2 = traci.vehicle.getVehicleClass(veh)
                    traci.vehicle.setType(vehID=veh, typeID="authority")
                    if (vClass_last2 != "passenger"):
                        traci.vehicle.setEmissionClass(veh, "zero")

            if restrictionMode == True:
                inList = False
                for edg in edges:
                    edgStrng = edg + "_0"
                    if edgStrng in control_area_edges:
                        inList = True
                if inList:
                    traci.vehicle.rerouteTraveltime(veh, True)



            print(veh, traci.vehicle.getTypeID(veh))

        #if auxSandra==0 and step != 0 and ((step % 50) == 0):

        if vehicles_in_simulation!=[] and restrictionMode== False and NOx_control_zone_restriction_mode > threshold:
            print("CONTROL ZONE ON", NOx_control_zone_restriction_mode )
            #auxSandra = 1
            restrictionMode = True
            print("B")

            for aEd in control_area_edges:
                traci.lane.setDisallowed(laneID=aEd, disallowedClasses=["passenger","evehicle"])
                print("disa ",traci.lane.getDisallowed(laneID=aEd))
                traci.lane.setAllowed(laneID=aEd, allowedClasses=["authority"])
                print("alo ",traci.lane.getAllowed(laneID=aEd))

            """
            traci.lane.setDisallowed(laneID="gneE22_0", disallowedClasses=["passenger", "evehicle"])
            #traci.lane.setDisallowed(laneID="-gneE22_0", disallowedClasses=["passenger", "evehicle"])"""

        if (restrictionMode == True and NOx_control_zone_restriction_mode <= threshold):
            print("CONTROL ZONE OFF")
            restrictionMode = False
            for aEd in control_area_edges:
                traci.lane.setAllowed(laneID=aEd, allowedClasses=["authority","passenger","evehicle"])
            for veh in vehicles_in_simulation:
                traci.vehicle.rerouteTraveltime(veh, True)


        print(step, "NOx_control_zone: ",NOx_control_zone, ". NOx_control_zone_restriction_mode: ",NOx_control_zone_restriction_mode,". NOx_total: ",NOx_total)



    minutes = round(step/60,3)
    for i in range(len(km_per_vehicle)):
        total_kilometers += km_per_vehicle[i][1]

    # Results:

    print("[step,vehicles_in_window, veh_total_number_window, NOx_total_window, NOx_control_zone] :")
    print(windows)
    print("NOx_per_vehicle: ",NOx_per_vehicle)
    print("NOx_total: ", NOx_total, ". NOx_control_zone", NOx_control_zone,". NOx_control_zone_restriction_mode: ",NOx_control_zone_restriction_mode)
    print(veh_total_number," vehicles - ",total_kilometers," kilometers")
    print("In ", step, "seconds (", minutes, " minutes)")

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
    traci.start([sumoBinary, "-c", "case3.sumocfg", "--tripinfo-output", "tripinfo.xml", "--emission-output", "emissionOutput.xml"])

    run()