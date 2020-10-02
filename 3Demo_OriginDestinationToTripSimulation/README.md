# SUMO: From OSM to Network + Random Trips Simulation

https://www.youtube.com/watch?v=LWecm_rCPJw&ab_channel=RodrigueTchamna

Firstly, install SUMO. 

After: 

  1) Search & download Open Street Map (OSM)

  2) Convert the Map into SUMO Network: netconvert --osm-files map.osm -o test.net.xml

  3) Add trip & route to the network using build-in Python scripts: randomTrips.py :
  ```
  python PATH\randomTrips.py -n test.net.xml -r test.rou.xml -e 50 -l
  ```

Lastly,in the folder, open my_config_file. It should open in SUMO. Or, open CMD: sumo-gui -c my_config_file.sumocfg

