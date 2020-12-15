""" Reads in a csv file and creates two lists, one with the names of the organizations and
    one with their address. This code can handle cases where the name and address take up
    two or three lines and are properly separated between those lines; however, it can not
    handle cases where the name and address are on only one line or if the name and address
    loop around between lines. It also can't get rid of duplicates.
"""
    
filename = "BostonCommunityFoundationGrantees.csv"

with open(filename, "r") as f:
        lines = f.readlines()
        name = []
        address = []
        contin = 0
        add = 0

        for line in lines[2:]:
            line = line.split('\n')

            if line[0][-1] != "," and contin == 0: # add name
                name.append(line[0])
                contin = 1
            elif line[0][-1] != "," and contin == 1: # add (1/2) address
                address.append(line[0])
                add = 1
            elif line[0][-1] == "," and contin == 1 and add == 0 : # add (1/1) address
                line = line[0].split(',')
                line = line[0] + "," + line[1]
                address.append(line)
                contin = 0
            elif line[0][-1] == "," and contin == 1 and add == 1: # add (2/2) address
                line = line[0].split(',')
                line = line[0] + "," + line[1]
                address[-1] = address[-1] + ", " + line
                contin = 0
                add = 0
            
                
