#!/bin/bash
cd /environment/testPlans/

sumFiles=$(ls -1 *.TapPlan 2>/dev/null | wc -l)
counter=1

if [ $sumFiles != 0 ]
then
    echo "Found $sumFiles test plan(s) to run"
else
    echo "No files found to run"
    exit 1
fi

while true; do
    read -p "Do you wish to run the above files? [y/n] " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit 0;;
        * ) echo "Please answer yes or no.";;
    esac
done

for file in *.TapPlan
do
    echo "Running $file ($counter/$sumFiles)"
    tap run -v $file
    ((counter++))
    echo "Done"
    sleep 1
done