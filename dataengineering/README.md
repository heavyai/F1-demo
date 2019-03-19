# Vehicle Telematics Analytics (VTA) Demo: Data Engineering

The core of the VTA demo data pipeline is [StreamSets Data Collector](https://streamsets.com/opensource), an open-source data pipeline manager. The three pipelines are located in the [pipelines folder](/dataengineering/pipelines) and are explained below.

### UDP to Kafka

![](/dataengineering/img/00_udp_pipeline.png)

The first part of the data pipeline listens on port 6789 for [UDP](https://searchnetworking.techtarget.com/definition/UDP-User-Datagram-Protocol) packets, which are sent from the F1 2018 game to a specified IP address (in this case, the IP address of the machine where StreamSets is running). You configure the IP address and port inside the F1 2018 game, and the port only within StreamSets.

After the data are received from UDP, StreamSets writes the results directly to Apache Kafka. This is to maximize data throughput to later stages of the pipeline. This also allows for re-processing the source data in the future, should that be necessary.

### Parse to JSON

![](/dataengineering/img/01_parse_to_JSON.png)

The second part of the data pipeline is to parse the UDP packets from their binary representation into JSON, with minor enrichment to add the timestamp for when the UDP packet was received. The core of the process to parse from binary to JSON is a [Java library](/dataengineering/f1-2018_telemetry), called using the Groovy processor in StreamSets.

The output of this stage of the pipeline is a separate Kafka than the UDP packets; this also allows for reprocessing if desired, but also to allow a separate level of parallelism for the third part of the pipeline that inserts the data into OmniSci.

### Data refinement and insert into OmniSci

![](/dataengineering/img/02_JSON_to_OmniSci.png)

The final part of the data pipeline is to take all of the JSON messages from the Kafka topic, sort them based on their `packetId` value, then process them based on their unique table characteristics. Once the data fields are processed and data types set, the final step is to insert the data into OmniSci using the OmniSci JDBC connector (available in all OmniSci versions).
