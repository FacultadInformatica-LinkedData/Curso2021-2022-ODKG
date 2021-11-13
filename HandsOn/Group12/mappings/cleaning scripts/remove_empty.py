original_filepath = 'data.nt'
new_filepath = 'data-cleaned.nt'

with open(original_filepath, encoding='utf-8') as original_file:
   with open(new_filepath, 'w', encoding='utf-8') as new_file:
      line = original_file.readline()
      while line:
         if ('""' not in line) and ('<>' not in line):
            new_file.write(line.strip()+'\n')
         line = original_file.readline()