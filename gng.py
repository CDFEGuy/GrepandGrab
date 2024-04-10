'''
                *******************************************************************
                *                        Grep and Grab                            *
                *                                                                 *
                * Description: This Python3 script takes your search term, in and *
                * GREPS it against your chosen target directory. If files are     *
                * found, it will then copy them to an output directory of your    *
                * choosing.                                                       *
                * Reqs: For use on Unix-based systems.                            *
                * Author: Taylor Nitschke, CDFE, CCI                              *
                *******************************************************************
                  Usage: python3 ./gng.py [-h] -s SEARCH -t TARGET -o OUTPUT [-v]
'''

import argcomplete,argparse
import re
import os,time
import shutil
import subprocess
from tqdm import tqdm
#PYTHON_ARGCOMPLETE_OK

__version__ = "0.16.1"
__date__ = "10 April 2024"

##############################################
# Introduce parser arguments                 #
# Create 4 - search, target, output, version #
##############################################

parser = argparse.ArgumentParser(description='This Python3 script takes your search term and GREPS it against your chosen target directory. If files are found, it will then copy them to an output directory of your choosing.')

parser.add_argument('-s','--search',nargs='+',required=True,help='The search term to grep (REQUIRED)')
parser.add_argument('-t','--target',type=str,required=True,help='The target directory to grep against (REQUIRED)')
parser.add_argument('-o','--output',type=str,required=True,help='The output directory where files containing the search term are copied to (REQUIRED)')
parser.add_argument('-v','--version',action='version',version=f'%(prog)s v{__version__} {__date__}')
argcomplete.autocomplete(parser)
args = parser.parse_args()

searchFor = args.search
target = args.target
output = args.output

print('''\n
  ________                                          .___   ________            ___.    
 /  _____/______   ____ ______   _____    ____    __| _/  /  _____/___________ \_ |__  
/   \  __\_  __ \_/ __ \\____ \  \__  \  /    \  / __ |  /   \  __\_  __ \__  \ | __ \ 
\    \_\  \  | \/\  ___/|  |_> >  / __ \|   |  \/ /_/ |  \    \_\  \  | \// __ \| \_\ \
 \______  /__|    \___  >   __/  (____  /___|  /\____ |   \______  /__|  (____  /___  /
        \/            \/|__|          \/     \/      \/          \/           \/    \/ 

Version 0.16.1
''')

# Objectives:
# 1. Check if target directory exists. Correct if False. Return target.
# 2. Run Grep and collect, decode files found - if any. Return list of files.
# 3. Check output. Create if False, only if total > 0. Return output.
# 4. Conduct the copy! Include pbar using tqdm. Should not need to return anything.

# Check target to ensure path exists. Loop to allow correction. Return target.
def target_check(target):
    print('\nChecking Target Directory...')
    time.sleep(0.5)
    while not os.path.exists(target):
        print('\nTarget directory does not exist. Please check it and try again')
        target = input('Target Directory: ')
    print('\nTarget directory found. Moving on...')
    return target

# Use subprocess.run to createterminal command GREP for string at target directory. Return files.
def search_tool(string, directory):
    search_string = ' '.join(string)
    print(f'\nGrepping "{search_string}" in {directory}...')
    search_pattern = '.*'.join(string)
    results = subprocess.run(['grep','-R','-l','-w',search_pattern,directory], capture_output = True)
    files = results.stdout.decode().split('\n')
    return files

# Get a count of files found containing string. Used later for status bar. Return total.
def file_counter(files, string):
    time.sleep(0.5)
    search_string = ' '.join(string)
    total = sum(1 for i in files if os.path.isfile(i))
    if total == 0:
        print(f'\nNo files found containing "{search_string}"!\n')
        exit()
    else:
        print('\nCounting Files...')
        print(f'\n{total} files found containing "{search_string}"!\n')
    return total

# Check output directory. Create if it doesn't exist. Return output.
def output_check(directory):
    print('\nChecking Output Directory...')
    if not os.path.exists(output):
        os.mkdir(directory)
        print('\nOutput Directory Created.')
    print('\nOutput directory found. Moving on...\n')
    return output

# Conduct copy. Use tqdm's pbar to show status of copy job. For loop to copy file to output.
def run_copier(total, files, output):
    with tqdm(total=total, desc="Copying files", unit="file") as pbar:
        for file in files:
            if os.path.isfile(file):
                shutil.copy(file, output)
                pbar.update(1)

# Put it all together!
def main():
    target_check(target)
    files = search_tool(searchFor, target)
    total = file_counter(files, searchFor)
    output_check(output)
    run_copier(total, files, output)
    search_string = ' '.join(searchFor)
    print(f'\nComplete! {total} files containing {search_string} were copied to {output}!\n')

# Execute!
if __name__ == "__main__":
    main()
