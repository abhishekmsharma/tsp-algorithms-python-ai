'''
Developer: Abhishek Manoj Sharma
Course: CS 256 Section 2
Homework: 4
Date: October 27, 2017
'''
from pyevolve_ex12_tsp import ga_main_run
from hw4_greedy import greedy_main_run
from hw4_astar import astar_main_run
from argparse import ArgumentParser
import os

help_description="The program accepts a single parameter which is the directory containing the TSP files"
parser = ArgumentParser(description=help_description)
parser.add_argument("-dir", help="Directory containing TSP files for benchmarking", required=True)
args = parser.parse_args()
file_names = os.listdir(args.dir)

#checking if directory path contains a slash in the end
if not args.dir.endswith("/"):
    args.dir+="/"

#iterating over all TSP files in the directory
for tsp_file in file_names:
    if tsp_file.lower().endswith(".tsp"):
        ga_main_run(args.dir+tsp_file)
        greedy_main_run(args.dir+tsp_file)
        astar_main_run(args.dir+tsp_file)