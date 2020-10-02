# SUMO: From OSM to Network + Random Trips Simulation

https://www.youtube.com/watch?v=LWecm_rCPJw&ab_channel=RodrigueTchamna

Firstly, install SUMO and Python. And create a new folder for the demo. 

After: 

  1) Search & download Open Street Map (OSM): Search an area and click in export. 

  2) Convert the Map into SUMO Network: netconvert --osm-files mapName.osm -o mapName.net.xml

  3) Go to C:\Program Files (x86)\Eclipse\Sumo\tools (YOUR RUTE). Copy randomTrips.py and paste in your folder. 
  Add trip & route to the network using build-in Python scripts: randomTrips.py :
  ```
  python (or py) YOURPATH\randomTrips.py -n mapName.net.xml -r mapName.rou.xml -e 50 (end of the simulation) -l
  ```
  4) Setup the configuration file and run the Network: Create mapName.sumocfg and lastly,in the folder, open my_config_file. It should open in SUMO. Or, open CMD: sumo-gui -c my_config_file.sumocfg

