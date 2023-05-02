FROM base_python_image:latest
RUN pip install haversine
COPY server /
COPY common/* /src/
ENTRYPOINT ["/bin/sh"]
