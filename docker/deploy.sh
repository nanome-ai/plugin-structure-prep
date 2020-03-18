#!/bin/bash

if [ "$(docker ps -aq -f name=structure-prep)" != "" ]; then
    echo "removing exited container"
    docker rm -f structure-prep
fi

docker run -d \
--name structure-prep \
--restart unless-stopped \
-e ARGS="$*" \
structure-prep
