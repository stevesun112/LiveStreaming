#!/bin/bash
# Supply the name of the script as the first argument
# Supply the ouput file as the second argument.

function kill_veil () {
    pkill -f veil_switch
    pkill -f veil_switch.pyc
    exit 0
}

trap kill_veil SIGINT

pkill -f veil_switch
pkill -f veil_switch.pyc

SCRIPT=$1
OUTPUT_FILE=$2

if [ ! -f $SCRIPT ]; then
    echo "Bad script name! $1 not found."
    exit 1;
fi

rm -fr $OUTPUT_FILE
sh $SCRIPT > $OUTPUT_FILE

# only exit on ctrl c
echo -n "Running"
while [ 1 ]; do 
    echo -n "."
    sleep 30
done