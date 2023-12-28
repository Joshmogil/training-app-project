#!/bin/bash

set -e

docker run \
    --name=neo4j \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$(pwd)/neo4j/data:/data \
    -d neo4j

docker container ls

file="./.gitignore"
if ! grep -q "neo4j" "$file"; then
    # If 'neo4j' is not found, append '**/neo4j' to the file
    echo "**/neo4j" >> "$file"
fi

echo "Neo4j up and running and available on http://localhost:7474"
echo "The default username/password in the UI is neo4j/neo4j"



exit 0