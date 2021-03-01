import random

def generateRoutes():
    random.seed(1)
    timeStep = 3600

    probability_E = 1. / 20 # Probability eVehicle
    probability_G = 1. / 20  # Probability gasolineEuroSix
    probability_D = 1. / 20  # Probability dieselEuroSix
    probability_HG = 1. / 20  # Probability hovDieselEuroSix
    probability_N = 1. / 20  # Probability normalVehicle
    probability_H = 1. / 40  # Probability highEmissions
    probability_T = 1. / 40  # Probability truck


    with open("changeName.rou.xml", "w") as routes:

        print(""" <routes>
        <!-- Zero label-->
        <vType id="eVehicle" emissionClass="Zero/default" vClass="evehicle" guiShape="evehicle" color="green"/>  
        <!-- C label -->
        <vType id="gasolineEuroSix" emissionClass="HBEFA3/LDV_G_EU6" vClass="passenger" guiShape="passenger" color="0,0,128"/>
        <vType id="dieselEuroSix" emissionClass="HBEFA3/LDV_D_EU6" vClass="passenger" guiShape="passenger" color="0,0,128"/>
        <vType id="hovDieselEuroSix" emissionClass="HBEFA3/PC_D_EU6" vClass="passenger" guiShape="passenger" color="0,0,128"/>
        <vType id="normalVehicle" emissionClass="HBEFA3/PC_G_EU4" vClass="passenger" guiShape="passenger" color="0,0,128"/>
        
        <!-- B label -->
        <vType id="highEmissions" emissionClass="HBEFA3/PC_G_EU3" vClass="passenger" guiShape="passenger" color="0,0,128"/>
        <vType id="truck" emissionClass="HBEFA3/HDV_D_EU4" vClass="truck" guiShape="passenger" color="0,0,128"/>
        
        <!-- Type authorized -->
        <vType id="authority" vClass="authority" guiShape="passenger" color="red" />\n""", file=routes)

        vehNr = 0


        cont_E = 0
        cont_G = 0
        cont_D = 0
        cont_HG = 0
        cont_N = 0
        cont_H = 0
        cont_T = 0


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
                cont_E +=1



            if random.uniform(0, 1) < probability_G:  #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="gasolineEuroSix" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1
                cont_G += 1


            if random.uniform(0, 1) < probability_D:  #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="dieselEuroSix" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1
                cont_D += 1


            if random.uniform(0, 1) < probability_HG:  #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="hovDieselEuroSix" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1
                cont_HG += 1

            if random.uniform(0, 1) < probability_N:  #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="normalVehicle" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1
                cont_N += 1

            if random.uniform(0, 1) < probability_H:  #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="highEmissions" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1
                cont_H += 1

            if random.uniform(0, 1) < probability_T:  #
                print('        <trip depart="%i" from="-%s" to="%s" color="yellow" type="truck" id="veh%i"/>' % (
                    i, origin, dest, vehNr), file=routes)
                vehNr += 1
                cont_T += 1

        print("</routes>", file=routes)

        print(cont_D,cont_E, cont_G, cont_H, cont_N, cont_HG, cont_T)


if __name__ == '__main__':
    generateRoutes()


