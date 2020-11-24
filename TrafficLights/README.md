# Traffic Lights


All traffic lights are generated with a fixed cycle and a default cycle time of 90s. This can be changed with the option --tls.cycle.time.

The green time is split equally between the main phases.

All green phases are followed by a yellow phase. The length of the yellow phase is computed from the maximum speed of the incoming roads but may be customized with the option --tls.yellow.time

https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html 

## Python: 

https://sumo.dlr.de/docs/Tools/tls.html#tls_csv2sumopy 

https://sumo.dlr.de/docs/Tools/tls.html#tls_csvsignalgrouppy
