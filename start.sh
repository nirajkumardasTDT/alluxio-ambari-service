#!/usr/bin/env bash

sudo su

git clone https://github.com/chuyqa/alluxio-ambari-service /var/lib/ambari-server/resources/stacks/HDP/2.5/services/ALLUXIO

wget http://alluxio.org/downloads/files/1.0.1/alluxio-1.0.1-bin.tar.gz -P /var/lib/ambari-server/resources/stacks/HDP/2.5/services/ALLUXIO/package/files
