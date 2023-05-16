import sys

number_of_clients = int(sys.argv[1])

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

  weather_processor:
    container_name: weather_processor
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
      - INSTANCE_ID=1

  weather_processor2:
    container_name: weather_processor2
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
      - INSTANCE_ID=2

  years_filterer:
    container_name: years_filterer
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
      - INSTANCE_ID=1

  years_filterer2:
    container_name: years_filterer2
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
      - INSTANCE_ID=2

  duplicated_processor:
    container_name: duplicated_processor
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
      - INSTANCE_ID=1

  duplicated_processor2:
    container_name: duplicated_processor2
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
      - INSTANCE_ID=2

  montreal_filterer:
    container_name: montreal_filterer
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
      - INSTANCE_ID=1

  montreal_filterer2:
    container_name: montreal_filterer2
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
      - INSTANCE_ID=2

  montreal_distance_processor:
    container_name: montreal_distance_processor
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
      - INSTANCE_ID=1

  montreal_distance_processor2:
    container_name: montreal_distance_processor2
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
      - INSTANCE_ID=2
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
