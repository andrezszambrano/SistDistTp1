FROM python:3.9.7-slim
RUN pip install haversine
COPY server /
COPY common/* /src/
ENTRYPOINT ["/bin/sh"]
