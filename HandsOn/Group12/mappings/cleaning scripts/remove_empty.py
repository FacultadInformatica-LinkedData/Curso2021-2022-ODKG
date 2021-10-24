

original_filepath = 'output.txt'
new_filepath = 'output_clean.txt'

with open(original_filepath) as original_file:
   with open(new_filepath, 'w') as new_file:
      line = original_file.readline()
      while line:
         if '""' not in line:
            new_file.write(line.strip()+'\n')
         line = original_file.readline()