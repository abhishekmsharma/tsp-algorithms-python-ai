'''
Developer: Abhishek Manoj Sharma
Course: CS 256 Section 2
Homework: 4
Date: October 27, 2017
'''

#TSP Reader contains the readTSP() method which first checks the EDGE_WEIGHT_TYPE of TSP file and then reads and returns the coordinates back
class TSPReader:
    def readTSPFile(self,tsp_file_name):
        coords = []
        with open(tsp_file_name) as tsp_file:
            for line in tsp_file:
                if "EDGE_WEIGHT_TYPE" in line:
                    splittedLine = line.strip().split(":")
                    if not ("ATT" in splittedLine[1] or "EUC_2D" in splittedLine[1]):
                        print tsp_file_name,"-","Edge weight type (",splittedLine[1].strip(),") not valid"
                        return False,None
                if "NODE_COORD_SECTION" in line:
                    for line in tsp_file:
                        if not (line.strip() == "EOF"):
                            splittedLine = line.strip().split()
                            coords.append((float(splittedLine[1]),float(splittedLine[2])))
        return True,coords