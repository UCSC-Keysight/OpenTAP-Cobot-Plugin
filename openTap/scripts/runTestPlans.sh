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

for file in *.TapPlan
do
    echo "Running $file ($counter/$sumFiles)"
    tap run -v $file
    ((counter++))
    echo "Done"
    sleep 1
done