# SUMO Emissions Simulator 

## Introduction

The purpose of this simulator is to use the SUMO traffic simulation tool with Python to research systems that restrict and control access to an urban area in order to maintain the pollution in that area below some admissible threshold.

The simulator offers us the possibility to execute situations using different configurations: # TODO

Here you'll find all the necessary documentation to use and develop new features in the SUMO Emissions Simulator. 

------------------------------
## Author - v1.0.0
Sandra Gómez-Gálvez (Github: @sandruskyi ), Alberto Fernández (Github: @albertofernandezurjc ), Holger Billhardt (Github: @holgerbillhardt ).

{sandra.gomez.galvez , alberto.fernandez, holger.billhardt}@urjc.es

------------------------------
## Publications 
- Billhardt, H. , Fernández, A., Gómez-Gálvez, S., Martí, P., Prieto Tejedor, J., and Ossowski, S. (2021). Reducing Emissions Prioritising Transport Utility.

------------------------------
## Keywords
traffic management, last-mile delivery, prioritized resource allocation, agreement technologies, SUMO

------------------------------
# GUIDE

------------------------------
## For Users 

- [] TODO

------------------------------
## For Developers
If you are a developer or researcher and wants to create new things for the simulator, you should start here. 

### Prerequisites

1. It should work on Windows, Linux, and macOS.

2. SUMO - Simulation of Urban MObility

   Download: https://www.eclipse.org/sumo/
   Version 1.7.0
   Next versions may work

3. Python

   https://www.python.org/
   Version 3.8
   Next versions may work
   
4. IDE Pycharm or similar
  
   https://www.jetbrains.com/es-es/pycharm/
   Community : Free
   Professional: Free if you are a student https://www.jetbrains.com/education/ 
   
5. Git

Please make sure that all the binaries are registered in your PATH.

### Getting Started for Development

- You should always run main.py because it is necessary to run TraCI for simulation. 
- TraCI is the SUMO Traffic Control Interface: https://sumo.dlr.de/docs/TraCI.html


### Setup

- [] TODO


### Build 
- [] TODO

------------------------------
## Simulation Guide

### A*) Initial glossary: 

   1) e(t): is a measure representing the average emission the vehicle carrying out the trip t would emit in the control zone.
   2) ![formula](https://render.githubusercontent.com/render/math?math=k_{t}): access permission level to the control zone at time t.
   3) ![formula](https://render.githubusercontent.com/render/math?math=p_{t}): measured pollution in the area (air) at time t.
   4) t: time step (seconds).
   5) pollution at time t: is the sum of the previous pollution plus the amount emitted by vehicles during the last time period minus a quantity that is removed by atmospheric effects: ![formula](https://render.githubusercontent.com/render/math?math=p_{t}) = ![formula](https://render.githubusercontent.com/render/math?math=p_{t})-1 + ![formula](https://render.githubusercontent.com/render/math?math=e_{t}) – λt·45000, where λt ∈ [0.8, +1.2] is a uniformly randomly generated factor that represents a ratio of 
pollutants removed from the air in time t (we set the constant 45000 empirically).
  
### A) Understanding the configurationFile.csv file

You can configure the value of the following variables in configurationFile.csv file. This file is situated in the folder ./SUMMO-emmisions/configuration . 
Variables: 

   - strategy -> Each strategy determines the access restrictions to be applied at each moment and decides the vehicles that can enter the control area. The idea of the strategy is to restrict access to the control zone in such a way that the ![formula](https://render.githubusercontent.com/render/math?math=p_{t}) is kept below a certain maximum at any time t. We calculate an ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) as follows: ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) = {1: ![formula](https://render.githubusercontent.com/render/math?math=p_{t})<= θL (no restrictions), 0: ![formula](https://render.githubusercontent.com/render/math?math=p_{t})>= θH (no vehicles allowed), ((θH - ![formula](https://render.githubusercontent.com/render/math?math=p_{t}))/(θH - θL)): otherwise); with 0<=![formula](https://render.githubusercontent.com/render/math?math=k_{t})<=1 and threshold values: θH (maximum allowed pollution) and θL (lower bound on ![formula](https://render.githubusercontent.com/render/math?math=p_{t})). Depend on ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) we define different control strategies. 
     Allowed options for the strategy variable (more information about each strategy in the section "Publications" specified above):
      - noControl: runs the simulation without restrictions.
      - baseline: The strategy is implemented by randomly granting access with probability k to each trip that request access to the restricted area. At each moment t, the value of ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) determines the ratio of trips that are allowed to enter the area. If random.uniform(0,1)<=![formula](https://render.githubusercontent.com/render/math?math=k_{t}) -> enter. Utility function: U(![formula](https://render.githubusercontent.com/render/math?math=t_{i})) = c, with c constant.
      - VE: Vehicle Emission. At each moment t, the value of ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) determines the ratio of trips that are allowed to enter the area. This strategy prioritizes trips having
lower emissions. Utility function: U(![formula](https://render.githubusercontent.com/render/math?math=t_{i})) = 1 / ( 1 + e(![formula](https://render.githubusercontent.com/render/math?math=t_{i})). 
      - VEP: Vehicle Emission per Package.  At each moment t, the value of ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) determines the ratio of trips that are allowed to enter the area. The access is prioritized with respect to the emissions of a trip and the importance of a trip (number of parcels carried), using the Utility:  U(![formula](https://render.githubusercontent.com/render/math?math=t_{i})) = (n) / (1 + e(![formula](https://render.githubusercontent.com/render/math?math=t_{i})). 
      - RRE: Ratio Reduction Emission. Given ![formula](https://render.githubusercontent.com/render/math?math=k_{t}), we calculate the ratio ![formula](https://render.githubusercontent.com/render/math?math=k_{t})' of vehicles with lowest emissions (with respect to the normal demand) that together produce the (kt*100)% of the emissions normally generated in the same moment or time frame. It holds that ![formula](https://render.githubusercontent.com/render/math?math=k_{t})'≥ ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) . Afterwards, the strategy applies the same prioritization schema as VE.
      - RREP: Ratio Reduction Emission per Package. Here ![formula](https://render.githubusercontent.com/render/math?math=k_{t}), we calculate the ratio ![formula](https://render.githubusercontent.com/render/math?math=k_{t}) is translated to a ratio of vehicles ![formula](https://render.githubusercontent.com/render/math?math=k_{t}), we calculate the ratio ![formula](https://render.githubusercontent.com/render/math?math=k_{t})'. Then, the same prioritization schema as in VEP is employed with the new ratio.

   - file_name_density : this variable is not changed here. You can change it on main.py. 
   - random_seed: We use the seed to obtain the same random numbers. If you change this number you would obtain other random numbers. Example: 42;
   
   - number_of_time_steps: Steps, in seconds. This variable is used to generate routes. During this time cars may appear. Example: 3600;
   - probability_E: eVehicle generation probability. This variable is used to generate routes. Example: 1. / 20;
   - probability_G: gasolineEuroSix generation probability. This variable is used to generate routes. Example: 1. / 20;
   - probability_D: dieselEuroSix generation probability. This variable is used to generate routes. Example: 1. / 20;
   - probability_HD: hovDieselEuroSix generation probability. This variable is used to generate routes. Example: 1. / 20;
   - probability_N: normalVehicle generation probability. This variable is used to generate routes. Example: 1. / 20;
   - probability_H: highEmissions generation probability. This variable is used to generate routes. Example: 1. / 40;
   - probability_T: truck generation probability. This variable is used to generate routes. Example: 1. / 40;

   - window_size: Steps, in seconds. Size of the emissions windows to control. Because we discount the proportional NOx of the last window. Example: 60;
   - threshold_L: NOx. Max threshold: maximum allowed pollution. See the formula in strategy. Example: 80000;
   - threshold_H: NOx. Min threshold: lower bound. See the formula in strategy. Example: 100000;
   
   - p_t_ini: NOx. Initial value. Initially measured pollution in the area. Example: 100000;
   - size_ratio: Ratio sub p_t_total. Ratio of size to subtract NOx. See in A*) Initial glossary -  5). Example: 4;
   - subs_NOx: Amount of NOx subtracted. This is multiplied by lambda. See in A*) Initial glossary -  5). Example: 9000;
   - e_ini: NOx. Initial emissions. For heating up if emissions are lower than e_ini, use e_ini in A*) Initial glossary -  5). Example: 4000;
   - ini_lambda_l: windows ratio ini lambda. See in A*) Initial glossary -  5). Example: 0.8;
   - min_randomLambda: windows ratio min. See in A*) Initial glossary -  5). Example: 0.8;
   - max_randomLambda: windows ratio max. See in A*) Initial glossary -  5). Example: 1.2;
   - ini_k_window: initial k (access permission level to the control zone) in windows. Example: 1;
   
   - min_packages: for strategies that use packages. Min number of packages. Example: 1;
   - max_packages: for strategies that use packages. Max number of packages. Example: 20;

   - control_area_edges_cnf: List of edges within the control zone. Example: "gneE191_0", "-gneE191_0", "gneE192_0", "-gneE192_0";
   - enter_control_area_edges: List of edges that border and are outside the control zone. Example: "gneE179_0", "-gneE179_0", "gneE181_0", "-gneE181_0";

### B) Generate routes
You need a route file to create a SUMO simulation, these steps show you how to create it:

   1. Go to folder: ./SUMMO-emmisions/configuration . Open configurationFile.csv and configure the variables ( description in A). Important variables: strategy, random_seed, number_of_time_steps, probability_E, probability_G, probability_D, probability_HD, probability_N, probability_H, probability_T
   2. Go to folder: ./SUMMO-emmisions/generate_routes . Run generateRoutes.py
   3. The .py generates a changeName.rou.xml. You must copy this file.
   4. Go to folder: ./SUMMO-emmisions/configuration . Paste the file, and change it name. Move the old rou.xml file to ./SUMMO-emmisions/configuration/someRoutes .
   5. In the folder ./SUMMO-emmisions/configuration open the file emissions.sumocfg, and change the old rou name for your new rou file name inside value in route-files.
   6. Now, You can run any simulation.

Example result: 

    <routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
       <vType id="eVehicle" vClass="evehicle" guiShape="evehicle" color="green"/>
       <vType id="normalVehicle" vClass="passenger" guiShape="passenger" color="0,0,128"/>
       <vType id="authority" vClass="authority" guiShape="passenger" color="red" />

       <trip depart="10" from="-A" to="C" color="yellow" type="eVehicle" id="veh1"/>
       <trip depart="20" from="-E" to="G" color="yellow" type="normalVehicle" id="veh2"/>
       <trip depart="30" from="-F" to="H" color="yellow" type="normalVehicle" id="veh3"/>
       <trip depart="80" from="-C" to="A" color="yellow" type="normalVehicle" id="veh4"/>
       <trip depart="85" from="-E" to="G" color="yellow" type="normalVehicle" id="veh5"/>
       <trip depart="90" from="-A" to="C" color="yellow" type="eVehicle" id="veh6"/>
       <trip depart="90" from="-E" to="G" color="yellow" type="normalVehicle" id="veh7"/>
       <trip depart="90" from="-E" to="G" color="yellow" type="normalVehicle" id="veh8"/>
       <trip depart="100" from="-G" to="E" color="yellow" type="eVehicle" id="veh9"/>
       <trip depart="120" from="-B" to="D" color="yellow" type="normalVehicle" id="veh10"/>
    </routes>
    
### C) Calculate emissions means
To calculate the density distribution of the vehicles in a simulation we need an emissions means. It can be calculated or put at our convenience. In the next steps, we can calculate the emissions means: 
   
   1. Go to folder: ./SUMMO-emmisions/configuration . Open configurationFile.csv and configure the variables ( description in A). All variables are important. 
   2. If you want to generate an emissions means with a specific strategy results go to the folder ./SUMMO-emmisions/calculate_em_means/noControl_resultsHistorical and paste your strategy results. Go to ./SUMMO-emmisions/calculate_em_means/calculateEmMeans.py and change the value of the variables folderNoControl and nameFileNoControl.
    Otherwise, if you want to generate a new strategy, skip this step. 
   3. Go to folder: ./SUMMO-emmisions/calculate_em_means and run calculateEmMeans.py . The program will ask you if you want to use your own strategy results file (step 2) or if you want to create a new file. Select an option. 
   4. The result of the program is saved in the folder ./SUMMO-emmisions/calculate_em_means/em_means_calculated . You can change this in calculateEmMeans.py changing the value of the variables fileEmMeansResults and folderEmMeansResults.

Example result: 
     
    vType;em_means
    eVehicle;0.0
    gasolineEuroSix;0.4964860223541296
    highEmissions;0.7052636035725058
    normalVehicle;0.8433368860367672
    hovDieselEuroSix;2.6070997833179304
    dieselEuroSix;3.659494950051576
    truck;76.61826583286638
      

### D) Calculate density distribution
The strategies need a density distribution. It can be calculated or put at our convenience. In the next steps, we can calculate the density distribution: 

   1. Go to folder: ./SUMMO-emmisions/configuration . Open configurationFile.csv and configure the variables ( description in A). All variables are important. 
   2. Go to folder: ./SUMMO-emmisions/calculate_density_distribution . Open calculateDensityDistribution.py .
   3. Change the value of the variable route_e_means_calculated if is necessary, and the variables folderResults and fileResults too. 
   4. Run the program (./SUMMO-emmisions/calculate_density_distribution/calculateDensityDistribution.py)
   5. The result of the program is saved in the folder ./SUMMO-emmisions/calculate_density_distribution/calculate_density_distribution_calculated . You can change this in calculateDensityDistribution.py changing the value of the variables folderResults and fileResults.

Example result: 
          
    vType;em_means
    eVehicle;0.0
    gasolineEuroSix;0.010730614366722355
    highEmissions;0.0183520895101087
    normalVehicle;0.03657923488347484
    hovDieselEuroSix;0.09292680788804934
    dieselEuroSix;0.1720199289789028
    truck;1.0
      

### B) Create a simulation

   1º) Go to folder: ./SUMMO-emmisions/configuration/
   2º) Open configurationFile.csv and configure the variables ( description in A) 




