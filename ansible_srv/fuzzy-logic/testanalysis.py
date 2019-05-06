import os
import re
import random
import numpy as np
import pandas as pd
# Stores all the test file names #38
list_of_output_files = [line.rstrip('\n') for line in open('output_files.txt')]

#number of iterations plus 1
numberOfIterations = 101

# Length of output files
length_output_files = len(list_of_output_files)

dataType = [('Test Number', int), ('Tests', int), ('Failed', int), ('Error', int), ('Skipped', int), ('Time', float)]

output_stats = np.zeros((length_output_files, 6), dtype=float)

#print(output_stats[:,:])

# Store set of regex matches : T : '==.*?.*:.*;',
regex_match = ['Tests run: \d*', 'Failures: \d*', 'Errors: \d*', 'Skipped: \d*', 'Time elapsed: \d*[.]?\d*']

# Iterate over all directories
for directory_number in range(1, numberOfIterations):
    directory_name = '/target_output/' + str(directory_number) + '/surefire-reports/'
    
    # Change directory        
    os.chdir(directory_name)
    
    #Set a counter for each file
    j = 0

    # Import all files
    for all_files in list_of_output_files:
        # Open each file
        file_name = [line.rstrip('\n') for line in open(all_files)][3]
        
        # Print file name    
        #print(file_name)

        # Set regex counter
        counter = 0
        output_stats [j, counter] = j

        counter += 1

        for each_match in regex_match:
            regex_pattern = re.compile(each_match)
            output_stats[j, counter] += (float(regex_pattern.search(file_name).group(0).split(':')[1]))
            counter += 1
        j += 1

tempList = []

df = pd.DataFrame(output_stats, columns=['File', 'Tests', 'Failed', 'Error', 'Skipped', 'Time'])
df.loc[:, 'Time'] /= 100
df = df.sort_values(by=['Failed', 'Time'], ascending=[False, True])

for i in range (0, length_output_files):
    tempList.append((output_stats[i, 0], output_stats[i, 1], output_stats[i, 2], output_stats[i, 3], output_stats[i, 4], output_stats[i, 5]))

#print(tempList)

#print(output_stats[:,:])  

output_stats_to_sort = np.array(tempList, dtype=dataType)

output_stats_to_sort = np.sort(output_stats_to_sort, order=['Failed', 'Time'])

#print('Test Name\tRun\tFailed\tAverage Time\n')

i = 0

output_string = '---------------------------------------------------------------------------------------------------------\n'
output_string += 'Run\tFailed\tErrors\tAverage Time\t\t\tTest Name\t\t\t\t\t\n'
output_string += '---------------------------------------------------------------------------------------------------------\n'

for i in range(0, length_output_files):
    output_string += str(df.iloc[i,1])+'\t'+str(df.iloc[i,2])+'\t'+str(df.iloc[i,3])+'\t'+str(df.iloc[i,5])+'\t'+str(list_of_output_files[int(df.iloc[i,0])])+'\n'

with open('/home/vagrant/output_analysis.txt', 'w') as file_to_save:
    file_to_save.write(output_string)
