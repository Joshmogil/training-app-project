#!/bin/bash


set -e

docker kill neo4j
docker rm neo4j

echo "Killed and removed neo4j container"
docker container ls



exit 0