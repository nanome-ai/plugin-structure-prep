if [[ $(docker volume inspect structure-prep-volume) ]]; then
    echo "Skipping structure-prep volume creation"
else
    echo "Creating new docker volume for structure-prep"
    docker volume create structure-prep-volume
fi

docker build -f structure-prep.Dockerfile -t structure-prep:latest ..