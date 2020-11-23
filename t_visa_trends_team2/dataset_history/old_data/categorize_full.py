from os import closerange
import shutil
import glob
import os
import pathlib

# Categorize text files by Year. (by month in progress). Assumes no categorization has been done prior. Uncomment print statements to see movement of each directory and file. 

# Use script in directory containing text files to be categorized. 


# for all files in the directory
for file in os.listdir(os.getcwd()):
    if file.endswith(".txt"):
        try:
            #print()
            #print('Current file : ' + file)
            f = open(file, 'r', encoding='utf-8')

            # since date comes after 'Date: ' in the file, split to find the month and year
            line = f.readline().split(': ')
            after_date_info = line[2]

            # to ignore applications related to family members as instructed
            if 'Supplement A, Application for Qualifying Family Member of a T-1 Nonimmigrant' in after_date_info:
                print(file + ' contains Application for family data')
                continue

            # placeholder to easily get month and year
            info = after_date_info.split(',')
    
            month = info[0].split()[0]
            year = info[1].split()[0]

            f.close()

            # handle formatting errors
            if len(year) !=  4:
                print(file + ' has incorrect format')
                continue
    
            try:
                # create directory for year
                os.mkdir(year + '/')
                
                #print('Directory ' + year + '/' + ' created')

                # move file into directory
                shutil.move(file, year + '/')

                #print(file + ' moved into directory ' + year + '/')

                # IN PROGRESS #
                # try:
                #     os.mkdir(month + '/')
                #     shutil.move(month + '/' , year + '/')
                #     print('Directory ' + year + '/' + month + '/' + ' created')
                #     shutil.move(year + '/' + file, year + '/' + month + '/')
                #     print('file' + str(counter) + ' moved into directory ' + year + '/' + month + '/')

                # except FileExistsError:
                #     shutil.move(year + '/' + file, year + '/' + month + '/')
                #     print('file' + str(counter) + ' moved into directory ' + year + '/' + month + '/')

            # directory already exists
            except FileExistsError:
                # move file to directory
                shutil.move(file, year + '/')

                #print(file + ' moved into directory ' + year + '/')

        # handle formatting errors
        except IndexError:
            print(file + ' has incorrect format')
            continue
