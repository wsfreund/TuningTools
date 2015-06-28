#!/bin/sh


# Default args:
Inits=100

while true
do
  echo "reading $1 $2"
  if test "$1" == "--datasetPlace"
  then
    DatasetPlace=$2
    echo "Setting DatasetPlace to $DatasetPlace"
    Dataset=`basename $DatasetPlace`
    shift 2
  elif test "$1" == "--jobConfig"
  then
    jobConfig="$2"
    echo "Setting jobConfig to $jobConfig"
    shift 2
  elif test "$1" == "--outputPlace"
  then
    outputPlace="$2"
    outputDestination=${outputPlace%%:*}
    outputFolder=${outputPlace#*:}
    echo "Setting outputPlace to $outputPlace: destination is $outputDestination and folder is $outputFolder"
    shift 2
  elif test "$1" == "--output"
  then
    output="$2"
    echo "Setting output to $output"
    shift 2
  else
    break
  fi
done

basePath=$PWD

# Check arguments
test "x$DatasetPlace" = "x" -o ! -f "$DatasetPlace" && echo "DatasetPlace \"$DatasetPlace\" doesn't exist" && exit 1;
test "x$jobConfig" = "x" -o ! -f "$jobConfig" && echo "JobConfig file \"$jobConfig\" doesn't exist" && exit 1;

# Retrieve package and compile
git clone https://github.com/joaoVictorPinto/TrigCaloRingerAnalysisPackages.git
sleep 1
rootFolder=$basePath/TrigCaloRingerAnalysisPackages/root
cd $rootFolder
echo "Previous installation environment"
env
source ./buildthis.sh
echo "Environment after instalation"
env
source ./FastNetTool/cmt/new_env_file.sh
echo "Environment after source"
env

# Go to job path:
gridSubFolder=$rootFolder/FastNetTool/scripts/grid_submit
cd $gridSubFolder

# Retrieve dataset
rsync -rvhzP $DatasetPlace .

# Run the job
./bsub_job.py $Dataset $jobConfig $output || { echo "Couldn't run job!" && return 1;}

# Copy output to outputPlace
ssh $outputDestination mkdir -p $outputFolder

rsync -rvhzP $output* "$outputPlace"
