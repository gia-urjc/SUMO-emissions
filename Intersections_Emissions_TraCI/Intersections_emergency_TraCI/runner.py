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


def generateRoutes():
    random.seed(1)
    timeStep = 300
    probability_e = 1./ 50
    probability_n = 1. / 20

    with open("emergency.rou.xml", "w") as routes:

        print(""" <routes>
        <vType id="emergency_car" vClass="emergency" guiShape="emergency"/>
        <vType id="normal_car" vClass="passenger" color="0,40,255"/>
        
        <route id="t_1" edges="e1a e1b e3"/>
        <route id="t_2" edges="e1a e1b e2"/>
        <route id="t_3" edges="e4 e3"/>
        <route id="t_4" edges="e4 e2"/>""", file = routes)

        vehNr = 0

        for i in range(timeStep):
            if random.uniform(0,1) < probability_e:
                print('     <vehicle id="NSe%i" type="emergency_car" route="t_1" depart="%i" />' % (
                        vehNr, i), file =routes)
                vehNr +=1
            if random.uniform(0, 1) < probability_n:
                print('     <vehicle id="NSn%i" type="normal_car" route="t_1" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < probability_e:
                print('     <vehicle id="NEe%i" type="emergency_car" route="t_2" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < probability_n:
                print('     <vehicle id="NEn%i" type="normal_car" route="t_2" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < probability_e:
                print('     <vehicle id="WSe%i" type="emergency_car" route="t_3" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < probability_n:
                print('     <vehicle id="WSn%i" type="normal_car" route="t_3" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0,1) < probability_e:
                print('     <vehicle id="WEe%i" type="emergency_car" route="t_4" depart="%i" />' % (
                        vehNr, i), file =routes)
                vehNr +=1
            if random.uniform(0, 1) < probability_n:
                print('     <vehicle id="WEn%i" type="normal_car" route="t_4" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1

        print("</routes>", file=routes)







def run():
    step = 0
    last_step_em =0
    while traci.simulation.getMinExpectedNumber() > 0: # While there are cars (and waiting cars)
        traci.simulationStep() # Advance one time step
        det_vehicles = traci.inductionloop.getLastStepVehicleIDs("det_1a")
        if step == (last_step_em +30):
            traci.lane.setAllowed(laneID="e1b_0", allowedClasses=["passenger","emergency"])
        for veh in det_vehicles:
            if "emergency_car" == traci.vehicle.getTypeID(vehID=veh):
                print("YES")
                traci.lane.setDisallowed(laneID="e1b_0",disallowedClasses=["passenger"])
                last_step_em = step

        step +=1

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
    generateRoutes()
    traci.start([sumoBinary, "-c", "emergency.sumocfg", "--tripinfo-output", "tripinfo.xml"])

    run()