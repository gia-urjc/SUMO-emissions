import os
import sys
import optparse
import random

# import python modules from $SUMO/HOME directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME' ")

from sumolib import checkBinary
import traci

def generateRoutes():
    random.seed(1)
    timeStep = 300
    probabilityNS = 1./10 # Del Norte al Sur
    probabilitySN = 1./ 12  # Del Sur al Norte
    probabilityEO = 1. / 8
    probabilityOE = 1. / 9
    probabilityAutonomous = 1./3

    with open("intersec_TL.rou.xml", "w") as routes:
        original_stdout = sys.stdout
        sys.stdout = routes
        print(""" <routes>
        <vType id="autonomous_car" vClass="evehicle" color="green"/>
        <vType id="normal_car" color="255,0,170"/>
        
        <route edges="-e4 e2" color="yellow" id="route_1"/>
        <route edges="-e3 -e1" color="yellow" id="route_2"/>
        <route edges="-e2 e4" color="yellow" id="route_3"/>
        <route edges="e1 e3" color="yellow" id="route_4"/>""") #OE SN EO NS

        vehNr = 0

        for i in range(timeStep):
            if random.uniform(0,1)<probabilityNS:
                print('     <vehicle id="NS%i" type="normal_car" route="route_4" depart="%i" />' % (
                        vehNr, i))
                vehNr +=1
            if random.uniform(0, 1) < probabilitySN:
                print('     <vehicle id="SN%i" type="normal_car" route="route_2" depart="%i" />' % (
                    vehNr, i))
                vehNr += 1
            if random.uniform(0, 1) < probabilityEO:
                print('     <vehicle id="EO%i" type="normal_car" route="route_3" depart="%i" />' % (
                    vehNr, i))
                vehNr += 1
            if random.uniform(0, 1) < probabilityOE:
                print('     <vehicle id="NS%i" type="normal_car" route="route_1" depart="%i" />' % (
                    vehNr, i))
                vehNr += 1
            possible_routes = ["route_1","route_2","route_3","route_4"]

            if random.uniform(0, 1) < probabilityAutonomous:
                print('     <vehicle id="Au{}" type="autonomous_car" route="{}" depart="{}"').format(
                    vehNr,random.choice(possible_routes),i)
                vehNr += 1
        print("</routes>")
        sys.stdout = original_stdout







def run():

    while traci.simulation.getMinExpectedNumber() > 0: # While there are cars (and waiting cars)
        traci.simulationStep() # Advance one time step

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

    traci.start([sumoBinary, "-c", "cross.sumocfg", "--tripinfo-output", "tripinfo.xml"])

    run()