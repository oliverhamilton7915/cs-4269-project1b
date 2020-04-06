# cs-4269 Post Break
CS 4269, post-break, Group 7

Group Members: Max Cummings, Alex Cho, Jacob Feldstein, and Oliver Hamilton

This repository contains two files: group7_project1b.py and World.py. The former is the driver class and the latter is defines our World and Country class. Each country has certain 'basic' and 'created' resources that are weighted by the scalars represented by RESOURCE_WEIGHTS in World.py. A countries utility is the weighted sum of its possessed resources. A world consists of 1 or more countries and its utility (big U) is the average utility of each country divided by the standard deviation of its countries' utilities. The world class has a get_successors function that models all different types and sizes of transform and tranfer operations and stores the resulting successors worlds in a priority queue organized by decreasing big U value. 

