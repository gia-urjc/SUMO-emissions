# SUMO: Origin - Destination To Trip Simulation

https://www.youtube.com/watch?v=R6v7wDkvXrk&ab_channel=RodrigueTchamna

Firstly, install SUMO. 

After: 

  1) Have the network file (myNetwork.net.xml) ready of the demo 2 

  2) Make the TAZ (traffic analysis zone) file (.xml): TAZ_file.taz.xml

  3) Make the OD (Origin-Destination) Matrix file (.od): OD_file.od
  
  4) Make the od2trips.config file (.xml) : od2trips.config.xml
  
  5) TAZ_file.taz.xml + OD_file.od + od2trips.config.xml = od_file.odtrips.xml. Combine = 
  ```
  od2trips -c YOURPATH\od2trips.config.xml -n YOURPATH\taz_file.taz.xml -d YOURPATH\OD_file.od -o YOURPATH\od_file.odtrips.xml
  ```  
  
  5) Make the duarouter.config file (.duarcfg)
  ```
  python PATH\randomTrips.py -n test.net.xml -r test.rou.xml -e 50 -l
  ```

Lastly,in the folder, open my_config_file. It should open in SUMO. Or, open CMD: sumo-gui -c my_config_file.sumocfg

