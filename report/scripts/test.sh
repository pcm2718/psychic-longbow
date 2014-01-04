#!/bin/bash

mkdir -p timedat

for i in {0..9}
do
	NODES=$(sed -n 7,231p ../tsp225.txt | shuf -n 25)
	for search in "fc" "sa"
	do
		echo -n "$NODES" | python ../src/test.py $search "60" # | cut -d'!' -f1 >> timedat/timedat_${search}_${i}.dat &
	done
done
