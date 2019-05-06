import os
import re
import random
import string

# Import all files
file_names = [line.rstrip('\n') for line in open('filenames.txt')] 

# Store set of regex matches : T : '==.*?.*:.*;',

regex_match = ['==', '!=', '> [0-9]+', '< [0-9]+' , '[4-9]', '".*"']

#print(file_names)

# Change to the base folder
os.chdir('./iTrust2-v4/iTrust2/src/main/java/edu/ncsu/csc/itrust2/')

# Initialise counter
counter = 0

# Initialise random string length
random_string_length = 15

# Loop through and change 10 files each time

while (counter < 10):
    # Set the check flag as false
    check_flag = False

    # Create new list to store output
    output_list = []

    # Get a random value
    random_operation_number = random.randint(0,4)
    random_file_number = random.randint(0,len(file_names) - 1)
    
    # Use the random value to select an operation to perform and file to select
    regex_pattern = re.compile(regex_match[random_operation_number])
    random_file = file_names[random_file_number]
    
    # Print selected filename 
    #print(random_file)

    # Open the selected file
    with open(random_file) as f:
        line = f.read()
    
    if(True):
    #for line in lines:
        temp_random_number = random.randint(4,9)
        regex_match_transform = ['!=',  '==', '< '+str(temp_random_number), '>'+str(temp_random_number), str(temp_random_number)]
        print(random_operation_number)
        if((regex_pattern.search(line) != None)):
            check_flag = True
            print(random_file)
            
            # Replace line in new output list
            if(random_operation_number == 5):
                # Generate random string
                letters = string.ascii_lowercase
                temp_str = '\"'
                temp_str_2 = ''.join(random.choice(letters) for i in range(random_string_length))
                temp_str += temp_str_2 + '\"'
                regex_match_transform.append(temp_str)
                
            #Replace using regex_match_transform
            line = re.sub(regex_pattern, str(regex_match_transform[random_operation_number]), line)
            print(regex_pattern)
            print(str(regex_match_transform[random_operation_number]))
        output_list.append(line)    

    if(check_flag == True):
        with open(random_file, 'w') as f:
            for item in output_list:
                f.write("%s" % item)
        counter += 1        
    
    