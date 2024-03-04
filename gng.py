'''
                *******************************************************************
                *                        Grep and Grab                            *
                *                                                                 *
                * Description: This Python3 script takes your search term, in     *
                * REGEX format, and GREPS it against your chosen target directory.*
                * If files are found, it will then copy them to an output         *
                * directory of your choosing.                                     *
                * Reqs: For use on Unix-based systems.                            *
                * Author: Taylor Nitschke, DFA, Sphinx, LLC                       *
                *******************************************************************
                  Usage: python3 ./gng.py [-h] -s SEARCH -t TARGET -o OUTPUT [-v]
'''

import argcomplete,argcomplete
import os
import shutil
import subprocess
#PYTHON_ARGCOMPLETE_OK

__version__ = "0.03"
__date__ = "1 March 2024"

parser = argparse.ArgumentParser(description='This Python3 script takes your search term, in REGEX format, and GREPS it against your chosen target directory. If files are found, it will then copy them to an output directory of your choosing.')
parser.add_argument('-s','--search',type=str,required=True,help='The search term to grep (REQUIRED)')
parser.add_argument('-t','--target',type=str,required=True,help='The target directory to grep against (REQUIRED)')
parser.add_argument('-o','--output',type=str,required=True,help='The output directory where files containing the search term are copied to (REQUIRED)')
parser.add_argument('-v','--version',action='version',version=f'%(prog)s v{__version__} {__date__}')

argcomplete.autocomplete(parser)
args = parser.parse_args()
searchFor = args.search
target = args.target
if os.path.exists(target):
    print('\nTarget directory found. Moving on...')
else:
    print('\n***WARNING: Target Directory does not exist. Please check it and try again.***')
    target = input('Target Directory: ')
    if os.path.exists(target):
        print('\nTarget directory found. Moving on...')
    else:
        print('\nDirectory not found. Please check it and try again.')
        exit()

output = args.output
if os.path.exists(output) != True:
    os.mkdir(output)
    print('\nOutput directory created. Moving on...')

print(f'\nRunning GREP -r -l for "{searchFor}" at {target}...')
results = subprocess.run(['grep','-r','-l',searchFor,target],capture_output = True)
if results:
    files = results.stdout.decode().split('\n')
    print(f'\nCopying files that contain "{searchFor}" at {target}...')
    for file in files:
        if os.path.isfile(file):
            shutil.copy(file,output)
            #subprocess.run(['sudo','cp',file,'-t',output])
    print(f'Complete! Please check {output} for your files.')
else:
    print(f'No files found containing "{searchFor}"')
