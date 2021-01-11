WORKS!!!!

###############################################################################################

In this example, the cars are going from one extreme to the other (N-> S/E, W->E)

There are 3 traffic lights (R-G-G and G-G-R):

![Traffic lights ](https://raw.githubusercontent.com/sandruskyi/SUMO_DEMOS/master/Intersections_Emissions_TraCI/Intersections_emergency_TraCI/image1.PNG)


On the intersection N->S/E, when the detector detects an emergency car, only the emergency cars can use the left lane (30 seconds). In this case, the emergency car can use both lanes. If the traffic line is red for the right lane, only emergency cars can use the left lane. 


Results: 

![Intersection](https://raw.githubusercontent.com/sandruskyi/SUMO_DEMOS/master/Intersections_Emissions_TraCI/Intersections_emergency_TraCI/image2.PNG)

- TripInfo, example: 
```
<tripinfo id="NSn0" depart="1.00" departLane="e1a_0" departPos="5.10" departSpeed="0.00" departDelay="0.00" arrival="19.00" arrivalLane="e3_0" arrivalPos="68.21" arrivalSpeed="13.56" duration="18.00" routeLength="192.06" waitingTime="0.00" waitingCount="0" stopTime="0.00" timeLoss="4.07" rerouteNo="0" devices="tripinfo_NSn0" vType="normal_car" speedFactor="1.06" vaporized=""/>
<tripinfo id="NEn2" depart="4.00" departLane="e1a_0" departPos="5.10" departSpeed="0.00" departDelay="2.00" arrival="26.00" arrivalLane="e2_1" arrivalPos="88.79" arrivalSpeed="13.72" duration="22.00" routeLength="207.27" waitingTime="0.00" waitingCount="0" stopTime="0.00" timeLoss="5.52" rerouteNo="0" devices="tripinfo_NEn2" vType="normal_car" speedFactor="1.01" vaporized=""/>
<tripinfo id="NEn3" depart="7.00" departLane="e1a_0" departPos="5.10" departSpeed="0.00" departDelay="3.00" arrival="28.00" arrivalLane="e2_1" arrivalPos="88.79" arrivalSpeed="14.22" duration="21.00" routeLength="207.27" waitingTime="0.00" waitingCount="0" stopTime="0.00" timeLoss="6.67" rerouteNo="0" devices="tripinfo_NEn3" vType="normal_car" speedFactor="1.08" vaporized=""/>
    
```
   

