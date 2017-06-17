#!/bin/sh
docker login -u admin -p 123456 192.168.43.10:5002
rm -rf ${WORKSPACE}/DockerBuild/javademo
#cd ${WORKSPACE}/WebContent
mv ${WORKSPACE}/WebContent ${WORKSPACE}/DockerBuild/javademo
cd ${WORKSPACE}/DockerBuild
docker build -t 192.168.43.10:5002/joe/java-demo:${BUILD_NUMBER} .
docker push 192.168.43.10:5002/joe/java-demo:${BUILD_NUMBER}
cd ${WORKSPACE}/DockerBuild
sed -i 's/\$\$BUILD_NUMBER\$\$/'${BUILD_NUMBER}'/g' docker-compose.yml
sed -i 's/\$\$PORT_NUMBER\$\$/'`expr 9000 + ${BUILD_NUMBER}`'/g' docker-compose.yml

## Update Stack by BuildNumber
#rancher-compose --url http://192.168.43.100 --access-key CD364FA2E6E3F2F0B91A --secret-key C4VEhhnGRXtvdPS9PL27NLJUatDQJNmxwogS5emM -p java-demo-build${BUILD_NUMBER} up -d

## Update Stack and keep OnlyOne
rancher-compose --url http://192.168.43.100 --access-key CD364FA2E6E3F2F0B91A --secret-key C4VEhhnGRXtvdPS9PL27NLJUatDQJNmxwogS5emM -p java-demo up -d --confirm-upgrade --upgrade


#python ./get_service.py  java-demo
#touch ${WORKSPACE}/propfile.txt
#export PUBILC_IP=`xargs -a public_ip.txt`
#echo "PUBILC_IP=$PUBILC_IP" > ${WORKSPACE}/propfile.txt
