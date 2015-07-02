#!/usr/bin/env python

try:
  import argparse
except ImportError:
  from FastNetTool import argparse

parser = argparse.ArgumentParser(description = 'Run training job on grid')
parser.add_argument('-d','--data', action='store', 
    required = True,
    help = "The file containing data for discriminator tunning")
parser.add_argument('-o','--output', action='store', 
    required = True,
    help = "The output base string for the discriminator file.")
parser.add_argument('-op','--outputPlace', action='store', 
    required = True,
    help = "The output place to a lxplus tmp.")
parser.add_argument('-i','--inputFolder', 
    metavar='InputFolder', 
    help = "Folder to loop upon files to retrieve configuration.")
parser.add_argument('--debug',  
    action='store_true',
    help = "Set queue to 1nh, and run for 3 files only.")
parser.add_argument('--local',  
    action='store_true',
    help = "For developing purproses only.")
parser.add_argument('--queue', 
    default='1nw',  
    help = "Choose queue if debug is not set.")
parser.add_argument('--pause', 
    default=5, type=int,
    help = "Time to wait between each submission.")
import sys
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)
# Retrieve parser args:
args = parser.parse_args()

if args.debug:
  limitFiles = 3
else:
  limitFiles = None

from FastNetTool.util import printArgs, getModuleLogger
logger = getModuleLogger(__name__)
printArgs( args, logger.info )

import os
#os.system('rcSetup -u')
inputFolder = os.path.abspath(args.inputFolder)
files = [ os.path.join(inputFolder,f) for f in os.listdir(inputFolder) if os.path.isfile(os.path.join(inputFolder,f)) ]
for n, f in enumerate(files):
  if limitFiles and n == limitFiles:
    break
  exec_str = """\
        env -i {bsub}\\
          {bsub_script} \\ 
            --jobConfig {jobFile} \\
            --datasetPlace {data} \\
            --output {output} \\
            --outputPlace {outputPlace}
      """.format(bsub = "bsub -q {queue} -u \"\" -J pyTrain".format(queue = args.queue,)
                 bsub_script = os.path.expandvars("$ROOTCOREBIN/user_scripts/FastNetTool/grid_submit/bsub_script.sh"),
                 data = args.data,
                 jobFile = f,
                 output = args.output,
                 outputPlace = args.outputPlace,
                 )
  logger.info("Executing following command:\n%s", exec_str)
  import re
  exec_str = re.sub(' +',' ',exec_str)
  exec_str = re.sub('\\\\','',exec_str) # FIXME We should be abble to do this only in one line...
  exec_str = re.sub('\n','',exec_str)
  #logger.info("Command without spaces:\n%s", exec_str)
  os.system(exec_str)
  import time
  time.sleep(args.pause)
