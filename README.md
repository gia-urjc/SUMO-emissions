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

### A) Understanding the configurationFile.csv file

You can configure the value of the following variables: 

   - strategy -> Each strategy determines the access restrictions to be applied at each moment and decides the vehicles that can enter the control area. The idea of the strategy is to restrict access to the control zone in such a way that the measured pollution in the area (pt) is kept below a certain maximum at any time t. We calculate an access permission level (kt) to the control zone as follows: kt = {1: pt<= θL (no restrictions), 0: pt>= θH (no vehicles allowed), ((θH - pt)/(θH - θL)): otherwise); with threshold values: θH (maximum allowed pollution) and θL (lower bound on pt). Depend on kt we define different control strategies. 
     Allowed options for the strategy variable (more information about each strategy in the section "Publications" specified above):
      - noControl: runs the simulation without restrictions
      - baseline:
      - VE:
      - VEP:
      - RRE:
      - RREP:

### A) Create a simulation

   1º) Go to folder: ./SUMMO-emmisions/configuration/
   2º) Open configurationFile.csv and configure the variables ( description in B) 




