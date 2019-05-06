import os
import string
import random

random_string_length = 10

letters = string.ascii_lowercase
temp_str_2 = ''.join(random.choice(letters) for i in range(random_string_length))

if(not os.path.exists('iTrust2-v4/iTrust2/RandomFolder')):
    os.mkdir('iTrust2-v4/iTrust2/RandomFolder')
if(not os.path.exists('checkboxio/RandomFolder')):
    os.mkdir('checkboxio/RandomFolder')

temp_file = open('iTrust2-v4/iTrust2/RandomFolder/{}'.format(temp_str_2), 'w')
temp_file.write(temp_str_2)
temp_file.close()

temp_file = open('checkboxio/RandomFolder/{}'.format(temp_str_2), 'w')
temp_file.write(temp_str_2)
temp_file.close()