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
    probabilityNS = 1./10 # Del Norte al Sur
    probabilitySN = 1./ 12  # Del Sur al Norte
    probabilityEO = 1. / 8
    probabilityOE = 1. / 9
    pAutonomousNS = 1./15
    pAutonomousSN = 2./15
    pAutonomousEO = 1. / 15
    pAutonomousOE = 2. / 15

    with open("intersec_TL.rou.xml", "w") as routes:

        print(""" <routes>
        <vType id="autonomous_car" vClass="evehicle" color="green"/>
        <vType id="normal_car" color="255,0,170"/>
        
        <route edges="-e4 e2" color="yellow" id="route_1"/>
        <route edges="-e3 -e1" color="yellow" id="route_2"/>
        <route edges="-e2 e4" color="yellow" id="route_3"/>
        <route edges="e1 e3" color="yellow" id="route_4"/>""", file = routes) #OE SN EO NS

        vehNr = 0

        for i in range(timeStep):
            if i<20:
                if random.uniform(0, 1) < pAutonomousNS:
                    print('    <vehicle id="Au%i" type="autonomous_car" route="route_4" depart="%i" />' % (
                        vehNr, i), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pAutonomousSN:
                    print('    <vehicle id="Au%i" type="autonomous_car" route="route_2" depart="%i" />' % (
                        vehNr, i), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pAutonomousEO:
                    print('    <vehicle id="Au%i" type="autonomous_car" route="route_3" depart="%i" />' % (
                        vehNr, i), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < pAutonomousOE:
                    print('    <vehicle id="Au%i" type="autonomous_car" route="route_1" depart="%i" />' % (
                        vehNr, i), file=routes)
                    vehNr += 1
            else:
                if random.uniform(0,1)<probabilityNS:
                    print('     <vehicle id="NS%i" type="normal_car" route="route_4" depart="%i" />' % (
                            vehNr, i), file =routes)
                    vehNr +=1
                if random.uniform(0, 1) < probabilitySN:
                    print('     <vehicle id="SN%i" type="normal_car" route="route_2" depart="%i" />' % (
                        vehNr, i), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < probabilityEO:
                    print('     <vehicle id="EO%i" type="normal_car" route="route_3" depart="%i" />' % (
                        vehNr, i), file=routes)
                    vehNr += 1
                if random.uniform(0, 1) < probabilityOE:
                    print('     <vehicle id="NS%i" type="normal_car" route="route_1" depart="%i" />' % (
                        vehNr, i), file=routes)
                    vehNr += 1
                possible_routes = ["route_1","route_2","route_3","route_4"]

        print("</routes>", file=routes)







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
    print("HOLA")
    if options.nogui:
        sumoBinary = checkBinary("SUMO")
    else:
        sumoBinary = checkBinary("sumo-gui")
    print("NO")
    generateRoutes()
    print("SI")
    traci.start([sumoBinary, "-c", "intersec_TL.sumocfg", "--tripinfo-output", "tripinfo.xml"])

    run()