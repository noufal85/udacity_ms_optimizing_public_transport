# Optimizing Public Transportation

Udacity Kafka ecosystem project for a Chicago Transit Authority status dashboard.

## Components

- `producers/` emits Avro arrival and turnstile events, weather through Kafka REST Proxy, and station data through Kafka Connect.
- `consumers/` runs the Faust station transformation, KSQL aggregation, and Tornado transit-status consumer.
- `tests/` contains rubric contract tests for the required schemas and completed assignment modules.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q producers consumers
```

The Kafka/Confluent services described in the assignment must be running before launching the producer, Faust worker, KSQL script, and web server.
