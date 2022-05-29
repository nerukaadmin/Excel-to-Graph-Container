#!/bin/sh
echo Pass argumrnt for script....
echo For all "a"
echo For team "t"
read input </dev/tty
docker build -t ex_to_graph:v1 .
docker run -v /home/neo/Desktop/Project_graph/dokcer_con:/excel ex_to_graph:v1 -e 
