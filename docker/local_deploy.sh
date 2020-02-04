if [ "$(docker ps -aq -f name=structure-prep)" != "" ]; then
        # cleanup
        echo "removing exited container"
        docker rm -f structure-prep
fi

if [ "$1" != "" ]; then
    echo "Using specified plugin server: $1"
    docker run -d \
    -p 8888:8888 \
    -e PLUGIN_SERVER=$1 \
    --name structure-prep structure-prep
else
    echo "Using default plugin server: plugins.nanome.ai"
    docker run -d \
    -p 8888:8888 \
    --name structure-prep structure-prep
fi