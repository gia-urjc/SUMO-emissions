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

### A*) Glossary: 

   - e(t): is a measure representing the average emission the vehicle carrying out the trip t would emit in the control zone.
   - ![formula](https://render.githubusercontent.com/render/math?math=k_{t}): access permission level  to the control zone 
   - ![formula](https://render.githubusercontent.com/render/math?math=p_{t}): measured pollution in the area 
   - t: time step
  
### A) Understanding the configurationFile.csv file

You can configure the value of the following variables: 

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
   - random_seed: We use the seed to obtain the same random numbers. If you change this number you would obtain other random numbers.
   - number_of_time_steps: In seconds. This variable is used to generate routes. During this time cars may appear.
   - probability_E: eVehicle generation probability. This variable is used to generate routes. 
   - probability_G: gasolineEuroSix generation probability. This variable is used to generate routes. 
   - probability_D: dieselEuroSix generation probability. This variable is used to generate routes. 
   - probability_HD: hovDieselEuroSix generation probability. This variable is used to generate routes. 
   - probability_N: normalVehicle generation probability. This variable is used to generate routes. 
   - probability_H: highEmissions generation probability. This variable is used to generate routes. 
   - probability_T: truck generation probability. This variable is used to generate routes. 

   - window_size: 
   - threshold_L;;80000;;NOx
   - threshold_H;;100000;;NOx
 
### B) Create a simulation

   1º) Go to folder: ./SUMMO-emmisions/configuration/
   2º) Open configurationFile.csv and configure the variables ( description in B) 




