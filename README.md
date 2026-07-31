# Optimizing Public Transportation

Udacity Kafka ecosystem project for a Chicago Transit Authority transit-status dashboard.

## What was completed

- Implemented Avro schemas for arrival, turnstile, and weather events.
- Added Kafka topic creation and Avro producers for station arrivals and turnstile events.
- Added weather publishing through the Kafka REST Proxy with the required Avro content type.
- Configured the PostgreSQL JDBC Source Connector to load the `stations` table using incrementing `stop_id`.
- Completed the Faust stream transformation from station records to line-specific station records.
- Completed KSQL table creation and turnstile station-count aggregation.
- Completed Kafka consumers for weather, stations, arrivals, and turnstile summaries.
- Added rubric contract tests and a clean `.gitignore`.

## Project layout

- `producers/` emits arrival and turnstile events, weather through Kafka REST Proxy, and station data through Kafka Connect.
- `consumers/` runs the Faust transformation, KSQL aggregation, and Tornado transit-status consumer.
- `tests/` contains automated rubric contract tests.

## Validation

The following checks passed locally and on the ThinkPad:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q producers consumers
```

The ThinkPad had Docker and Docker Compose available, but did not have the CTA Kafka/Confluent stack running. Therefore, full Kafka end-to-end validation was not performed there.

## Running the application

Start the Kafka ecosystem described by the assignment, then run the components from separate terminals:

```bash
cd producers
python3 simulation.py
```

```bash
cd consumers
faust -A faust_stream worker -l info
```

```bash
cd consumers
python3 ksql.py
```

```bash
cd consumers
python3 server.py
```

The web dashboard is served at `http://localhost:3000`.
