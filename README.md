[Documentation 4+1](https://docs.google.com/document/d/1XDQToCCFDg2lCdNnH7EYLO4A9ozPr4JifoqsJPjl-80/edit?usp=sharing) 

---------------------------------------------------------------

To run the application, clone this repository and download the [kaggle's data](https://www.kaggle.com/datasets/jeanmidev/public-bike-sharing-in-north-america) .zip, extract it
to a folder named data (son of the root folder).
Now, execute on the root folder:
```
make docker-compose-up
```
By default, the amount of duplicated processes on each node is two. To change this, execute the following command:
```
python set_up_scaled_docker.py REPLICATED_NODES_PER_LAYER
```

REPLICATED_NODES_PER_LAYER being a number. Because of other priorities, I could not personalize further the number of nodes of a specific process.

When the application ends execution, results are both printed to screen and saved to a file.
```
make docker-compose-logs | grep "client "
```
To check the results file, open the file in /var/lib/docker/volumes/tp1-results/_data/results.txt (you may need to be a super user).


------------------------------------------------------------------
To stop the application and see that the processes exit gracefully:
Run the application. Then, on one terminal, run:
```
make docker-compose-logs | grep "exited "
```
On another terminal, to send sigterm to all processes run:
```
make docker-compose-stop
```

On the first terminal, all processes should exit with 0 code. Same goes when the application ends successfully.

Note: Client's QueryAsker periodically sleeps to ask the server for the current query results. When sigterm signal is received, if the process is sleeping it continues and then finishes gracefully. That is the main reason why the client may take a bit longer to shutdown gracefully.  

To improve (due to lack of time):
* When the an accepting node (client_main_api or query_processor) is accepting the connection and it receives a sigterm, I could not handle the exception in a good fashion so those nodes do not end gracefully.
* To wait for rabbit sleeps are used. Client sleeps to wait to start a connection with Rabbit.
* Sequence diagram is missing.
