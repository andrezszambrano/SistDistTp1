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

