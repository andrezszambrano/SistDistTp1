FROM base_python_image:latest

RUN pip install haversine
COPY common /src/
COPY server/server_common /src/
COPY server/montreal_distance_processor /
ENTRYPOINT ["/bin/sh"]