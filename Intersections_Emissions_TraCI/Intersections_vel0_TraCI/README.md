WORKS!!!!

###############################################################################################

In this example, the cars are going from one extreme to the other. 


When a detector detects the car, the car stops and we can recover the CO2 emission in this step. 


20ms later the car continues on its way.


At the end of the simulation, the total CO2 emission is recovered.

![Intersection](https://raw.githubusercontent.com/sandruskyi/SUMO_DEMOS/master/Intersections_Emissions_TraCI/Intersections_vel0_TraCI/image1.PNG)
Results: 

- Console Results, example: 

![Consol results](https://raw.githubusercontent.com/sandruskyi/SUMO_DEMOS/master/Intersections_Emissions_TraCI/Intersections_vel0_TraCI/image2.PNG)


- TripInfo, example: 
```
<tripinfo id="Au0" depart="2.00" departLane="-e3_0" departPos="5.10" departSpeed="0.00" departDelay="0.00" arrival="90.00" arrivalLane="-e1_0" arrivalPos="431.25" arrivalSpeed="14.72" duration="88.00" routeLength="911.58" waitingTime="17.00" waitingCount="1" stopTime="0.00" timeLoss="25.44" rerouteNo="0" devices="tripinfo_Au0" vType="autonomous_car@Au0" speedFactor="1.06" vaporized=""/>
    <tripinfo id="Au3" depart="5.00" departLane="e1_0" departPos="5.10" departSpeed="0.00" departDelay="0.00" arrival="93.00" arrivalLane="e3_0" arrivalPos="464.63" arrivalSpeed="15.04" duration="88.00" routeLength="911.58" waitingTime="18.00" waitingCount="1" stopTime="0.00" timeLoss="26.99" rerouteNo="0" devices="tripinfo_Au3" vType="autonomous_car@Au3" speedFactor="1.08" vaporized=""/>
    ```
    
- Detectors out, example: 
```
<interval begin="0.00" end="300.00" id="det_1_0" nVehContrib="14" flow="168.00" occupancy="26.07" speed="8.06" harmonicMeanSpeed="0.97" length="5.00" nVehEntered="16"/>
    <interval begin="0.00" end="300.00" id="det_1_1" nVehContrib="10" flow="120.00" occupancy="28.69" speed="6.44" harmonicMeanSpeed="0.58" length="5.00" nVehEntered="10"/>
    <interval begin="0.00" end="300.00" id="det_2_0" nVehContrib="10" flow="120.00" occupancy="37.06" speed="3.93" harmonicMeanSpeed="0.45" length="5.00" nVehEntered="11"/>
    <interval begin="0.00" end="300.00" id="det_2_1" nVehContrib="11" flow="132.00" occupancy="40.14" speed="3.94" harmonicMeanSpeed="0.49" length="5.00" nVehEntered="12"/>
    <interval begin="0.00" end="300.00" id="det_3_0" nVehContrib="13" flow="156.00" occupancy="52.47" speed="4.26" harmonicMeanSpeed="0.41" length="5.00" nVehEntered="13"/>
    <interval begin="0.00" end="300.00" id="det_3_1" nVehContrib="8" flow="96.00" occupancy="46.06" speed="2.97" harmonicMeanSpeed="0.36" length="5.00" nVehEntered="10"/>
    <interval begin="0.00" end="300.00" id="det_4_0" nVehContrib="12" flow="144.00" occupancy="58.49" speed="2.87" harmonicMeanSpeed="0.34" length="5.00" nVehEntered="12"/>
    <interval begin="0.00" end="300.00" id="det_4_1" nVehContrib="10" flow="120.00" occupancy="51.97" speed="2.26" harmonicMeanSpeed="0.33" length="5.00" nVehEntered="11"/>
    <interval begin="300.00" end="531.00" id="det_1_0" nVehContrib="2" flow="31.17" occupancy="9.76" speed="4.23" harmonicMeanSpeed="0.44" length="5.00" nVehEntered="3"/>
    <interval begin="300.00" end="531.00" id="det_1_1" nVehContrib="2" flow="31.17" occupancy="10.20" speed="1.37" harmonicMeanSpeed="0.42" length="5.00" nVehEntered="2"/>
    <interval begin="300.00" end="531.00" id="det_2_0" nVehContrib="6" flow="93.51" occupancy="47.11" speed="0.93" harmonicMeanSpeed="0.28" length="5.00" nVehEntered="6"/>
    <interval begin="300.00" end="531.00" id="det_2_1" nVehContrib="6" flow="93.51" occupancy="43.70" speed="1.16" harmonicMeanSpeed="0.28" length="5.00" nVehEntered="5"/>
    <interval begin="300.00" end="531.00" id="det_3_0" nVehContrib="2" flow="31.17" occupancy="4.52" speed="9.57" harmonicMeanSpeed="9.57" length="5.00" nVehEntered="3"/>
    <interval begin="300.00" end="531.00" id="det_3_1" nVehContrib="2" flow="31.17" occupancy="10.34" speed="0.31" harmonicMeanSpeed="0.29" length="5.00" nVehEntered="1"/>
    <interval begin="300.00" end="531.00" id="det_4_0" nVehContrib="8" flow="124.68" occupancy="51.23" speed="1.01" harmonicMeanSpeed="0.34" length="5.00" nVehEntered="8"/>
    <interval begin="300.00" end="531.00" id="det_4_1" nVehContrib="7" flow="109.09" occupancy="70.06" speed="0.23" harmonicMeanSpeed="0.23" length="5.00" nVehEntered="7"/>
    ```

    

    


