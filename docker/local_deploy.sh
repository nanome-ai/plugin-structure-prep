docker run -d \
-p 8888:8888 \
--mount source=structure-prep-volume,destination=/app \
--name local_structure-prep structure-prep