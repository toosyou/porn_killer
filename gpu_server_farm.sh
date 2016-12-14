#!/bin/bash

for port in $(seq 9000 9009)
do
    echo 'start server at port: ' $port
    python gpu_server.py $port &
done

PumpkinLB.py gpu_server_farm.cfg
