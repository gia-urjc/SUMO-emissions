import random

def generateRoutes():
    random.seed(1)
    timeStep = 1000
    probability_E = 1. / 20 # Probability eVehicle
    probability_N = 1. / 20 # Probability normalVehicle

    with open("changeName.rou.xml", "w") as routes:

        print(""" <routes>
        <vType id="eVehicle" vClass="evehicle" guiShape="evehicle" color="green"/>
        <vType id="normalVehicle" vClass="passenger" guiShape="passenger" color="0,0,128"/>
        <vType id="authority" vClass="authority" guiShape="passenger" color="red" />\n""", file=routes)

        vehNr = 0

        for i in range(timeStep):
            # -A -> C # -C -> A
            # -B -> D # -D -> B
            # -E -> G # -G -> E
            # -F -> H # -H -> F
            o_list = ["A","B","C","D","E","F","G","H"]
            o_d_dict = {"A":"C","C":"A","B":"D","D":"B","E":"G","G":"E","F":"H","H":"F"}

            origin = random.choice(o_list)
            dest = o_d_dict[origin]


            if random.uniform(0, 1) < probability_E: #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="eVehicle" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1

            if random.uniform(0, 1) < probability_N:  #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="normalVehicle" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1


        print("</routes>", file=routes)


if __name__ == '__main__':
    generateRoutes()

