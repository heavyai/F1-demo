## f1dash

![Dash app](/f1dash/assets/dash-screenshot.png)

### Background

The f1dash is a Plotly Dash application which uses [pymapd](https://github.com/omnisci/pymapd) to query for new data every 5-15 seconds, displaying the data in the app in a near-real-time manner. This is possible because of how OmniSci stores and processes data; because OmniSci doesn't use indexing to achieve performance, as soon as data is streamed into an OmniSci database, it can be available for use.

The [dataengineering](https://github.com/omnisci/vehicle-telematics-analytics-demo/tree/master/dataengineering) folder highlights the data pipeline for ingesting the data into OmniSci using Apache Kafka and the OmniSci JDBC driver via StreamSets.

### Setup

The python code for this app has the following reference in [app.py](https://github.com/omnisci/vehicle-telematics-analytics-demo/blob/master/f1dash/app.py#L10):

```python
from credentials import host, user, password, dbname, port
```

This file `credentials.py` was not checked into the repo (for obvious reasons). To re-create this file, create a file `credentials.py` at the same directory level as `app.py`, substituting your values for the following:

```python
host="localhost"
user="mapd"
password="HyperInteractive"
dbname="mapd"
```

### Running the app in production

For development purposes, you can run this app locally using the internal Dash/Flask webserver. To run this app in production, using multiple threads/workers, we used [gunicorn with nginx](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04). 

Note that a single instance of OmniSci isn't really meant to be used as a production backend server for a CRUD app. This Dash app ran successfully in 2 or 3 separate browser instances against a single OmniSci instance, but for a public level of traffic, it is unlikely that a non-distributed/non-load-balanced instance of OmniSci will be able to handle more than a handful of active connections.
