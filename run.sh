#!/bin/sh
echo Pass argumrnt for script....
echo For all "a"
echo For team "t"
echo Input:
read input </dev/tty
python3 ex_to_graph.py $input
