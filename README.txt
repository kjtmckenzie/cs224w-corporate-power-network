This directory contains the following files:

---------------Files--------------
+ board_relationships.csv - contains the raw LittleSis data I collected using SQL
+ board_relationships.py - contains source code to generate networks
+ corp_edge_dict.csv - raw file used to speed up graph generation
+ corporation_network.graph - the corportation - corporation network
+ dir_edge_dict.csv - raw file used to speed up graph generation
+ director_network.graph - the director - director network


---------------To Use--------------
You'll need gnuplot if you plan on graphing, as well as snap.py

run the following to generate all the graphs:
python board_relationships.py

If you delete the graph and CSV dictionary files, it will take about 10 minutes to regenerate them (depending on how fast your computer is), but you really should never have to do that.  Every other time it takes about 5 seconds to load the graphs.

To do any analysis of the graphs, write a function and throw it in to the board_relationships file.  You can then call it in main function.


-------------Data Org------------
The data is the 896 companies in the LittleSis database

While running the python code:

relationships[i][0] = Board Member ID
relationships[i][1] = Board Member First Name
relationships[i][2] = Board Member Last Name
relationships[i][3] = Standardized Company Name in 896 companies
relationships[i][4] = Standardized Company ID

all_directors is a dictionary of Board Member ID -> Board Member Name
all_companies is a dictionary of Company ID -> Company Name

director_network is the network of directors that are linked by edges representing company boards that they both sit on

corporation_network is the network of corporations that are linked by edges representing directors that sit on both boards

corp_edge_dict is a dictionary with two fields:
    Key) string that has the two corporation IDs that are linked
    Value) the number of shared directors

director_edge_dict is a dictionary with two fields:
    Key) string that has the two board member IDs that are linked
    Value) the number of boards that they both sit on

