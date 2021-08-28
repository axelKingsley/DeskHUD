#!/bin/bash

exec 77<> /dev/ttyACM1

for (( i=1; i<300; i++))
do
  echo $i >&77
  sleep 0.01
done

exec 77>&-
