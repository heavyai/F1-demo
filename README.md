# F1 demo
Real-time vehicle telematics analytics demo using OmniSci, debuted at [NVIDIA GTC 2019](https://www.nvidia.com/en-us/gtc/) San Jose and later at [OmniSci Converge 2019](https://converge.omnisci.com/).

![Dash app](/f1dash/assets/dash-screenshot.png)

This demo is built using only open-source components:

- [OmniSci Core](https://github.com/omnisci/mapd-core)
- [pymapd](https://github.com/omnisci/pymapd)
- [StreamSets Open Source](https://streamsets.com/opensource)
- [Apache Kafka](https://kafka.apache.org/)
- [Dash by Plotly](https://plot.ly/products/dash/)

This repo is set up as a monorepo; see the [data engineering](https://github.com/omnisci/vehicle-telematics-analytics-demo/tree/master/dataengineering) and [f1dash](https://github.com/omnisci/vehicle-telematics-analytics-demo/tree/master/f1dash) folders for the README's for StreamSets and Python/Dash code, respectively.

## Blog Posts

The following blog posts were published to the [OmniSci Blog](https://www.omnisci.com/blog) to give an in-depth explanation of how everything works:

[Creating the OmniSci F1 Demo: Real-Time Data Ingestion With StreamSets](https://www.omnisci.com/blog/creating-the-omnisci-f1-demo)

[Plotly Dash and OmniSciDB for Real-Time Data Visualization](https://www.omnisci.com/blog/plotly-dash-and-omniscidb-for-real-time-data-visualization)

## Data

We want to see what YOU would build with this dataset!

In addition to providing all of the code, OmniSci is providing the data for all laps in an S3 bucket.  The table definitions are in the [ddl folder](https://github.com/omnisci/vehicle-telematics-analytics-demo/tree/updatereadme/ddl); use OmniSci Core or OmniSci Cloud to load the data and to perform your queries, then use OmniSci Immerse or your favorite visualization tool to explore the data.

Please be respectful and make a copy to your own location rather than direct-linking against this bucket: s3://mapd-cloud/DataSets/vehicle_telematics_dataset_f12018/
