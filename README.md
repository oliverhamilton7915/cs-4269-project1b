# cs-4269-project1b
CS 4269, Project 1a, Group 7

Group Members: Max Cummings, Alex Cho, Jacob Feldstein, and Oliver Hamilton

This repository contains two files: group7_project1b.py and World.py. The former is the driver class and the latter is defines our World and Country class. Each country has certain 'basic' and 'created' resources that are weighted by the scalars represented by RESOURCE_WEIGHTS in World.py. A countries utility is the weighted sum of its possessed resources. A world consists of 1 or more countries and its utility (big U) is the average utility of each country divided by the standard deviation of its countries' utilities. The world class has a get_successors function that models all different types and sizes of transform and tranfer operations and stores the resulting successors worlds in a priority queue organized by decreasing big U value. 

Example run:
Current World State: 
France: r1: 100 r2: 30 r3: 110 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 140.0
Germany: r1: 140 r2: 120 r3: 65 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 185.0
America: r1: 190 r2: 130 r3: 100 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 230.0
Thailand: r1: 35 r2: 12 r3: 45 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 57.0
Big U: 1.196994031612113

--- WORLD'S SUCCESSORS: ---
('TRANSFER', 'America', 'r2', 25, 'Thailand', 'r3', 25)
Current World State: 
France: r1: 100 r2: 30 r3: 110 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 140.0
Germany: r1: 140 r2: 120 r3: 65 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 185.0
America: r1: 190 r2: 105 r3: 75 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 180.0
Thailand: r1: 35 r2: 37 r3: 70 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 107.0
Big U: 2.4077327136142053

('TRANSFER', 'Germany', 'r2', 25, 'Thailand', 'r3', 25)
Current World State: 
France: r1: 100 r2: 30 r3: 110 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 140.0
Germany: r1: 140 r2: 95 r3: 40 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 135.0
America: r1: 190 r2: 130 r3: 100 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 230.0
Thailand: r1: 35 r2: 37 r3: 70 r21: 0 r21': 0 r22: 0 r22': 0 r23: 0 r23': 0 utility: 107.0
Big U: 1.6558208830993588

...
...
...
