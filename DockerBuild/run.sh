#!/bin/bash
set -e

cd /usr/local/tomcat/bin
./startup.sh

echo "start sleep........."
while [ 1 ]
do
        sleep 300
done
