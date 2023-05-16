import sys

number_of_replicates = int(sys.argv[1])

f = open("docker-compose-dev.yaml", "w")

f.write('''services:
  rabbitmq:
    container_name: rabbitmq
    image: rabbitmq:latest
    ports:
      - 15672:15672
    networks:
      - testing_net

  client:
    container_name: client
    image: client:latest
    entrypoint: python3 /main.py
    restart: on-failure
    environment:
      - CLI_ID=1
      - CLI_LOG_LEVEL=DEBUG
    networks:
      - testing_net
    volumes:  
      - type: bind
        source: ./data/archive
        target: /data
      - type: bind
        source: ./client/config.ini
        target: /config/config.ini
        read_only: true
      - results:/results
    depends_on:
      - client_main_api_processor
      - query_processor

  client_main_api_processor:
    container_name: client_main_api_processor
    image: client_main_api_processor:latest
    entrypoint: python3 /main.py
    restart: on-failure
    environment:
      - PYTHONUNBUFFERED=1
      - LOGGING_LEVEL=DEBUG
    networks:
      - testing_net
    volumes:
      - type: bind
        source: ./server/client_main_api_processor/config.ini
        target: /config/config.ini
        read_only: true

  data_distributor_processor:
    container_name: data_distributor_processor
    image: data_distributor_processor:latest
    entrypoint: python3 /main.py
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1
      
  query_processor:
    container_name: query_processor
    image: query_processor:latest
    entrypoint: python3 /main.py
    #restart: on-failure
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1

  result_processor:
    container_name: result_processor
    image: result_processor:latest
    entrypoint: python3 /main.py
    #restart: on-failure
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1
''')

for i in range(1, 1 + number_of_replicates):
    f.write(f'''
  weather_processor{i}:
    container_name: weather_processor{i}
    image: weather_processor_image:latest
    entrypoint: python3 /main.py
    #restart: on-failure
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1
      - INSTANCE_ID={i}

  years_filterer{i}:
    container_name: years_filterer{i}
    image: years_filterer:latest
    entrypoint: python3 /main.py
    #restart: on-failure
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1
      - INSTANCE_ID={i}

  duplicated_processor{i}:
    container_name: duplicated_processor{i}
    image: duplicated_processor:latest
    entrypoint: python3 /main.py
    #restart: on-failure
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1
      - INSTANCE_ID={i}

  montreal_filterer{i}:
    container_name: montreal_filterer{i}
    image: montreal_filterer:latest
    entrypoint: python3 /main.py
    #restart: on-failure
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1
      - INSTANCE_ID={i}

  montreal_distance_processor{i}:
    container_name: montreal_distance_processor{i}
    image: montreal_distance_processor:latest
    entrypoint: python3 /main.py
    #restart: on-failure
    depends_on:
      - rabbitmq
    networks:
      - testing_net
    links:
      - rabbitmq
    environment:
      - PYTHONUNBUFFERED=1
      - INSTANCE_ID={i}
    ''')

f.write('''
volumes:
  server-config:
    external: false
  client-config:
    external: false
  dataset:
    external: false
  results:

networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24
''')
f.write("\n")

f.close()

c = open("./server/server_common/config.ini", "w")
c.write(f'''[DEFAULT]
PROCESSES_PER_LAYER = {number_of_replicates}
''')
c.close()
