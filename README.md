# HCI
A simple Python script to determine the cheapest way to get Grade 1 Hannish Certificates of Import.

Requires Python 3.8 or newer

There is a .bat file included, which will work with the default parameters, searching Lich on Light and writing the results to stdio.

The server or datacenter can be changed by calling the script directly through `python HCI.py [World/DC] [-w]`

There are two optional arguments:
  
  `[World/DC]` - The world or datacenter to be searched, accepts a case insensitive string. If a world is chosen only results from this world will be considered. If a datacenter is chosen the cheapest offer from any world on that datacenter will be included. If no world/DC or an unknown string is entered, the program will default to (Light) Lich.
  
  `[-w]` - Switch to also write the output into a file called *Data.txt* in the same directory as the script. Defaults to *False*